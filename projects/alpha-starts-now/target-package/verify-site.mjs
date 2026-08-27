import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const publishedPages = [
  'index.html',
  'start-here.html',
  'recommended.html',
  'about.html',
  'ritual.html',
  'blog.html',
  'contact.html',
  'privacy.html',
  'terms.html',
  'affiliate-disclosure.html',
  'disclaimer.html',
  '404.html',
  'blog/why-structure-beats-motivation.html',
  'blog/morning-reset-for-real-life.html',
  'blog/protect-one-useful-hour.html',
  'blog/mastering-mental-sovereignty.html',
  'blog/biological-longevity-protocols.html'
];
const requiredFiles = [
  'styles/site.css',
  'scripts/site.js',
  'data/site-data.js',
  'assets/hero-cinematic.jpg',
  'assets/pillar-body.svg',
  'assets/pillar-mind.svg',
  'assets/pillar-discipline.svg',
  'assets/pillar-money.svg',
  'assets/pillar-relationships.svg',
  'assets/favicon.svg',
  'assets/og-image.svg',
  'robots.txt',
  'sitemap.xml',
  'site.webmanifest'
];
const errors = [];
const notices = [];
const exists = (relativePath) => fs.existsSync(path.join(root, relativePath));

for (const file of [...publishedPages, ...requiredFiles]) {
  if (!exists(file)) errors.push(`Missing required file: ${file}`);
}

const read = (relativePath) => fs.readFileSync(path.join(root, relativePath), 'utf8');
const htmlFiles = publishedPages.filter((file) => exists(file));

for (const file of htmlFiles) {
  const source = read(file);
  const title = source.match(/<title>([^<]+)<\/title>/i);
  const description = source.match(/<meta[^>]+name=["']description["'][^>]+content=["']([^"']+)["']/i);
  if (!title?.[1]?.trim()) errors.push(`${file}: missing title`);
  if (!description?.[1]?.trim()) errors.push(`${file}: missing meta description`);
  if (!source.match(/<html[^>]+lang=["']en["']/i)) errors.push(`${file}: missing lang=en`);
  if (!source.includes('skip-link')) errors.push(`${file}: missing skip link`);
  if (!source.match(/<main\b/i)) errors.push(`${file}: missing main landmark`);

  const references = [...source.matchAll(/(?:href|src)=["']([^"']+)["']/gi)].map((match) => match[1]);
  for (const reference of references) {
    if (/^(https?:|mailto:|tel:|data:|javascript:|#)/i.test(reference)) continue;
    const cleanReference = reference.split('#')[0].split('?')[0];
    if (!cleanReference) continue;
    const target = path.normalize(path.join(path.dirname(path.join(root, file)), cleanReference));
    if (!target.startsWith(root) || !fs.existsSync(target)) {
      errors.push(`${file}: broken internal reference ${reference}`);
    }
  }

  if (/<script[^>]+src=["']https?:/i.test(source)) errors.push(`${file}: external script dependency found`);
}

const index = read('index.html');
const css = read('styles/site.css');
const script = read('scripts/site.js');
const data = read('data/site-data.js');
const forbidden = [
  ['index.html', /gsap|ScrollTrigger|lucide|heroCanvas|frame-0001|ACCESSING SYSTEM|loader/i],
  ['published pages', /GETRESPONSE_API_KEY|X-Auth-Token|api\.getresponse\.com|campaignId/i],
  ['site.js', /console\.log\(/i]
];
for (const [label, pattern] of forbidden) {
  const source = label === 'index.html' ? index : label === 'site.js' ? script : htmlFiles.map(read).join('\n');
  if (pattern.test(source)) errors.push(`${label}: forbidden legacy or secret pattern found`);
}
if (!index.includes('id="lead-magnet"')) errors.push('index.html: missing primary lead section');
if (!index.includes('data-form-type="lead"')) errors.push('index.html: missing lead form');
if (!index.includes('id="system"') || !index.includes('id="pillars"') || !index.includes('id="about"')) errors.push('index.html: missing core information architecture anchors');
if (!index.includes('blog/why-structure-beats-motivation.html') || !read('blog.html').includes('blog/why-structure-beats-motivation.html')) errors.push('article index: missing static article fallback');
if (!css.includes('@media (prefers-reduced-motion: reduce)')) errors.push('site.css: missing reduced-motion rule');
if (!script.includes('prefers-reduced-motion')) errors.push('site.js: missing reduced-motion behavior');
if (!data.includes('leadEndpoint')) errors.push('site-data.js: missing lead endpoint configuration');

const heroSize = exists('assets/hero-cinematic.jpg') ? fs.statSync(path.join(root, 'assets/hero-cinematic.jpg')).size : 0;
if (heroSize > 500 * 1024) notices.push(`Hero still is ${Math.round(heroSize / 1024)} KB, above the preferred 500 KB mobile budget.`);
if (heroSize > 1024 * 1024) errors.push('Hero still exceeds the 1 MB hard review threshold.');

if (errors.length) {
  console.error('SITE_VERIFY_FAIL');
  errors.forEach((error) => console.error(`- ${error}`));
  process.exitCode = 1;
} else {
  console.log(`SITE_VERIFY_PASS pages=${htmlFiles.length} required_files=${requiredFiles.length} hero_bytes=${heroSize}`);
  notices.forEach((notice) => console.log(`NOTICE: ${notice}`));
}
