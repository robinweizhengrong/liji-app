#!/usr/bin/env python3
"""
直接抓取免费图片网站的真实图片
"""
import re
import os
import json
import time
import random
import requests
from pathlib import Path
from urllib.parse import urljoin, urlparse

BASE_DIR = Path.home() / "Desktop/礼纪APP/assets/scenes_real"
BASE_DIR.mkdir(parents=True, exist_ok=True)

# 职业和关键词
PROFESSIONS = {
    "策划师": {"unsplash": "funeral+ceremony", "pexels": "funeral", "pixabay": "funeral"},
    "主持人": {"unsplash": "memorial+service", "pexels": "memorial", "pixabay": "memorial"},
    "礼仪师": {"unsplash": "funeral+service", "pexels": "ceremony", "pixabay": "ceremony"},
    "入殓师": {"unsplash": "mortician", "pexels": "mortician", "pixabay": "mortician"},
    "花艺师": {"unsplash": "funeral+flowers", "pexels": "white+flowers", "pixabay": "funeral+flowers"},
    "摄像师": {"unsplash": "videographer", "pexels": "videographer", "pixabay": "videographer"},
    "摄影师": {"unsplash": "photographer", "pexels": "photographer", "pixabay": "photographer"},
    "歌手": {"unsplash": "singer", "pexels": "singer", "pixabay": "singer"},
    "舞蹈": {"unsplash": "dancer", "pexels": "dance", "pixabay": "dance"},
    "乐队": {"unsplash": "band", "pexels": "band", "pixabay": "band"},
    "法事": {"unsplash": "buddhist+ceremony", "pexels": "buddhist", "pixabay": "buddhist"},
    "殡仪馆": {"unsplash": "funeral+home", "pexels": "funeral+home", "pixabay": "funeral+home"},
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

session = requests.Session()
session.headers.update(HEADERS)

def download_file(url, filepath):
    """下载文件"""
    try:
        time.sleep(random.uniform(0.5, 1.5))
        resp = session.get(url, timeout=30)
        if resp.status_code == 200 and len(resp.content) > 3000:
            with open(filepath, 'wb') as f:
                f.write(resp.content)
            return len(resp.content)
    except Exception as e:
        pass
    return 0

def scrape_unsplash(profession, keyword, max_count=5):
    """从Unsplash搜索图片"""
    downloads = []
    prof_dir = BASE_DIR / profession
    prof_dir.mkdir(exist_ok=True)
    
    try:
        url = f"https://unsplash.com/s/photos/{keyword}"
        resp = session.get(url, timeout=30)
        
        # 提取图片URL
        pattern = r'https://images\.unsplash\.com/photo-[a-zA-Z0-9_-]+\?[^"\s>]+'
        matches = list(set(re.findall(pattern, resp.text)))
        
        for i, img_url in enumerate(matches[:max_count]):
            filename = f"unsplash_{profession}_{i+1:02d}.jpg"
            filepath = prof_dir / filename
            
            # 获取高质量版本
            img_url = re.sub(r'w=\d+', 'w=800', img_url)
            if 'w=' not in img_url:
                img_url += '&w=800' if '?' in img_url else '?w=800'
            
            size = download_file(img_url, filepath)
            if size > 0:
                downloads.append(filename)
                print(f"  ✓ {filename} ({size} bytes)")
            else:
                print(f"  ✗ {filename}")
    except Exception as e:
        print(f"  错误: {e}")
    
    return downloads

def scrape_pexels(profession, keyword, max_count=5):
    """从Pexels搜索图片"""
    downloads = []
    prof_dir = BASE_DIR / profession
    prof_dir.mkdir(exist_ok=True)
    
    try:
        url = f"https://www.pexels.com/search/{keyword}/"
        resp = session.get(url, timeout=30)
        
        # 提取图片ID
        pattern = r'photos/(\d+)/'
        ids = list(set(re.findall(pattern, resp.text)))
        
        for i, pid in enumerate(ids[:max_count]):
            filename = f"pexels_{profession}_{i+1:02d}.jpg"
            filepath = prof_dir / filename
            
            img_url = f"https://images.pexels.com/photos/{pid}/pexels-photo-{pid}.jpeg?auto=compress&cs=tinysrgb&w=800"
            
            size = download_file(img_url, filepath)
            if size > 0:
                downloads.append(filename)
                print(f"  ✓ {filename} ({size} bytes)")
            else:
                print(f"  ✗ {filename}")
    except Exception as e:
        print(f"  错误: {e}")
    
    return downloads

def scrape_pixabay(profession, keyword, max_count=5):
    """从Pixabay搜索图片"""
    downloads = []
    prof_dir = BASE_DIR / profession
    prof_dir.mkdir(exist_ok=True)
    
    try:
        url = f"https://pixabay.com/images/search/{keyword}/"
        resp = session.get(url, timeout=30)
        
        # 提取图片URL
        pattern = r'https://cdn\.pixabay\.com/photo/[^"\s>]+\.jpg'
        matches = list(set(re.findall(pattern, resp.text)))
        
        for i, img_url in enumerate(matches[:max_count]):
            filename = f"pixabay_{profession}_{i+1:02d}.jpg"
            filepath = prof_dir / filename
            
            size = download_file(img_url, filepath)
            if size > 0:
                downloads.append(filename)
                print(f"  ✓ {filename} ({size} bytes)")
            else:
                print(f"  ✗ {filename}")
    except Exception as e:
        print(f"  错误: {e}")
    
    return downloads

# 主程序
print("=" * 60)
print("礼纪APP - 殡葬场景图片下载")
print("=" * 60)

results = {}
for profession, keywords in PROFESSIONS.items():
    print(f"\n【{profession}】")
    prof_downloads = []
    
    # 从每个网站下载
    if 'unsplash' in keywords:
        d = scrape_unsplash(profession, keywords['unsplash'], 5)
        prof_downloads.extend(d)
    
    if len(prof_downloads) < 15 and 'pexels' in keywords:
        d = scrape_pexels(profession, keywords['pexels'], 5)
        prof_downloads.extend(d)
    
    if len(prof_downloads) < 15 and 'pixabay' in keywords:
        d = scrape_pixabay(profession, keywords['pixabay'], 5)
        prof_downloads.extend(d)
    
    results[profession] = prof_downloads
    print(f"  完成: {len(prof_downloads)} 张")

# 统计
total = sum(len(v) for v in results.values())

# 保存报告
report = {
    'total': total,
    'professions': results,
    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
}

with open(BASE_DIR / 'download_report.json', 'w') as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

print("\n" + "=" * 60)
print(f"总计下载: {total} 张图片")
print(f"保存位置: {BASE_DIR}")
print("=" * 60)
