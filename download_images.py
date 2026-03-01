#!/usr/bin/env python3
"""
礼纪APP - 殡葬场景图片下载器
使用requests从Unsplash、Pexels、Pixabay下载图片
"""

import os
import json
import time
import random
import requests
import re
from pathlib import Path
from urllib.parse import urlparse

# 基础目录
BASE_DIR = Path.home() / "Desktop/礼纪APP/assets/scenes_real"

# 职业和搜索关键词映射
PROFESSIONS = {
    "策划师": {
        "unsplash": ["funeral ceremony", "memorial service setup", "funeral planning"],
        "pexels": ["funeral ceremony", "memorial service"],
        "pixabay": ["funeral", "memorial service"]
    },
    "主持人": {
        "unsplash": ["memorial service speaker", "funeral ceremony", "memorial ceremony"],
        "pexels": ["memorial service", "funeral ceremony"],
        "pixabay": ["funeral", "memorial service"]
    },
    "礼仪师": {
        "unsplash": ["funeral service", "ceremony usher", "memorial service"],
        "pexels": ["funeral service", "ceremony"],
        "pixabay": ["funeral service", "memorial"]
    },
    "入殓师": {
        "unsplash": ["mortician", "funeral director", "embalming"],
        "pexels": ["funeral home", "mortician"],
        "pixabay": ["funeral home", "mortician"]
    },
    "花艺师": {
        "unsplash": ["funeral flowers", "white flowers", "funeral wreath", "memorial flowers"],
        "pexels": ["white flowers", "funeral flowers"],
        "pixabay": ["funeral flowers", "white flowers"]
    },
    "摄像师": {
        "unsplash": ["event videographer", "camera operator", "video recording ceremony"],
        "pexels": ["videographer", "camera operator"],
        "pixabay": ["videographer", "camera"]
    },
    "摄影师": {
        "unsplash": ["event photographer", "camera ceremony", "memorial photography"],
        "pexels": ["photographer", "event photography"],
        "pixabay": ["photographer", "camera"]
    },
    "歌手": {
        "unsplash": ["memorial singer", "funeral singer", "memorial performance"],
        "pexels": ["singer performance", "memorial singer"],
        "pixabay": ["singer", "memorial performance"]
    },
    "舞蹈": {
        "unsplash": ["memorial dance", "ceremonial dance", "memorial performance"],
        "pexels": ["dance performance", "memorial dance"],
        "pixabay": ["dance", "memorial performance"]
    },
    "乐队": {
        "unsplash": ["memorial band", "funeral band", "live band ceremony"],
        "pexels": ["live band", "memorial band"],
        "pixabay": ["band", "memorial band"]
    },
    "法事": {
        "unsplash": ["buddhist ceremony", "taoist ceremony", "religious funeral"],
        "pexels": ["buddhist ceremony", "religious ceremony"],
        "pixabay": ["buddhist ceremony", "taoist ceremony"]
    },
    "殡仪馆": {
        "unsplash": ["funeral home", "crematorium", "funeral chapel", "memorial hall"],
        "pexels": ["funeral home", "crematorium"],
        "pixabay": ["funeral home", "crematorium"]
    }
}

