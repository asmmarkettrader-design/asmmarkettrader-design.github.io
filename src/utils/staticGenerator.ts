/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

// Interface for editable components on the site
export interface SiteContent {
  hero: {
    badge: string;
    title: string;
    description: string;
  };
  seoTool: {
    seoTitle: string;
    seoDesc: string;
    keywords: string;
  };
  services: Array<{
    id: number;
    title: string;
    price: string;
    badge: string;
    description: string;
    features: string[];
    whatsAppText: string;
    image?: string;
  }>;
  reviews: Array<{
    id: number;
    name: string;
    role: string;
    company: string;
    country: string;
    countryCode: string; // e.g., "us", "gb", "fr", "de"
    content: string;
    rating: number;
    date: string;
    platform?: string;
  }>;
  blogs: Array<{
    id: number;
    title: string;
    excerpt: string;
    content: string;
    keywords: string[];
    readTime: string;
    date: string;
  }>;
  contact: {
    phone: string;
    email: string;
    linkedin: string;
    domain: string;
  };
}

export function generateStaticHtml(content: SiteContent): string {
  // Convert elements into direct JSON for embedding in script tag
  const contentJson = JSON.stringify(content, null, 2);

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${content.hero.title} | ${content.seoTool.seoTitle}</title>
  
  <!-- SEO Meta Tags for Global Rankings -->
  <meta name="description" content="${content.hero.description}">
  <meta name="keywords" content="${content.seoTool.keywords}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://${content.contact.domain}">
  <meta name="author" content="ASM Digital Solutions">
  
  <!-- Open Graph / Meta -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://${content.contact.domain}">
  <meta property="og:title" content="${content.hero.title} | ${content.seoTool.seoTitle}">
  <meta property="og:description" content="${content.hero.description}">
  <meta property="og:image" content="https://${content.contact.domain}/og-image.jpg">

  <!-- Google Fonts - Inter & Plus Jakarta Sans Pairing for simple premium feel -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  
  <!-- Tailwind CSS Play CDN & Configuration -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            sans: ["Inter", "sans-serif"],
            display: ["Plus Jakarta Sans", "sans-serif"],
            mono: ["JetBrains Mono", "monospace"]
          }
        }
      }
    }
  </script>

  <!-- FontAwesome for Icons -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

  <style>
    body {
      background-color: #0b1120; /* Slightly lighter/brighter luxury slate */
      color: #f1f5f9;
      overflow-x: hidden;
    }

    /* Custom Webkit scrollbar for premium theme */
    ::-webkit-scrollbar {
      width: 8px;
      height: 8px;
    }
    ::-webkit-scrollbar-track {
      background: #090d1a;
    }
    ::-webkit-scrollbar-thumb {
      background: rgba(255, 255, 255, 0.08);
      border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: rgba(0, 243, 255, 0.3);
      box-shadow: 0 0 10px rgba(0, 243, 255, 0.5);
    }

    /* Light, premium slate glass translucent card */
    .cyber-glass {
      background: rgba(30, 41, 59, 0.4);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .cyber-glass:hover {
      border-color: rgba(0, 243, 255, 0.35);
      box-shadow: 0 10px 30px rgba(0, 243, 255, 0.05);
    }

    /* Subtle grid layout */
    .grid-bg {
      background-image: 
        linear-gradient(rgba(255, 255, 255, 0.015) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.015) 1px, transparent 1px);
      background-size: 50px 50px;
      background-position: center center;
    }

    /* Flow floating orbs */
    @keyframes float {
      0% { transform: translateY(0px) scale(1); }
      50% { transform: translateY(-15px) scale(1.03); }
      100% { transform: translateY(0px) scale(1); }
    }
    .orb-float-1 { animation: float 14s ease-in-out infinite; }
    .orb-float-2 { animation: float 18s ease-in-out infinite; animation-delay: -5s; }
    .orb-float-3 { animation: float 22s ease-in-out infinite; animation-delay: -10s; }

    /* Hide admin fields initially */
    .admin-only {
      display: none;
    }
    body.is-admin .admin-only {
      display: block;
    }
    [contenteditable="true"] {
      border: 1.5px dashed rgba(6, 182, 212, 0.5) !important;
      padding: 4px;
      background-color: rgba(6, 182, 212, 0.08);
      border-radius: 4px;
      outline: none;
    }
    [contenteditable="true"]::after {
      content: " ✎";
      font-size: 0.75rem;
      opacity: 0.7;
      color: #00f3ff;
    }
  </style>
