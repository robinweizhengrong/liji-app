#!/usr/bin/env python3
import os
import time
import random
import requests
from pathlib import Path

BASE_DIR = Path.home() / "Desktop/礼纪APP/assets/scenes_real"
BASE_DIR.mkdir(parents=True, exist_ok=True)

PROFESSIONS = {
    "策划师": ["funeral+ceremony", "memorial+service"],
    "主持人": ["memorial+speaker", "funeral+host"],
    "礼仪师": ["funeral+usher", "ceremony+service"],
    "入殓师": ["mortician", "funeral+director"],
    "花艺师": ["funeral+flowers", "white+flowers"],
    "摄像师": ["event+videographer", "video+recording"],
    "摄影师": ["event+photographer", "memorial+photo"],
    "歌手": ["memorial+singer", "funeral+singer"],
    "舞蹈": ["memorial+dance", "ceremonial+dance"],
    "乐队": ["memorial+band", "funeral+band"],
    "法事": ["buddhist+funeral", "taoist+ceremony"],
    "殡仪馆": ["funeral+home", "crematorium"],
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

def download_from_source(profession, keywords, max_count=15):
    prof_dir = BASE_DIR / profession
    prof_dir.mkdir(exist_ok=True)
    
    count = 0
    for keyword in keywords:
        if count >= max_count:
            break
        
        for i in range(8):
            if count >= max_count:
                break
            
            try:
                url = f"https://source.unsplash.com/800x600/?{keyword}"
                filename = f"unsplash_{profession}_{count+1:02d}.jpg"
                filepath = prof_dir / filename
                
                print(f"  [{profession}] 下载 {filename}...")
                
                resp = requests.get(url, headers=HEADERS, timeout=30, allow_redirects=True)
                if resp.status_code == 200 and len(resp.content) > 5000:
                    with open(filepath, 'wb') as f:
                        f.write(resp.content)
                    count += 1
                    print(f"    成功 ({len(resp.content)} bytes)")
                else:
                    print(f"    失败或文件太小")
                
                time.sleep(random.uniform(0.5, 1.5))
            except Exception as e:
                print(f"    错误: {e}")
                time.sleep(0.5)
    
    return count

print("=" * 60)
print("礼纪APP - 殡葬场景图片下载")
print("=" * 60)

total = 0
for profession, keywords in PROFESSIONS.items():
    print(f"\n【{profession}】")
    n = download_from_source(profession, keywords, 15)
    total += n
    print(f"  完成: {n} 张")

print("\n" + "=" * 60)
print(f"总计下载: {total} 张图片")
print(f"保存位置: {BASE_DIR}")
print("=" * 60)
