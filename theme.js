// Apply the chosen preview before paint. Query links can be shared with clients.
(() => {
  const choice = new URLSearchParams(location.search).get('design');
  let saved = '';
  try {
    if (choice === '1' || choice === '2') localStorage.setItem('tirDesign', choice);
    saved = localStorage.getItem('tirDesign') || '';
  } catch { /* The default design remains usable if storage is unavailable. */ }
  document.documentElement.dataset.design = (choice === '2' || (choice !== '1' && saved === '2')) ? '2' : '1';
})();