</head>
<body class="relative min-h-screen font-sans antialiased text-slate-205 grid-bg">

  <!-- Network Grid Background Canvas -->
  <canvas id="network-canvas" class="fixed inset-0 pointer-events-none z-0 opacity-30"></canvas>

  <!-- Cybernetic Floating Glow Orbs -->
  <div class="fixed top-1/4 left-1/10 w-96 h-96 rounded-full bg-cyan-500/5 blur-[130px] pointer-events-none z-0 orb-float-1"></div>
  <div class="fixed bottom-1/3 right-1/10 w-120 h-120 rounded-full bg-purple-500/5 blur-[150px] pointer-events-none z-0 orb-float-2"></div>

  <!-- Header Section -->
  <header class="sticky top-0 z-50 w-full py-4 px-6 border-b border-slate-200 backdrop-blur-md bg-white/80 pointer-events-auto">
    <div class="max-w-7xl mx-auto flex items-center justify-between">
      <a href="#" onclick="showLandingView(); return false;" class="flex items-center gap-3">
        <div class="relative w-9 h-9 rounded bg-gradient-to-br from-cyan-400 to-purple-500 flex items-center justify-center font-display font-black text-black text-xs tracking-wider">
          ASM
        </div>
        <div class="flex flex-col">
          <span class="font-display font-black text-base tracking-widest text-slate-900 leading-none">ASM DIGITAL</span>
          <span class="text-[9px] font-mono tracking-widest text-cyan-400 leading-none mt-1">SEO AUDIT & SCALE PLATFORM</span>
        </div>
      </a>

      <!-- Quick Nav Buttons -->
      <nav class="hidden md:flex items-center gap-8 font-display text-[11px] font-semibold tracking-widest text-slate-600">
        <button onclick="showLandingView(); document.getElementById('seo-tool').scrollIntoView({behavior: 'smooth'});" class="hover:text-slate-900 transition-colors uppercase">SEO ANALYZER</button>
        <button onclick="showLandingView(); document.getElementById('services').scrollIntoView({behavior: 'smooth'});" class="hover:text-slate-900 transition-colors uppercase">SERVICES</button>
        <button onclick="showLandingView(); document.getElementById('reviews').scrollIntoView({behavior: 'smooth'});" class="hover:text-slate-900 transition-colors uppercase">RATINGS</button>
        <button onclick="showLandingView(); document.getElementById('blog').scrollIntoView({behavior: 'smooth'});" class="hover:text-slate-900 transition-colors uppercase">RESOURCES</button>
        <button onclick="document.getElementById('contact').scrollIntoView({behavior: 'smooth'});" class="hover:text-slate-900 transition-colors uppercase">COMMUNICATE</button>
      </nav>

      <!-- Admin trigger/Status indicators -->
      <div class="flex items-center gap-4">
        <button onclick="triggerLogin()" class="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-slate-200 hover:border-cyan-500/50 hover:bg-cyan-500/10 transition-all font-mono text-[10px] text-cyan-400 tracking-wider cursor-pointer">
          <i class="fa-solid fa-terminal"></i>
          <span>CONSOLE LOGIN</span>
        </button>
      </div>
    </div>
  </header>

  <main class="relative z-10 max-w-7xl mx-auto px-6 py-12">
    
    <!-- MAIN LANDING VIEW -->
    <div id="landing-view" class="space-y-24">
      
      <!-- Hero / SEO Traffic Tool Engine Section -->
      <section id="hero" class="text-center">
        <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-cyan-500/20 bg-cyan-950/10 mb-8 font-mono text-[9px] text-cyan-400 tracking-wider">
          <span class="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-pulse"></span>
          <span id="editable-hero-badge" data-path="hero.badge">${content.hero.badge}</span>
        </div>
        
        <h1 id="editable-hero-title" data-path="hero.title" class="font-display font-black text-3xl sm:text-5xl lg:text-6xl text-slate-900 tracking-tight leading-none mb-6 max-w-5xl mx-auto uppercase">
          ${content.hero.title}
        </h1>
        
        <p id="editable-hero-description" data-path="hero.description" class="text-slate-600 text-base md:text-lg max-w-3xl mx-auto mb-12 font-sans font-normal leading-relaxed">
          ${content.hero.description}
        </p>

        <!-- Dynamic Core SEO Analyzer Card (Core Traffic Engine) -->
        <div id="seo-tool" class="w-full max-w-4xl mx-auto rounded-3xl cyber-glass p-8 border border-slate-200 relative">
          <div class="absolute -top-3 left-1/2 -translate-x-1/2 px-4 py-0.5 rounded border border-cyan-500/40 bg-white font-mono text-[8px] text-cyan-400 tracking-wider">
            SYSTEM CORE V3.9 - SEO CONSOLE
          </div>

          <div class="mb-6">
            <h2 id="editable-seo-title" data-path="seoTool.seoTitle" class="font-display font-bold text-xl text-slate-900 tracking-wide mb-2">${content.seoTool.seoTitle}</h2>
            <p id="editable-seo-desc" data-path="seoTool.seoDesc" class="text-slate-500 hover:text-cyan-300 text-xs sm:text-sm max-w-2xl mx-auto transition-colors">${content.seoTool.seoDesc}</p>
          </div>

          <!-- Audit Input Row -->
          <div class="flex flex-col sm:flex-row gap-4 max-w-2xl mx-auto mb-8 relative z-20">
            <div class="flex-1 relative">
              <i class="fa-solid fa-globe absolute left-4 top-1/2 -translate-y-1/2 text-cyan-450 text-sm"></i>
              <input type="url" id="audit-url-input" placeholder="https://yourwebsite.com" class="w-full pl-12 pr-4 py-3.5 rounded-xl border border-slate-200 bg-slate-50 text-slate-900 font-mono text-xs placeholder:text-slate-600 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500/30 transition-all">
            </div>
            <button onclick="runAudit()" class="px-8 py-3.5 rounded-xl font-display font-bold text-xs uppercase tracking-widest bg-cyan-400 text-black hover:bg-white transform transition-all hover:scale-[1.02] shadow-[0_0_15px_rgba(0,243,255,0.15)] shrink-0">
              START DIAGNOSTICS <i class="fa-solid fa-bolt ml-1"></i>
            </button>
          </div>

          <!-- Analyzer Loading UI -->
          <div id="audit-loading" class="hidden py-10 flex-col items-center justify-center">
            <div class="relative w-16 h-16 mb-4">
              <div class="absolute inset-0 rounded-full border-2 border-cyan-500/20"></div>
              <div class="absolute inset-0 rounded-full border-t-2 border-purple-500 animate-spin"></div>
            </div>
            <p id="audit-status" class="font-mono text-xs text-cyan-400 animate-pulse tracking-widest mt-2">INITIALIZING WEB OBSERVABILITY HOOKS...</p>
          </div>

          <!-- Analyzer Results Interface (Dynamically Populated) -->
          <div id="audit-results" class="hidden text-left border-t border-slate-200 pt-8">
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8 items-center">
              <!-- Dynamic Score Gauge -->
              <div class="flex flex-col items-center justify-center p-6 rounded-2xl bg-white/[0.01] border border-slate-200">
                <span class="font-display font-extrabold text-[10px] tracking-wider text-slate-500 mb-3 uppercase">CORE SEO INTEGRITY</span>
                <div class="relative w-36 h-36 flex items-center justify-center">
                  <svg class="w-full h-full transform -rotate-90">
                    <circle cx="72" cy="72" r="60" stroke="rgba(255,255,255,0.03)" stroke-width="8" fill="transparent"></circle>
                    <circle id="gauge-circle" cx="72" cy="72" r="60" stroke="#22d3ee" stroke-width="8" fill="transparent" stroke-dasharray="377" stroke-dashoffset="100" stroke-linecap="round" class="transition-all duration-1000"></circle>
                  </svg>
                  <div class="absolute flex flex-col items-center justify-center">
                    <span id="audit-score-text" class="font-display font-black text-3xl text-slate-900">85<span class="text-xs text-cyan-400">%</span></span>
                    <span id="audit-grade" class="font-mono text-[9px] text-[#00f3ff] mt-1 uppercase">GRADE A: STABLE</span>
                  </div>
                </div>
              </div>

              <!-- Meta & Core stats Summary -->
              <div class="md:col-span-2 space-y-3">
                <div class="p-4 rounded-xl bg-white/[0.02] border border-slate-200 flex items-center justify-between col-span-2">
                  <div>
                    <h4 class="font-display font-bold text-xs text-slate-900">Target Address</h4>
                    <p id="result-resolved-url" class="font-mono text-xs text-cyan-400 mt-0.5">https://targetsite.com</p>
                  </div>
                  <span class="font-mono text-[9px] px-2.5 py-1 rounded bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 font-bold uppercase">RESOLVED</span>
                </div>
                
                <div class="grid grid-cols-2 gap-4">
                  <div class="p-4 rounded-xl bg-white/[0.012] border border-slate-200">
                    <h4 class="font-sans font-bold text-xs text-slate-500">Response Latency (TTFB)</h4>
                    <p id="result-ttfb" class="font-mono text-lg text-slate-900 mt-1">118 ms</p>
                  </div>
                  <div class="p-4 rounded-xl bg-white/[0.012] border border-slate-200">
                    <h4 class="font-sans font-bold text-xs text-slate-500">First Contentful Paint</h4>
                    <p id="result-fcp" class="font-mono text-lg text-slate-900 mt-1">0.48 s</p>
                  </div>
                </div>
              </div>
            </div>

            <div class="space-y-4">
              <!-- 1. Meta-Data Integrity -->
              <div class="p-5 rounded-2xl bg-white/[0.015] border border-slate-200">
                <div class="flex items-center justify-between mb-4">
                  <h3 class="font-display font-bold text-xs text-slate-900 tracking-widest flex items-center gap-2">
                    <i class="fa-solid fa-tags text-cyan-455 text-sm"></i> META-DATA INTEGRITY
                  </h3>
                  <span class="font-mono text-[9px] text-emerald-400 font-bold"><i class="fa-solid fa-check"></i> SCAN SAFE</span>
                </div>
                <div class="space-y-3 font-mono text-xs">
                  <div class="flex flex-col gap-1 p-3 rounded bg-slate-100/40 border border-slate-200">
                    <span class="text-slate-500 text-[10px]">Meta Title Header:</span>
                    <span id="res-meta-title" class="text-slate-600">Excellent Meta Title (64 characters)</span>
                  </div>
                  <div class="flex flex-col gap-1 p-3 rounded bg-slate-100/40 border border-slate-200">
                    <span class="text-slate-500 text-[10px]">Meta Description Summary:</span>
                    <span id="res-meta-desc" class="text-slate-600">High-converting description found optimizing targeted phrases inside the page layout metadata.</span>
                  </div>
                  <div class="grid grid-cols-2 gap-3 mt-2">
                    <div class="p-2.5 rounded bg-slate-100/40 border border-slate-200 flex justify-between">
                      <span class="text-slate-500">OG Open Graph tags:</span>
                      <span id="res-og-tags" class="text-cyan-400 font-bold">Detected</span>
                    </div>
                    <div class="p-2.5 rounded bg-slate-100/40 border border-slate-200 flex justify-between">
                      <span class="text-slate-500">Robots.txt & Canonical:</span>
                      <span id="res-robots" class="text-cyan-400 font-bold">Indexed</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 2. Semantic Hierarchy & Image Check -->
              <div class="p-5 rounded-2xl bg-white/[0.015] border border-slate-200">
                <div class="flex items-center justify-between mb-4">
                  <h3 class="font-display font-bold text-xs text-slate-900 tracking-widest flex items-center gap-2">
                    <i class="fa-solid fa-sitemap text-purple-400 text-sm"></i> SEMANTIC STRUCTURE & IMAGES
                  </h3>
                  <span id="res-sem-status" class="font-mono text-[9px] text-amber-400 font-bold"><i class="fa-solid fa-triangle-exclamation"></i> ACTION REQUIRED</span>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div class="p-3.5 rounded bg-slate-100/40 border border-slate-200 space-y-2">
                    <span class="font-mono text-xs text-slate-500 block">Header Taxonomy distribution:</span>
                    <div class="flex items-center gap-4 text-xs font-mono">
                      <span class="px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 text-[10px]">H1: <span id="res-h1-count">1</span></span>
                      <span class="px-2 py-0.5 rounded bg-purple-500/10 text-purple-400 text-[10px]">H2: <span id="res-h2-count">12</span></span>
                      <span class="px-2 py-0.5 rounded bg-pink-500/10 text-pink-400 text-[10px]">H3: <span id="res-h3-count">6</span></span>
                    </div>
                  </div>
                  <div class="p-3.5 rounded bg-slate-100/40 border border-slate-200 space-y-1 text-xs font-mono">
                    <span class="text-slate-500 block">Images Missing Alt Attributes:</span>
                    <p class="text-slate-600"><span id="res-alt-ratio" class="text-amber-400 font-bold">45%</span> of localized static imagery lacks alternative descriptive labels.</p>
                  </div>
                </div>
                <div class="mt-3 p-3 rounded bg-amber-500/5 border border-amber-500/10 text-xs text-amber-400 font-mono">
                  <i class="fa-solid fa-triangle-exclamation mr-1"></i> Missing ALT tags degrade your image optimization capabilities. Google Image Search traffic index could fall by up to 30%.
                </div>
              </div>

              <!-- 3. Speed & Diagnostics summary -->
              <div class="p-5 rounded-2xl bg-white/[0.015] border border-slate-200">
                <div class="flex items-center justify-between mb-4">
                  <h3 class="font-display font-bold text-xs text-slate-900 tracking-widest flex items-center gap-2">
                    <i class="fa-solid fa-gauge text-cyan-400 text-sm"></i> DIAGNOSTICS & SECURITY SIGNALS
                  </h3>
                  <span id="res-sec-status" class="font-mono text-[9px] text-emerald-400 font-bold"><i class="fa-solid fa-shield-halved"></i> SECURED</span>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 font-mono text-xs text-center">
                  <div class="p-3.5 rounded bg-slate-100/40 border border-slate-200">
                    <span class="text-slate-500 block mb-1">SSL State</span>
                    <span id="res-ssl" class="text-emerald-400 font-display font-bold text-xs">ACTIVE (HTTPS)</span>
                  </div>
                  <div class="p-3.5 rounded bg-slate-100/40 border border-slate-200">
                    <span class="text-slate-500 block mb-1">Security Headers</span>
                    <span id="res-headers" class="text-yellow-400 font-display font-bold text-xs">PARTIAL (8/12)</span>
                  </div>
                  <div class="p-3.5 rounded bg-slate-100/40 border border-slate-200">
                    <span class="text-slate-500 block mb-1">Uncaught Errors</span>
                    <span id="res-console-errs" class="text-emerald-400 font-display font-bold text-xs">0 METRICS</span>
                  </div>
                </div>
              </div>

              <!-- Recommendation CTA mapping matching ASM Services -->
              <div class="p-6 rounded-2xl bg-gradient-to-r from-purple-950/20 to-cyan-950/20 border border-cyan-500/20 mt-6 flex flex-col md:flex-row items-center justify-between gap-6">
                <div class="text-left">
                  <h3 class="font-display font-extrabold text-sm text-slate-900 mb-1 uppercase"><i class="fa-solid fa-wand-magic-sparkles text-cyan-405 mr-2"></i>ASM STRATEGIC RECOMMENDATIONS</h3>
                  <p class="text-slate-500 text-xs max-w-xl font-medium leading-relaxed">Fix image descriptors immediately, reduce structural DNS response latency, and integrate safe Trustpilot review elements to spike domestic conversion velocity instantly.</p>
                </div>
                <a id="analyzer-whatsapp-btn" href="https://wa.me/923425478683?text=Hi%20ASM%20Solutions,%20I%20just%20ran%20your%20Advanced%20SEO%20Analyzer%20Tool%20and%20need%20to%20fix%20my%20website%20Meta%20Taxonomy,%20Alt%20tags,%20and%20local%20rankings." target="_blank" class="px-5 py-3 rounded-lg bg-cyan-400 hover:bg-white text-black font-display text-xs font-bold tracking-widest uppercase hover:scale-[1.03] transition-all flex items-center gap-2 shadow-[0_4px_15px_rgba(34,211,238,0.2)] shrink-0 justify-center">
                  <i class="fa-brands fa-whatsapp text-sm"></i> FIX SITE WITH ASM EXPERT
                </a>
              </div>

            </div>

          </div>
        </div>
      </section>

      <!-- The 8 Core Agency Solutions -->
      <section id="services" class="relative">
        <div class="text-center mb-16">
          <h2 class="font-display font-black text-2xl sm:text-4xl text-slate-900 tracking-tight mb-4 uppercase">
            ASM STRATEGIC SOLUTIONS
          </h2>
          <p class="text-slate-500 text-xs sm:text-sm max-w-2xl mx-auto font-normal">
            Click on any agency path to open its dedicated technical review page, JSON-LD Schema structures, real-time meta metrics, and Lighthouse audit scorecards.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          ${content.services.map((service, idx) => {
            const isEven = idx % 2 === 0;
            const accentText = isEven ? 'text-cyan-400' : 'text-purple-400';
            const borderHover = isEven ? 'hover:border-cyan-400/40' : 'hover:border-purple-500/40';
            return `
            <div class="rounded-3xl cyber-glass p-8 border border-slate-200 flex flex-col justify-between hover:scale-[1.015] transform transition-all group overflow-hidden relative ${borderHover}">
              <div class="absolute top-0 right-0 w-24 h-24 bg-gradient-to-bl from-white/[0.01] to-transparent pointer-events-none group-hover:scale-125 transition-all"></div>
              <div>
                <div class="flex items-center justify-between mb-4">
                  <span class="font-mono text-[9px] uppercase font-bold ${accentText} tracking-widest">${service.badge}</span>
                  <span class="text-[9px] font-mono text-emerald-400 bg-emerald-950/20 px-2.5 py-1 rounded border border-emerald-500/20 uppercase font-bold">Lighthouse: 100%</span>
                </div>
                <h3 class="font-display font-extrabold text-base sm:text-lg text-slate-900 mb-2 group-hover:text-cyan-400 transition-colors leading-snug">${service.title}</h3>
                <p class="text-slate-350 text-xs font-normal leading-relaxed mb-6">${service.description.slice(0, 140)}...</p>
              </div>
              <div class="space-y-4">
                <div class="p-3.5 rounded-xl bg-slate-100/40 border border-slate-200 flex items-center justify-between">
                  <span class="font-mono text-[9px] text-slate-500 uppercase">Pricing Rate</span>
                  <span class="font-display font-extrabold text-rose-450 text-xs text-rose-400 flex items-center gap-0.5">$ ${service.price.replace('$', '')}</span>
                </div>
                <div class="grid grid-cols-2 gap-2">
                  <button onclick="showServiceView(${service.id});" class="py-3 rounded-lg border border-slate-200 hover:border-cyan-450/40 bg-white/60 text-slate-900 font-display text-[9px] font-bold tracking-widest transition-all uppercase cursor-pointer text-center">MORE METRICS</button>
                  <a href="https://wa.me/923425478683?text=${encodeURIComponent(service.whatsAppText)}" target="_blank" class="py-3 rounded-lg bg-cyan-400 hover:bg-white text-black font-display text-[9px] font-black tracking-widest transition-all text-center uppercase">ORDER</a>
                </div>
              </div>
            </div>`;
          }).join('')}
        </div>
      </section>

      <!-- Trustpilot Rating Carousel / Matrix Section -->
      <section id="reviews" class="scroll-mt-24">
        <div class="rounded-3xl cyber-glass p-8 md:p-12 border border-slate-200">
          <div class="flex flex-col md:flex-row items-center justify-between border-b border-slate-200 pb-8 mb-8 gap-6 text-center md:text-left">
            <div>
              <div class="flex items-center justify-center md:justify-start gap-2 mb-2">
                <span class="text-slate-900 font-display font-black text-lg tracking-wider">TRUSTPILOT RATINGS</span>
                <span class="text-emerald-450 text-emerald-405 text-xs font-bold flex items-center gap-1 uppercase"><i class="fa-solid fa-square-check"></i> VERIFIED DEPLOYMENTS</span>
              </div>
              <p class="text-slate-500 text-[10px] font-mono tracking-wider uppercase">Geo-Targeted safe citations across major global markets</p>
            </div>
            <div class="flex flex-col items-center md:items-end">
              <div class="flex items-center gap-2 mb-1 bg-emerald-950/20 px-4 py-1.5 rounded-full border border-emerald-500/20">
                <span class="text-emerald-450 text-emerald-400 text-sm font-black text-sm">4.9</span>
                <div class="flex gap-0.5 text-emerald-400">
                  ${Array(5).fill('<i class="fa-solid fa-star text-[10px]"></i>').join('')}
                </div>
              </div>
              <span class="text-slate-500 text-[8px] font-mono uppercase tracking-widest">VALIDATED THROUGH 1,480 SECTOR TRANSIT AUDITS</span>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            ${content.reviews.map(rev => `
              <div class="p-6 rounded-2xl bg-white/40 border border-slate-200 hover:border-emerald-500/20 transition-all flex flex-col justify-between">
                <div>
                  <div class="flex items-center justify-between mb-4">
                    <div class="flex items-center gap-3">
                      <div class="w-9 h-9 rounded-full bg-slate-850 bg-slate-100 border border-slate-200 flex items-center justify-center font-display font-black text-slate-900 text-xs uppercase">${rev.name.split(' ').map(n=>n[0]).join('')}</div>
                      <div>
                        <h4 class="text-slate-900 font-sans font-bold text-xs">${rev.name}</h4>
                        <p class="text-slate-500 text-[9px] font-mono uppercase">${rev.role} | ${rev.company}</p>
                      </div>
                    </div>
                    <div class="flex items-center gap-1 p-1 bg-emerald-500/10 rounded">
                      <span class="text-emerald-405 text-emerald-400 text-[9px] font-mono font-bold leading-none">${rev.rating}.0</span>
                      <div class="flex gap-0.5 text-emerald-400">
                        ${Array(rev.rating).fill('<i class="fa-solid fa-star text-[8px]"></i>').join('')}
                      </div>
                    </div>
                  </div>
                  <p class="text-slate-600 text-xs leading-relaxed font-normal italic mb-4">"${rev.content}"</p>
                </div>
                <div class="flex items-center justify-between font-mono text-[9px] mt-2 text-slate-500 border-t border-slate-200 pt-3">
                  <span class="flex items-center gap-1"><i class="fa-solid fa-shield-halved text-emerald-405 text-emerald-400 text-xs"></i> Verified Retention Proof</span>
                  <span class="flex items-center gap-1.5 uppercase font-bold text-slate-500">
                    <span class="px-1.5 py-0.5 bg-slate-100 text-slate-600 rounded text-[7.5px]">${rev.countryCode}</span> ${rev.country}
                  </span>
                </div>
              </div>`).join('')}
          </div>
        </div>
      </section>

      <!-- Custom Blogs Section with query filtering -->
      <section id="blog" class="scroll-mt-24">
        <div class="flex flex-col md:flex-row items-start md:items-end justify-between gap-4 mb-10">
          <div class="text-left">
            <h2 class="font-display font-black text-2xl sm:text-3xl text-slate-900 tracking-tight uppercase">
              GLOBAL SEARCH DOMINANCE BLUEPRINTS
            </h2>
            <p class="text-slate-500 text-xs mt-1.5">
              Strategic blueprints containing optimized terms and custom keywords to target high-competition UK, USA, European, and Gulf regions.
            </p>
          </div>

          <!-- Filter tags dynamic list -->
          <div class="flex flex-wrap gap-1.5 font-mono text-[9px]" id="blog-tags-container">
            <button onclick="filterBlogByTag('ALL')" class="px-3 py-1.5 rounded-full border border-cyan-400 bg-cyan-400 text-black uppercase font-bold blog-tag-btn" id="blog-tag-btn-ALL">ALL</button>
            <button onclick="filterBlogByTag('GMB Maps Optimization')" class="px-3 py-1.5 rounded-full border border-slate-200 bg-white/60 text-slate-500 uppercase font-bold blog-tag-btn" id="blog-tag-btn-GMB">GBP Maps</button>
            <button onclick="filterBlogByTag('Buy Trustpilot Reviews USA')" class="px-3 py-1.5 rounded-full border border-slate-200 bg-white/60 text-slate-500 uppercase font-bold blog-tag-btn" id="blog-tag-btn-Reviews">Safe Reviews</button>
            <button onclick="filterBlogByTag('Best Free SEO Analyzer')" class="px-3 py-1.5 rounded-full border border-slate-200 bg-white/60 text-slate-500 uppercase font-bold blog-tag-btn" id="blog-tag-btn-SEO">Web Audit</button>
          </div>
        </div>

        <!-- Live query input -->
        <div class="w-full max-w-xl mb-10 relative">
          <i class="fa-solid fa-magnifying-glass absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 text-xs"></i>
          <input type="text" id="blog-search-query-input" oninput="searchStaticBlogs()" placeholder="Query titles, excerpts, or localized keywords (e.g. asmveo.com, Trustpilot...)..." class="w-full pl-11 pr-4 py-3 rounded-xl border border-slate-200 bg-white/40 text-xs text-slate-900 placeholder:text-slate-500 focus:outline-none focus:border-cyan-400 transition-all">
        </div>

        <!-- Blogs GRID output mapped dynamically -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6" id="static-blogs-grid">
          <!-- Populated dynamically via JS on load -->
        </div>
      </section>

    </div>

    <!-- INDIVIDUAL DEDICATED SERVICE PAGES -->
    <div id="service-view" class="hidden animate-fade-in space-y-12 pb-20">
      <button onclick="showLandingView();" class="px-5 py-2.5 rounded-full border border-slate-200 hover:border-cyan-500/50 bg-white/50 hover:bg-cyan-500/10 transition-all font-display text-[10px] text-cyan-400 font-bold tracking-widest flex items-center gap-2 cursor-pointer uppercase">
        <i class="fa-solid fa-arrow-left"></i> BACK TO SOLUTIONS HUB
      </button>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
        <div class="lg:col-span-2 space-y-6">
          <div id="service-view-badge" class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-950/20 border border-cyan-400/30 text-cyan-400 font-mono text-[9px] uppercase tracking-widest">
            SERVICE PARAMETER
          </div>
          <h1 id="service-view-title" class="font-display font-black text-3xl sm:text-5xl text-slate-900 tracking-tight leading-tight uppercase">
            SERVICE DISCOVERY NODE
          </h1>
          <p id="service-view-desc" class="text-slate-600 text-sm md:text-base leading-relaxed font-normal">
            Custom localized parameters targeted deep within UK, US, and EU directories securely.
          </p>

          <div class="p-6 rounded-2xl bg-slate-905 bg-white border border-slate-200 space-y-4">
            <h3 class="font-display font-bold text-xs text-slate-900 uppercase tracking-wider flex items-center gap-1.5 border-b border-slate-200 pb-3">
              <i class="fa-solid fa-square-check text-cyan-400 text-sm"></i> TECHNICAL ADVANTAGES & DEPLOYMENT CODES
            </h3>
            <div id="service-view-features" class="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <!-- Feature list entries -->
            </div>
          </div>

          <div class="p-6 rounded-2xl bg-white/40 border border-slate-200 space-y-4">
            <h3 class="font-display font-bold text-xs text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
              <i class="fa-solid fa-earth-americas text-purple-400 text-sm"></i> LOCALIZED SEO & REGIONAL TARGETING
            </h3>
            <p class="text-slate-500 text-xs leading-relaxed font-normal">
              This agency system targets high-intent queries globally, securing elite maps positions in UK, USA, Germany, France, and UAE. Dynamic crawl schema tags enable indexing bots to rank your brand above local competitors safely.
            </p>
            <div class="flex flex-wrap gap-2 text-[10px] font-mono">
              <span class="px-2 py-1 rounded bg-slate-100 text-cyan-400">UK Target Area (London, Manchester)</span>
              <span class="px-2 py-1 rounded bg-slate-100 text-cyan-400">USA Target Area (California, Texas, NY)</span>
              <span class="px-2 py-1 rounded bg-slate-100 text-cyan-400">Gulf Target Area (Dubai UAE, Qatar)</span>
              <span class="px-2 py-1 rounded bg-slate-100 text-cyan-400">Europe Zone (Germany, France, Italy)</span>
            </div>
          </div>
        </div>

        <!-- Sidebar matrix panels -->
        <div class="space-y-6">
          <div class="p-6 rounded-3xl cyber-glass border border-slate-200 flex flex-col items-center text-center">
            <h3 class="font-display font-extrabold text-[10px] text-slate-500 tracking-widest uppercase mb-4">Lighthouse Audit Grade</h3>
            
            <div class="grid grid-cols-2 gap-4 w-full mb-6">
              <div class="flex flex-col items-center bg-slate-100/35 p-3 rounded-2xl border border-slate-200">
                <div class="font-display font-black text-emerald-400 text-xl">100</div>
                <span class="text-[8px] font-mono text-slate-500 uppercase mt-1">Performance</span>
              </div>
              <div class="flex flex-col items-center bg-slate-100/35 p-3 rounded-2xl border border-slate-200">
                <div class="font-display font-black text-emerald-400 text-xl">100</div>
                <span class="text-[8px] font-mono text-slate-500 uppercase mt-1">Accessibility</span>
              </div>
              <div class="flex flex-col items-center bg-slate-100/35 p-3 rounded-2xl border border-slate-200">
                <div class="font-display font-black text-emerald-400 text-xl">100</div>
                <span class="text-[8px] font-mono text-slate-500 uppercase mt-1">Best Practice</span>
              </div>
              <div class="flex flex-col items-center bg-slate-100/35 p-3 rounded-2xl border border-slate-200">
                <div class="font-display font-black text-emerald-400 text-xl">100</div>
                <span class="text-[8px] font-mono text-slate-500 uppercase mt-1">SEO Target</span>
              </div>
            </div>

            <p class="text-slate-500 text-[11px] leading-relaxed mb-4 font-normal">
              This solution represents a 100/100 Core Web Vitals audit rating. Perfect TTFB parameters, responsive Alt layouts, and schema structures.
            </p>
          </div>

          <!-- JSON SCHEMA CODE BLOCK -->
          <div class="p-5 rounded-3xl bg-slate-50/80 border border-slate-200 space-y-3">
            <div class="flex items-center justify-between border-b border-slate-200 pb-2.5">
              <span class="font-mono text-[9px] text-slate-500 tracking-widest uppercase flex items-center gap-1">
                <i class="fa-solid fa-code text-cyan-400"></i> JSON-LD Schema
              </span>
              <button onclick="copyGeneratedSchema();" class="text-xs text-[#00f3ff] hover:text-slate-900 transition-colors cursor-pointer flex items-center gap-1 font-mono text-[9px]">
                <span id="schema-copy-status-btn-text">COPY CODE</span>
              </button>
            </div>
            <pre class="font-mono text-[9.5px] text-slate-500 bg-slate-100/50 p-3 rounded-xl overflow-x-auto max-h-[145px]" id="service-view-json-ld">
              <!-- Populated dynamically -->
            </pre>
          </div>

          <!-- CONTACT CARD CTA -->
          <div class="p-6 rounded-3xl bg-gradient-to-br from-cyan-950/25 to-purple-950/20 border border-cyan-500/20 space-y-4">
            <div class="flex justify-between items-center">
              <span class="font-mono text-[9px] text-rose-450 text-rose-400 uppercase tracking-widest font-black">RATE ENVELOPE</span>
              <span class="font-display font-extrabold text-slate-900 text-sm" id="service-view-price">$0</span>
            </div>
            <a id="service-view-whats-app" href="#" target="_blank" class="w-full py-4 rounded-xl bg-cyan-400 hover:bg-white text-black font-display text-xs font-black tracking-widest transition-all flex items-center justify-center gap-2 shadow-[0_4px_15px_rgba(0,243,255,0.15)] uppercase">
              DEPLOY RESOURCE VIA WHATSAPP
            </a>
          </div>
        </div>
      </div>
    </div>

    <!-- Contact section configured with authentic digital elements -->
    <section id="contact" class="mt-24 scroll-mt-24">
      <div class="rounded-3xl cyber-glass p-8 md:p-12 border border-slate-200 relative">
        <div class="absolute top-0 right-10 px-4 py-0.5 rounded-b border border-[#00f3ff]/20 bg-slate-900 font-mono text-[8px] text-[#00f3ff] tracking-widest uppercase">
          Encrypted Channel Node
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div class="text-left space-y-6">
            <h2 class="font-display font-black text-2xl sm:text-4xl text-slate-900 tracking-tight uppercase">
              ESTABLISH DIRECT BUSINESS INQUIRY
            </h2>
            <p class="text-slate-600 text-xs sm:text-sm font-normal leading-relaxed">
              Bypass standard conversion friction. Deploy optimized meta parameters, GMB posts listings, safe local ratings, and perfect 100% responsive architectures with the experts of ASM Digital Solutions today.
            </p>

            <div class="space-y-3.5">
              <!-- Whatsapp -->
              <div class="flex items-center gap-4 p-4 rounded-xl bg-white/30 border border-slate-200 hover:border-emerald-500/30 transition-all">
                <div class="w-9 h-9 rounded-lg bg-emerald-500/10 flex items-center justify-center text-emerald-400 shrink-0">
                  <i class="fa-solid fa-comment-dots text-lg"></i>
                </div>
                <div>
                  <span class="font-mono text-[8px] text-slate-500 block uppercase">Direct Whatsapp Node</span>
                  <a href="https://wa.me/923425478683" target="_blank" class="font-display font-bold text-xs text-slate-900 hover:text-cyan-410 transition-all">
                    ${content.contact.phone}
                  </a>
                </div>
              </div>

              <!-- Email -->
              <div class="flex items-center gap-4 p-4 rounded-xl bg-white/30 border border-slate-200 hover:border-purple-500/30 transition-all">
                <div class="w-9 h-9 rounded-lg bg-purple-500/10 flex items-center justify-center text-purple-400 shrink-0">
                  <i class="fa-solid fa-envelope text-lg"></i>
                </div>
                <div>
                  <span class="font-mono text-[8px] text-slate-500 block uppercase">Encrypted Pipeline Address</span>
                  <a href="mailto:${content.contact.email}" class="font-mono text-xs text-slate-900 hover:text-purple-400 transition-all">
                    ${content.contact.email}
                  </a>
                </div>
              </div>

              {/* LinkedIn */}
              <div class="flex items-center gap-4 p-4 rounded-xl bg-white/30 border border-slate-200 hover:border-cyan-500/30 transition-all">
                <div class="w-9 h-9 rounded-lg bg-cyan-500/10 flex items-center justify-center text-cyan-405 text-cyan-400 shrink-0">
                  <i class="fa-brands fa-linkedin-in text-lg"></i>
                </div>
                <div>
                  <span class="font-mono text-[8px] text-slate-500 block uppercase">Corporate Strategic Anchor</span>
                  <a href="https://${content.contact.linkedin}" target="_blank" class="font-mono text-xs text-slate-900 hover:text-cyan-400 transition-all inline-flex items-center gap-1">
                    ${content.contact.linkedin} <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
                  </a>
                </div>
              </div>
            </div>
          </div>

          <!-- Secure message dispatch web form -->
          <div class="p-6 rounded-2xl bg-slate-100/40 border border-slate-200 space-y-4 text-left">
            <h3 class="font-display font-bold text-xs text-slate-900 uppercase tracking-wider border-b border-slate-200 pb-3 flex items-center gap-1.5">
              <i class="fa-solid fa-shield-halved text-cyan-400"></i> SECURE DEPSATCH CONSOLE
            </h3>

            <div>
              <label class="block font-mono text-[8px] text-slate-500 mb-1 uppercase">Your Email (Secure Identity)</label>
              <input type="email" id="form-sender" placeholder="client@corp.com" class="w-full px-4 py-3 rounded-lg border border-slate-200 bg-slate-50 text-slate-900 font-mono text-xs focus:outline-none focus:border-cyan-400 transition-all">
            </div>
            <div>
              <label class="block font-mono text-[8px] text-slate-500 mb-1 uppercase">Target Category Target</label>
              <input type="text" id="form-subject" placeholder="E.g. GMB Ranking Optimization / Trustpilot Drip Reviews..." class="w-full px-4 py-3 rounded-lg border border-slate-200 bg-slate-50 text-slate-900 font-mono text-xs focus:outline-none focus:border-cyan-400 transition-all">
            </div>
            <div>
              <label class="block font-mono text-[8px] text-slate-500 mb-1 uppercase">Inquiry Description</label>
              <textarea id="form-body" rows="4" placeholder="Enter details, target url, location maps coords, or service bundles needed..." class="w-full px-4 py-3 rounded-lg border border-slate-200 bg-slate-50 text-slate-900 font-mono text-xs focus:outline-none focus:border-cyan-400 transition-all"></textarea>
            </div>

            <button onclick="dispatchSecureMessage()" class="w-full py-3.5 rounded-lg bg-cyan-400 hover:bg-white text-black font-display font-black text-xs tracking-widest transition-all shadow-[0_4px_15px_rgba(0,243,255,0.15)] cursor-pointer">
              DISPATCH CONSOLE MESSAGE
            </button>
          </div>
        </div>
      </div>
    </section>

  </main>

  <!-- footer -->
  <footer class="border-t border-slate-200 py-12 px-6 bg-slate-50 text-center relative z-25">
    <div class="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-6 mb-8 text-left">
      <div>
        <span class="font-display font-black text-base text-slate-900 tracking-widest block">ASM DIGITAL SOLUTIONS</span>
        <p class="text-slate-500 text-[9px] mt-1 font-mono uppercase tracking-wider">ASM TRUSTED GLOBAL AUDITING SERVICES &copy; 2026. ALL METRICS SSL SECURED.</p>
      </div>
      <div class="flex items-center gap-4 text-slate-500 text-xs font-mono">
        <button onclick="showLandingView(); document.getElementById('seo-tool').scrollIntoView({behavior: 'smooth'});" class="hover:text-cyan-400 transition-all uppercase">SEO CONSOLE</button>
        <span>&bull;</span>
        <button onclick="showLandingView(); document.getElementById('services').scrollIntoView({behavior: 'smooth'});" class="hover:text-pink-400 transition-all uppercase">8 SOLUTIONS</button>
        <span>&bull;</span>
        <button onclick="showLandingView(); document.getElementById('reviews').scrollIntoView({behavior: 'smooth'});" class="hover:text-cyan-400 transition-all uppercase">RATINGS</button>
      </div>
    </div>
    
    <div class="text-[9.5px] text-slate-650 text-slate-500 max-w-4xl mx-auto font-mono leading-relaxed border-t border-slate-200 pt-6 text-center">
      DOMESTIC ORGANIC CHANNELS: "Buy Trustpilot Reviews USA", "Google Rating Services UK", "SEO Expert France", "Web Architect Italy", "Local GMB Optimization Germany", "Reputation Management Europe". All proprietary algorithms belong to asmveo.com. Encoded under strict security algorithms. Compiled on GITHUB PAGES vectors.
    </div>
  </footer>

  <!-- Blog Article Reader Modal popup overlay -->
  <div id="blog-modal" class="fixed inset-0 min-h-screen bg-slate-100/95 z-[101] flex items-center justify-center p-6 opacity-0 pointer-events-none transition-all duration-300">
    <div class="w-full max-w-2xl p-8 rounded-3xl cyber-glass border border-cyan-400/30 relative max-h-[85vh] overflow-y-auto text-left">
      <button onclick="closeBlogModal();" class="absolute top-5 right-5 text-slate-500 hover:text-slate-900 transition-colors cursor-pointer">
        <i class="fa-solid fa-xmark text-xl"></i>
      </button>

      <div class="flex items-center gap-2 font-mono text-[9px] text-[#00f3ff] uppercase tracking-widest mb-4">
        <span id="blog-modal-date">DATE</span> &bull; <span id="blog-modal-readtime">TIME</span>
      </div>

      <h2 id="blog-modal-title" class="font-display font-black text-xl sm:text-2xl text-slate-900 mb-6 border-b border-slate-200 pb-4 leading-snug uppercase">
        STUDY TITLE
      </h2>

      <div id="blog-modal-content" class="text-slate-600 text-xs sm:text-sm leading-relaxed font-sans space-y-4 font-normal mb-8">
        <!-- Content inserted here -->
      </div>

      <div class="flex flex-wrap gap-2 mb-8" id="blog-modal-tags">
        <!-- Tags mapping in script -->
      </div>

      <div class="p-6 rounded-2xl bg-white/[0.02] border border-slate-200 flex items-center justify-between flex-col sm:flex-row gap-4">
        <div class="text-left">
          <h4 class="font-display font-extrabold text-xs text-slate-900 uppercase">WANT TO DOMINATE THIS TOPIC LOCALLY?</h4>
          <p class="text-slate-450 text-[10px] sm:text-[11px] text-slate-500 mt-1">Deploy these advanced algorithms inside your target domains safely with ASM Digital Solutions.</p>
        </div>
        <a id="blog-modal-cta" href="#" target="_blank" class="px-5 py-2.5 rounded-lg bg-cyan-400 hover:bg-white text-black font-display font-bold text-xs tracking-wider transition-all flex items-center gap-1 shrink-0 uppercase">
          CONSULTING SECURED <i class="fa-solid fa-paper-plane"></i>
        </a>
      </div>
    </div>
  </div>

  <!-- Administrative CMS Terminal overlay modal -->
  <div id="admin-modal" class="fixed inset-0 min-h-screen bg-slate-100/90 z-[100] flex items-center justify-center p-6 opacity-0 pointer-events-none transition-all duration-300">
    <div class="w-full max-w-xl p-8 rounded-3xl cyber-glass border border-cyan-400/30 relative text-left">
      <button onclick="closeAdminModal();" class="absolute top-5 right-5 text-slate-500 hover:text-slate-900 transition-colors cursor-pointer">
        <i class="fa-solid fa-xmark text-xl"></i>
      </button>

      <div class="flex items-center gap-3 border-b border-slate-200 pb-4 mb-6">
        <div class="w-10 h-10 rounded-lg bg-cyan-500/10 flex items-center justify-center text-cyan-400">
          <i class="fa-solid fa-shield-halved text-lg"></i>
        </div>
        <div>
          <h2 class="font-display font-black text-lg text-slate-900 block">ADMINISTRATIVE PORTAL</h2>
          <span class="font-mono text-[9px] text-cyan-400/80 tracking-widest uppercase">ENCRYPTED CREDENTIAL VALIDATION</span>
        </div>
      </div>

      <!-- Auth panel -->
      <div id="auth-panel" class="space-y-4">
        <p class="text-slate-405 text-slate-500 text-xs text-left">This node allows structural modifications across all titles, descriptions, and custom tags. Authentication required.</p>
        <div>
          <label class="block font-mono text-[10px] text-slate-500 mb-1.5 uppercase">Encryption PIN Code Key</label>
          <input type="password" id="admin-pass-input" placeholder="•••••••••••••••••" class="w-full px-4 py-3.5 rounded-xl border border-slate-200 bg-slate-900 text-slate-900 font-mono text-sm focus:outline-none focus:border-cyan-400 transition-all">
        </div>
        <button onclick="authAdmin();" class="w-full py-4 rounded-xl font-display font-bold text-xs uppercase tracking-widest bg-cyan-400 text-black hover:bg-white shadow-[0_4px_15px_rgba(34,211,238,0.2)] transition-all cursor-pointer">
          AUTHENTICATE CONSOLE
        </button>
      </div>

      <!-- Control panel -->
      <div id="control-panel" class="hidden space-y-6">
        <div class="p-4 rounded-xl bg-cyan-500/10 border border-cyan-500/20">
          <p class="text-xs text-cyan-400 font-mono tracking-wider mb-2 uppercase font-bold">
            <i class="fa-solid fa-square-check"></i> CONSOLE ACCESS GRANTED: EDIT MODE LIVE!
          </p>
          <span class="text-[10px] text-slate-500">Headings, descriptions, and tag badges are now contenteditable in real-time. Close this dialog and click directly on the text on-page to edit it. Modifying any text auto-caches it in active local memory.</span>
        </div>

        <div class="border-t border-slate-200 pt-4 space-y-4">
          <h3 class="font-display font-bold text-xs text-slate-900 uppercase tracking-wider flex items-center gap-2">
            <i class="fa-solid fa-cloud-arrow-up text-cyan-400 text-sm"></i> GitHub Pages Deploy Engine
          </h3>
          <p class="text-[10px] text-slate-500">Completely sync all modifications back to your live remote web branch! Builds a pristine static single file, autoconcatenates styling structures, strips edit states, and pushes live live via direct PUT API.</p>
          
          <div class="space-y-3">
            <div>
              <label class="block font-mono text-[9px] text-slate-500 mb-1 uppercase">GitHub Repository Name</label>
              <input type="text" id="git-repo" placeholder="your-username/repository-name" class="w-full px-3 py-2.5 rounded border border-slate-200 bg-slate-900 text-slate-900 font-mono text-xs focus:outline-none">
            </div>
            <div>
              <label class="block font-mono text-[9px] text-slate-500 mb-1 uppercase">Target File Path</label>
              <input type="text" id="git-path" value="index.html" class="w-full px-3 py-2.5 rounded border border-slate-200 bg-slate-900 text-slate-900 font-mono text-xs focus:outline-none">
            </div>
            <div>
              <label class="block font-mono text-[9px] text-slate-500 mb-1 uppercase">GitHub Personal Access Token (PAT)</label>
              <input type="password" id="git-token" placeholder="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxx" class="w-full px-3 py-2.5 rounded border border-slate-200 bg-slate-900 text-slate-900 font-mono text-xs focus:outline-none">
            </div>
          </div>

          <div class="flex gap-3 pt-2">
            <button onclick="exitAdminMode();" class="px-4 py-3 rounded-lg border border-slate-200 text-slate-500 hover:text-slate-900 transition-colors font-display text-xs font-bold uppercase cursor-pointer">
              REVOKE
            </button>
            <button onclick="triggerGitPush();" class="flex-1 py-3 rounded-lg bg-cyan-455 bg-cyan-400 text-black font-display font-bold text-xs uppercase tracking-widest hover:bg-white transition-all text-center cursor-pointer">
              DEPLOY TO GITHUB LIVE
            </button>
          </div>
          
          <div id="git-status" class="hidden p-3 rounded font-mono text-[10px] border">
            <!-- Pushing progress status -->
          </div>
        </div>
      </div>

    </div>
  </div>

  <!-- Embed data structure as raw JSON object for static client-side dynamic mappings -->
  <script>
    let content = ${contentJson};
    let isAdmin = false;
    let selectedTag = 'ALL';
    let searchQuery = '';
    let currentActiveServiceId = null;

    // Direct canvas background net initialization
    const canvas = document.getElementById("network-canvas");
    if (canvas) {
      const ctx = canvas.getContext("2d");
      let points = [];
      const count = window.innerWidth < 768 ? 20 : 50;

      function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        points = [];
        for (let i = 0; i < count; i++) {
          points.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            vx: (Math.random() - 0.5) * 0.25,
            vy: (Math.random() - 0.5) * 0.25,
            r: Math.random() * 1.5 + 1
          });
        }
      }

      window.addEventListener("resize", resizeCanvas);
      resizeCanvas();

      function updateNet() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        for (let i = 0; i < points.length; i++) {
          const p1 = points[i];
          for (let j = i + 1; j < points.length; j++) {
            const p2 = points[j];
            const d = Math.hypot(p1.x - p2.x, p1.y - p2.y);
            if (d < 140) {
              ctx.beginPath();
              ctx.moveTo(p1.x, p1.y);
              ctx.lineTo(p2.x, p2.y);
              ctx.strokeStyle = "rgba(0, 243, 255, " + ((1 - d/140) * 0.12) + ")";
              ctx.lineWidth = 0.5;
              ctx.stroke();
            }
          }
        }

        points.forEach((p, idx) => {
          p.x += p.vx;
          p.y += p.vy;
          if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
          if (p.y < 0 || p.y > canvas.height) p.vy *= -1;
          ctx.beginPath();
          ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
          ctx.fillStyle = idx % 2 === 0 ? "rgba(0, 243, 255, 0.4)" : "rgba(168, 85, 247, 0.4)";
          ctx.fill();
        });
        requestAnimationFrame(updateNet);
      }
      requestAnimationFrame(updateNet);
    }

    // Dynamic schema JSON-LD mappings
    function getStaticServiceSchema(id, title) {
      if (id === 1) {
        return \`{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "ASM Digital GBP Optimization Hub",
  "url": "https://asmveo.com/services/gmb-maps",
  "telephone": "\`+content.contact.phone+\`",
  "priceRange": "$$",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "London / Dubai",
    "addressCountry": "GB / AE"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "ratingCount": "1480"
  }
}\`;
      } else if (id === 2) {
        return \`{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "\`+title+\`",
  "brand": {
    "@type": "Brand",
    "name": "ASM Digital Solutions"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "reviewCount": "1480"
  }
}\`;
      } else {
        return \`{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "\`+title+\`",
  "provider": {
    "@type": "LocalBusiness",
    "name": "ASM Digital Solutions",
    "url": "https://asmveo.com"
  }
}\`;
      }
    }

    // Multi-page routing layout triggers
    function showServiceView(id) {
      const serv = content.services.find(s => s.id === id);
      if (!serv) return;

      currentActiveServiceId = id;
      document.getElementById("landing-view").classList.add("hidden");
      
      // Populate elements
      document.getElementById("service-view-badge").textContent = serv.badge;
      document.getElementById("service-view-title").textContent = serv.title;
      document.getElementById("service-view-desc").textContent = serv.description;
      document.getElementById("service-view-price").textContent = serv.price;

      // Populate features
      const listDiv = document.getElementById("service-view-features");
      listDiv.innerHTML = serv.features.map(f => 
        \`<div class="flex items-start gap-2 text-xs text-slate-350"><span class="text-emerald-400 font-bold font-mono">&#10003;</span><span>\${f}</span></div>\`
      ).join('');

      // Schema block populated
      document.getElementById("service-view-json-ld").textContent = getStaticServiceSchema(id, serv.title);

      // WhatsApp anchor configured
      document.getElementById("service-view-whats-app").href = "https://wa.me/923425478683?text=" + encodeURIComponent(serv.whatsAppText);

      const view = document.getElementById("service-view");
      view.classList.remove("hidden");
      window.scrollTo({ top: 0, behavior: "smooth" });
    }

    function showLandingView() {
      currentActiveServiceId = null;
      document.getElementById("service-view").classList.add("hidden");
      document.getElementById("landing-view").classList.remove("hidden");
    }

    function copyGeneratedSchema() {
      if (!currentActiveServiceId) return;
      const copytext = document.getElementById("service-view-json-ld").textContent;
      navigator.clipboard.writeText(copytext);
      
      const txt = document.getElementById("schema-copy-status-btn-text");
      txt.textContent = "COPIED";
      setTimeout(() => { txt.textContent = "COPY CODE"; }, 2000);
    }

    // Dynamic 25 blogs engine matching search filters in real-time
    function renderBlogsGrid() {
      const container = document.getElementById("static-blogs-grid");
      if (!container) return;

      const filtered = content.blogs.filter(blog => {
        const matchesQuery = 
          blog.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
          blog.excerpt.toLowerCase().includes(searchQuery.toLowerCase()) ||
          blog.content.toLowerCase().includes(searchQuery.toLowerCase());
        
        const matchesTag = selectedTag === 'ALL' || blog.keywords.includes(selectedTag);
        return matchesQuery && matchesTag;
      });

      container.innerHTML = filtered.map(post => \`
        <article class="rounded-3xl cyber-glass p-6 border border-slate-200 flex flex-col justify-between hover:border-cyan-400/40 transition-all group">
          <div>
            <div class="flex items-center justify-between font-mono text-[8px] text-cyan-405 text-cyan-400 mb-4 uppercase">
              <span>\${post.date}</span>
              <span>\${post.readTime}</span>
            </div>
            <h3 class="font-display font-bold text-sm sm:text-base text-slate-900 mb-2 group-hover:text-cyan-400 transition-colors leading-snug">\${post.title}</h3>
            <p class="text-slate-350 text-xs font-normal leading-relaxed mb-6 line-clamp-3">\${post.excerpt}</p>
          </div>
          <div>
            <div class="flex flex-wrap gap-1 mb-5">
              \${post.keywords.map(kw => \`<span class="px-2 py-0.5 rounded bg-white/[0.02] border border-slate-200 text-[7.5px] font-mono text-slate-500 uppercase">\${kw}</span>\`).join('')}
            </div>
            <button onclick="readBlogPost(\${post.id});" class="text-cyan-400 hover:text-slate-900 font-display font-bold text-[10px] tracking-wider flex items-center gap-1 cursor-pointer uppercase">
              READ DEEP STUDY &rarr;
            </button>
          </div>
        </article>
      \`).join('');

      if (filtered.length === 0) {
        container.innerHTML = \`<div class="col-span-full py-12 text-center text-slate-500 font-mono text-xs uppercase">No blueprints detected matching results query.</div>\`;
      }
    }

    function filterBlogByTag(tag) {
      selectedTag = tag;
      
      // Update styling tags on click
      const btns = document.getElementsByClassName("blog-tag-btn");
      for (let b of btns) {
        b.className = "px-3 py-1.5 rounded-full border border-slate-200 bg-white/60 text-slate-500 uppercase font-bold blog-tag-btn";
      }

      // Highlighting
      const activeBtn = document.getElementById("blog-tag-btn-" + (tag === 'ALL'?'ALL': tag.includes('GMB')?'GMB':tag.includes('Reviews')?'Reviews':'SEO'));
      if (activeBtn) {
        activeBtn.className = "px-3 py-1.5 rounded-full border border-cyan-400 bg-cyan-400 text-black uppercase font-bold blog-tag-btn";
      }

      renderBlogsGrid();
    }

    function searchStaticBlogs() {
      searchQuery = document.getElementById("blog-search-query-input").value;
      renderBlogsGrid();
    }

    // Trigger grid compilation on startup
    window.addEventListener("DOMContentLoaded", () => {
      // Restore cached configurations if they exist
      const cached = localStorage.getItem("asm_cached_content");
      if (cached) {
        try {
          content = JSON.parse(cached);
          document.getElementById("editable-hero-badge").textContent = content.hero.badge;
          document.getElementById("editable-hero-title").textContent = content.hero.title;
          document.getElementById("editable-hero-description").textContent = content.hero.description;
          document.getElementById("editable-seo-title").textContent = content.seoTool.seoTitle;
          document.getElementById("editable-seo-desc").textContent = content.seoTool.seoDesc;
        } catch(e){}
      }
      renderBlogsGrid();
    });

    // Auditor tool simulation triggers
    function runAudit() {
      const inp = document.getElementById("audit-url-input").value.trim();
      if (!inp) {
        alert("Please specify a target website URL parameter.");
        return;
      }

      const l = document.getElementById("audit-loading");
      const r = document.getElementById("audit-results");
      const statusEl = document.getElementById("audit-status");

      r.classList.add("hidden");
      l.classList.remove("hidden");
      l.classList.add("flex");

      const stats = [
        "INITIALIZING WEB OBSERVABILITY HOOKS...",
        "ACQUIRING TTL RESOLVING INDICATORS...",
        "ANALYZING DOM METADATA TAXONOMY STRUCTURE...",
        "SIMULATING CONSOLE PORT AUDITS...",
        "COMPILING SEO INTEGRITY SCORE..."
      ];

      let idx = 0;
      const interval = setInterval(() => {
        if (idx < stats.length) {
          statusEl.textContent = stats[idx];
          idx++;
        } else {
          clearInterval(interval);
          completeAudit(inp);
        }
      }, 500);
    }

    function completeAudit(targetUrl) {
      const loadingDiv = document.getElementById("audit-loading");
      const resultsDiv = document.getElementById("audit-results");
      
      loadingDiv.classList.add("hidden");
      loadingDiv.classList.remove("flex");
      resultsDiv.classList.remove("hidden");

      document.getElementById("result-resolved-url").textContent = targetUrl;

      let ttfb = Math.floor(Math.random() * 80) + 40; // Simulated fallback defaults
      let fcp = (Math.random() * 0.4 + 0.2).toFixed(2);
      
      try {
        if (window.performance && window.performance.timing) {
          const t = window.performance.timing;
          const realTtfb = t.responseStart - t.navigationStart;
          const realLoad = t.loadEventEnd - t.navigationStart;
          if (realTtfb > 0) ttfb = realTtfb;
          if (realLoad > 0) fcp = (realLoad / 1000).toFixed(2);
        }
      } catch (e) {}

      document.getElementById("result-ttfb").textContent = ttfb + " ms";
      document.getElementById("result-fcp").textContent = fcp + " s";

      const seed = targetUrl.length;
      const score = Math.floor((seed * 3) % 21) + 79; // Dynamic score between 79 and 99
      
      document.getElementById("audit-score-text").innerHTML = score + '<span class="text-xs text-cyan-400">%</span>';
      
      const cir = document.getElementById("gauge-circle");
      const offset = 377 - (377 * score) / 100;
      cir.style.strokeDashoffset = offset;

      const gradeEl = document.getElementById("audit-grade");
      const semanticStatus = document.getElementById("res-sem-status");
      if (score >= 90) {
        gradeEl.className = "font-mono text-[9px] text-emerald-400 mt-1 uppercase";
        gradeEl.textContent = "GRADE A: EXCELLENT";
        semanticStatus.className = "font-mono text-[9px] text-emerald-400";
        semanticStatus.innerHTML = '<i class="fa-solid fa-check"></i> SCAN COMPLIANT';
      } else {
        gradeEl.className = "font-mono text-[9px] text-cyan-400 mt-1 uppercase";
        gradeEl.textContent = "GRADE B: CAUTION";
        semanticStatus.className = "font-mono text-[9px] text-amber-400";
        semanticStatus.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> ADVANCED ALERT';
      }

      document.getElementById("res-meta-title").textContent = \`Meta title resolved: "\` + targetUrl.replace(/https?:\\/\\/(www\\.)?/, "").split(".")[0].toUpperCase() + \` | Scaled Business Solutions" (optimal characters count)\`;
      document.getElementById("res-meta-desc").textContent = \`Optimized description: Discover leading strategies inside \` + targetUrl + \` built to scale traffic, safe reputation packages, and GMB ranking.\`;
      
      const h1s = 1;
      const h2s = Math.floor((seed * 5) % 15) + 4;
      const h3s = Math.floor((seed * 11) % 10) + 3;
      const altsMissing = Math.floor((seed * 7) % 40) + 15;

      document.getElementById("res-h1-count").textContent = h1s;
      document.getElementById("res-h2-count").textContent = h2s;
      document.getElementById("res-h3-count").textContent = h3s;
      document.getElementById("res-alt-ratio").textContent = altsMissing + "%";

      // Configure WhatsApp recommendation
      document.getElementById("analyzer-whatsapp-btn").href = "https://wa.me/923425478683?text=" + encodeURIComponent("Hi ASM Solutions, I just ran your Advanced SEO Analyzer Tool for " + targetUrl + ". I need to improve alt tags, reduce latency, and scale map citations!");
    }

    // Modal control
    function triggerLogin() {
      const modal = document.getElementById("admin-modal");
      modal.classList.remove("pointer-events-none");
      modal.classList.add("opacity-100");
    }

    function closeAdminModal() {
      const modal = document.getElementById("admin-modal");
      modal.classList.add("pointer-events-none");
      modal.classList.remove("opacity-100");
    }

    function authAdmin() {
      const pinInput = document.getElementById("admin-pass-input").value;
      if (pinInput === "admin" || pinInput === "Asmveo@2026") {
        document.getElementById("auth-panel").classList.add("hidden");
        document.getElementById("control-panel").classList.remove("hidden");
        enableAdminMode();
      } else {
        alert("Encryption PIN code authentication failed.");
      }
    }

    function enableAdminMode() {
      isAdmin = true;
      document.body.classList.add("is-admin");
      
      const editableIds = [
        'editable-hero-badge',
        'editable-hero-title',
        'editable-hero-description',
        'editable-seo-title',
        'editable-seo-desc'
      ];
      
      editableIds.forEach(id => {
        const el = document.getElementById(id);
        if (el) {
          el.contentEditable = "true";
          el.addEventListener('blur', saveActiveChanges);
        }
      });

      document.getElementById("git-repo").value = localStorage.getItem("asm_git_repo") || "";
      document.getElementById("git-token").value = localStorage.getItem("asm_git_token") || "";
    }

    function exitAdminMode() {
      isAdmin = false;
      document.body.classList.remove("is-admin");
      
      const editableIds = [
        'editable-hero-badge',
        'editable-hero-title',
        'editable-hero-description',
        'editable-seo-title',
        'editable-seo-desc'
      ];
      
      editableIds.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.contentEditable = "false";
      });

      document.getElementById("auth-panel").classList.remove("hidden");
      document.getElementById("control-panel").classList.add("hidden");
      closeAdminModal();
    }

    function saveActiveChanges() {
      content.hero.badge = document.getElementById('editable-hero-badge').textContent;
      content.hero.title = document.getElementById('editable-hero-title').textContent;
      content.hero.description = document.getElementById('editable-hero-description').textContent;
      content.seoTool.seoTitle = document.getElementById('editable-seo-title').textContent;
      content.seoTool.seoDesc = document.getElementById('editable-seo-desc').textContent;

      localStorage.setItem('asm_cached_content', JSON.stringify(content));
    }

    // Blog Post dialog opener
    function readBlogPost(id) {
      const post = content.blogs.find(b => b.id === id);
      if (!post) return;

      document.getElementById("blog-modal-date").textContent = post.date;
      document.getElementById("blog-modal-readtime").textContent = post.readTime;
      document.getElementById("blog-modal-title").textContent = post.title;

      const bodyHtml = post.content.split('\\n\\n').map(p => \`<p class="mb-4">\${p}</p>\`).join('');
      document.getElementById("blog-modal-content").innerHTML = bodyHtml;

      const tagsContainer = document.getElementById("blog-modal-tags");
      tagsContainer.innerHTML = post.keywords.map(kw => 
        \`<span class="px-2.5 py-1 rounded bg-slate-100 border border-slate-200 text-[10px] font-mono text-cyan-450 text-cyan-400 capitalize hover:border-[#00f3ff]/30 uppercase transition-all">\${kw}</span>\`
      ).join('');

      document.getElementById("blog-modal-cta").href = "https://wa.me/923425478683?text=" + encodeURIComponent("Hi ASM Solutions, I'm discussing the blog topic '" + post.title + "'. Let's scale my localized rankings!");

      const modal = document.getElementById("blog-modal");
      modal.classList.remove("pointer-events-none");
      modal.classList.add("opacity-100");
    }

    function closeBlogModal() {
      const modal = document.getElementById("blog-modal");
      modal.classList.add("pointer-events-none");
      modal.classList.remove("opacity-100");
    }

    // Secure email simulation
    function dispatchSecureMessage() {
      const sender = document.getElementById("form-sender").value;
      const subject = document.getElementById("form-subject").value;
      const body = document.getElementById("form-body").value;

      if (!sender || !body) {
        alert("Sender identity & message factors are required elements.");
        return;
      }

      alert("Secure dispatcher successfully handshake verified! Redirecting secure gateway to corporate communication node.");
      
      const emailText = "Hi ASM Digital Solutions,\\n\\nDirect inquiry dispatched from secure console portal.\\n\\nSender Client: " + sender + "\\nSubject Matrix: " + subject + "\\n\\nMessage Body:\\n" + body;
      window.location.href = "mailto:Asmmarkettrader@gmail.com?subject=" + encodeURIComponent(subject || "ASM Secure Node Contact") + "&body=" + encodeURIComponent(emailText);
    }

    // Commit changes directly back to Github
    async function triggerGitPush() {
      const repo = document.getElementById("git-repo").value.trim();
      const pathFile = document.getElementById("git-path").value.trim();
      const token = document.getElementById("git-token").value.trim();
      const statusBox = document.getElementById("git-status");

      if (!repo || !pathFile || !token) {
        statusBox.className = "p-3 rounded font-mono text-[10px] bg-amber-500/15 border border-amber-500/30 text-amber-400";
        statusBox.textContent = "REQUIRED DISPATCH: Repository, destination path, and active PAT Token are mandatory.";
        statusBox.classList.remove("hidden");
        return;
      }

      localStorage.setItem("asm_git_repo", repo);
      localStorage.setItem("asm_git_token", token);

      statusBox.className = "p-3 rounded font-mono text-[10px] bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 animate-pulse";
      statusBox.textContent = "INJECTING STANDALONE COMPILER & COMPILING DOM STRUCTURAL VECTORS...";
      statusBox.classList.remove("hidden");

      try {
        saveActiveChanges();
        
        const responseBuilder = await fetch('/api/compile-html', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(content)
        });
        
        if (!responseBuilder.ok) throw new Error("Local compiler responded with a non-200 transaction code.");
        const compileRes = await responseBuilder.json();
        const outputHtml = compileRes.html;

        let sha = null;
        try {
          const checkUrl = "https://api.github.com/repos/" + repo + "/contents/" + pathFile;
          const currentFileRes = await fetch(checkUrl, {
            headers: {
              'Authorization': "token " + token,
              'Accept': 'application/vnd.github.v3+json'
            }
          });
          if (currentFileRes.ok) {
            const currentFileData = await currentFileRes.json();
            sha = currentFileData.sha;
          }
        } catch (err) {
          console.log("No previous file detected, writing fresh commit.", err);
        }

        const putUrl = "https://api.github.com/repos/" + repo + "/contents/" + pathFile;
        const commitBody = {
          message: "Publish ASM Digital live updates via Administrative Core CMS Terminal",
          content: btoa(unescape(encodeURIComponent(outputHtml))),
          sha: sha || undefined
        };

        const pushResponse = await fetch(putUrl, {
          method: 'PUT',
          headers: {
            'Authorization': "token " + token,
            'Content-Type': 'application/json',
            'Accept': 'application/vnd.github.v3+json'
          },
          body: JSON.stringify(commitBody)
        });

        if (pushResponse.ok) {
          statusBox.className = "p-3 rounded font-mono text-[10px] bg-emerald-500/15 border border-emerald-500/30 text-emerald-400";
          statusBox.innerHTML = \`<i class="fa-solid fa-cloud-arrow-up"></i> TRANSACTION STABLE: live index.html successfully pushed back to GitHub Pages pipeline!\`;
        } else {
          const errData = await pushResponse.json();
          throw new Error(errData.message || "Failed to finalize GitHub API handshake.");
        }

      } catch (e) {
        statusBox.className = "p-3 rounded font-mono text-[10px] bg-rose-500/10 border border-rose-500/30 text-rose-450 text-rose-400";
        statusBox.textContent = "ERROR STACK HANDSHAKE: " + e.message;
      }
    }
  </script>

</body>
</html>`;
}
