#!/usr/bin/env python3
"""
礼纪APP - AI 虚拟头像批量生成脚本
为12个职业生成120个虚拟头像（每职业10人，5男5女）
"""

import os
import sys
import time
import requests
from pathlib import Path
from typing import Dict, List

# 配置
OUTPUT_BASE_DIR = Path.home() / "Desktop/礼纪APP/assets/avatars"
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY", "")
TOGETHER_API_URL = "https://api.together.xyz/v1/images/generations"

# 职业配置
PROFESSIONS: Dict[str, Dict] = {
    "策划师": {
        "male": "Professional Chinese male event planner, 35-45 years old, professional appearance, calm and approachable expression, wearing business casual attire",
        "female": "Professional Chinese female event planner, 35-45 years old, professional appearance, calm and approachable expression, wearing elegant business attire",
        "traits": "professional, calm, approachable"
    },
    "主持人": {
        "male": "Chinese male host/MC, 30-40 years old, confident posture, loud and clear voice expression, excellent temperament, wearing formal suit",
        "female": "Chinese female host/MC, 30-40 years old, confident posture, loud and clear voice expression, excellent temperament, wearing elegant dress",
        "traits": "loud voice, excellent temperament, confident"
    },
    "礼仪师": {
        "male": "Chinese male etiquette master, 35-50 years old, dignified appearance, polite and gentle expression, proper posture, wearing traditional or formal attire",
        "female": "Chinese female etiquette master, 35-50 years old, dignified appearance, polite and gentle expression, proper posture, wearing elegant traditional dress",
        "traits": "dignified, polite, gentle"
    },
    "入殓师": {
        "male": "Chinese male mortician/embalmer, 35-50 years old, professional appearance, careful and meticulous expression, solemn demeanor, wearing clean work uniform",
        "female": "Chinese female mortician/embalmer, 35-50 years old, professional appearance, careful and meticulous expression, solemn demeanor, wearing clean work uniform",
        "traits": "professional, careful, solemn"
    },
    "花艺师": {
        "male": "Chinese male florist, 30-45 years old, artistic appearance, delicate and aesthetic sense, surrounded by flowers, wearing casual artistic attire",
        "female": "Chinese female florist, 30-45 years old, artistic appearance, delicate and aesthetic sense, surrounded by flowers, wearing elegant artistic attire",
        "traits": "artistic, delicate, aesthetic"
    },
    "摄像师": {
        "male": "Chinese male videographer/cameraman, 30-45 years old, technical appearance, focused expression, holding camera equipment, wearing practical work clothes",
        "female": "Chinese female videographer/cameraman, 30-45 years old, technical appearance, focused expression, holding camera equipment, wearing practical work clothes",
        "traits": "technical, focused, professional"
    },
    "摄影师": {
        "male": "Chinese male photographer, 30-45 years old, artistic appearance, keen eye expression, holding professional camera, wearing casual artistic attire",
        "female": "Chinese female photographer, 30-45 years old, artistic appearance, keen eye expression, holding professional camera, wearing casual artistic attire",
        "traits": "artistic, keen, professional"
    },
    "歌手": {
        "male": "Chinese male singer, 25-40 years old, expressive appearance, excellent voice quality, confident stage presence, wearing performance attire",
        "female": "Chinese female singer, 25-40 years old, expressive appearance, excellent voice quality, confident stage presence, wearing elegant performance dress",
        "traits": "expressive, excellent voice, confident"
    },
    "舞蹈": {
        "male": "Chinese male dancer, 25-40 years old, excellent physique, expressive posture, graceful movements, wearing dance practice attire",
        "female": "Chinese female dancer, 25-40 years old, excellent physique, expressive posture, graceful movements, wearing dance practice attire",
        "traits": "excellent physique, expressive, graceful"
    },
    "乐队": {
        "male": "Chinese male band musician, 30-45 years old, musical appearance, professional demeanor, holding musical instrument, wearing artistic attire",
        "female": "Chinese female band musician, 30-45 years old, musical appearance, professional demeanor, holding musical instrument, wearing artistic attire",
        "traits": "musical, professional, artistic"
    },
    "法事": {
        "male": "Chinese male Taoist priest/ceremony master, 40-55 years old, solemn appearance, cultivated demeanor, wearing traditional Taoist robe",
        "female": "Chinese female Taoist priest/ceremony master, 40-55 years old, solemn appearance, cultivated demeanor, wearing traditional Taoist robe",
        "traits": "solemn, cultivated, spiritual"
    },
    "殡仪馆": {
        "male": "Chinese male funeral home staff, 35-50 years old, professional appearance, stable and reliable demeanor, wearing formal dark uniform",
        "female": "Chinese female funeral home staff, 35-50 years old, professional appearance, stable and reliable demeanor, wearing formal dark uniform",
        "traits": "professional, stable, reliable"
    }
}

