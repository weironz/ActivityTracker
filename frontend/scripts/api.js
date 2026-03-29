// ShopTrack API调用和事件追踪

/**
 * 发送事件到 Kafka（经由后端）
 * @param {string} eventType - 事件类型
 * @param {object} data - 事件数据
 * @returns {Promise<object>} - 返回Kafka写入结果
 */
async function track(eventType, data) {
  const event = {
    eventType,
    userId,
    timestamp: new Date().toISOString(),
    url: location.href,
    ...data
  };

  addLog(eventType, data.productName || data.category || data.keyword || '-');

  try {
    const res = await fetch(`${BACKEND}/track`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(event)
    });
    const result = await res.json();
    addLog(eventType, `✓ 写入 Kafka (offset: ${result.offset ?? '?'})`, true);
    return result;
  } catch(e) {
    addLog(eventType, '⚠ 后端未连接（仅演示）', false, true);
    return null;
  }
}

/**
 * 获取推荐
 * @returns {Promise<object>} - 推荐结果
 */
async function fetchRecommendations() {
  try {
    const res = await fetch(`${BACKEND}/recommendations?userId=${userId}`);
    const data = await res.json();
    renderRecommendations(data.recommendations);
    if (!uiState.recOpen) toggleRec();
  } catch(e) {
    // 后端未连接时显示模拟推荐
    const mockRecs = products.slice(0, 3).map(p => ({
      ...p,
      score: Math.random().toFixed(2)
    }));
    renderRecommendations(mockRecs);
    if (!uiState.recOpen) toggleRec();
  }
}

/**
 * 添加日志到事件日志区域
 * @param {string} evType - 事件类型
 * @param {string} msg - 日志消息
 * @param {boolean} success - 是否成功
 * @param {boolean} warn - 是否警告
 */
function addLog(evType, msg, success = false, warn = false) {
  const container = document.getElementById('log-lines');
  const ts = new Date().toTimeString().split(' ')[0];
  const line = document.createElement('div');
  line.className = 'log-line';
  const color = warn ? '#f59e0b' : success ? 'var(--ok)' : 'var(--muted)';
  line.innerHTML = `<span class="ts">${ts}</span> <span class="ev-type">[${evType}]</span> <span style="color:${color}">${msg}</span>`;
  container.appendChild(line);
  container.scrollTop = container.scrollHeight;

  // 保留最近 50 条
  while (container.children.length > 50) {
    container.removeChild(container.firstChild);
  }
}
