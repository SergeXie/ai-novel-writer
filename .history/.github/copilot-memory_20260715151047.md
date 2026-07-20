# Vue + Vite 项目布局常见陷阱

> 2025-07-15 调试 NovelView 自适应布局时总结

## 1. 嵌套 `id="app"` 导致宽度塌陷

**问题**: `index.html` 有 `<div id="app">`，`App.vue` 模板根元素也是 `<div id="app">`，导致 DOM 中出现两层同 id 嵌套。外层 `#app` 设了 `display: flex`，内层 `#app` 作为 flex 子元素，宽度会收缩为内容固有宽度（而非拉伸到父容器宽度）。

**表现**: 页面在大屏幕（如 1800px）下内容区域不贴边，所有子元素宽度约 786px。

**修复**: 移除 `App.vue` 模板中的 `<div id="app">` 包裹层，让 navbar/main/footer 直接作为 `index.html` 中 `#app` 的子元素。Vue 3 支持多根节点（fragments）。

**验证方法**: `document.querySelector('#app').children` 检查子元素数量和标签。

## 2. `align-items: normal` 不一定等于 `stretch`

**问题**: `#app` 作为 column flex 容器，默认 `align-items: normal`。理论上 `normal` 在 flex 中应等同于 `stretch`，但当子元素有 `display: flex` 或 `position: sticky` 时可能不生效。

**修复**: 显式设置 `align-items: stretch`。

## 3. `body` 居中样式影响全站布局

**问题**: Vite 脚手架默认在 `base.css`/`main.css` 中有 `body { display: flex; place-items: center; }`（≥1024px 断点），导致 `#app` 居中而非贴边。

**修复**: 删除该媒体查询，或改为 `place-items: stretch`。

## 4. `position: sticky` 与 flex 的宽度交互

**问题**: `position: sticky` 的 flex 子元素在某些浏览器中不被 `align-items: stretch` 拉伸。

**修复**: 显式添加 `width: 100%`。

## 5. `overflow: auto` 创建层叠上下文

**问题**: `messages-area` 设了 `overflow: auto`，会创建新的层叠上下文，可能拦截上方元素（如 `top-bar`）的点击事件。

**修复**: 给 `top-bar` 加 `position: relative; z-index: 1`，给 `messages-area` 加 `min-height: 0` 防止 flex 子元素溢出。

## 6. Flex 子元素高度溢出

**问题**: 在 column flex 布局中，`messages-area` 用 `flex: 1` 填充剩余空间，但 `welcome-screen` 设了 `height: 100%` 可能导致溢出。

**修复**: `messages-area` 加 `min-height: 0; flex-shrink: 0`（对 input-area），`welcome-screen` 改用 `min-height: 100%`。
