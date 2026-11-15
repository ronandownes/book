/* Colour the six top-level PreTeXt parts without changing the book content. */
(() => {
  const targets = {
    "part-junior-cycle.html":"jc",
    "part-transition-year.html":"ty",
    "part-leaving-certificate.html":"lc",
    "part-foundation.html":"foundation",
    "part-leaving-certificate-applied.html":"lca",
    "part-official-appendices.html":"appendices"
  };
  function paint(){
    document.querySelectorAll('a[href]').forEach(a => {
      const file = a.getAttribute('href').split(/[?#]/)[0].split('/').pop();
      const program = targets[file];
      if (!program || a.classList.contains('maths-programme-link')) return;
      const nav = a.closest('nav, .toc, .ptx-toc, .toc-container, #toc');
      if (!nav) return;
      a.classList.add('maths-programme-link', 'maths-programme-'+program);
      const parent = a.parentElement;
      if (parent && parent.tagName.toLowerCase() !== 'li' &&
          !parent.classList.contains('toc') &&
          !parent.classList.contains('toc-item')) {
        parent.classList.add('maths-programme-container', 'maths-programme-'+program);
      }
    });
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',paint,{once:true});
  else paint();
})();
