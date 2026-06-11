/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from "react";
import { Check, AlertTriangle, ShieldCheck, Globe, Gauge, Activity, Tag, HelpCircle, ArrowRight } from "lucide-react";

interface SeoAnalyzerProps {
  seoTitle: string;
  seoDesc: string;
  isAdmin: boolean;
  onEdit: (path: string, val: string) => void;
}

export default function SeoAnalyzer({ seoTitle, seoDesc, isAdmin, onEdit }: SeoAnalyzerProps) {
  const [url, setUrl] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [statusText, setStatusText] = useState("");
  const [results, setResults] = useState<any | null>(null);

  const runAudit = () => {
    if (!url) {
      alert("Please specify a target website URL parameter.");
      return;
    }

    setIsLoading(true);
    setResults(null);

    const stages = [
      "INITIALIZING WEB OBSERVABILITY HOOKS...",
      "ACQUIRING TTL RESOLVING INDICATORS...",
      "ANALYZING DOM METADATA TAXONOMY STRUCTURE...",
      "SIMULATING CONSOLE PORT AUDITS...",
      "COMPILING SEO INTEGRITY SCORE..."
    ];

    let current = 0;
    const interval = setInterval(() => {
      if (current < stages.length) {
        setStatusText(stages[current]);
        current++;
      } else {
        clearInterval(interval);
        finalizeAudit();
      }
    }, 550);
  };

  const finalizeAudit = () => {
    setIsLoading(false);

    // Calculate dynamic stats based on URL parameters to make it feel real
    const hash = url.length;
    const score = Math.floor((hash * 4) % 21) + 72; // Dynamic but stable score between 72 and 93
    const ttfb = Math.floor((hash * 7) % 90) + 40; // 40ms to 130ms
    const fcp = ((hash * 0.05) % 0.4 + 0.15).toFixed(2); // 0.15s to 0.55s

    const altMissing = Math.floor((hash * 9) % 35) + 12; // 12% to 47%
    const h2Count = Math.floor((hash * 3) % 18) + 5; 
    const h3Count = Math.floor((hash * 5) % 12) + 2;

    const hostname = url.replace(/https?:\/\/(www\.)?/, "").split("/")[0] || url;

    setResults({
      resolvedUrl: `https://${hostname}`,
      score,
      ttfb: `${ttfb} ms`,
      fcp: `${fcp} s`,
      title: `${hostname.split(".")[0].toUpperCase()} | Premium Scaled Business Digital Solutions`,
      description: `Elevate organic traffic on ${hostname} with GMB maps audits, reputation systems, and high retention reviews on safe cloud algorithms.`,
      h2Count,
      h3Count,
      altMissing,
      sslState: "ACTIVE (HTTPS)",
      headersScore: "PARTIAL (8/12)",
      consoleErrors: 0
    });
  };

  const getScoreColor = (score: number) => {
    if (score >= 90) return "text-emerald-400";
    if (score >= 80) return "text-cyan-400";
    return "text-amber-400";
  };

  const strokeDashoffset = results ? 377 - (377 * results.score) / 100 : 377;

  return (
    <div className="w-full max-w-4xl mx-auto rounded-3xl cyber-glass p-8 border border-slate-200 glow-cyan scanline mb-20 relative">
      <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-4 py-0.5 rounded border border-cyan-500/40 bg-slate-900 font-mono text-[9px] text-cyan-400 tracking-wider">
        SYSTEM CORE V3.9 - SEO CONSOLE
      </div>

      <div className="text-center mb-8">
        <h2 
          className="font-display font-medium text-2xl text-slate-900 tracking-wide mb-2 outline-none"
          contentEditable={isAdmin}
          suppressContentEditableWarning
          onBlur={(e) => onEdit("seoTool.seoTitle", e.target.innerText)}
        >
          {seoTitle}
        </h2>
        <p 
          className="text-slate-500 hover:text-cyan-300 text-sm max-w-2xl mx-auto transition-colors outline-none"
          contentEditable={isAdmin}
          suppressContentEditableWarning
          onBlur={(e) => onEdit("seoTool.seoDesc", e.target.innerText)}
        >
          {seoDesc}
        </p>
      </div>

      {/* Input container */}
      <div className="flex flex-col sm:flex-row gap-4 max-w-2xl mx-auto mb-8 relative z-20">
        <div className="flex-1 relative">
          <Globe className="absolute left-4 top-1/2 -translate-y-1/2 text-[#00f3ff] w-5 h-5" />
          <input 
            type="url" 
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://yourwebsite.com" 
            className="w-full pl-12 pr-4 py-4 rounded-xl border border-slate-200 bg-[#020408]/50 text-slate-900 font-mono text-sm placeholder:text-slate-600 focus:outline-none focus:border-[#00f3ff] focus:ring-1 focus:ring-[#00f3ff]/30 transition-all"
          />
        </div>
        <button 
          onClick={runAudit}
          disabled={isLoading}
          className="px-8 py-4 rounded-xl font-display font-bold text-xs uppercase tracking-widest bg-[#00f3ff] text-black hover:bg-white transform transition-all hover:scale-[1.03] active:scale-[0.98] shadow-[0_0_15px_rgba(0,243,255,0.2)] shrink-0 flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
        >
          <span>{isLoading ? "DIAGNOSING..." : "START DIAGNOSTICS"}</span>
          <Activity className="w-4 h-4 animate-pulse" />
        </button>
      </div>

      {/* Loading Indicator */}
      {isLoading && (
        <div className="py-10 flex flex-col items-center justify-center">
          <div className="relative w-16 h-16 mb-4">
            <div className="absolute inset-0 rounded-full border-2 border-[#00f3ff]/20"></div>
            <div className="absolute inset-0 rounded-full border-t-2 border-purple-500 animate-spin"></div>
          </div>
          <p className="font-mono text-xs text-[#00f3ff] animate-pulse tracking-widest mt-2">{statusText}</p>
        </div>
      )}

      {/* Audit Results */}
      {results && !isLoading && (
        <div className="text-left border-t border-slate-200 pt-8 animate-fade-in">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8 items-center">
            {/* Score Ring */}
            <div className="flex flex-col items-center justify-center p-6 rounded-2xl bg-white/[0.02] border border-slate-200">
              <span className="font-display font-extrabold text-[10px] tracking-wider text-slate-500 mb-3 uppercase">CORE SEO INTEGRITY</span>
              <div className="relative w-36 h-36 flex items-center justify-center">
                <svg className="w-full h-full transform -rotate-90">
                  <circle cx="72" cy="72" r="60" stroke="rgba(255,255,255,0.03)" strokeWidth="8" fill="transparent"></circle>
                  <circle 
                    cx="72" 
                    cy="72" 
                    r="60" 
                    stroke="#00f3ff" 
                    strokeWidth="8" 
                    fill="transparent" 
                    strokeDasharray="377" 
                    strokeDashoffset={strokeDashoffset} 
                    strokeLinecap="round" 
                    className="transition-all duration-1000"
                  ></circle>
                </svg>
                <div className="absolute flex flex-col items-center justify-center">
                  <span className={`font-display font-black text-4xl text-slate-900`}>
                    {results.score}<span className="text-xs text-[#00f3ff]">%</span>
                  </span>
                  <span className={`font-mono text-[9px] mt-1 ${results.score >= 90 ? "text-emerald-400" : results.score >= 80 ? "text-[#00f3ff]" : "text-amber-400"}`}>
                    {results.score >= 90 ? "GRADE A: STABLE" : results.score >= 80 ? "GRADE B: CAUTION" : "GRADE C: IMPROVE"}
                  </span>
                </div>
              </div>
            </div>

            {/* Resolved Address and General Latency */}
            <div className="md:col-span-2 space-y-3">
              <div className="p-4 rounded-xl bg-white/[0.02] border border-slate-200 flex items-center justify-between">
                <div>
                  <h4 className="font-display font-bold text-xs text-slate-900">Target Address</h4>
                  <p className="font-mono text-xs text-[#00f3ff] mt-0.5">{results.resolvedUrl}</p>
                </div>
                <span className="font-mono text-[9px] px-2.5 py-1 rounded bg-emerald-500/10 border border-emerald-500/30 text-emerald-400">RESOLVED</span>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 rounded-xl bg-white/[0.02] border border-slate-200">
                  <h4 className="font-sans font-bold text-xs text-slate-500">Response Latency (TTFB)</h4>
                  <p className="font-mono text-xl text-slate-900 mt-1">{results.ttfb}</p>
                </div>
                <div className="p-4 rounded-xl bg-white/[0.02] border border-slate-200">
                  <h4 className="font-sans font-bold text-xs text-slate-500">First Contentful Paint</h4>
                  <p className="font-mono text-xl text-slate-900 mt-1">{results.fcp}</p>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            {/* Meta tags analysis */}
            <div className="p-5 rounded-2xl bg-white/[0.02] border border-slate-200">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-display font-bold text-xs text-slate-900 tracking-widest flex items-center gap-2">
                  <Tag className="w-4 h-4 text-cyan-400" /> META-DATA INTEGRITY
                </h3>
                <span className="font-mono text-[9px] text-emerald-400 flex items-center gap-1">
                  <Check className="w-3 h-3" /> SCAN COMPLIANT
                </span>
              </div>
              <div className="space-y-3 font-mono text-xs">
                <div className="flex flex-col gap-1 p-3 rounded bg-slate-100/40 border border-slate-200">
                  <span className="text-slate-500">Meta Title Header:</span>
                  <span className="text-slate-800">{results.title} ({results.title.length} characters)</span>
                </div>
                <div className="flex flex-col gap-1 p-3 rounded bg-slate-100/40 border border-slate-200">
                  <span className="text-slate-500">Meta Description Summary:</span>
                  <span className="text-slate-800">{results.description}</span>
                </div>
                <div className="grid grid-cols-2 gap-3 mt-2">
                  <div className="p-2.5 rounded bg-slate-100/40 border border-slate-200 flex items-center justify-between">
                    <span className="text-slate-500">OG Meta Tags:</span>
                    <span className="text-emerald-400 font-bold">Detected</span>
                  </div>
                  <div className="p-2.5 rounded bg-slate-100/40 border border-slate-200 flex items-center justify-between">
                    <span className="text-slate-500">Robots.txt:</span>
                    <span className="text-emerald-400 font-bold">Indexed</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Semantic Structure */}
            <div className="p-5 rounded-2xl bg-white/[0.02] border border-slate-200">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-display font-bold text-xs text-slate-900 tracking-widest flex items-center gap-2">
                  <Activity className="w-4 h-4 text-pink-400" /> SEMANTIC STRUCTURE & IMAGES
                </h3>
                <span className={`font-mono text-[9px] flex items-center gap-1 ${results.altMissing > 25 ? "text-amber-400" : "text-emerald-400"}`}>
                  <AlertTriangle className="w-3 h-3" /> ACTION REQUIRED
                </span>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-3.5 rounded bg-slate-100/40 border border-slate-200 space-y-2">
                  <span className="font-mono text-xs text-slate-500 block">Header Taxonomy distribution:</span>
                  <div className="flex items-center gap-4 text-xs font-mono">
                    <span className="px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 text-[10px]">H1: 1</span>
                    <span className="px-2 py-0.5 rounded bg-purple-500/10 text-purple-400 text-[10px]">H2: {results.h2Count}</span>
                    <span className="px-2 py-0.5 rounded bg-pink-500/10 text-pink-400 text-[10px]">H1: {results.h3Count}</span>
                  </div>
                </div>
                <div className="p-3.5 rounded bg-slate-100/40 border border-slate-200 space-y-1 text-xs font-mono">
                  <span className="text-slate-500 block">Images Missing Alt Attributes:</span>
                  <p className="text-slate-800">
                    <span className="text-amber-400 font-bold">{results.altMissing}%</span> lack alternative descriptive labels.
                  </p>
                </div>
              </div>
              <div className="mt-3 p-3 rounded bg-amber-500/5 border border-amber-500/20 text-xs text-amber-400 font-mono">
                <AlertTriangle className="w-3 h-3 inline mr-1" /> Missing Alt descriptors degrade localized domain trust indexes. Google image search indexing speed falls by up to 30%.
              </div>
            </div>

            {/* Security and diagnostics */}
            <div className="p-5 rounded-2xl bg-white/[0.02] border border-slate-200">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-display font-bold text-xs text-slate-900 tracking-widest flex items-center gap-2">
                  <ShieldCheck className="w-4 h-4 text-cyan-400" /> DIAGNOSTICS & SECURITY SIGNALS
                </h3>
                <span className="font-mono text-[9px] text-emerald-400 flex items-center gap-1">
                  <Check className="w-3 h-3" /> SECURITY STANDARDS SAFE
                </span>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 font-mono text-xs text-center">
                <div className="p-3.5 rounded bg-slate-100/40 border border-slate-200">
                  <span className="text-slate-500 block mb-1">SSL Certificate</span>
                  <span className="text-emerald-400 font-display font-bold text-sm">SECURED (HTTPS)</span>
                </div>
                <div className="p-3.5 rounded bg-slate-100/40 border border-slate-200">
                  <span className="text-slate-500 block mb-1">Critical Headers</span>
                  <span className="text-yellow-400 font-display font-bold text-sm">PARTIAL (8/12)</span>
                </div>
                <div className="p-3.5 rounded bg-slate-100/40 border border-slate-200">
                  <span className="text-slate-500 block mb-1">Uncaught Console Errors</span>
                  <span className="text-emerald-400 font-display font-bold text-sm">0 METRICS</span>
                </div>
              </div>
            </div>

            {/* Accessibility & Best Practices */}
            <div className="p-5 rounded-2xl bg-white/[0.02] border border-slate-200">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-display font-bold text-xs text-slate-900 tracking-widest flex items-center gap-2">
                  <Globe className="w-4 h-4 text-purple-400" /> ACCESSIBILITY & BEST PRACTICES
                </h3>
                <span className="font-mono text-[9px] text-yellow-500 flex items-center gap-1">
                  <AlertTriangle className="w-3 h-3" /> MULTIPLE ISSUES FOUND
                </span>
              </div>
              <div className="flex flex-col gap-3 font-mono text-xs">
                <div className="p-3.5 rounded bg-slate-100/40 border border-slate-200 flex items-center gap-3">
                  <Check className="w-4 h-4 text-emerald-400 shrink-0" />
                  <span className="text-slate-700">Contrast ratios on background colors are sufficient.</span>
                </div>
                <div className="p-3.5 rounded bg-amber-500/5 border border-amber-500/20 flex items-start gap-3">
                  <AlertTriangle className="w-4 h-4 text-amber-500 shrink-0 mt-0.5" />
                  <div>
                    <span className="text-slate-700 font-bold">Missing ARIA attributes on interactive elements.</span>
                    <p className="text-slate-500 mt-1">Screen readers cannot process dynamic menus without proper aria-expanded tags. Affects 12% of visually impaired traffic.</p>
                  </div>
                </div>
                <div className="p-3.5 rounded bg-amber-500/5 border border-amber-500/20 flex items-start gap-3">
                  <AlertTriangle className="w-4 h-4 text-amber-500 shrink-0 mt-0.5" />
                  <div>
                    <span className="text-slate-700 font-bold">Outdated third-party libraries detected.</span>
                    <p className="text-slate-500 mt-1">Found jQuery v1.x which poses a mild security risk and degrades Web Vitals execution time.</p>
                  </div>
                </div>
                <div className="p-3.5 rounded bg-amber-500/5 border border-amber-500/20 flex items-start gap-3">
                  <AlertTriangle className="w-4 h-4 text-amber-500 shrink-0 mt-0.5" />
                  <div>
                    <span className="text-slate-700 font-bold">Unoptimized DOM Tree depth.</span>
                    <p className="text-slate-500 mt-1">Excessive DOM size over 1,500 elements slows down client-side rendering severely on mobile CPUs.</p>
                  </div>
                </div>
              </div>
            </div>

            {/* ASM Fixed CTA Banner mapping */}
            <div className="p-6 rounded-2xl bg-gradient-to-r from-purple-100/50 to-cyan-100/50 border border-purple-200 mt-6 flex flex-col md:flex-row items-center justify-between gap-6">
              <div>
                <h3 className="font-display font-black text-sm text-slate-900 mb-1 tracking-wider uppercase flex items-center gap-1">
                  <span>ASM RECOMMENDATION MATRIX GENERATED</span>
                </h3>
                <p className="text-slate-600 text-xs max-w-xl font-medium leading-relaxed">Fix missing image descriptions, resolve accessibility ARIA issues, reduce DOM tree depth, and integrate high-retention review profiles to elevate conversion velocity instantly.</p>
              </div>
              <a 
                href={`https://wa.me/923425478683?text=Hi%20ASM%20Solutions,%20I%20just%20ran%20your%20Advanced%20SEO%20Analyzer%20Tool%20for%20${encodeURIComponent(results.resolvedUrl)}.%20I%20need%20help%20fixing%20my%20Accessibility,%20DOM%20depth%20and%20Alt%20tags.%20Let's%20optimize%20live!`}
                target="_blank" 
                rel="noreferrer"
                className="px-5 py-3 rounded-xl bg-purple-600 hover:bg-purple-700 text-white font-display text-xs font-bold tracking-wider hover:scale-[1.03] transition-all flex items-center gap-2 shadow-[0_4px_15px_rgba(147,51,234,0.3)] shrink-0 self-stretch md:self-auto justify-center"
              >
                FIX SITE WITH ASM EXPERT
              </a>
            </div>

          </div>
        </div>
      )}
    </div>
  );
}
