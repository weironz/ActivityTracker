// ShopTrack 配置和常量

// 当通过 nginx 访问时，API 调用走相对路径；直接访问时用完整 URL
const BACKEND = window.location.hostname === 'localhost' ? 'http://localhost:5000' : '';

// 生成随机 userId（模拟登录用户）
const userId = 'user_' + Math.random().toString(36).substr(2, 6);

// 商品数据
const products = [
  { id: 1,  name: 'AirPods Pro 2',    category: '数码', price: 1799, emoji: '🎧', hot: true  },
  { id: 2,  name: '机械键盘 87键',     category: '数码', price: 459,  emoji: '⌨️', hot: false },
  { id: 3,  name: '4K 显示器 27寸',   category: '数码', price: 2299, emoji: '🖥️', hot: true  },
  { id: 4,  name: '无线充电底座',      category: '数码', price: 199,  emoji: '🔋', hot: false },
  { id: 5,  name: '北欧风台灯',        category: '家居', price: 329,  emoji: '💡', hot: false },
  { id: 6,  name: '香氛蜡烛套装',      category: '家居', price: 189,  emoji: '🕯️', hot: true  },
  { id: 7,  name: '懒人沙发豆袋',      category: '家居', price: 599,  emoji: '🛋️', hot: false },
  { id: 8,  name: '复古牛仔夹克',      category: '服饰', price: 699,  emoji: '🧥', hot: true  },
  { id: 9,  name: '手工真皮钱包',      category: '服饰', price: 399,  emoji: '👛', hot: false },
  { id: 10, name: '联名帆布鞋',        category: '服饰', price: 529,  emoji: '👟', hot: true  },
  { id: 11, name: '日本抹茶礼盒',      category: '食品', price: 128,  emoji: '🍵', hot: false },
  { id: 12, name: '手工巧克力礼盒',    category: '食品', price: 228,  emoji: '🍫', hot: true  },
];

// 分类映射
const categoryMap = {
  '全部': 'all',
  '数码': '数码',
  '家居': '家居',
  '服饰': '服饰',
  '食品': '食品'
};

// UI 状态
const uiState = {
  recOpen: false,
  currentSearchKeyword: '',
  searchTimeout: null
};
