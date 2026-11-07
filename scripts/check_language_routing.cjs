// Static guard: the published pages must not force a language redirect.
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const site = fs.readFileSync(path.join(root, 'assets', 'site.js'), 'utf8');
const index = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
if (site.includes('location.replace') || index.includes('location.replace') || index.includes('data-auto-language')) {
  throw new Error('forced language redirect is still in the published site');
}
console.log('PASS: published pages do not force a language redirect. Run python scripts/check_language_routing.py for the suggestion rules.');
