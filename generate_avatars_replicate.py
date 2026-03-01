#!/usr/bin/env python3
"""
礼纪APP - AI 虚拟头像批量生成脚本 (Replicate 版本)
为12个职业生成120个虚拟头像（每职业10人，5男5女）
"""

import os
import sys
import time
import requests
from pathlib import Path
from typing import Dict

# 配置
OUTPUT_BASE_DIR = Path.home() / "Desktop/礼纪APP/assets/avatars"
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN", "")
REPLICATE_API_URL = "https://api.replicate.com/v1/predictions"

# 职业配置 (英文提示词，针对 SDXL 优化)
PROFESSIONS: Dict[str, Dict] = {
    "策划师": {
        "male": "Professional Chinese male event planner, 35-45 years old, professional appearance, calm and approachable expression, business casual attire, office background",
        "female": "Professional Chinese female event planner, 35-45 years old, professional appearance, calm and approachable expression, elegant business attire, office background",
    },
    "主持人": {
        "male": "Chinese male host MC, 30-40 years old, confident posture, excellent temperament, formal suit, stage background",
        "female": "Chinese female host MC, 30-40 years old, confident posture, excellent temperament, elegant dress, stage background",
    },
    "礼仪师": {
        "male": "Chinese male etiquette master, 35-50 years old, dignified appearance, polite gentle expression, traditional formal attire",
        "female": "Chinese female etiquette master, 35-50 years old, dignified appearance, polite gentle expression, elegant traditional dress",
    },
    "入殓师": {
        "male": "Chinese male mortician embalmer, 35-50 years old, professional appearance, careful meticulous expression, solemn demeanor, clean work uniform",
        "female": "Chinese female mortician embalmer, 35-50 years old, professional appearance, careful meticulous expression, solemn demeanor, clean work uniform",
    },
    "花艺师": {
        "male": "Chinese male florist, 30-45 years old, artistic appearance, delicate aesthetic sense, surrounded by flowers, casual artistic attire, flower shop background",
        "female": "Chinese female florist, 30-45 years old, artistic appearance, delicate aesthetic sense, surrounded by flowers, elegant artistic attire, flower shop background",
    },
    "摄像师": {
        "male": "Chinese male videographer cameraman, 30-45 years old, technical appearance, focused expression, camera equipment, practical work clothes",
        "female": "Chinese female videographer cameraman, 30-45 years old, technical appearance, focused expression, camera equipment, practical work clothes",
    },
    "摄影师": {
        "male": "Chinese male photographer, 30-45 years old, artistic appearance, keen eye expression, professional camera, casual artistic attire",
        "female": "Chinese female photographer, 30-45 years old, artistic appearance, keen eye expression, professional camera, casual artistic attire",
    },
    "歌手": {
        "male": "Chinese male singer, 25-40 years old, expressive appearance, confident stage presence, performance attire, concert background",
        "female": "Chinese female singer, 25-40 years old, expressive appearance, confident stage presence, elegant performance dress, concert background",
    },
    "舞蹈": {
        "male": "Chinese male dancer, 25-40 years old, excellent physique, expressive posture, graceful movements, dance practice attire, dance studio background",
        "female": "Chinese female dancer, 25-40 years old, excellent physique, expressive posture, graceful movements, dance practice attire, dance studio background",
    },
    "乐队": {
        "male": "Chinese male band musician, 30-45 years old, musical appearance, professional demeanor, musical instrument, artistic attire",
        "female": "Chinese female band musician, 30-45 years old, musical appearance, professional demeanor, musical instrument, artistic attire",
    },
    "法事": {
        "male": "Chinese male Taoist priest ceremony master, 40-55 years old, solemn appearance, cultivated demeanor, traditional Taoist robe, temple background",
        "female": "Chinese female Taoist priest ceremony master, 40-55 years old, solemn appearance, cultivated demeanor, traditional Taoist robe, temple background",
    },
    "殡仪馆": {
        "male": "Chinese male funeral home staff, 35-50 years old, professional appearance, stable reliable demeanor, formal dark uniform",
        "female": "Chinese female funeral home staff, 35-50 years old, professional appearance, stable reliable demeanor, formal dark uniform",
    }
}

# 通用风格后缀
STYLE_SUFFIX = ", photorealistic portrait, neutral elegant color tone, soft natural lighting, high quality, detailed facial features, professional headshot, 8k"

