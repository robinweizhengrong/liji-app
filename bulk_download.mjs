import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import os from 'os';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const BASE_DIR = path.join(os.homedir(), 'Desktop/礼纪APP/assets/scenes_real');

const PROFESSIONS = {
  "策划师": ["funeral ceremony", "memorial service setup", "funeral planning"],
  "主持人": ["memorial service speaker", "funeral ceremony host", "memorial ceremony"],
  "礼仪师": ["funeral service usher", "ceremony service", "memorial service staff"],
  "入殓师": ["mortician", "funeral director", "embalming preparation"],
  "花艺师": ["funeral flowers", "white flowers memorial", "funeral wreath"],
  "摄像师": ["event videographer", "funeral video recording", "ceremony videographer"],
  "摄影师": ["event photographer", "memorial photography", "ceremony photographer"],
  "歌手": ["memorial singer", "funeral singer performance", "memorial music"],
  "舞蹈": ["memorial dance", "ceremonial dance performance", "memorial performance"],
  "乐队": ["memorial band", "funeral band performance", "live band ceremony"],
  "法事": ["buddhist funeral ceremony", "taoist ceremony", "religious funeral ritual"],
  "殡仪馆": ["funeral home", "crematorium", "funeral chapel", "memorial hall"]
};

async function downloadImages(page, profession, keywords, source, maxCount = 5) {
  const downloads = [];
  const profDir = path.join(BASE_DIR, profession);
  fs.mkdirSync(profDir, { recursive: true });
  
  let baseUrl = '';
  let selector = '';
  
  if (source === 'unsplash') {
    baseUrl = 'https://unsplash.com/s/photos/';
    selector = 'img[src*="images.unsplash.com/photo-"]';
  } else if (source === 'pexels') {
    baseUrl = 'https://www.pexels.com/search/';
    selector = 'img[src*="images.pexels.com"]';
  } else if (source === 'pixabay') {
    baseUrl = 'https://pixabay.com/images/search/';
    selector = 'img[src*="cdn.pixabay.com"]';
  }
  
  for (const keyword of keywords) {
    if (downloads.length >= maxCount) break;
    
    try {
      console.log(`  [${source}] 搜索: ${keyword}`);
      const url = `${baseUrl}${encodeURIComponent(keyword)}${source === 'unsplash' ? '?orientation=landscape' : ''}`;
      
      await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
      await page.waitForTimeout(2000);
      
      const images = await page.evaluate(({ sel, srcName }) => {
        const imgs = document.querySelectorAll(sel);
        return Array.from(imgs)
          .map(img => ({ url: img.src, alt: img.alt || '' }))
          .filter(img => {
            if (srcName === 'unsplash') return img.url.includes('photo-');
            if (srcName === 'pexels') return img.url.includes('/photos/');
            if (srcName === 'pixabay') return img.url.includes('/photo/');
            return true;
          });
      }, { sel: selector, srcName: source });
      
      console.log(`    找到 ${images.length} 张图片`);
      
      for (let i = 0; i < images.length && downloads.length < maxCount; i++) {
        const img = images[i];
        const ext = img.url.includes('.png') ? '.png' : '.jpg';
        const filename = `${source}_${profession}_${String(downloads.length + 1).padStart(2, '0')}${ext}`;
        const filepath = path.join(profDir, filename);
        
        try {
          const response = await page.evaluate(async (url) => {
            const res = await fetch(url);
            const blob = await res.blob();
            const reader = new FileReader();
            return new Promise((resolve) => {
              reader.onloadend = () => resolve(reader.result);
              reader.readAsDataURL(blob);
            });
          }, img.url);
          
          const base64 = response.split(',')[1];
          fs.writeFileSync(filepath, Buffer.from(base64, 'base64'));
          downloads.push({ source, filename });
          console.log(`    ✓ ${filename}`);
          
          await page.waitForTimeout(500);
        } catch (e) {
          console.log(`    ✗ 失败`);
        }
      }
    } catch (e) {
      console.log(`  错误: ${e.message}`);
    }
  }
  
  return downloads;
}

async function main() {
  console.log('='.repeat(60));
  console.log('礼纪APP - 殡葬场景图片批量下载器');
  console.log('='.repeat(60));
  
  const browser = await chromium.launch({ 
    headless: true,
    args: ['--disable-blink-features=AutomationControlled']
  });
  
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
  });
  
  const page = await context.newPage();
  const allDownloads = [];
  
  for (const [profession, keywords] of Object.entries(PROFESSIONS)) {
    console.log(`\n【${profession}】`);
    let profDownloads = [];
    
    // 每个网站尝试下载5张，总计15张
    const unsplash = await downloadImages(page, profession, keywords, 'unsplash', 5);
    profDownloads.push(...unsplash);
    
    if (profDownloads.length < 15) {
      const pexels = await downloadImages(page, profession, keywords, 'pexels', 5);
      profDownloads.push(...pexels);
    }
    
    if (profDownloads.length < 15) {
      const pixabay = await downloadImages(page, profession, keywords, 'pixabay', 5);
      profDownloads.push(...pixabay);
    }
    
    allDownloads.push({ profession, count: profDownloads.length, images: profDownloads });
    console.log(`  小计: ${profDownloads.length} 张`);
    
    await page.waitForTimeout(2000);
  }
  
  await browser.close();
  
  const report = {
    total: allDownloads.reduce((sum, p) => sum + p.count, 0),
    timestamp: new Date().toISOString(),
    details: allDownloads
  };
  
  fs.writeFileSync(
    path.join(BASE_DIR, 'download_report.json'),
    JSON.stringify(report, null, 2)
  );
  
  console.log('\n' + '='.repeat(60));
  console.log(`✅ 下载完成! 总计: ${report.total} 张图片`);
  console.log(`📁 保存位置: ${BASE_DIR}`);
  console.log('='.repeat(60));
}

main().catch(console.error);
