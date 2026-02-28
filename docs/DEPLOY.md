# 礼纪APP部署指南

## 🚀 本地部署

### 步骤1：安装Node.js
访问 https://nodejs.org 下载并安装LTS版本

### 步骤2：进入项目目录
```bash
cd ~/Desktop/礼纪APP
```

### 步骤3：运行启动脚本
```bash
./start.sh
```

或者手动启动：
```bash
# 安装依赖
cd backend
npm install

# 初始化数据库
cd ../database
node init.js

# 启动服务器
cd ../backend
npm start
```

### 步骤4：访问应用
- 本地访问：http://localhost:3000
- 手机访问：使用电脑IP地址（如 http://192.168.1.100:3000）

## 🌐 GitHub Pages部署（前端）

### 步骤1：创建GitHub仓库
1. 登录GitHub
2. 创建新仓库，命名为 `liji-app`

### 步骤2：上传文件
1. 进入frontend目录
2. 将index.html上传到仓库根目录

### 步骤3：开启GitHub Pages
1. 进入仓库Settings
2. 找到Pages选项
3. Source选择 main分支
4. 保存并等待部署

### 访问地址
https://你的用户名.github.io/liji-app/

## ☁️ Vercel部署

### 步骤1：安装Vercel CLI
```bash
npm i -g vercel
```

### 步骤2：部署
```bash
cd ~/Desktop/礼纪APP/backend
vercel
```

### 步骤3：配置环境变量
在Vercel控制台添加必要的环境变量

## 📱 手机访问

### 同一WiFi下访问
1. 确保手机和电脑在同一WiFi
2. 查看电脑IP地址
3. 手机浏览器输入：`http://电脑IP:3000`

### 公网访问
- 使用内网穿透工具（如ngrok）
- 部署到云服务器
- 使用Vercel/Netlify等托管平台

## 🔧 常见问题

### 1. 端口被占用
修改backend/server.js中的PORT变量
```javascript
const PORT = process.env.PORT || 3001;
```

### 2. 数据库权限错误
检查database目录权限
```bash
chmod 755 ~/Desktop/礼纪APP/database
```

### 3. 文件上传失败
检查uploads目录是否存在
```bash
mkdir -p ~/Desktop/礼纪APP/uploads
```

## 📊 生产环境建议

### 1. 安全性
- 添加用户认证系统
- 使用HTTPS
- 数据库加密敏感信息

### 2. 性能
- 使用CDN加速静态资源
- 数据库索引优化
- 缓存策略

### 3. 备份
- 定期备份数据库
- 文件自动备份到云存储

## 📝 更新日志

### v1.0.0 (2026-02-26)
- ✅ 初始版本发布
- ✅ 完成基础功能开发
- ✅ 支持本地部署
