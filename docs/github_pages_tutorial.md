# GitHub Pages 设置教程

## 设置步骤

### 第1步：打开GitHub仓库
访问：https://github.com/robinweizhengrong/liji-app

### 第2步：进入Settings
在仓库页面顶部，点击 Settings 标签（在最右边）

### 第3步：找到Pages设置
在左侧菜单栏向下滚动，找到 Pages 选项

### 第4步：配置Source
在 Build and deployment 区域：
- Source: 选择 Deploy from a branch
- Branch: 选择 main
- 文件夹: 选择 /(root)
- 点击 Save 按钮

### 第5步：确认设置成功
设置成功后，页面上方会显示绿色提示：
Your site is live at https://robinweizhengrong.github.io/liji-app/

### 第6步：访问网站
等待2-5分钟后，访问：
https://robinweizhengrong.github.io/liji-app/

---

## 常见问题

### 问题1：404错误
原因：Branch设置错误
解决：确认Branch选择的是 main（不是master）

### 问题2：页面空白
原因：index.html不在根目录
解决：检查仓库根目录是否有index.html

### 问题3：CSS/JS加载失败
原因：路径错误
解决：检查文件引用路径

---

## 快速检查清单

- [ ] 访问 github.com/robinweizhengrong/liji-app
- [ ] 点击 Settings
- [ ] 点击左侧 Pages
- [ ] Source 选择 Deploy from a branch
- [ ] Branch 选择 main
- [ ] 选择 /(root) 文件夹
- [ ] 点击 Save
- [ ] 等待2-5分钟
- [ ] 访问 robinweizhengrong.github.io/liji-app/