class ImageDownloader:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/'
        }
        self.session.headers.update(self.headers)
        self.downloaded = []
        
    def download_image(self, url, filepath):
        """下载单个图片"""
        try:
            time.sleep(random.uniform(0.5, 1.5))
            
            # 清理URL
            url = url.replace('&amp;', '&')
            
            response = self.session.get(url, timeout=30)
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                return True
        except Exception as e:
            print(f"    Error: {e}")
        return False
    
    def unsplash_search(self, query, per_page=20):
        """搜索Unsplash图片"""
        try:
            search_url = f"https://unsplash.com/s/photos/{query.replace(' ', '-')}?orientation=landscape"
            response = self.session.get(search_url, timeout=30)
            
            # 解析图片URL - 从 noscript 标签中提取
            pattern = r'data-photo-id="[^"]*"[^>]*data-src="([^"]+)"'
            matches = re.findall(pattern, response.text)
            
            # 也尝试其他模式
            if not matches:
                pattern2 = r'src="(https://images\.unsplash\.com/photo-[a-zA-Z0-9_-]+[^"]*)"'
                matches = re.findall(pattern2, response.text)
            
            # 去重
            unique_urls = []
            for url in matches:
                if 'images.unsplash.com' in url and url not in unique_urls:
                    unique_urls.append(url)
            
            return unique_urls[:per_page]
        except Exception as e:
            print(f"    Unsplash error: {e}")
            return []
    
    def pexels_search(self, query, per_page=20):
        """搜索Pexels图片"""
        try:
            search_url = f"https://www.pexels.com/search/{query.replace(' ', '%20')}/"
            response = self.session.get(search_url, timeout=30)
            
            pattern = r'photos/(\d+)/[^"\']*\.(?:jpeg|jpg)'
            matches = re.findall(pattern, response.text)
            
            unique_ids = list(set(matches))
            urls = [f"https://images.pexels.com/photos/{pid}/pexels-photo-{pid}.jpeg" for pid in unique_ids]
            return urls[:per_page]
        except Exception as e:
            print(f"    Pexels error: {e}")
            return []
    
    def pixabay_search(self, query, per_page=20):
        """搜索Pixabay图片"""
        try:
            search_url = f"https://pixabay.com/images/search/{query.replace(' ', '%20')}/"
            response = self.session.get(search_url, timeout=30)
            
            pattern = r'cdn\.pixabay\.com/photo/[^"\']+\.(?:jpg|jpeg)'
            matches = re.findall(pattern, response.text)
            
            unique_urls = list(set(["https://" + m for m in matches]))
            return unique_urls[:per_page]
        except Exception as e:
            print(f"    Pixabay error: {e}")
            return []
    
    def download_for_profession(self, profession, max_images=15):
        """为单个职业下载图片"""
        print(f"\n【{profession}】")
        
        prof_dir = BASE_DIR / profession
        prof_dir.mkdir(exist_ok=True)
        
        keywords = PROFESSIONS.get(profession, {})
        downloaded_count = 0
        used_urls = set()
        
        for site, queries in keywords.items():
            if downloaded_count >= max_images:
                break
                
            for query in queries:
                if downloaded_count >= max_images:
                    break
                
                if site == "unsplash":
                    urls = self.unsplash_search(query, per_page=20)
                elif site == "pexels":
                    urls = self.pexels_search(query, per_page=20)
                else:
                    urls = self.pixabay_search(query, per_page=20)
                
                for url in urls:
                    if downloaded_count >= max_images:
                        break
                    if url in used_urls:
                        continue
                    
                    ext = '.jpg' if '.jpg' in url.lower() else '.jpeg' if '.jpeg' in url.lower() else '.png' if '.png' in url.lower() else '.jpg'
                    filename = f"{site}_{profession}_{downloaded_count+1:02d}{ext}"
                    filepath = prof_dir / filename
                    
                    if self.download_image(url, filepath):
                        downloaded_count += 1
                        used_urls.add(url)
                        self.downloaded.append({
                            'profession': profession,
                            'source': site,
                            'filename': filename,
                            'url': url
                        })
        
        print(f"  ✓ 下载完成: {downloaded_count} 张")
        return downloaded_count
    
    def run(self):
        """运行完整下载任务"""
        total = 0
        
        print("=" * 60)
        print("礼纪APP - 殡葬场景图片下载器")
        print("=" * 60)
        print(f"目标目录: {BASE_DIR}")
        print(f"职业数量: {len(PROFESSIONS)}")
        print("=" * 60)
        
        for profession in PROFESSIONS.keys():
            count = self.download_for_profession(profession, max_images=15)
            total += count
            time.sleep(random.uniform(1, 3))
        
        # 保存报告
        report = {
            'total_downloaded': total,
            'download_time': time.strftime('%Y-%m-%d %H:%M:%S'),
            'images': self.downloaded
        }
        
        report_path = BASE_DIR / 'download_report.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print("\n" + "=" * 60)
        print(f"✅ 全部完成! 总计下载: {total} 张图片")
        print(f"📁 保存位置: {BASE_DIR}")
        print(f"📄 下载报告: {report_path}")
        print("=" * 60)
        
        return total


if __name__ == "__main__":
    downloader = ImageDownloader()
    total = downloader.run()
