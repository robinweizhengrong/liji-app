# 礼纪APP AI 虚拟头像生成方案

## 任务概述
为12个职业生成120个虚拟头像（每职业10人，5男5女）

## 已创建的脚本

### 1. generate_avatars.py (Together AI)
- 使用 Together AI 的 Stable Diffusion XL 模型
- 新用户可获得 $5 免费额度
- 注册地址: https://api.together.ai/
- 使用方法:
  ```bash
  export TOGETHER_API_KEY='your-api-key'
  python3 generate_avatars.py
  ```

### 2. generate_avatars_replicate.py (Replicate)
- 使用 Replicate 的 SDXL 模型
- 新用户有免费试用额度
- 注册地址: https://replicate.com/
- 使用方法:
  ```bash
  export REPLICATE_API_TOKEN='your-token'
  python3 generate_avatars_replicate.py
  ```

## 备选方案

### 方案 A: Silicon Flow (推荐)
国内服务，注册即可获得免费额度
- 注册地址: https://siliconflow.cn/
- 模型选择: stabilityai/stable-diffusion-xl-base-1.0

### 方案 B: 阿里云 DashScope
- 注册地址: https://dashscope.aliyun.com/
- 模型选择: wanx-v1 (通义万相)
- 新用户有免费额度

### 方案 C: 本地部署 Stable Diffusion
如果有 NVIDIA GPU，可以本地部署:
```bash
pip install diffusers torch transformers
python -c "from diffusers import StableDiffusionPipeline; ..."
```

## 目录结构
```
~/Desktop/礼纪APP/assets/avatars/
├── 策划师/          # 10张 (5男5女)
├── 主持人/          # 10张
├── 礼仪师/          # 10张
├── 入殓师/          # 10张
├── 花艺师/          # 10张
├── 摄像师/          # 10张
├── 摄影师/          # 10张
├── 歌手/            # 10张
├── 舞蹈/            # 10张
├── 乐队/            # 10张
├── 法事/            # 10张
└── 殡仪馆/          # 10张
```

## 生成参数
- 尺寸: 512x512
- 风格: 写实照片风格
- 色调: 中性素雅
- 年龄: 30-50岁为主（歌手、舞蹈 25-40岁）
- 背景: 简洁纯色或工作环境

## 职业列表与特征

| 职业 | 男性特征 | 女性特征 |
|------|----------|----------|
| 策划师 | 专业、沉稳、有亲和力 | 专业、沉稳、有亲和力 |
| 主持人 | 声音洪亮、气质佳 | 声音洪亮、气质佳 |
| 礼仪师 | 端庄、有礼、温和 | 端庄、有礼、温和 |
| 入殓师 | 专业、细心、庄重 | 专业、细心、庄重 |
| 花艺师 | 艺术感、细腻、有审美 | 艺术感、细腻、有审美 |
| 摄像师 | 技术感、专注 | 技术感、专注 |
| 摄影师 | 艺术感、敏锐 | 艺术感、敏锐 |
| 歌手 | 有表现力、声音好 | 有表现力、声音好 |
| 舞蹈 | 形体好、有表现力 | 形体好、有表现力 |
| 乐队 | 音乐感、专业 | 音乐感、专业 |
| 法事 | 庄重、有修为 | 庄重、有修为 |
| 殡仪馆 | 专业、稳重 | 专业、稳重 |

## 下一步操作

1. 选择上述任一 API 服务注册账号
2. 获取 API Key/Token
3. 设置环境变量
4. 运行对应的生成脚本

预计生成时间: 约 30-60 分钟（120张图片，每张约 15-30 秒）
