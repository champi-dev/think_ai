const puppeteer = require('puppeteer');
const fs = require('fs');

const resolutions = [
  { name: 'mobile', width: 320, height: 480 },
  { name: 'tablet', width: 768, height: 1024 },
  { name: 'desktop', width: 1920, height: 1080 },
  { name: '4k', width: 3840, height: 2160 },
];

const url = 'https://thinkai.lat';
const dir = './screenshots';

if (!fs.existsSync(dir)){
    fs.mkdirSync(dir);
}

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();

  for (const resolution of resolutions) {
    console.log(`Capturing screenshot for ${resolution.name} (${resolution.width}x${resolution.height})`);
    await page.setViewport({ width: resolution.width, height: resolution.height });
    await page.goto(url, { waitUntil: 'networkidle2' });
    await page.screenshot({ path: `${dir}/${resolution.name}.png` });
  }

  await browser.close();
  console.log('Screenshots captured successfully!');
})();