def create_prediction(prompt: str, api_token: str) -> str:
    """创建 Replicate 预测任务"""
    headers = {
        "Authorization": f"Token {api_token}",
        "Content-Type": "application/json"
    }
    
    # 使用 SDXL 模型
    payload = {
        "version": "39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
        "input": {
            "prompt": prompt,
            "width": 512,
            "height": 512,
            "num_inference_steps": 30,
            "guidance_scale": 7.5,
            "seed": hash(prompt) % 1000000
        }
    }
    
    response = requests.post(REPLICATE_API_URL, headers=headers, json=payload, timeout=60)
    
    if response.status_code != 201:
        print(f"    错误: API 返回 {response.status_code}")
        print(f"    响应: {response.text[:200]}")
        return None
    
    return response.json().get("id")

def get_prediction_result(prediction_id: str, api_token: str, max_retries: int = 60) -> str:
    """获取预测结果"""
    headers = {"Authorization": f"Token {api_token}"}
    
    for _ in range(max_retries):
        response = requests.get(
            f"{REPLICATE_API_URL}/{prediction_id}",
            headers=headers,
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"    错误: 获取结果失败 {response.status_code}")
            return None
        
        data = response.json()
        status = data.get("status")
        
        if status == "succeeded":
            output = data.get("output")
            if isinstance(output, list) and len(output) > 0:
                return output[0]
            elif isinstance(output, str):
                return output
            return None
        elif status == "failed":
            print(f"    错误: 生成失败 - {data.get('error', 'Unknown error')}")
            return None
        
        # 等待后重试
        time.sleep(2)
    
    print("    错误: 超时")
    return None

def generate_avatar(profession: str, gender: str, index: int, api_token: str) -> bool:
    """生成单个头像"""
    prof_config = PROFESSIONS[profession]
    base_prompt = prof_config["male"] if gender == "male" else prof_config["female"]
    full_prompt = base_prompt + STYLE_SUFFIX
    
    output_dir = OUTPUT_BASE_DIR / profession
    output_dir.mkdir(parents=True, exist_ok=True)
    
    filename = f"{profession}_{gender}_{index+1:02d}.jpg"
    output_path = output_dir / filename
    
    # 检查是否已存在
    if output_path.exists():
        print(f"  跳过 (已存在): {filename}")
        return True
    
    print(f"  生成: {filename}")
    
    # 创建预测任务
    prediction_id = create_prediction(full_prompt, api_token)
    if not prediction_id:
        return False
    
    # 获取结果
    image_url = get_prediction_result(prediction_id, api_token)
    if not image_url:
        return False
    
    # 下载图片
    try:
        img_response = requests.get(image_url, timeout=60)
        if img_response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(img_response.content)
            print(f"    ✓ 已保存: {output_path}")
            return True
        else:
            print(f"    错误: 下载图片失败 {img_response.status_code}")
            return False
    except Exception as e:
        print(f"    错误: {str(e)}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("礼纪APP - AI 虚拟头像批量生成 (Replicate)")
    print("=" * 60)
    print()
    
    api_token = REPLICATE_API_TOKEN
    
    if not api_token:
        print("⚠️  警告: 未检测到 REPLICATE_API_TOKEN")
        print()
        print("请按以下步骤获取 API Token:")
        print("1. 访问 https://replicate.com/")
        print("2. 注册账号（支持邮箱或 GitHub 账号）")
        print("3. 进入 Account Settings → API Tokens")
        print("4. 创建新的 API Token")
        print("5. 设置环境变量: export REPLICATE_API_TOKEN='your-token'")
        print()
        print("新用户有免费试用额度")
        print()
        return
    
    # 统计
    total_count = 0
    success_count = 0
    
    # 为每个职业生成头像
    for profession in PROFESSIONS.keys():
        print(f"\n【{profession}】")
        print("-" * 40)
        
        for gender in ["male", "female"]:
            gender_cn = "男" if gender == "male" else "女"
            print(f"  生成 5 位{gender_cn}性头像:")
            
            for i in range(5):
                total_count += 1
                if generate_avatar(profession, gender, i, api_token):
                    success_count += 1
                # 添加延迟避免 rate limit
                time.sleep(3)
    
    print()
    print("=" * 60)
    print("生成完成!")
    print("=" * 60)
    print(f"总计: {total_count} 张")
    print(f"成功: {success_count} 张")
    print(f"失败: {total_count - success_count} 张")
    print(f"\n保存路径: {OUTPUT_BASE_DIR}")
    print()
    
    # 列出生成的文件
    print("目录结构:")
    for profession in PROFESSIONS.keys():
        prof_dir = OUTPUT_BASE_DIR / profession
        if prof_dir.exists():
            files = list(prof_dir.glob("*.jpg"))
            print(f"  {profession}/: {len(files)} 张")

if __name__ == "__main__":
    main()
