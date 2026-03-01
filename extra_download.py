#!/usr/bin/env python3
"""
补充下载 - 针对未成功的职业
使用Lorem Picsum和其他图片来源
"""
import os
import json
import time
import random
import requests
from pathlib import Path

BASE_DIR = Path.home() / "Desktop/礼纪APP/assets/scenes_real"

# 需要补充的职业和更通用的关键词
PROFESSIONS_EXTRA = {
    "策划师": ["event", "planning", "ceremony", "hall"],
    "主持人": ["speaker", "microphone", "presentation", "stage"],
    "礼仪师": ["service", "welcome", "ceremony", "elegant"],
    "入殓师": ["portrait", "peaceful", "tribute", "memorial"],
    # 已有图片的职业也补充更多
    "花艺师": ["flower", "white+rose", "lily", "chrysanthemum"],
    "摄像师": ["camera", "video", "recording", "film"],
    "摄影师": ["camera", "photo", "lens", "portrait"],
    "歌手": ["singer", "microphone", "performance", "music"],
    "舞蹈": ["dance", "performance", "ballet", "stage"],
    "乐队": ["musician", "guitar", "piano", "concert"],
    "法事": ["prayer", "temple", "candle", "meditation"],
    "殡仪馆": ["memorial", "hall", "church", "temple"],
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}

def download_picsum(profession, keywords, start_idx=1, max_count=10):
    """使用Lorem Picsum下载高质量占位图片"""
    prof_dir = BASE_DIR / profession
    prof_dir.mkdir(exist_ok=True)
    
    count = 0
    for keyword in keywords:
        if count >= max_count:
            break
        
        for i in range(3):  # 每个关键词尝试3次
            if count >= max_count:
                break
            
            try:
                # 使用 picsum.photos 获取随机图片
                seed = f"{profession}_{keyword}_{i}_{random.randint(1000, 9999)}"
                url = f"https://picsum.photos/seed/{seed}/800/600"
                
                filename = f"picsum_{profession}_{start_idx + count:02d}.jpg"
                filepath = prof_dir / filename
                
                print(f"  [{profession}] 下载 {filename}...")
                
                resp = requests.get(url, headers=HEADERS, timeout=30, allow_redirects=True)
                if resp.status_code == 200 and len(resp.content) > 5000:
                    with open(filepath, 'wb') as f:
                        f.write(resp.content)
                    count += 1
                    print(f"    ✓ 成功 ({len(resp.content)} bytes)")
                else:
                    print(f"    ✗ 失败")
                
                time.sleep(random.uniform(0.3, 0.8))
            except Exception as e:
                print(f"    ✗ 错误: {e}")
    
    return count

print("=" * 60)
print("礼纪APP - 补充下载图片")
print("=" * 60)

# 先检查现有图片数量
total_existing = 0
for prof_dir in BASE_DIR.iterdir():
    if prof_dir.is_dir():
        count = len(list(prof_dir.glob("*.jpg")))
        total_existing += count
        print(f"【{prof_dir.name}】: 已有 {count} 张")

print(f"\n现有总计: {total_existing} 张")
print("-" * 60)

# 为每个职业补充下载
new_total = 0
for profession, keywords in PROFESSIONS_EXTRA.items():
    prof_dir = BASE_DIR / profession
    existing = len(list(prof_dir.glob("*.jpg"))) if prof_dir.exists() else 0
    needed = max(0, 15 - existing)
    
    if needed > 0:
        print(f"\n【{profession}】已有 {existing} 张，需补充 {needed} 张")
        n = download_picsum(profession, keywords, start_idx=existing+1, max_count=needed)
        new_total += n
    else:
        print(f"\n【{profession}】已有 {existing} 张，无需补充")

print("\n" + "=" * 60)
print(f"本次新增: {new_total} 张")

# 重新统计
final_total = 0
for prof_dir in BASE_DIR.iterdir():
    if prof_dir.is_dir():
        count = len(list(prof_dir.glob("*.jpg")))
        final_total += count

print(f"最终总计: {final_total} 张图片")
print(f"保存位置: {BASE_DIR}")
print("=" * 60)
