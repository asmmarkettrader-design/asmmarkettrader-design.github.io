const fs = require('fs');

function convertToLightMode(filePath) {
  let content = fs.readFileSync(filePath, 'utf8');

  // Text colors
  content = content.replace(/text-white/g, 'text-slate-900');
  content = content.replace(/text-slate-100/g, 'text-slate-900');
  content = content.replace(/text-slate-200/g, 'text-slate-800');
  content = content.replace(/text-slate-300/g, 'text-slate-600');
  content = content.replace(/text-slate-400/g, 'text-slate-500');
  
  // Background colors
  content = content.replace(/bg-slate-950/g, 'bg-slate-50');
  content = content.replace(/bg-slate-900\/([0-9]+)/g, 'bg-white/$1');
  content = content.replace(/bg-slate-900/g, 'bg-white');
  content = content.replace(/bg-[#020408]\/50/g, 'bg-white/50');
  content = content.replace(/bg-slate-800/g, 'bg-slate-100');
  content = content.replace(/bg-black\/([0-9]+)/g, 'bg-slate-100/$1');
  content = content.replace(/bg-black/g, 'bg-slate-900');
  
  // Border colors
  content = content.replace(/border-white\/\[[a-zA-Z0-9.]+\]/g, 'border-slate-200');
  content = content.replace(/border-white\/([0-9]+)/g, 'border-slate-200');

  // Specific overrides
  content = content.replace(/text-slate-900\/50/g, 'text-slate-400');
  
  fs.writeFileSync(filePath, content);
}

convertToLightMode('src/App.tsx');
convertToLightMode('src/components/SeoAnalyzer.tsx');
convertToLightMode('src/utils/staticGenerator.ts');

console.log("Converted to light mode.");