# 通用风格后缀
STYLE_SUFFIX = ", photorealistic portrait photography, neutral and elegant color tone, clean solid color or work environment background, soft natural lighting, high quality, 8k, detailed facial features, professional headshot"

def generate_avatar(profession: str, gender: str, index: int, api_key: str) -> bool:
    """生成单个头像"""
    if not api_key:
        print("错误: 未设置 TOGETHER_API_KEY 环境变量")
        print("请访问 https://api.together.ai/settings/api-keys 获取免费 API Key")
        return False
    
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
    print(f"    提示词: {full_prompt[:80]}...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "stabilityai/stable-diffusion-xl-base-1.0",
        "prompt": full_prompt,
        "width": 512,
        "height": 512,
        "steps": 30,
        "n": 1,
        "seed": hash(f"{profession}_{gender}_{index}") % 1000000
    }
    
    try:
        response = requests.post(
            TOGETHER_API_URL,
            headers=headers,
            json=payload,
            timeout=120
        )
        
        if response.status_code != 200:
            print(f"    错误: API 返回 {response.status_code}")
            print(f"    响应: {response.text[:200]}")
            return False
        
        data = response.json()
        
        # 检查响应格式
        if "data" in data and len(data["data"]) > 0:
            image_url = data["data"][0].get("url", "")
        elif "output" in data and "choices" in data["output"]:
            image_url = data["output"]["choices"][0].get("image_url", "")
        else:
            print(f"    错误: 无法解析响应格式")
            print(f"    响应: {str(data)[:200]}")
            return False
        
        if not image_url:
            print(f"    错误: 响应中没有图片 URL")
            return False
        
        # 下载图片
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
    print("礼纪APP - AI 虚拟头像批量生成")
    print("=" * 60)
    print()
    
    api_key = TOGETHER_API_KEY
    
    if not api_key:
        print("⚠️  警告: 未检测到 TOGETHER_API_KEY")
        print()
        print("请按以下步骤获取免费 API Key:")
        print("1. 访问 https://api.together.ai/")
        print("2. 注册账号（支持邮箱或 Google 账号）")
        print("3. 进入 Settings → API Keys")
        print("4. 创建新的 API Key")
        print("5. 设置环境变量: export TOGETHER_API_KEY='your-key'")
        print()
        print("新用户可获得 $5 免费额度，足够生成 120+ 张图片")
        print()
        response = input("是否继续查看生成计划? (y/n): ")
        if response.lower() != 'y':
            sys.exit(0)
    
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
                if api_key:
                    if generate_avatar(profession, gender, i, api_key):
                        success_count += 1
                    # 添加延迟避免 rate limit
                    time.sleep(1)
                else:
                    print(f"    - {profession}_{gender}_{i+1:02d}.jpg (需要 API Key)")
    
    print()
    print("=" * 60)
    print("生成完成!")
    print("=" * 60)
    print(f"总计: {total_count} 张")
    if api_key:
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
