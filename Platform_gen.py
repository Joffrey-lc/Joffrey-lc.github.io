#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Generate homepage Platform Highlight cards from ``demo.pptx``.

The PowerPoint slide is the card editor: text, static pictures, borders and the
placement of embedded GIFs are all taken from the slide.  For every slide this
script exports a static poster with desktop PowerPoint, composites the embedded
GIF frames at their PowerPoint positions, and writes browser-friendly WebM and
MP4 files.  A static-only slide is emitted as a poster-only card.

Default workflow::

    python Platform_gen.py
    python build_CV.py

Requirements: Windows desktop PowerPoint, Pillow, and ffmpeg on PATH.
"""

from __future__ import annotations

import argparse
import bisect
import html
import json
import math
import os
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple
from xml.etree import ElementTree as ET
from zipfile import ZipFile

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover - dependency check
    raise SystemExit("缺少 Pillow。请先运行：python -m pip install pillow") from exc


P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
NS = {"p": P_NS, "a": A_NS, "r": R_NS, "pr": PKG_REL_NS}

PLATFORM_HEADING = "Platform Highlight"
GENERATED_START = "<!-- PLATFORM_GEN_START -->"
GENERATED_END = "<!-- PLATFORM_GEN_END -->"


def _safe_title(value: str, fallback: str) -> str:
    value = re.sub(r"\s+", " ", value or "").strip()
    return value or fallback


def _resolve_part(base_part: str, target: str) -> str:
    return posixpath.normpath(posixpath.join(posixpath.dirname(base_part), target))


def _relationship_map(zf: ZipFile, slide_number: int) -> Dict[str, str]:
    rel_part = f"ppt/slides/_rels/slide{slide_number}.xml.rels"
    root = ET.fromstring(zf.read(rel_part))
    slide_part = f"ppt/slides/slide{slide_number}.xml"
    return {
        rel.get("Id", ""): _resolve_part(slide_part, rel.get("Target", ""))
        for rel in root
        if rel.get("Id") and rel.get("Target")
    }


def _xfrm_box(xfrm: Optional[ET.Element]) -> Optional[Tuple[int, int, int, int]]:
    if xfrm is None:
        return None
    off = xfrm.find("./a:off", NS)
    ext = xfrm.find("./a:ext", NS)
    if off is None or ext is None:
        return None
    return (
        int(off.get("x", "0")),
        int(off.get("y", "0")),
        int(ext.get("cx", "0")),
        int(ext.get("cy", "0")),
    )


def _slide_title(root: ET.Element, slide_width: int, slide_height: int, number: int) -> str:
    """Find the top title by geometry instead of relying on a title placeholder."""
    pieces: List[Tuple[int, str]] = []
    for shape in root.findall(".//p:sp", NS):
        text = "".join((node.text or "") for node in shape.findall(".//a:t", NS)).strip()
        if not text:
            continue
        box = _xfrm_box(shape.find("./p:spPr/a:xfrm", NS))
        if not box:
            continue
        x, y, width, h = box
        # Ignore tiny/off-canvas metadata text boxes sometimes left by PowerPoint.
        if width < slide_width * 0.05 or h < slide_height * 0.01:
            continue
        if y + h / 2 <= slide_height * 0.18:
            pieces.append((x, text))
    if pieces:
        pieces.sort(key=lambda item: item[0])
        return _safe_title("".join(text for _x, text in pieces), f"Platform {number}")
    return f"Platform {number}"


@dataclass(frozen=True)
class GifPlacement:
    media_part: str
    x: int
    y: int
    width: int
    height: int
    crop_left: int = 0
    crop_top: int = 0
    crop_right: int = 0
    crop_bottom: int = 0
    flip_h: bool = False
    flip_v: bool = False
    rotation: int = 0


@dataclass
class SlideSpec:
    number: int
    title: str
    gif_placements: List[GifPlacement]


def inspect_deck(pptx_path: Path) -> Tuple[int, int, List[SlideSpec]]:
    with ZipFile(pptx_path) as zf:
        presentation = ET.fromstring(zf.read("ppt/presentation.xml"))
        size = presentation.find("p:sldSz", NS)
        if size is None:
            raise RuntimeError("PPTX 中缺少幻灯片尺寸信息。")
        slide_width = int(size.get("cx", "0"))
        slide_height = int(size.get("cy", "0"))
        slide_parts = sorted(
            (
                name
                for name in zf.namelist()
                if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)
            ),
            key=lambda name: int(re.search(r"(\d+)", Path(name).stem).group(1)),
        )

        slides: List[SlideSpec] = []
        for number, slide_part in enumerate(slide_parts, start=1):
            root = ET.fromstring(zf.read(slide_part))
            rels = _relationship_map(zf, number)
            placements: List[GifPlacement] = []
            for pic in root.findall(".//p:pic", NS):
                blip = pic.find("./p:blipFill/a:blip", NS)
                rel_id = blip.get(f"{{{R_NS}}}embed") if blip is not None else ""
                media_part = rels.get(rel_id or "", "")
                if not media_part.lower().endswith(".gif"):
                    continue
                box = _xfrm_box(pic.find("./p:spPr/a:xfrm", NS))
                if not box:
                    print(f"[WARN] 第 {number} 页有一个 GIF 缺少位置，已跳过：{media_part}")
                    continue
                xfrm = pic.find("./p:spPr/a:xfrm", NS)
                src_rect = pic.find("./p:blipFill/a:srcRect", NS)
                crop = src_rect.attrib if src_rect is not None else {}
                placements.append(
                    GifPlacement(
                        media_part=media_part,
                        x=box[0],
                        y=box[1],
                        width=box[2],
                        height=box[3],
                        crop_left=int(crop.get("l", "0")),
                        crop_top=int(crop.get("t", "0")),
                        crop_right=int(crop.get("r", "0")),
                        crop_bottom=int(crop.get("b", "0")),
                        flip_h=(xfrm.get("flipH") == "1") if xfrm is not None else False,
                        flip_v=(xfrm.get("flipV") == "1") if xfrm is not None else False,
                        rotation=int(xfrm.get("rot", "0")) if xfrm is not None else 0,
                    )
                )
            slides.append(
                SlideSpec(
                    number=number,
                    title=_slide_title(root, slide_width, slide_height, number),
                    gif_placements=placements,
                )
            )
    return slide_width, slide_height, slides


def export_posters_with_powerpoint(
    pptx_path: Path, output_dir: Path, width: int, height: int
) -> None:
    """Use desktop PowerPoint for faithful text/font/static-shape rendering."""
    env = os.environ.copy()
    env["PLATFORM_PPTX"] = str(pptx_path.resolve())
    env["PLATFORM_OUT"] = str(output_dir.resolve())
    env["PLATFORM_WIDTH"] = str(width)
    env["PLATFORM_HEIGHT"] = str(height)
    script = r"""
