# 礼纪APP - AI生成殡葬场景图片

## 任务概述
生成120张殡葬行业场景图片，12个职业类别，每个10张。

## 目录结构
```
~/Desktop/礼纪APP/assets/scenes_ai/
├── 01_策划师/ (10张)
├── 02_主持人/ (10张)
├── 03_礼仪师/ (10张)
├── 04_入殓师/ (10张)
├── 05_花艺师/ (10张)
├── 06_摄像师/ (10张)
├── 07_摄影师/ (10张)
├── 08_歌手/ (10张)
├── 09_舞蹈/ (10张)
├── 10_乐队/ (10张)
├── 11_法事/ (10张)
└── 12_殡仪馆/ (10张)
```

## API提供商选择

### 1. Together AI (推荐)
- 网址: https://api.together.xyz/
- 优惠: 新用户免费$5额度
- 模型: black-forest-labs/FLUX.1-schnell
- 设置: `export TOGETHER_API_KEY=your_api_key`

### 2. Silicon Flow (国内)
- 网址: https://siliconflow.cn/
- 特点: 国内服务，访问稳定
- 模型: black-forest-labs/FLUX.1-schnell
- 设置: `export SILICONFLOW_API_KEY=your_api_key`

### 3. Replicate
- 网址: https://replicate.com/
- 模型: black-forest-labs/flux-schnell
- 设置: `export REPLICATE_API_TOKEN=your_api_token`

## 图片规格
- 尺寸: 1024x1024 或 1024x768
- 格式: JPG
- 风格: 写实照片风格，中性素雅色调

## 使用方法

### 方式1: 使用Python脚本
```bash
cd ~/.openclaw/workspace
export TOGETHER_API_KEY=your_api_key
python3 generate_funeral_scenes.py
```

## 生成脚本
脚本位置: `~/.openclaw/workspace/generate_funeral_scenes.py`

## 当前状态
- 目录结构: 已创建 ✓
- 生成脚本: 已准备 ✓
- API密钥: 待设置
- 图片生成: 待执行
