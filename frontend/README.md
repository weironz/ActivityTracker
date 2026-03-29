# ShopTrack 前端项目

## 📁 项目结构

```
frontend/
├── index.html              # 主HTML文件
├── Dockerfile             # Docker镜像构建
├── activityTracker.conf.template  # Nginx配置模板
├── docker-entrypoint.sh   # 容器启动脚本
├── styles/               # 样式文件
│   ├── main.css         # 主样式
│   └── components.css   # 组件样式
└── scripts/             # JavaScript模块
    ├── config.js        # 配置和常量
    ├── api.js          # API调用和事件追踪
    ├── search.js       # 搜索功能
    ├── products.js     # 商品渲染
    ├── recommendations.js # 推荐系统
    └── ui.js          # UI交互
```

## 🎯 模块说明

### HTML文件
- `index.html` - 页面结构，引用所有样式和脚本

### 样式文件
- `main.css` - 全局样式、布局、基础组件
- `components.css` - 可复用组件样式

### JavaScript模块
- `config.js` - 配置、常量、状态管理
- `api.js` - 后端API调用、Kafka事件追踪
- `search.js` - 搜索功能实现
- `products.js` - 商品列表渲染和交互
- `recommendations.js` - 推荐系统UI
- `ui.js` - 通用UI组件和工具函数

## 🚀 开发说明

### 本地开发
```bash
# 直接在浏览器中打开 index.html
open frontend/index.html
```

### Docker部署
```bash
# 构建镜像
docker-compose build frontend

# 启动服务
docker-compose up frontend
```

## 📊 功能特性

- ✅ 实时搜索（带防抖和高亮）
- ✅ 分类筛选
- ✅ 商品浏览追踪
- ✅ 点击行为追踪
- ✅ 购买行为追踪
- ✅ 搜索关键词追踪
- ✅ 个性化推荐
- ✅ Kafka事件流日志

## 🔧 配置

后端地址在 `scripts/config.js` 中配置：
```javascript
const BACKEND = window.location.hostname === 'localhost'
  ? 'http://localhost:5000'
  : '';
```

## 🎨 样式自定义

修改CSS变量在 `styles/main.css` 的 `:root` 选择器中：
```css
:root {
  --accent: #e8c547;      /* 主色调 */
  --accent2: #ff6b35;     /* 辅助色 */
  --bg: #0e0e0e;         /* 背景色 */
  --surface: #1a1a1a;     /* 表面色 */
  --text: #f0ede8;        /* 文本色 */
}
```
