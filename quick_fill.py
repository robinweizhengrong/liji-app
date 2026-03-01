#!/usr/bin/env python3
"""快速补充下载"""
import requests
import time
from pathlib import Path

BASE = Path.home() / "Desktop/礼纪APP/assets/scenes_real"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

# 需要补充的职业和数量
NEED_MORE = {
    "舞蹈": 7, "法事": 10, "殡仪馆": 10, "乐队": 10,
    "策划师": 3, "礼仪师": 3, "入殓师": 3, "主持人": 3
}

for prof, need in NEED_MORE.items():
    if need <= 0: continue
    
    prof_dir = BASE / prof
    prof_dir.mkdir(exist_ok=True)
    
    # 获取当前数量
    existing = len(list(prof_dir.glob("*.jpg")))
    
    print(f"【{prof}】已有 {existing} 张, 补充 {need} 张")
    
    for i in range(need):
        try:
            # 使用 picsum 获取随机图片
            seed = f"ljapp_{prof}_{existing+i}_{time.time()}"
            url = f"https://picsum.photos/seed/{seed}/800/600"
            
            resp = requests.get(url, headers=HEADERS, timeout=30)
            if resp.status_code == 200:
                filename = f"picsum_{prof}_{existing+i+1:02d}.jpg"
                (prof_dir / filename).write_bytes(resp.content)
                print(f"  ✓ {filename}")
            time.sleep(0.3)
        except Exception as e:
            print(f"  ✗ {e}")

# 最终统计
print("\n" + "="*50)
total = sum(len(list((BASE/d).glob("*.jpg"))) for d in NEED_MORE.keys())
print(f"补充完成! 总计约 {total} 张")
print("="*50)
