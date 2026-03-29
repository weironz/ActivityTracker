// ShopTrack 商品渲染功能

/**
 * 渲染商品列表
 * @param {string} filter - 筛选条件 ('all' 或分类名称)
 */
function renderProducts(filter = 'all') {
  const grid = document.getElementById('product-grid');
  const list = filter === 'all' ? products : products.filter(p => p.category === filter);

  grid.innerHTML = list.map(p => `
    <div class="product-card" onclick="trackClick(${p.id})" onmouseenter="trackView(${p.id})">
      <div class="card-img">
        ${p.hot ? '<span class="tag">HOT</span>' : ''}
        <span>${p.emoji}</span>
      </div>
      <div class="card-body">
        <div class="card-cat">${p.category}</div>
        <div class="card-name">${p.name}</div>
        <div class="card-footer">
          <span class="price">¥${p.price}</span>
          <button class="buy-btn" onclick="trackPurchase(event, ${p.id})">加入购物车</button>
        </div>
      </div>
    </div>
  `).join('');
}

/**
 * 按分类筛选商品
 * @param {string} cat - 分类名称
 * @param {HTMLElement} btn - 点击的按钮元素
 */
function filterProducts(cat, btn) {
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');

  // 清空搜索框并恢复分类筛选
  document.getElementById('search-input').value = '';
  uiState.currentSearchKeyword = '';

  renderProducts(cat);
  track('filter', { category: cat });
}

/**
 * 追踪商品浏览
 * @param {number} productId - 商品ID
 */
function trackView(productId) {
  const p = products.find(x => x.id === productId);
  track('page_view', { productId, productName: p.name, category: p.category });
}

/**
 * 追踪商品点击
 * @param {number} productId - 商品ID
 */
function trackClick(productId) {
  const p = products.find(x => x.id === productId);
  track('click', { productId, productName: p.name, category: p.category });
  showToast('click', `点击了 ${p.name}`);
  fetchRecommendations();
}

/**
 * 追踪购买行为
 * @param {Event} e - 事件对象
 * @param {number} productId - 商品ID
 */
function trackPurchase(e, productId) {
  e.stopPropagation();
  const p = products.find(x => x.id === productId);
  track('purchase', { productId, productName: p.name, category: p.category, price: p.price });
  showToast('purchase', `加入购物车 ${p.name}`);
  fetchRecommendations();
}
