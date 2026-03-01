#!/usr/bin/env python3
"""
礼纪APP - AI 虚拟头像批量生成脚本 (Silicon Flow 版本)
Silicon Flow 是国内服务，新用户有免费额度
"""

import os
import sys
import time
import requests
from pathlib import Path
from typing import Dict

# 配置
OUTPUT_BASE_DIR = Path.home() / "Desktop/礼纪APP/assets/avatars"
SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY", "")
SILICONFLOW_API_URL = "https://api.siliconflow.cn/v1/images/generations"

# 职业配置
PROFESSIONS: Dict[str, Dict] = {
    "策划师": {
        "male": "专业中国男性策划师，35-45岁，职业形象，沉稳有亲和力的表情，穿着商务休闲装，办公室背景",
        "female": "专业中国女性策划师，35-45岁，职业形象，沉稳有亲和力的表情，穿着优雅商务装，办公室背景",
    },
    "主持人": {
        "male": "中国男性主持人，30-40岁，自信站姿，气质佳，穿着正装西装，舞台背景",
        "female": "中国女性主持人，30-40岁，自信站姿，气质佳，穿着优雅礼服，舞台背景",
    },
    "礼仪师": {
        "male": "中国男性礼仪师，35-50岁，端庄形象，有礼温和的表情，得体举止，穿着传统或正装",
        "female": "中国女性礼仪师，35-50岁，端庄形象，有礼温和的表情，得体举止，穿着优雅传统服装",
    },
    "入殓师": {
        "male": "中国男性入殓师，35-50岁，职业形象，细心庄重的表情，肃穆气质，穿着整洁工作服",
        "female": "中国女性入殓师，35-50岁，职业形象，细心庄重的表情，肃穆气质，穿着整洁工作服",
    },
    "花艺师": {
        "male": "中国男性花艺师，30-45岁，艺术气质，细腻有审美的感觉，被鲜花环绕，穿着休闲艺术装，花店背景",
        "female": "中国女性花艺师，30-45岁，艺术气质，细腻有审美的感觉，被鲜花环绕，穿着优雅艺术装，花店背景",
    },
    "摄像师": {
        "male": "中国男性摄像师，30-45岁，技术感形象，专注的表情，手持摄像设备，穿着实用工作服",
        "female": "中国女性摄像师，30-45岁，技术感形象，专注的表情，手持摄像设备，穿着实用工作服",
    },
    "摄影师": {
        "male": "中国男性摄影师，30-45岁，艺术气质，敏锐的眼神，手持专业相机，穿着休闲艺术装",
        "female": "中国女性摄影师，30-45岁，艺术气质，敏锐的眼神，手持专业相机，穿着休闲艺术装",
    },
    "歌手": {
        "male": "中国男性歌手，25-40岁，有表现力的形象，自信的台风，穿着演出服装，演唱会背景",
        "female": "中国女性歌手，25-40岁，有表现力的形象，自信的台风，穿着优雅演出礼服，演唱会背景",
    },
    "舞蹈": {
        "male": "中国男性舞者，25-40岁，形体好，有表现力的姿态，优雅的动作，穿着舞蹈练习服，舞蹈室背景",
        "female": "中国女性舞者，25-40岁，形体好，有表现力的姿态，优雅的动作，穿着舞蹈练习服，舞蹈室背景",
    },
    "乐队": {
        "male": "中国男性乐队乐手，30-45岁，音乐气质，专业举止，手持乐器，穿着艺术装",
        "female": "中国女性乐队乐手，30-45岁，音乐气质，专业举止，手持乐器，穿着艺术装",
    },
    "法事": {
        "male": "中国男性法事主持，40-55岁，庄重形象，有修为的气质，穿着传统道袍，寺庙背景",
        "female": "中国女性法事主持，40-55岁，庄重形象，有修为的气质，穿着传统道袍，寺庙背景",
    },
    "殡仪馆": {
        "male": "中国男性殡仪馆工作人员，35-50岁，职业形象，稳重可靠的举止，穿着正式深色制服",
        "female": "中国女性殡仪馆工作人员，35-50岁，职业形象，稳重可靠的举止，穿着正式深色制服",
    }
}

# 通用风格后缀
STYLE_SUFFIX = "，写实照片风格肖像，中性素雅色调，简洁纯色或工作环境背景，柔和自然光，高质量，详细面部特征，专业头像，8k"

def generate_avatar(profession: str, gender: str, index: int, api_key: str) -> bool:
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
    print(f"    提示词: {full_prompt[:60]}...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "stabilityai/stable-diffusion-xl-base-1.0",
        "prompt": full_prompt,
        "size": "512x512",
        "seed": hash(f"{profession}_{gender}_{index}") % 1000000
    }
    
    try:
        response = requests.post(
            SILICONFLOW_API_URL,
            headers=headers,
            json=payload,
            timeout=120
        )
        
        if response.status_code != 200:
            print(f"    错误: API 返回 {response.status_code}")
            print(f"    响应: {response.text[:200]}")
            return False
        
        data = response.json()
        
        # 解析响应
        if "data" in data and len(data["data"]) > 0:
            image_url = data["data"][0].get("url", "")
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
    print("礼纪APP - AI 虚拟头像批量生成 (Silicon Flow)")
    print("=" * 60)
    print()
    
    api_key = SILICONFLOW_API_KEY
    
    if not api_key:
        print("⚠️  警告: 未检测到 SILICONFLOW_API_KEY")
        print()
        print("请按以下步骤获取免费 API Key:")
        print("1. 访问 https://siliconflow.cn/")
        print("2. 注册账号（支持手机号或邮箱）")
        print("3. 进入控制台 → API Keys")
        print("4. 创建新的 API Key")
        print("5. 设置环境变量: export SILICONFLOW_API_KEY='your-key'")
        print()
        print("新用户有免费额度")
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
                if api_key:
                    if generate_avatar(profession, gender, i, api_key):
                        success_count += 1
                    # 添加延迟避免 rate limit
                    time.sleep(2)
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
