/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useRef } from "react";
import { 
  Shield, 
  Terminal, 
  Check, 
  CheckCircle, 
  MessageSquare, 
  Mail, 
  Linkedin, 
  ExternalLink, 
  Star, 
  X, 
  Globe, 
  Activity, 
  FileText, 
  Sparkles, 
  Send,
  Loader,
  Laptop,
  CheckSquare,
  DollarSign,
  ArrowRight,
  ArrowLeft,
  Search,
  Tag,
  Copy,
  Code
} from "lucide-react";
import SeoAnalyzer from "./components/SeoAnalyzer";
import { initialSiteData } from "./data/defaultData";
import { SiteContent } from "./utils/staticGenerator";

export default function App() {
  const [content, setContent] = useState<SiteContent>(() => {
    const saved = localStorage.getItem("asm_cached_content");
    if (saved) {
      try {
        return JSON.parse(saved);
      } catch (e) {
        console.warn("Could not hydrate site cache", e);
      }
    }
    return initialSiteData;
  });

  const [isAdmin, setIsAdmin] = useState(false);
  const [showAdminModal, setShowAdminModal] = useState(false);
  const [passwordInput, setPasswordInput] = useState("");
  const [isAuthUnlocked, setIsAuthUnlocked] = useState(false);

  // GitHub deploy engine state
  const [gitRepo, setGitRepo] = useState(() => localStorage.getItem("asm_git_repo") || "");
  const [gitPath, setGitPath] = useState("index.html");
  const [gitToken, setGitToken] = useState(() => localStorage.getItem("asm_git_token") || "");
  const [gitStatus, setGitStatus] = useState<{ type: "success" | "error" | "loading" | null; message: string }>({ type: null, message: "" });

  // Navigation and active views
  const [activeServiceId, setActiveServiceId] = useState<number | null>(null);
  const [selectedBlogId, setSelectedBlogId] = useState<number | null>(null);

  // Blog Search and Filter states
  const [blogSearchQuery, setBlogSearchQuery] = useState("");
  const [selectedBlogTag, setSelectedBlogTag] = useState<string>("ALL");

  // Copied alert for technical schemas
  const [copiedSchemaId, setCopiedSchemaId] = useState<number | null>(null);

  // Secure message dispatch form
  const [formEmail, setFormEmail] = useState("");
  const [formSubject, setFormSubject] = useState("");
  const [formMessage, setFormMessage] = useState("");

  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  // Background particle net canvas logic
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animationId: number;
    let points: Array<{ x: number; y: number; vx: number; vy: number; r: number }> = [];
    const maxPoints = window.innerWidth < 768 ? 25 : 55;

    const initPoints = () => {
      points = [];
      for (let i = 0; i < maxPoints; i++) {
        points.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          vx: (Math.random() - 0.5) * 0.25,
          vy: (Math.random() - 0.5) * 0.25,
          r: Math.random() * 1.5 + 1
        });
      }
    };

    const handleResize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      initPoints();
    };

    window.addEventListener("resize", handleResize);
    handleResize();

    const drawPoints = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Lines
      for (let i = 0; i < points.length; i++) {
        const p1 = points[i];
        for (let j = i + 1; j < points.length; j++) {
          const p2 = points[j];
          const dist = Math.hypot(p1.x - p2.x, p1.y - p2.y);
          if (dist < 140) {
            ctx.beginPath();
            ctx.moveTo(p1.x, p1.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.strokeStyle = `rgba(14, 165, 233, ${(1 - dist / 140) * 0.15})`;
            ctx.lineWidth = 0.5;
            ctx.stroke();
          }
        }
      }

      // Nodes
      for (let i = 0; i < points.length; i++) {
        const p = points[i];
        p.x += p.vx;
        p.y += p.vy;

        if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
        if (p.y < 0 || p.y > canvas.height) p.vy *= -1;

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = i % 2 === 0 ? "rgba(14, 165, 233, 0.4)" : "rgba(168, 85, 247, 0.4)";
        ctx.fill();
      }

      animationId = requestAnimationFrame(drawPoints);
    };

    drawPoints();

    return () => {
      window.removeEventListener("resize", handleResize);
      cancelAnimationFrame(animationId);
    };
  }, []);

  // Save changes callback from any contenteditable element
  const handleFieldEdit = (path: string, val: string) => {
    setContent(prev => {
      const keys = path.split(".");
      const copy = { ...prev };
      
      let cursor: any = copy;
      for (let i = 0; i < keys.length - 1; i++) {
        cursor = cursor[keys[i]];
      }
      cursor[keys[keys.length - 1]] = val;

      localStorage.setItem("asm_cached_content", JSON.stringify(copy));
      return copy;
    });
  };

  // Authenticate Admin Pin Code logic
  const handleAuthPin = () => {
    if (passwordInput === "admin" || passwordInput === "Asmveo@2026") {
      setIsAuthUnlocked(true);
      setIsAdmin(true);
    } else {
      alert("Encryption authorization vector failed. Re-enter Pin Code.");
    }
  };

  // Log in out toggle controls
  const handleRevoke = () => {
    setIsAdmin(false);
    setIsAuthUnlocked(false);
    setPasswordInput("");
    setShowAdminModal(false);
  };

  // Dispatch secure email form
  const handleSecureDispatch = () => {
    if (!formEmail || !formMessage) {
      alert("Sender identity & message factors are required elements.");
      return;
    }

    alert("Secure dispatcher successfully verified! Launching secure email gateway.");
    const emailBody = `Hi ASM Digital Solutions,\n\nDirect inquiry dispatched from secure console portal.\n\nSender Client: ${formEmail}\nSubject Matrix: ${formSubject || "General Scales Consultation"}\n\nMessage Body:\n${formMessage}`;
    
    window.location.href = `mailto:Asmmarkettrader@gmail.com?subject=${encodeURIComponent(formSubject || "ASM Secure Node Contact")}&body=${encodeURIComponent(emailBody)}`;
  };

  // Remote GitHub pages deploy PUT handshake
  const handleGitDeploy = async () => {
    if (!gitRepo || !gitPath || !gitToken) {
      setGitStatus({
        type: "error",
        message: "REQUIRED DISPATCH: Repository, destination file path, and active PAT Token are mandatory."
      });
      return;
    }

    // Cache parameters
    localStorage.setItem("asm_git_repo", gitRepo);
    localStorage.setItem("asm_git_token", gitToken);

    setGitStatus({
      type: "loading",
      message: "INJECTING STANDALONE COMPILER & COMPILING DIRECT DOM STRUCTURAL VECTORS..."
    });

    try {
      const res = await fetch("/api/compile-html", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(content)
      });

      if (!res.ok) throw new Error("Local compiler responded with a non-200 transaction code.");
      const data = await res.json();
      const outputHtml = data.html;

      let sha: string | null = null;
      try {
        const checkUrl = `https://api.github.com/repos/${gitRepo}/contents/${gitPath}`;
        const currentFileRes = await fetch(checkUrl, {
          headers: {
            "Authorization": `token ${gitToken}`,
            "Accept": "application/vnd.github.v3+json"
          }
        });
        if (currentFileRes.ok) {
          const fileData = await currentFileRes.json();
          sha = fileData.sha;
        }
      } catch (err) {
        console.log("No previous repository files detected, creating fresh index.", err);
      }

      const putUrl = `https://api.github.com/repos/${gitRepo}/contents/${gitPath}`;
      const payload = {
        message: "Publish ASM Digital live updates via Administrative Core CMS Terminal",
        content: btoa(unescape(encodeURIComponent(outputHtml))),
        sha: sha || undefined
      };

      const pushResponse = await fetch(putUrl, {
        method: "PUT",
        headers: {
          "Authorization": `token ${gitToken}`,
          "Content-Type": "application/json",
          "Accept": "application/vnd.github.v3+json"
        },
        body: JSON.stringify(payload)
      });

      if (pushResponse.ok) {
        setGitStatus({
          type: "success",
          message: "TRANSACTION STABLE: index.html successfully pushed back to GitHub Pages pipeline!"
        });
      } else {
        const errJson = await pushResponse.json();
        throw new Error(errJson.message || "Failed to finalize GitHub API handshake.");
      }

    } catch (e: any) {
      setGitStatus({
        type: "error",
        message: "ERROR STACK HANDSHAKE: " + (e.message || "Unknown error")
      });
    }
  };

  const selectedBlog = content.blogs.find(b => b.id === selectedBlogId);
  const activeService = content.services.find(s => s.id === activeServiceId);

  // Extract all unique blog tags
  const allBlogTags = ["ALL", ...Array.from(new Set(content.blogs.flatMap(b => b.keywords)))];

  // Filtering blogs based on Search input and selection Tag
  const filteredBlogs = content.blogs.filter(blog => {
    const matchesQuery = 
      blog.title.toLowerCase().includes(blogSearchQuery.toLowerCase()) || 
      blog.excerpt.toLowerCase().includes(blogSearchQuery.toLowerCase()) || 
      blog.content.toLowerCase().includes(blogSearchQuery.toLowerCase());
    
    const matchesTag = selectedBlogTag === "ALL" || blog.keywords.includes(selectedBlogTag);
    return matchesQuery && matchesTag;
  });

  // Unique service specific JSON-LD Schema blueprints
  const getServiceSchema = (id: number, title: string) => {
    switch (id) {
      case 1:
        return `{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "ASM Digital GBP Optimization Hub",
  "url": "https://asmveo.com/services/gmb-maps",
  "telephone": "${content.contact.phone}",
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
}`;
      case 2:
        return `{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "${title}",
  "brand": {
    "@type": "Brand",
    "name": "ASM Digital Solutions"
  },
  "review": {
    "@type": "Review",
    "reviewRating": {
      "@type": "Rating",
      "ratingValue": "5",
      "bestRating": "5"
    },
    "author": {
      "@type": "Person",
      "name": "Marcus Dupont"
    }
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "reviewCount": "1480"
  }
}`;
      case 3:
        return `{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "ASM High-Performance static core compiler",
  "operatingSystem": "All",
  "applicationCategory": "BusinessApplication",
  "offers": {
    "@type": "Offer",
    "price": "349.00",
    "priceCurrency": "USD"
  }
}`;
      default:
        return `{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "${title}",
  "provider": {
    "@type": "LocalBusiness",
    "name": "ASM Digital Solutions",
    "url": "https://asmveo.com"
  },
  "areaServed": ["US", "UK", "FR", "DE", "AE"]
}`;
    }
  };

  const copySchemaToClipboard = (schemaText: string, id: number) => {
    navigator.clipboard.writeText(schemaText);
    setCopiedSchemaId(id);
    setTimeout(() => setCopiedSchemaId(null), 2000);
  };

  return (
    <div className="relative min-h-screen font-sans antialiased text-slate-800 grid-bg overflow-x-hidden pt-1">
      
      {/* Subtle Grid Net Canvas Background */}
      <canvas ref={canvasRef} className="fixed inset-0 pointer-events-none z-0 opacity-30"></canvas>

      {/* Floating Soft Ambient Lights */}
      <div className="absolute top-[-10%] left-[-5%] w-[500px] h-[500px] bg-cyan-500/5 rounded-full blur-[140px] pointer-events-none z-0 orb-float-1"></div>
      <div className="absolute bottom-[-15%] right-[-5%] w-[500px] h-[500px] bg-purple-500/5 rounded-full blur-[140px] pointer-events-none z-0 orb-float-2"></div>

      {/* Primary Sticky Command Bar Header */}
      <header className="sticky top-0 z-50 w-full h-18 flex items-center justify-between px-8 border-b border-slate-200 backdrop-blur-lg bg-white/80 pointer-events-auto">
        <div className="w-full max-w-7xl mx-auto flex items-center justify-between">
          <a href="#" onClick={() => { setActiveServiceId(null); setSelectedBlogId(null); }} className="flex items-center gap-3">
            <div className="relative w-9 h-9 rounded bg-gradient-to-br from-cyan-400 to-purple-500 flex items-center justify-center font-display font-medium text-black text-sm tracking-widest shadow-lg">
              ASM
            </div>
            <div className="flex flex-col">
              <span className="font-display font-extrabold text-base tracking-widest text-slate-900 leading-none">ASM DIGITAL</span>
              <span className="text-[9px] font-mono tracking-widest text-[#00f3ff] leading-none mt-1 uppercase">SEO AUDIT & SCALE PLATFORM</span>
            </div>
          </a>

          <nav className="hidden md:flex items-center gap-8 font-display text-[11px] font-semibold tracking-widest text-slate-350">
            <button onClick={() => { setActiveServiceId(null); }} className="hover:text-slate-900 transition-colors uppercase">SEO ANALYZER</button>
            <a href="#services" onClick={() => { setActiveServiceId(null); }} className="hover:text-slate-900 transition-colors uppercase">SERVICES</a>
            <a href="#reviews" onClick={() => { setActiveServiceId(null); }} className="hover:text-slate-900 transition-colors uppercase">RATINGS</a>
            <a href="#blog" onClick={() => { setActiveServiceId(null); }} className="hover:text-slate-900 transition-colors uppercase">RESOURCES</a>
            <a href="#contact" className="hover:text-slate-900 transition-colors uppercase">COMMUNICATE</a>
          </nav>

          <div className="flex items-center gap-4">
            <button 
              onClick={() => setShowAdminModal(true)}
              className="flex items-center gap-2 px-3.5 py-2 rounded-xl border border-slate-200 hover:border-[#00f3ff]/45 hover:bg-[#00f3ff]/5 text-slate-900/90 hover:text-slate-900 transition-all font-mono text-[10px] tracking-wider cursor-pointer"
            >
              <Terminal className="w-3.5 h-3.5 text-[#00f3ff]" />
              <span>{isAdmin ? "ADMIN CONTROL" : "CONSOLE LOGIN"}</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Container Core */}
      <main className="relative z-10 max-w-7xl mx-auto px-6 py-12">
        
        {/* Router condition - if a service page is active, show the details instead of landing page */}
        {activeService ? (
          <div className="animate-fade-in space-y-12 pb-20">
            <button 
              onClick={() => { setActiveServiceId(null); window.scrollTo({ top: 300, behavior: "smooth" }); }}
              className="px-5 py-2.5 rounded-full border border-slate-200 hover:border-[#00f3ff]/50 bg-white/50 hover:bg-[#00f3ff]/5 transition-all font-display text-[10px] text-[#00f3ff] font-bold tracking-widest flex items-center gap-2 cursor-pointer"
            >
              <ArrowLeft className="w-3.5 h-3.5" /> BACK TO SOLUTIONS HUB
            </button>

            {/* Service Headline */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
              <div className="lg:col-span-2 space-y-6">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-950/20 border border-cyan-400/30 text-cyan-400 font-mono text-[9px] uppercase tracking-widest">
                  {activeService.badge}
                </div>
                <h1 className="font-display font-black text-3xl sm:text-5xl text-slate-900 tracking-tight leading-tight">
                  {activeService.title}
                </h1>
                <p className="text-slate-600 text-sm md:text-base leading-relaxed font-normal">
                  {activeService.description}
                </p>

                <div className="p-6 rounded-2xl bg-white/60 border border-slate-200 space-y-4">
                  <h3 className="font-display font-bold text-xs text-slate-900 uppercase tracking-wider flex items-center gap-1.5 border-b border-slate-200 pb-3">
                    <CheckSquare className="w-4 h-4 text-[#00f3ff]" /> TECHNICAL ADVANTAGES & DEPLOYMENT CODES
                  </h3>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {activeService.features.map((feat, i) => (
                      <div key={i} className="flex items-start gap-2 text-xs font-normal text-slate-450">
                        <Check className="w-4 h-4 text-emerald-405 shrink-0 mt-0.5" />
                        <span>{feat}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Localized Territory Rankings Description Panel */}
                <div className="p-6 rounded-2xl bg-white/40 border border-slate-200 space-y-4">
                  <h3 className="font-display font-bold text-xs text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
                    <Globe className="w-4 h-4 text-purple-400" /> LOCALIZED SEO & REGIONAL TARGETING
                  </h3>
                  <p className="text-slate-450 text-xs leading-relaxed font-normal">
                    This agency system targets high-intent queries globally, securing elite maps positions in UK, USA, Germany, France, and UAE. Dynamic crawl schema tags enable indexing bots to rank your brand above local competitors safely.
                  </p>
                  <div className="flex flex-wrap gap-2 text-[10px] font-mono">
                    <span className="px-2 py-1 rounded bg-slate-100 text-cyan-400">UK Target Area (London, Manchester)</span>
                    <span className="px-2 py-1 rounded bg-slate-100 text-cyan-400">USA Target Area (California, Texas, NY)</span>
                    <span className="px-2 py-1 rounded bg-slate-100 text-cyan-400">Gulf Target Area (Dubai UAE, Qatar)</span>
                    <span className="px-2 py-1 rounded bg-slate-100 text-cyan-400">Europe Zone (Germany, France, Italy)</span>
                  </div>
                </div>
              </div>

              {/* Sidebar Controls with Lighthouse score aggregation & code Schema */}
              <div className="space-y-6">
                {/* 100% Score card */}
                <div className="p-6 rounded-3xl cyber-glass border border-slate-200 flex flex-col items-center text-center">
                  <h3 className="font-display font-extrabold text-[10px] text-slate-500 tracking-widest uppercase mb-4">Lighthouse Audit Grade</h3>
                  
                  {/* Score Matrix Grid */}
                  <div className="grid grid-cols-2 gap-4 w-full mb-6">
                    <div className="flex flex-col items-center bg-slate-100/35 p-3 rounded-2xl border border-slate-200">
                      <div className="font-display font-black text-emerald-400 text-xl">100</div>
                      <span className="text-[8px] font-mono text-slate-500 uppercase mt-1">Performance</span>
                    </div>
                    <div className="flex flex-col items-center bg-slate-100/35 p-3 rounded-2xl border border-slate-200">
                      <div className="font-display font-black text-emerald-400 text-xl">100</div>
                      <span className="text-[8px] font-mono text-slate-500 uppercase mt-1">Accessibility</span>
                    </div>
                    <div className="flex flex-col items-center bg-slate-100/35 p-3 rounded-2xl border border-slate-200">
                      <div className="font-display font-black text-emerald-400 text-xl">100</div>
                      <span className="text-[8px] font-mono text-slate-500 uppercase mt-1">Best Practice</span>
                    </div>
                    <div className="flex flex-col items-center bg-slate-100/35 p-3 rounded-2xl border border-slate-200">
                      <div className="font-display font-black text-emerald-400 text-xl">100</div>
                      <span className="text-[8px] font-mono text-slate-500 uppercase mt-1">SEO Target</span>
                    </div>
                  </div>

                  <p className="text-slate-450 text-[11px] leading-relaxed mb-4 font-normal">
                    This solution represents a 100/100 Core Web Vitals audit rating. Perfect TTFB parameters, responsive Alt layouts, and schema structures.
                  </p>
                </div>

                {/* Structured Schema output card */}
                <div className="p-5 rounded-3xl bg-slate-50/80 border border-slate-200 space-y-3">
                  <div className="flex items-center justify-between border-b border-slate-200 pb-2.5">
                    <span className="font-mono text-[9px] text-slate-500 tracking-widest uppercase flex items-center gap-1">
                      <Code className="w-3.5 h-3.5 text-cyan-400" /> JSON-LD Schema
                    </span>
                    <button 
                      onClick={() => copySchemaToClipboard(getServiceSchema(activeService.id, activeService.title), activeService.id)}
                      className="text-xs text-[#00f3ff] hover:text-slate-900 transition-colors cursor-pointer flex items-center gap-1 font-mono text-[9px]"
                    >
                      <span>{copiedSchemaId === activeService.id ? "COPIED" : "COPY CODE"}</span>
                    </button>
                  </div>
                  <pre className="font-mono text-[9px] text-slate-500 bg-slate-100/50 p-3 rounded-xl overflow-x-auto max-h-[140px]">
                    {getServiceSchema(activeService.id, activeService.title)}
                  </pre>
                </div>

                {/* CTA Action WhatsApp Card */}
                <div className="p-6 rounded-3xl bg-gradient-to-br from-cyan-950/20 to-purple-950/20 border border-cyan-500/20 space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="font-mono text-[9px] text-rose-400 uppercase tracking-widest font-black">RATE ENVELOPE</span>
                    <span className="font-display font-extrabold text-slate-900 text-sm">{activeService.price}</span>
                  </div>
                  <a 
                    href={`https://wa.me/923425478683?text=${encodeURIComponent(activeService.whatsAppText)}`}
                    target="_blank" 
                    rel="noreferrer"
                    className="w-full py-4 rounded-xl bg-[#00f3ff] hover:bg-white text-black font-display text-xs font-black tracking-widest transition-all flex items-center justify-center gap-2 shadow-[0_4px_15px_rgba(0,243,255,0.15)] select-none"
                  >
                    DEPLOY RESOURCE VIA WHATSAPP
                  </a>
                </div>
              </div>
            </div>

            {/* Simulated target page list indicator */}
            <div className="border-t border-slate-200 pt-12">
              <h3 className="font-display font-black text-xl text-slate-900 mb-6 uppercase">OTHER STRATEGIC SOLVING VEHICLES</h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
                {content.services.filter(s => s.id !== activeServiceId).slice(0, 4).map(serv => (
                  <button 
                    key={serv.id}
                    onClick={() => { setActiveServiceId(serv.id); window.scrollTo({ top: 0, behavior: "smooth" }); }}
                    className="p-5 rounded-2xl bg-white/60 border border-slate-200 hover:border-[#00f3ff]/40 text-left transition-all cursor-pointer group flex flex-col justify-between"
                  >
                    <span className="font-mono text-[8px] text-slate-500 uppercase tracking-wider">{serv.badge}</span>
                    <h4 className="font-display font-bold text-xs text-slate-900 uppercase group-hover:text-[#00f3ff] transition-colors mt-2">{serv.title}</h4>
                  </button>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <div className="animate-fade-in space-y-24">
            {/* Landing Hero Area */}
            <section id="hero" className="text-center pt-8">
              <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-cyan-400/20 bg-cyan-950/10 mb-8 font-mono text-[9px] text-[#00f3ff] tracking-widest uppercase">
                <span className="w-1.5 h-1.5 rounded-full bg-[#00f3ff] animate-pulse"></span>
                <span 
                  className="outline-none"
                  contentEditable={isAdmin}
                  suppressContentEditableWarning
                  onBlur={(e) => handleFieldEdit("hero.badge", e.target.innerText)}
                >
                  {content.hero.badge}
                </span>
              </div>
              
              <h1 
                className="font-display font-black text-3xl sm:text-5xl lg:text-6xl text-slate-900 tracking-tight leading-none mb-6 max-w-5xl mx-auto outline-none uppercase"
                contentEditable={isAdmin}
                suppressContentEditableWarning
                onBlur={(e) => handleFieldEdit("hero.title", e.target.innerText)}
              >
                {content.hero.title}
              </h1>
              
              <p 
                className="text-slate-600 text-base md:text-lg max-w-3xl mx-auto mb-12 font-normal leading-relaxed outline-none"
                contentEditable={isAdmin}
                suppressContentEditableWarning
                onBlur={(e) => handleFieldEdit("hero.description", e.target.innerText)}
              >
                {content.hero.description}
              </p>

              {/* Connected Core SEO Analyzer Tool */}
              <div id="seo-analyzer-mount">
                <SeoAnalyzer 
                  seoTitle={content.seoTool.seoTitle}
                  seoDesc={content.seoTool.seoDesc}
                  isAdmin={isAdmin}
                  onEdit={handleFieldEdit}
                />
              </div>
            </section>

            {/* Interactive Grid of Services - clicking a service redirects to multi-page detail layout */}
            <section id="services" className="relative scroll-mt-24">
              <div className="text-center mb-16">
                <h2 className="font-display font-black text-2xl sm:text-4xl text-slate-900 tracking-tight mb-4">
                  ASM STRATEGIC SOLUTIONS
                </h2>
                <p className="text-slate-500 text-xs sm:text-sm max-w-2xl mx-auto font-normal">
                  Click on any agency path to open its dedicated technical review page, JSON-LD Schema structures, real-time meta metrics, and Lighthouse audit scorecards.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {content.services.map((service, index) => {
                  const isEven = index % 2 === 0;
                  const borderGlow = isEven ? "hover:border-[#00f3ff]/45" : "hover:border-purple-500/45";
                  const accentColor = isEven ? "text-[#00f3ff]" : "text-purple-400";
                  const bgGradient = isEven ? "from-[#00f3ff]/5" : "from-purple-500/10";

                  return (
                    <div 
                      key={service.id}
                      className={`rounded-3xl cyber-glass p-8 border border-slate-200 flex flex-col justify-between hover:scale-[1.015] transform transition-all group overflow-hidden relative ${borderGlow}`}
                    >
                      <div className="absolute top-0 right-0 w-24 h-24 bg-gradient-to-bl from-white/[0.02] to-transparent pointer-events-none group-hover:scale-125 transition-all"></div>
                      
                      <div>
                        {service.image && (
                          <div className="rounded-xl overflow-hidden mb-4 border border-slate-200 aspect-video relative group-hover:shadow-[0_4px_15px_rgba(0,0,0,0.05)] transition-all">
                            <img src={service.image} alt={service.title} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                          </div>
                        )}
                        <div className="flex items-center justify-between mb-4">
                          <span className={`font-mono text-[9px] uppercase font-bold ${accentColor} tracking-widest`}>
                            {service.badge}
                          </span>
                          <span className="text-[10px] font-mono text-emerald-400 flex items-center gap-1 bg-emerald-950/20 px-2.5 py-1 rounded border border-emerald-500/20">
                            Lighthouse Score: 100%
                          </span>
                        </div>

                        <h3 className="font-display font-extrabold text-base sm:text-lg text-slate-900 mb-2 group-hover:text-[#00f3ff] transition-colors leading-snug">
                          {service.title}
                        </h3>
                        
                        <p className="text-slate-600 text-xs font-normal leading-relaxed mb-6">
                          {service.description.slice(0, 140)}...
                        </p>
                      </div>

                      <div className="space-y-4">
                        <div className="p-3.5 rounded-xl bg-slate-100/40 border border-slate-200 flex items-center justify-between">
                          <span className="font-mono text-[9px] text-slate-500 uppercase">Pricing Rate</span>
                          <span className="font-display font-black text-rose-400 text-xs flex items-center">
                            <DollarSign className="w-3.5 h-3.5" /> {service.price}
                          </span>
                        </div>

                        <div className="grid grid-cols-2 gap-2">
                          <button 
                            onClick={() => { setActiveServiceId(service.id); window.scrollTo({ top: 0, behavior: "smooth" }); }}
                            className="py-3 rounded-lg border border-slate-200 hover:border-[#00f3ff]/50 bg-white/60 text-slate-900 font-display text-[9px] font-bold tracking-widest transition-all cursor-pointer text-center"
                          >
                            MORE CODES & METRICS
                          </button>
                          <a 
                            href={`https://wa.me/923425478683?text=${encodeURIComponent(service.whatsAppText)}`}
                            target="_blank" 
                            rel="noreferrer"
                            className="py-3 rounded-lg bg-[#00f3ff] hover:bg-white text-black font-display text-[9px] font-black tracking-widest transition-all text-center"
                          >
                            ORDER
                          </a>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </section>

            {/* Global Review Authority */}
            <section id="reviews" className="scroll-mt-24">
              <div className="rounded-3xl cyber-glass p-8 md:p-12 border border-slate-200">
                
                <div className="flex flex-col md:flex-row items-center justify-between border-b border-slate-200 pb-8 mb-8 gap-6 text-center md:text-left">
                  <div>
                    <div className="flex items-center justify-center md:justify-start gap-2 mb-2">
                      <span className="text-slate-900 font-display font-black text-lg tracking-wider">TRUSTPILOT RATINGS</span>
                      <span className="text-emerald-400 text-xs font-bold flex items-center gap-1 uppercase">
                        <CheckSquare className="w-4 h-4" /> VERIFIED DEPLOYMENTS
                      </span>
                    </div>
                    <p className="text-slate-500 text-[10px] font-mono tracking-wider uppercase">
                      Geo-Targeted safe citations across major global markets
                    </p>
                  </div>

                  <div className="flex flex-col items-center md:items-end">
                    <div className="flex items-center gap-2 mb-1 bg-yellow-500/10 px-4 py-1.5 rounded-full border border-yellow-500/20">
                      <span className="text-yellow-600 text-sm font-black">4.9</span>
                      <div className="flex gap-0.5 text-yellow-500">
                        {Array(5).fill(0).map((_, i) => (
                          <Star key={i} className="w-3.5 h-3.5 fill-yellow-400 stroke-none text-yellow-400" />
                        ))}
                      </div>
                    </div>
                    <span className="text-slate-500 text-[8px] font-mono uppercase tracking-widest">VALIDATED THROUGH 1,480 SECTOR TRANSIT AUDITS</span>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {content.reviews.map(rev => (
                    <div 
                      key={rev.id}
                      className="p-6 rounded-2xl bg-white/40 border border-slate-200 hover:border-emerald-500/30 transition-all flex flex-col justify-between"
                    >
                      <div>
                        <div className="flex items-center justify-between mb-4">
                          <div className="flex items-center gap-3">
                            <div className="w-9 h-9 rounded-full bg-slate-100 border border-slate-200 flex items-center justify-center font-display font-black text-slate-900 text-xs">
                              {rev.name.split(" ").map(n => n[0]).join("")}
                            </div>
                            <div>
                              <h4 className="text-slate-900 font-sans font-bold text-xs">{rev.name}</h4>
                              <p className="text-slate-500 text-[9px] font-mono uppercase">{rev.role} | {rev.company}</p>
                            </div>
                          </div>
                          <div className="flex flex-col items-end gap-1">
                            <span className="text-slate-400 text-[8px] font-bold tracking-wider uppercase font-mono">
                              {["Trustpilot", "Google", "Clutch"][rev.id % 3]} verified
                            </span>
                            <div className="flex items-center gap-1 p-1 bg-yellow-50 rounded border border-yellow-100">
                              <span className="text-yellow-600 text-[9px] font-mono font-bold leading-none">{rev.rating}.0</span>
                              <div className="flex gap-0.2 text-yellow-500">
                                {Array(rev.rating).fill(0).map((_, i) => (
                                  <Star key={i} className="w-2.5 h-2.5 fill-yellow-400 text-yellow-500 stroke-none" />
                                ))}
                              </div>
                            </div>
                          </div>
                        </div>
                        <p className="text-slate-600 text-xs leading-relaxed font-normal italic mb-4">
                          "{rev.content}"
                        </p>
                      </div>
                      <div className="flex items-center justify-between font-mono text-[9px] mt-2 text-slate-500 border-t border-slate-200 pt-3">
                        <span className="flex items-center gap-1 text-slate-450">
                          <Shield className="w-3 h-3 text-emerald-400 shrink-0" /> Verified Retention Proof
                        </span>
                        <span className="flex items-center gap-1.5 uppercase font-bold text-slate-500">
                          <span className="px-1.5 py-0.5 bg-slate-100 text-slate-600 rounded text-[8px] font-mono">{rev.countryCode}</span> {rev.country}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </section>

            {/* Custom 25 Blog articles Hub with powerful search and filters */}
            <section id="blog" className="scroll-mt-24">
              <div className="flex flex-col md:flex-row items-start md:items-end justify-between gap-4 mb-10">
                <div className="text-left">
                  <h2 className="font-display font-black text-2xl sm:text-3xl text-slate-900 tracking-tight uppercase">
                    GLOBAL SEARCH DOMINANCE BLUEPRINTS
                  </h2>
                  <p className="text-slate-450 text-xs font-normal mt-1.5">
                    Strategic blueprints containing optimized terms and custom keywords to target high-competition UK, USA, European, and Gulf regions.
                  </p>
                </div>

                {/* Filter and tag selector buttons */}
                <div className="flex flex-wrap gap-1.5 font-mono text-[9px]">
                  {allBlogTags.slice(0, 5).map(tag => (
                    <button 
                      key={tag}
                      onClick={() => setSelectedBlogTag(tag)}
                      className={`px-3 py-1.5 rounded-full border transition-all cursor-pointer uppercase font-bold ${
                        selectedBlogTag === tag 
                          ? "bg-[#00f3ff] text-black border-[#00f3ff]" 
                          : "border-slate-200 bg-white/60 hover:border-slate-200 text-slate-500 hover:text-slate-900"
                      }`}
                    >
                      {tag}
                    </button>
                  ))}
                </div>
              </div>

              {/* Live search input bar */}
              <div className="w-full max-w-xl mb-10 relative">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 w-4 h-4" />
                <input 
                  type="text" 
                  value={blogSearchQuery}
                  onChange={(e) => setBlogSearchQuery(e.target.value)}
                  placeholder="Query titles, excerpts, or localized keywords (e.g. asmveo.com, Trustpilot...)..." 
                  className="w-full pl-11 pr-4 py-3 rounded-xl border border-slate-200 bg-white/40 text-xs text-slate-900 placeholder:text-slate-500 focus:outline-none focus:border-[#00f3ff] transition-all"
                />
              </div>

              {/* Grid of highly relevant filter result blogs (25 blogs capacity) */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {filteredBlogs.map(post => (
                  <article 
                    key={post.id}
                    className="rounded-3xl cyber-glass p-6 border border-slate-200 flex flex-col justify-between hover:border-[#00f3ff]/30 transition-all group"
                  >
                    <div>
                      <div className="flex items-center justify-between font-mono text-[8px] text-[#00f3ff] mb-4 uppercase">
                        <span>{post.date}</span>
                        <span>{post.readTime}</span>
                      </div>
                      
                      <h3 className="font-display font-bold text-sm sm:text-base text-slate-900 mb-2 group-hover:text-[#00f3ff] transition-colors leading-snug">
                        {post.title}
                      </h3>
                      
                      <p className="text-slate-600 text-xs font-normal leading-relaxed mb-6 line-clamp-3">
                        {post.excerpt}
                      </p>
                    </div>

                    <div>
                      <div className="flex flex-wrap gap-1 mb-5">
                        {post.keywords.map((kw, i) => (
                          <span key={i} className="px-2 py-0.5 rounded bg-white/[0.02] border border-slate-200 text-[7.5px] font-mono text-slate-500 uppercase cursor-default">
                            {kw}
                          </span>
                        ))}
                      </div>

                      <button 
                        onClick={() => setSelectedBlogId(post.id)}
                        className="text-[#00f3ff] hover:text-slate-900 font-display font-bold text-[10px] tracking-wider flex items-center gap-1 group-hover:translate-x-1 transition-transform cursor-pointer"
                      >
                        READ DEEP STUDY <ArrowRight className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </article>
                ))}

                {filteredBlogs.length === 0 && (
                  <div className="col-span-full py-12 text-center text-slate-500 font-mono text-xs">
                    No blueprints detected matching the filtered key query.
                  </div>
                )}
              </div>
            </section>
          </div>
        )}

        {/* Contact section configured with authentic digital elements */}
        <section id="contact" className="mt-24 scroll-mt-24">
          <div className="rounded-3xl cyber-glass p-8 md:p-12 border border-slate-200 relative">
            <div className="absolute top-0 right-10 px-4 py-0.5 rounded-b border border-[#00f3ff]/20 bg-slate-900 font-mono text-[8px] text-[#00f3ff] tracking-widest uppercase">
              Encrypted Channel Node
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
              <div className="text-left space-y-6">
                <h2 className="font-display font-black text-2xl sm:text-4xl text-slate-900 tracking-tight uppercase">
                  ESTABLISH DIRECT BUSINESS INQUIRY
                </h2>
                <p className="text-slate-350 text-xs sm:text-sm font-normal leading-relaxed">
                  Bypass standard conversion friction. Deploy optimized meta parameters, custom GMB listings, safe SEO ratings, and perfect 100% responsive architectures with the experts of ASM Digital Solutions today.
                </p>

                <div className="space-y-3.5">
                  {/* Whatsapp */}
                  <div className="flex items-center gap-4 p-4 rounded-xl bg-white/30 border border-slate-200 hover:border-emerald-500/30 transition-all">
                    <div className="w-9 h-9 rounded-lg bg-emerald-500/10 flex items-center justify-center text-emerald-400 shrink-0">
                      <MessageSquare className="w-4 h-4" />
                    </div>
                    <div>
                      <span className="font-mono text-[8px] text-slate-500 block uppercase">Direct Whatsapp Node</span>
                      <a href={`https://wa.me/923425478683`} target="_blank" rel="noreferrer" className="font-display font-bold text-xs text-slate-900 hover:text-[#00f3ff] transition-all">
                        {content.contact.phone}
                      </a>
                    </div>
                  </div>

                  {/* Email */}
                  <div className="flex items-center gap-4 p-4 rounded-xl bg-white/30 border border-slate-200 hover:border-purple-500/30 transition-all">
                    <div className="w-9 h-9 rounded-lg bg-purple-500/10 flex items-center justify-center text-purple-400 shrink-0">
                      <Mail className="w-4 h-4" />
                    </div>
                    <div>
                      <span className="font-mono text-[8px] text-slate-500 block uppercase">Encrypted Pipeline Address</span>
                      <a href={`mailto:${content.contact.email}`} className="font-mono text-xs text-slate-900 hover:text-purple-450 transition-all">
                        {content.contact.email}
                      </a>
                    </div>
                  </div>

                  {/* LinkedIn */}
                  <div className="flex items-center gap-4 p-4 rounded-xl bg-white/30 border border-slate-200 hover:border-[#00f3ff]/30 transition-all">
                    <div className="w-9 h-9 rounded-lg bg-blue-500/10 flex items-center justify-center text-blue-400 shrink-0">
                      <Linkedin className="w-4 h-4" />
                    </div>
                    <div>
                      <span className="font-mono text-[8px] text-slate-500 block uppercase">Corporate Strategic Anchor</span>
                      <a href={`https://${content.contact.linkedin}`} target="_blank" rel="noreferrer" className="font-mono text-xs text-slate-900 hover:text-[#00f3ff] transition-all inline-flex items-center gap-1">
                        {content.contact.linkedin} <ExternalLink className="w-3 w-3" />
                      </a>
                    </div>
                  </div>
                </div>
              </div>

              {/* Secure message dispatch web form */}
              <div className="p-6 rounded-2xl bg-slate-100/40 border border-slate-200 space-y-4">
                <h3 className="font-display font-bold text-xs text-slate-900 uppercase tracking-wider border-b border-slate-200 pb-3 flex items-center gap-1.5 font-bold">
                  <Shield className="w-4 h-4 text-[#00f3ff]" /> SECURE DESPATCH CONSOLE
                </h3>

                <div>
                  <label className="block font-mono text-[8px] text-slate-500 mb-1 uppercase">Your Email (Secure Identity)</label>
                  <input 
                    type="email" 
                    value={formEmail}
                    onChange={(e) => setFormEmail(e.target.value)}
                    placeholder="client@corp.com" 
                    className="w-full px-4 py-3 rounded-lg border border-slate-200 bg-slate-50 text-slate-900 font-mono text-xs focus:outline-none focus:border-[#00f3ff] focus:ring-1 focus:ring-[#00f3ff]/30 transition-all"
                  />
                </div>
                <div>
                  <label className="block font-mono text-[8px] text-slate-500 mb-1 uppercase">Target Category Target</label>
                  <input 
                    type="text" 
                    value={formSubject}
                    onChange={(e) => setFormSubject(e.target.value)}
                    placeholder="E.g. GMB Ranking Optimization / Trustpilot Drip Reviews..." 
                    className="w-full px-4 py-3 rounded-lg border border-slate-200 bg-slate-50 text-slate-900 font-mono text-xs focus:outline-none focus:border-[#00f3ff] focus:ring-1 focus:ring-[#00f3ff]/30 transition-all"
                  />
                </div>
                <div>
                  <label className="block font-mono text-[8px] text-slate-500 mb-1 uppercase">Inquiry Description</label>
                  <textarea 
                    rows={4} 
                    value={formMessage}
                    onChange={(e) => setFormMessage(e.target.value)}
                    placeholder="Enter details, target url, location maps coords, or service bundles needed..." 
                    className="w-full px-4 py-3 rounded-lg border border-slate-200 bg-slate-50 text-slate-900 font-mono text-xs focus:outline-none focus:border-[#00f3ff] focus:ring-1 focus:ring-[#00f3ff]/30 transition-all"
                  />
                </div>

                <button 
                  onClick={handleSecureDispatch}
                  className="w-full py-3.5 rounded-lg bg-[#00f3ff] hover:bg-white text-black font-display font-black text-xs tracking-widest transition-all shadow-[0_4px_15px_rgba(0,243,255,0.15)] cursor-pointer"
                >
                  DISPATCH CONSOLE MESSAGE
                </button>
              </div>
            </div>
          </div>
        </section>

      </main>

      {/* Top Companies Marquee */}
      <section className="border-t border-slate-200 py-10 bg-white relative z-20 overflow-hidden">
        <div className="text-center mb-6">
          <p className="font-display font-bold text-xs text-slate-500 tracking-widest uppercase">
            200+ Companies Worldwide Choose Our SEO Expertise
          </p>
        </div>
        <div className="marquee-container h-16 w-full flex items-center relative after:absolute after:inset-y-0 after:right-0 after:w-32 after:bg-gradient-to-l after:from-white after:to-transparent before:absolute before:inset-y-0 before:left-0 before:w-32 before:bg-gradient-to-r before:from-white before:to-transparent before:z-10 after:z-10">
          <div className="marquee-track flex items-center gap-16 px-8 text-slate-400">
             {/* Duplicate set for infinite loop */}
             {[...Array(2)].map((_, i) => (
              <React.Fragment key={i}>
                <div className="flex items-center gap-2 font-display font-black text-xl italic"><Globe className="w-6 h-6"/> NEXUS GLOBAL</div>
                <div className="flex items-center gap-2 font-display font-bold text-xl"><Activity className="w-6 h-6"/> VANGUARD TECH</div>
                <div className="flex items-center gap-2 font-sans font-bold text-xl"><Shield className="w-5 h-5"/> DUPONT STRUCTURAL</div>
                <div className="flex items-center gap-2 font-mono font-bold text-xl">STERLING<span className="font-light">HEMP</span></div>
                <div className="flex items-center gap-2 font-display font-black text-xl tracking-tighter">MÜLLER <span className="text-slate-300">AUTO</span></div>
                <div className="flex items-center gap-2 font-sans font-extrabold text-xl"><CheckCircle className="w-5 h-5"/> REACH DIGITAL</div>
                <div className="flex items-center gap-2 font-display font-bold text-xl">FINSERVE MX</div>
                <div className="flex items-center gap-2 font-mono font-medium text-xl border border-slate-300 px-3 border-dashed">ROSSI LOGISTICS</div>
              </React.Fragment>
             ))}
          </div>
        </div>
      </section>

      {/* footer bar */}
      <footer className="border-t border-slate-200 py-12 px-6 bg-slate-50 text-center relative z-20">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-6 mb-8 text-left">
          <div>
            <span className="font-display font-black text-base text-slate-900 tracking-widest">ASM DIGITAL SOLUTIONS</span>
            <p className="text-slate-500 text-[10px] mt-1 font-mono uppercase tracking-wider">ASM TRUSTED GLOBAL AUDITING SERVICES &copy; 2026. ALL METRICS SSL SECURED.</p>
          </div>
          <div className="flex items-center gap-4 text-slate-500 text-xs font-mono">
            <button onClick={() => { setActiveServiceId(null); window.scrollTo({ top: 300, behavior: "smooth" }); }} className="hover:text-cyan-400 transition-all uppercase">SEO CONSOLE</button>
            <span>&bull;</span>
            <a href="#services" onClick={() => { setActiveServiceId(null); }} className="hover:text-pink-400 transition-all uppercase">8 BUNDLES</a>
            <span>&bull;</span>
            <a href="#reviews" onClick={() => { setActiveServiceId(null); }} className="hover:text-cyan-400 transition-all uppercase">RATINGS</a>
          </div>
        </div>
        
        <div className="text-[9px] text-slate-600 max-w-4xl mx-auto font-mono leading-relaxed border-t border-slate-200 pt-6">
          DOMESTIC ORGANIC CHANNELS: "Buy Trustpilot Reviews USA", "Google Rating Services UK", "SEO Expert France", "Web Architect Italy", "Local GMB Optimization Germany", "Reputation Management Europe". All proprietary algorithms belong to asmveo.com. Encoded under strict security algorithms. Securely compiled on GITHUB PAGES vectors.
        </div>
      </footer>

      {/* Blog Article Reader Modal popup overlay */}
      {selectedBlog && (
        <div className="fixed inset-0 min-h-screen bg-slate-100/95 z-[101] flex items-center justify-center p-6 transition-all duration-300">
          <div className="w-full max-w-2xl p-8 rounded-3xl cyber-glass border border-[#00f3ff]/30 shadow-[#00f3ff]/5 relative max-h-[85vh] overflow-y-auto">
            <button 
              onClick={() => setSelectedBlogId(null)}
              className="absolute top-5 right-5 text-slate-500 hover:text-slate-900 transition-colors cursor-pointer"
            >
              <X className="w-6 h-6" />
            </button>

            <div className="flex items-center gap-2 font-mono text-[9px] text-[#00f3ff] uppercase tracking-widest mb-4">
              <span>{selectedBlog.date}</span> &bull; <span>{selectedBlog.readTime}</span>
            </div>

            <h2 className="font-display font-black text-xl sm:text-2xl text-slate-900 mb-6 border-b border-slate-200 pb-4 leading-snug">
              {selectedBlog.title}
            </h2>

            <div className="text-slate-350 text-xs sm:text-sm leading-relaxed font-sans space-y-4 font-normal mb-8">
              {selectedBlog.content.split("\\n\\n").map((par, i) => (
                <p key={i} className="mb-4">{par}</p>
              ))}
            </div>

            <div className="flex flex-wrap gap-2 mb-8">
              {selectedBlog.keywords.map((kw, i) => (
                <span key={i} className="px-2.5 py-1 rounded bg-slate-100 border border-slate-200 text-[10px] font-mono text-[#00f3ff] uppercase cursor-default">
                  {kw}
                </span>
              ))}
            </div>

            <div className="p-6 rounded-2xl bg-white/[0.02] border border-slate-200 flex items-center justify-between flex-col sm:flex-row gap-4">
              <div className="text-left">
                <h4 className="font-display font-extrabold text-xs text-slate-900">WANT TO DOMINATE THIS TOPIC LOCALLY?</h4>
                <p className="text-slate-500 text-[10px] mt-1 font-sans">Deploy these advanced algorithms inside your target domains safely with ASM Digital Solutions.</p>
              </div>
              <a 
                href={`https://wa.me/923425478683?text=Hi%20ASM%20Solutions,%20I'm%20discussing%2520the%2520topic%2520'${encodeURIComponent(selectedBlog.title)}'.%20Let's%20discuss%20improving%20my%20topical%2520rankings!`} 
                target="_blank" 
                rel="noreferrer"
                className="px-5 py-2.5 rounded-lg bg-[#00f3ff] hover:bg-white text-black font-display font-bold text-xs tracking-wider transition-all flex items-center gap-1 shrink-0"
              >
                CONSULTING SECURED <Mail className="w-4 h-4" />
              </a>
            </div>
          </div>
        </div>
      )}

      {/* Administrative CMS terminal overlay modal */}
      {showAdminModal && (
        <div className="fixed inset-0 min-h-screen bg-slate-100/90 z-[100] flex items-center justify-center p-6 animate-fade-in">
          <div className="w-full max-w-xl p-8 rounded-3xl cyber-glass border border-[#00f3ff]/30 shadow-[#00f3ff]/5 relative">
            <button 
              onClick={() => setShowAdminModal(false)}
              className="absolute top-5 right-5 text-slate-500 hover:text-slate-900 transition-colors cursor-pointer"
            >
              <X className="w-6 h-6" />
            </button>

            <div className="flex items-center gap-3 border-b border-slate-200 pb-4 mb-6">
              <div className="w-10 h-10 rounded-lg bg-purple-500/10 flex items-center justify-center text-purple-400">
                <Shield className="w-5 h-5" />
              </div>
              <div className="text-left">
                <h2 className="font-display font-black text-lg text-slate-900">ADMINISTRATIVE PORTAL</h2>
                <span className="font-mono text-[9px] text-purple-400/80 tracking-widest uppercase">ENCRYPTED CREDENTIAL VALIDATION</span>
              </div>
            </div>

            {!isAuthUnlocked ? (
              <div className="space-y-4">
                <p className="text-slate-500 text-xs text-left">This node allows structural modification across all pricing bands, titles, description frames, and articles. Authentication required.</p>
                <div>
                  <label className="block text-left font-mono text-[10px] text-slate-500 mb-1.5 uppercase">Encryption PIN Code Key</label>
                  <input 
                    type="password" 
                    value={passwordInput}
                    onChange={(e) => setPasswordInput(e.target.value)}
                    placeholder="•••••••••••••••••" 
                    className="w-full px-4 py-3.5 rounded-xl border border-slate-200 bg-slate-900 text-slate-900 font-mono text-sm focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500/30 transition-all"
                  />
                </div>
                <button 
                  onClick={handleAuthPin}
                  className="w-full py-4 rounded-xl font-display font-bold text-xs uppercase tracking-widest bg-purple-600 text-slate-900 hover:bg-white hover:text-black shadow-[0_4px_15px_rgba(147,51,234,0.3)] transition-all cursor-pointer"
                >
                  AUTHENTICATE CONSOLE
                </button>
              </div>
            ) : (
              <div className="space-y-6 text-left">
                <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20">
                  <p className="text-xs text-emerald-400 font-mono tracking-wider mb-2 flex items-center gap-1.5">
                    <CheckCircle className="w-4 h-4" /> CONSOLE ACCESS GRANTED: EDIT MODE LIVE!
                  </p>
                  <span className="text-[10px] text-slate-500">Headings, descriptions, and tag Badges are now contenteditable in real-time. Simply close this dialog and click directly on the text on-page to edit it. Modifying any text auto-caches it in active local memory.</span>
                </div>

                <div className="border-t border-slate-200 pt-4 space-y-4">
                  <h3 className="font-display font-bold text-xs text-slate-900 uppercase tracking-wider flex items-center gap-2">
                    <Globe className="w-4 h-4 text-[#00f3ff]" /> GitHub Pages Deploy Engine
                  </h3>
                  <p className="text-[10px] text-slate-500">Completely sync all modifications back to your live remote web branch! Builds a pristine static single file, autoconcatenates styling structures, strips edit states, and pushes live live via direct PUT API.</p>
                  
                  <div className="space-y-3">
                    <div>
                      <label className="block font-mono text-[9px] text-slate-500 mb-1 uppercase">GitHub Repository Name</label>
                      <input 
                        type="text" 
                        value={gitRepo}
                        onChange={(e) => setGitRepo(e.target.value)}
                        placeholder="your-username/repository-name" 
                        className="w-full px-3 py-2.5 rounded hover:border-[#00f3ff]/50 transition-all border border-slate-200 bg-slate-900 text-slate-900 font-mono text-xs focus:outline-none"
                      />
                    </div>
                    <div>
                      <label className="block font-mono text-[9px] text-slate-500 mb-1 uppercase">Target File Path</label>
                      <input 
                        type="text" 
                        value={gitPath}
                        onChange={(e) => setGitPath(e.target.value)}
                        placeholder="index.html" 
                        className="w-full px-3 py-2.5 rounded hover:border-[#00f3ff]/50 transition-all border border-slate-200 bg-slate-900 text-slate-900 font-mono text-xs focus:outline-none"
                      />
                    </div>
                    <div>
                      <label className="block font-mono text-[9px] text-slate-500 mb-1 uppercase">GitHub Personal Access Token (PAT)</label>
                      <input 
                        type="password" 
                        value={gitToken}
                        onChange={(e) => setGitToken(e.target.value)}
                        placeholder="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxx" 
                        className="w-full px-3 py-2.5 rounded hover:border-[#00f3ff]/50 transition-all border border-slate-200 bg-slate-900 text-slate-900 font-mono text-xs focus:outline-none"
                      />
                    </div>
                  </div>

                  <div className="flex gap-3 pt-2">
                    <button 
                      onClick={handleRevoke}
                      className="px-4 py-3 rounded-lg border border-slate-200 text-slate-500 hover:text-slate-900 transition-colors font-display text-xs font-bold leading-none cursor-pointer"
                    >
                      REVOKE ADMIN MODE
                    </button>
                    <button 
                      onClick={handleGitDeploy}
                      className="flex-1 py-3 rounded-lg bg-[#00f3ff] font-display font-bold text-xs text-black uppercase tracking-widest hover:bg-white transition-all flex items-center justify-center gap-2 cursor-pointer"
                    >
                      DEPLOY TO GITHUB LIVE
                    </button>
                  </div>
                  
                  {gitStatus.type && (
                    <div className={`p-3 rounded font-mono text-[10px] flex items-center gap-2 mt-4 border ${
                      gitStatus.type === "loading" ? "bg-cyan-500/10 border-cyan-500/20 text-[#00f3ff]" :
                      gitStatus.type === "success" ? "bg-emerald-500/15 border-emerald-500/30 text-emerald-400" :
                      "bg-rose-500/10 border-rose-500/30 text-rose-400"
                    }`}>
                      {gitStatus.type === "loading" && <Loader className="w-3.5 h-3.5 animate-spin shrink-0" />}
                      <span>{gitStatus.message}</span>
                    </div>
                  )}
                </div>
              </div>
            )}

          </div>
        </div>
      )}

    </div>
  );
}
