const fs = require('fs');
const path = require('path');

const dir = __dirname;
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));

for (const file of files) {
  const filePath = path.join(dir, file);
  let content = fs.readFileSync(filePath, 'utf8');

  // Remove the static gradient from page-header and make it transparent
  content = content.replace(/linear-gradient\(135deg,\s*#3F0608\s*0%,\s*#5A0C12\s*50%,\s*#2A0406\s*100%\)/g, 'transparent');

  // Remove radial gradients from page-header so it doesn't block
  content = content.replace(/radial-gradient\(circle at top left,\s*rgba\(254,\s*206,\s*8,\s*0\.28\),\s*transparent 32%\),\s*radial-gradient\(circle at 85%\s*15%,\s*rgba\(255,\s*255,\s*255,\s*0\.14\),\s*transparent 18%\),/g, '');

  fs.writeFileSync(filePath, content);
  console.log('Processed', file);
}
