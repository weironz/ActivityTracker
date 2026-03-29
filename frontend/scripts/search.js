// ShopTrack 搜索功能

/**
 * 处理搜索输入（带防抖）
 * @param {string} keyword - 搜索关键词
 */
function handleSearch(keyword) {
  uiState.currentSearchKeyword = keyword.trim();
  clearTimeout(uiState.searchTimeout);

  // 防抖：500ms内没有新输入才执行搜索
  uiState.searchTimeout = setTimeout(() => {
    performSearch();
  }, 500);
}

/**
 * 执行搜索
 */
function performSearch() {
  if (uiState.currentSearchKeyword.length === 0) {
    // 清空搜索时恢复当前分类筛选
    const activeBtn = document.querySelector('.filter-btn.active');
    const currentCategory = activeBtn ? activeBtn.textContent : '全部';
    renderProducts(categoryMap[currentCategory] || 'all');
    return;
  }

  // 执行搜索并追踪到Kafka
  track('search', { keyword: uiState.currentSearchKeyword });

  // 实时搜索结果
  const searchResults = products.filter(p =>
    p.name.toLowerCase().includes(uiState.currentSearchKeyword.toLowerCase()) ||
    p.category.toLowerCase().includes(uiState.currentSearchKeyword.toLowerCase())
  );

  renderSearchResults(searchResults);
}

/**
 * 渲染搜索结果
 * @param {Array} results - 搜索结果商品列表
 */
function renderSearchResults(results) {
  const grid = document.getElementById('product-grid');

  if (results.length === 0) {
    grid.innerHTML = `
      <div style="grid-column: 1/-1; text-align: center; padding: 3rem; color: var(--muted);">
        <div style="font-size: 2rem; margin-bottom: 1rem;">🔍</div>
        <div>未找到 "${uiState.currentSearchKeyword}" 的相关商品</div>
      </div>
    `;
    return;
  }

  grid.innerHTML = results.map(p => `
    <div class="product-card" onclick="trackClick(${p.id})" onmouseenter="trackView(${p.id})">
      <div class="card-img">
        ${p.hot ? '<span class="tag">HOT</span>' : ''}
        <span>${p.emoji}</span>
      </div>
      <div class="card-body">
        <div class="card-cat">${p.category}</div>
        <div class="card-name">${highlightMatch(p.name, uiState.currentSearchKeyword)}</div>
        <div class="card-footer">
          <span class="price">¥${p.price}</span>
          <button class="buy-btn" onclick="trackPurchase(event, ${p.id})">加入购物车</button>
        </div>
      </div>
    </div>
  `).join('');
}

/**
 * 高亮搜索匹配的关键词
 * @param {string} text - 原文本
 * @param {string} keyword - 搜索关键词
 * @returns {string} - 高亮后的HTML
 */
function highlightMatch(text, keyword) {
  if (!keyword) return text;
  const regex = new RegExp(`(${keyword})`, 'gi');
  return text.replace(regex, '<span style="background: rgba(232,197,71,0.2);">$1</span>');
}
