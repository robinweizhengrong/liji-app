# 礼纪APP功能清单

## ✅ 已实现功能

### 1. 前端界面
- [x] 工具箱页面（首页）
- [x] 档期日历页面
- [x] 客户管理页面
- [x] 个人中心页面
- [x] 底部导航切换
- [x] 响应式设计（移动端适配）

### 2. 后端API
- [x] 档期管理API（增删改查）
- [x] 客户管理API（增删改查）
- [x] 文件上传API
- [x] 统计数据API

### 3. 数据库
- [x] SQLite数据库
- [x] 档期表
- [x] 客户表
- [x] 服务记录表
- [x] 文件上传表
- [x] 数据库初始化脚本

### 4. 文件上传
- [x] 支持图片上传
- [x] 支持文档上传
- [x] 10MB文件大小限制
- [x] 上传文件管理

## 🚧 待开发功能

### 1. 用户系统
- [ ] 用户注册/登录
- [ ] JWT身份认证
- [ ] 密码加密存储

### 2. 档期管理增强
- [ ] 日历视图月/周切换
- [ ] 档期时间冲突检测
- [ ] 档期提醒通知
- [ ] 档期状态管理（已接/预留/取消）

### 3. 客户管理增强
- [ ] 客户搜索功能
- [ ] 客户标签分类
- [ ] 客户历史服务记录
- [ ] 一键拨号

### 4. 工具箱内容
- [ ] 主持词库（告别仪式、守灵、出殡等）
- [ ] 悼词模板（通用、长辈专用、简约版）
- [ ] 仪式流程表
- [ ] 报价单生成
- [ ] 合同模板

### 5. VIP功能
- [ ] VIP会员体系
- [ ] 付费解锁内容
- [ ] 收入统计图表

### 6. 团队功能
- [ ] 团队创建/加入
- [ ] 团队成员管理
- [ ] 团队共享日历
- [ ] 团队业绩统计

### 7. 其他功能
- [ ] 数据备份/恢复
- [ ] 导出Excel
- [ ] 打印功能
- [ ] 暗黑模式

## 📝 项目文件清单

```
礼纪APP/
├── README.md                 # 项目说明
├── FEATURES.md               # 本文件
├── start.sh                  # 启动脚本
├── frontend/                 # 前端目录
│   ├── index.html           # 主页面
│   └── js/
│       └── api.js           # API接口
├── backend/                  # 后端目录
│   ├── package.json         # 依赖配置
│   └── server.js            # Express服务器
├── database/                 # 数据库目录
│   ├── init.js              # 初始化脚本
│   └── liji.db              # SQLite数据库
├── uploads/                  # 上传文件目录
└── docs/                     # 文档目录
```

## 🚀 部署方式

### 方式1：本地运行
```bash
./start.sh
```

### 方式2：GitHub Pages
前端静态文件可部署到GitHub Pages

### 方式3：Vercel
支持部署到Vercel（需要配置后端）

## 📊 数据库结构

### bookings（档期表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | TEXT | 主键 |
| type | TEXT | 服务类型 |
| start_time | TEXT | 开始时间 |
| end_time | TEXT | 结束时间 |
| customer_name | TEXT | 客户姓名 |
| customer_phone | TEXT | 客户电话 |
| location | TEXT | 服务地点 |
| amount | REAL | 服务金额 |
| notes | TEXT | 备注 |
| status | TEXT | 状态 |
| created_at | TEXT | 创建时间 |

### customers（客户表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | TEXT | 主键 |
| name | TEXT | 姓名 |
| phone | TEXT | 电话 |
| notes | TEXT | 备注 |
| source | TEXT | 来源 |
| created_at | TEXT | 创建时间 |

## 🔧 技术栈
- 前端：HTML5 + CSS3 + JavaScript
- 后端：Node.js + Express
- 数据库：SQLite3
- 文件上传：Multer