$ErrorActionPreference = 'Stop'
$pptPath = $env:PLATFORM_PPTX
$outDir = $env:PLATFORM_OUT
$width = [int]$env:PLATFORM_WIDTH
$height = [int]$env:PLATFORM_HEIGHT
New-Item -ItemType Directory -Path $outDir -Force | Out-Null
$app = $null
$pres = $null
try {
  $app = New-Object -ComObject PowerPoint.Application
  $app.Visible = -1
  $pres = $app.Presentations.Open($pptPath, $true, $false, $false)
  for ($i = 1; $i -le $pres.Slides.Count; $i++) {
    $poster = Join-Path $outDir ('platform-slide-{0:D2}-poster.png' -f $i)
    $pres.Slides.Item($i).Export($poster, 'PNG', $width, $height)
  }
  Write-Output ('POSTERS=' + $pres.Slides.Count)
}
finally {
  if ($pres) {
    $pres.Close()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($pres) | Out-Null
  }
  if ($app) {
    $app.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($app) | Out-Null
  }
}
"""
    powershell = shutil.which("powershell.exe") or shutil.which("powershell")
    if not powershell:
        raise RuntimeError("找不到 PowerShell，无法调用桌面 PowerPoint。")
    result = subprocess.run(
        [powershell, "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script],
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "未知 PowerPoint 错误").strip()
        raise RuntimeError("PowerPoint 导出静态封面失败：\n" + detail)


class AnimatedGifLayer:
    def __init__(
        self,
        gif_bytes: bytes,
        placement: GifPlacement,
        slide_size: Tuple[int, int],
        output_size: Tuple[int, int],
        sample_times_ms: Sequence[float],
    ) -> None:
        slide_width, slide_height = slide_size
        output_width, output_height = output_size
        self.x = round(placement.x / slide_width * output_width)
        self.y = round(placement.y / slide_height * output_height)
        self.width = max(1, round(placement.width / slide_width * output_width))
        self.height = max(1, round(placement.height / slide_height * output_height))

        gif = Image.open(BytesIO(gif_bytes))
        durations: List[int] = []
        frame_count = getattr(gif, "n_frames", 1)
        for index in range(frame_count):
            gif.seek(index)
            durations.append(max(10, int(gif.info.get("duration", 100) or 100)))
        self.duration_ms = max(1, sum(durations))
        cumulative: List[int] = []
        running = 0
        for duration in durations:
            running += duration
            cumulative.append(running)

        needed_indices = {
            min(len(cumulative) - 1, bisect.bisect_right(cumulative, time_ms % self.duration_ms))
            for time_ms in sample_times_ms
        }
        self.frames: Dict[int, Image.Image] = {}
        for index in sorted(needed_indices):
            gif.seek(index)
            frame = gif.convert("RGBA")
            source_width, source_height = frame.size
            left = round(source_width * placement.crop_left / 100000)
            top = round(source_height * placement.crop_top / 100000)
            right = round(source_width * (1 - placement.crop_right / 100000))
            bottom = round(source_height * (1 - placement.crop_bottom / 100000))
            if right > left and bottom > top:
                frame = frame.crop((left, top, right, bottom))
            frame = frame.resize((self.width, self.height), Image.Resampling.LANCZOS)
            if placement.flip_h:
                frame = frame.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            if placement.flip_v:
                frame = frame.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            if placement.rotation:
                degrees = placement.rotation / 60000.0
                frame = frame.rotate(-degrees, resample=Image.Resampling.BICUBIC, expand=False)
            self.frames[index] = frame
        self.cumulative = cumulative

    def frame_at(self, time_ms: float) -> Image.Image:
        index = min(
            len(self.cumulative) - 1,
            bisect.bisect_right(self.cumulative, time_ms % self.duration_ms),
        )
        return self.frames[index]


class RawVideoEncoder:
    def __init__(
        self,
        ffmpeg: str,
        output_path: Path,
        width: int,
        height: int,
        fps: int,
        kind: str,
    ) -> None:
        common = [
            ffmpeg,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-s",
            f"{width}x{height}",
            "-r",
            str(fps),
            "-i",
            "-",
            "-an",
        ]
        if kind == "webm":
            codec = [
                "-c:v",
                "libvpx-vp9",
                "-crf",
                "34",
                "-b:v",
                "0",
                "-deadline",
                "good",
                "-cpu-used",
                "3",
                "-row-mt",
                "1",
                "-pix_fmt",
                "yuv420p",
            ]
        elif kind == "mp4":
            codec = [
                "-c:v",
                "libx264",
                "-preset",
                "medium",
                "-crf",
                "25",
                "-pix_fmt",
                "yuv420p",
                "-movflags",
                "+faststart",
            ]
        elif kind == "gif":
            codec = [
                "-filter_complex",
                "[0:v]split[a][b];[a]palettegen=max_colors=192[p];[b][p]paletteuse=dither=sierra2_4a",
            ]
        else:  # pragma: no cover - protected by call sites
            raise ValueError(kind)
        self.output_path = output_path
        self.process = subprocess.Popen(
            common + codec + [str(output_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )

    def write(self, frame: Image.Image) -> None:
        if self.process.stdin is None:
            raise RuntimeError("ffmpeg 输入管道不可用。")
        self.process.stdin.write(frame.convert("RGB").tobytes())

    def close(self) -> None:
        if self.process.stdin is not None:
            self.process.stdin.close()
        stderr = self.process.stderr.read().decode("utf-8", errors="replace") if self.process.stderr else ""
        code = self.process.wait()
        if code != 0:
            raise RuntimeError(f"ffmpeg 生成 {self.output_path.name} 失败：\n{stderr.strip()}")


def _web_path(path: Path) -> str:
    try:
        relative = path.resolve().relative_to(Path.cwd().resolve())
    except ValueError as exc:
        raise RuntimeError(f"网页资源必须位于当前网站目录内：{path}") from exc
    return "./" + relative.as_posix()


def render_slide_media(
    zf: ZipFile,
    slide: SlideSpec,
    slide_size: Tuple[int, int],
    output_dir: Path,
    output_size: Tuple[int, int],
    fps: int,
    ffmpeg: str,
    make_gif: bool,
) -> Dict[str, object]:
    poster_name = f"platform-slide-{slide.number:02d}-poster.png"
    poster_path = output_dir / poster_name
    if not poster_path.exists():
        raise RuntimeError(f"缺少第 {slide.number} 页封面：{poster_path}")

    card: Dict[str, object] = {
        "slide": slide.number,
        "title": slide.title,
        "poster": _web_path(poster_path),
        "animated_gifs": len(slide.gif_placements),
    }
    if not slide.gif_placements:
        card["duration_seconds"] = 0
        return card

    duration_ms = 0
    for placement in slide.gif_placements:
        with Image.open(BytesIO(zf.read(placement.media_part))) as image:
            total = 0
            for index in range(getattr(image, "n_frames", 1)):
                image.seek(index)
                total += max(10, int(image.info.get("duration", 100) or 100))
            duration_ms = max(duration_ms, total)

    total_frames = max(1, math.ceil(duration_ms / 1000 * fps))
    sample_times = [frame_number * 1000.0 / fps for frame_number in range(total_frames)]
    layers = [
        AnimatedGifLayer(
            zf.read(placement.media_part),
            placement,
            slide_size,
            output_size,
            sample_times,
        )
        for placement in slide.gif_placements
    ]

    webm_name = f"platform-slide-{slide.number:02d}.webm"
    mp4_name = f"platform-slide-{slide.number:02d}.mp4"
    encoders = [
        RawVideoEncoder(ffmpeg, output_dir / webm_name, output_size[0], output_size[1], fps, "webm"),
        RawVideoEncoder(ffmpeg, output_dir / mp4_name, output_size[0], output_size[1], fps, "mp4"),
    ]
    gif_name = ""
    if make_gif:
        gif_name = f"platform-slide-{slide.number:02d}.gif"
        encoders.append(
            RawVideoEncoder(ffmpeg, output_dir / gif_name, output_size[0], output_size[1], fps, "gif")
        )

    base = Image.open(poster_path).convert("RGBA")
    try:
        for frame_number, time_ms in enumerate(sample_times, start=1):
            canvas = base.copy()
            for layer in layers:
                canvas.alpha_composite(layer.frame_at(time_ms), (layer.x, layer.y))
            for encoder in encoders:
                encoder.write(canvas)
            if frame_number % max(fps * 3, 1) == 0 or frame_number == total_frames:
                seconds = frame_number / fps
                print(
                    f"  第 {slide.number} 页：已合成 {seconds:.1f}/{duration_ms / 1000:.1f} 秒",
                    flush=True,
                )
    finally:
        close_error: Optional[Exception] = None
        for encoder in encoders:
            try:
                encoder.close()
            except Exception as exc:  # finish/collect every child process
                close_error = close_error or exc
        if close_error:
            raise close_error

    card.update(
        {
            "webm": _web_path(output_dir / webm_name),
            "mp4": _web_path(output_dir / mp4_name),
            "duration_seconds": round(duration_ms / 1000, 2),
        }
    )
    if gif_name:
        card["gif"] = _web_path(output_dir / gif_name)
    return card


def _markdown_entry(card: Dict[str, object]) -> str:
    fields = [str(card["title"])]
    if card.get("webm"):
        fields.append(f"WebM: {card['webm']}")
    if card.get("mp4"):
        fields.append(f"MP4: {card['mp4']}")
    if card.get("gif"):
        fields.append(f"GIF: {card['gif']}")
    fields.append(f"Poster: {card['poster']}")
    fields.append(f"Alt: {card['title']}平台展示")
    fields.append(f"Source: demo.pptx#slide={card['slide']}")
    return "- " + " | ".join(fields)


def update_cv_markdown(cv_path: Path, cards: Sequence[Dict[str, object]]) -> None:
    generated = GENERATED_START + "\n" + "\n".join(_markdown_entry(card) for card in cards) + "\n" + GENERATED_END
    text = cv_path.read_text(encoding="utf-8")
    marker_re = re.compile(
        re.escape(GENERATED_START) + r".*?" + re.escape(GENERATED_END),
        flags=re.S,
    )
    if marker_re.search(text):
        updated = marker_re.sub(generated, text, count=1)
    else:
        heading_re = re.compile(r"(?m)^##\s+" + re.escape(PLATFORM_HEADING) + r"\s*$")
        heading_match = heading_re.search(text)
        if heading_match:
            insert_at = heading_match.end()
            updated = text[:insert_at] + "\n\n" + generated + text[insert_at:]
        else:
            section = f"## {PLATFORM_HEADING}\n\n{generated}\n\n"
            publications = re.search(r"(?m)^##\s+Selected Publications\\部分成果\s*$", text)
            insert_at = publications.start() if publications else len(text)
            prefix = text[:insert_at].rstrip() + "\n\n"
            suffix = text[insert_at:].lstrip("\n")
            updated = prefix + section + suffix
    cv_path.write_text(updated, encoding="utf-8", newline="\n")


def write_manifest(output_dir: Path, pptx_path: Path, cards: Sequence[Dict[str, object]], width: int, height: int, fps: int) -> Path:
    manifest_path = output_dir / "platform_cards.json"
    payload = {
        "source": pptx_path.name,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "width": width,
        "height": height,
        "fps": fps,
        "cards": list(cards),
    }
    manifest_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest_path


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="将 demo.pptx 的每一页生成一张 Platform Highlight 卡片。")
    parser.add_argument("--pptx", default="demo.pptx", help="输入 PPTX，默认 demo.pptx")
    parser.add_argument("--output-dir", default="assets/platforms", help="卡片资源输出目录")
    parser.add_argument("--cv", default="CV.md", help="需要更新的 CV.md")
    parser.add_argument("--width", type=int, default=960, help="输出宽度，默认 960")
    parser.add_argument("--fps", type=int, default=12, help="动画帧率，默认 12")
    parser.add_argument("--gif", action="store_true", help="额外生成整页 GIF（文件通常较大）")
    parser.add_argument("--no-update-cv", action="store_true", help="只生成资源，不更新 CV.md")
    parser.add_argument("--reuse-posters", action="store_true", help="复用已有封面，不调用 PowerPoint")
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    root = Path.cwd()
    pptx_path = (root / args.pptx).resolve()
    output_dir = root / args.output_dir
    cv_path = root / args.cv
    if not pptx_path.exists():
        raise SystemExit(f"找不到输入文件：{pptx_path}\n请将演示文稿命名为 demo.pptx 并放在脚本同一目录。")
    if args.width < 320 or args.width > 3840:
        raise SystemExit("--width 应位于 320–3840。")
    if args.fps < 1 or args.fps > 30:
        raise SystemExit("--fps 应位于 1–30。")

    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise SystemExit("找不到 ffmpeg。请安装 ffmpeg 并确保 ffmpeg.exe 位于 PATH。")

    slide_width, slide_height, slides = inspect_deck(pptx_path)
    output_height = round(args.width * slide_height / slide_width)
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"[INFO] 检测到 {len(slides)} 页，比例 {slide_width / slide_height:.4f}，输出 {args.width}x{output_height}")

    if not args.reuse_posters:
        print("[INFO] 正在用 PowerPoint 导出静态封面……", flush=True)
        export_posters_with_powerpoint(pptx_path, output_dir, args.width, output_height)

    cards: List[Dict[str, object]] = []
    with ZipFile(pptx_path) as zf:
        for slide in slides:
            print(f"[INFO] 第 {slide.number} 页：{slide.title}（{len(slide.gif_placements)} 个嵌入 GIF）", flush=True)
            card = render_slide_media(
                zf,
                slide,
                (slide_width, slide_height),
                output_dir,
                (args.width, output_height),
                args.fps,
                ffmpeg,
                args.gif,
            )
            cards.append(card)

    manifest = write_manifest(output_dir, pptx_path, cards, args.width, output_height, args.fps)
    if not args.no_update_cv:
        if not cv_path.exists():
            raise SystemExit(f"资源已生成，但找不到 {cv_path}，无法写入 Platform Highlight。")
        update_cv_markdown(cv_path, cards)
        print(f"[OK] 已更新：{cv_path}")
    print(f"[OK] 已生成 {len(cards)} 张平台卡片；清单：{manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
