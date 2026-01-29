(function () {
  function wrapImages() {
    const root = document.querySelector('.markdown-body') || document;
    const imgs = root.querySelectorAll('img');

    imgs.forEach((img) => {
      // 跳过：已经在 fancybox 链接里、或没有 src
      if (!img.getAttribute('src')) return;
      if (img.closest('a[data-fancybox], a.fancybox')) return;

      // 可选：跳过表情/图标等（按需加规则）
      if (img.classList.contains('emoji')) return;

      const src = img.getAttribute('src');
      const caption = img.getAttribute('alt') || img.getAttribute('title') || '';

      const a = document.createElement('a');
      a.className = 'fancybox fancybox.image img-zoom-wrapper';
      a.href = src;
      a.setAttribute('data-fancybox', 'default');
      a.setAttribute('rel', 'default');
      a.setAttribute('itemscope', '');
      a.setAttribute('itemtype', 'http://schema.org/ImageObject');
      a.setAttribute('itemprop', 'url');
      if (caption) {
        a.setAttribute('title', caption);
        a.setAttribute('data-caption', caption);
      }

      img.parentNode.insertBefore(a, img);
      a.appendChild(img);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', wrapImages);
  } else {
    wrapImages();
  }

  // 兼容少数主题/插件的局部刷新（有就赚，没有不影响）
  document.addEventListener('pjax:complete', wrapImages);
})();