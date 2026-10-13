// Берёт собранный интерфейс из ../znamenskoye/dist/index.html и кладёт в www/ как обычную страницу.
const fs = require('fs'), path = require('path');
const src = fs.readFileSync(path.join(__dirname, '..', 'znamenskoye', 'dist', 'index.html'), 'utf8');
const page = '<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="color-scheme" content="light dark"><style>html,body{margin:0;padding:0}</style></head><body>' + src + '</body></html>';
fs.mkdirSync(path.join(__dirname, 'www'), { recursive: true });
fs.writeFileSync(path.join(__dirname, 'www', 'index.html'), page);
console.log('www/index.html', Math.round(page.length / 1024) + ' KB');
