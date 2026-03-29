// ShopTrack UI交互功能

/**
 * 显示Toast通知
 * @param {string} type - 事件类型
 * @param {string} msg - 通知消息
 */
function showToast(type, msg) {
  const toast = document.getElementById('toast');
  document.getElementById('toast-ev').textContent = `[${type.toUpperCase()}]`;
  document.getElementById('toast-msg').textContent = msg;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 2500);
}

/**
 * 页面加载初始化
 */
window.addEventListener('load', () => {
  renderProducts();
  track('page_view', { page: 'home', productName: 'homepage' });
});
