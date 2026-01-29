(function () {
  function realSrc(img) {
    return (
      img.getAttribute("data-src") ||
      img.getAttribute("data-original") ||
      img.getAttribute("data-srcset") ||
      img.currentSrc ||
      img.getAttribute("src") ||
      ""
    );
  }

  function normalizeZoom(img) {
    // 把 style="zoom:33%" 转成 width，更通用
    const z = (img.style && img.style.zoom) || "";
    if (!z) return;

    let pct = null;
    if (z.includes("%")) pct = parseFloat(z);
    else {
      const f = parseFloat(z);
      if (!Number.isNaN(f) && f > 0) pct = f * 100;
    }
    if (pct && pct > 0) {
      img.style.width = pct + "%";
      img.style.zoom = "";
    }
  }

  function wrapOne(img) {
    // 已经是 fancybox 包裹/已经在链接里，就跳过
    if (img.closest('a[data-fancybox], a.fancybox')) return;
    if (img.dataset.fancyboxized === "1") return;

    const src = realSrc(img);
    if (!src || src.startsWith("data:")) return;

    normalizeZoom(img);

    const cap = (img.getAttribute("alt") || "").trim();

    // 复刻你给的结构
    const a = document.createElement("a");
    a.className = "fancybox fancybox.image";
    a.href = src;
    a.setAttribute("itemscope", "");
    a.setAttribute("itemtype", "http://schema.org/ImageObject");
    a.setAttribute("itemprop", "url");
    a.setAttribute("data-fancybox", "default");
    a.setAttribute("rel", "default");
    if (cap) {
      a.setAttribute("title", cap);
      a.setAttribute("data-caption", cap);
    }

    img.dataset.fancyboxized = "1";

    img.parentNode.insertBefore(a, img);
    a.appendChild(img);
  }

  function run() {
    const scope = document.querySelector(".markdown-body");
    if (!scope) return;

    scope.querySelectorAll("img").forEach(wrapOne);

    // 重新绑定 fancybox（兼容不同版本）
    try {
      if (window.Fancybox && typeof window.Fancybox.bind === "function") {
        window.Fancybox.bind('[data-fancybox="default"]', {});
      } else if (window.jQuery && window.jQuery.fn && window.jQuery.fn.fancybox) {
        window.jQuery('[data-fancybox="default"]').fancybox();
      } else if (window.$ && window.$.fn && window.$.fn.fancybox) {
        window.$('[data-fancybox="default"]').fancybox();
      }
    } catch (_) {}
  }

  // 首次 + 延迟（等 lazyload/主题脚本跑完）
  document.addEventListener("DOMContentLoaded", () => {
    run();
    setTimeout(run, 800);
    setTimeout(run, 2000);

    // 监听后续 DOM 变化（懒加载替换 src、pjax 等）
    const scope = document.querySelector(".markdown-body");
    if (scope) {
      const mo = new MutationObserver(() => run());
      mo.observe(scope, { childList: true, subtree: true, attributes: true, attributeFilter: ["src", "data-src", "data-original"] });
    }
  });
})();