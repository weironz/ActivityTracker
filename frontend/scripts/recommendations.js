// ShopTrack 推荐系统功能

/**
 * 渲染推荐商品
 * @param {Array} recs - 推荐商品列表
 */
function renderRecommendations(recs) {
  const el = document.getElementById('rec-list');

  if (!recs || recs.length === 0) {
    el.innerHTML = '<div style="color:var(--muted);font-size:0.8rem">暂无推荐</div>';
    return;
  }

  el.innerHTML = recs.map(p => `
    <div class="rec-item" onclick="trackClick(${p.id})">
      <span class="rec-icon">${p.emoji}</span>
      <div class="rec-info">
        <div class="rec-name">${p.name}</div>
        <div class="rec-price">¥${p.price}</div>
      </div>
    </div>
  `).join('');
}

/**
 * 切换推荐面板显示状态
 */
function toggleRec() {
  uiState.recOpen = !uiState.recOpen;
  document.getElementById('rec-panel').classList.toggle('open', uiState.recOpen);
  document.getElementById('rec-toggle').classList.toggle('shifted', uiState.recOpen);
}
