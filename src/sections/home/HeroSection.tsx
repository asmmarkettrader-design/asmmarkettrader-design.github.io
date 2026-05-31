import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import ParticleCanvas from '../../components/ParticleCanvas'

export default function HeroSection() {
  const [line1, setLine1] = useState('')
  const [line2, setLine2] = useState('')
  const [showSub, setShowSub] = useState(false)
  const [showButtons, setShowButtons] = useState(false)

  const text1 = 'Your All-in-One'
  const text2 = 'Business Growth Partner'

  useEffect(() => {
    let index1 = 0
    const interval1 = setInterval(() => {
      if (index1 < text1.length) {
        setLine1(text1.slice(0, index1 + 1))
        index1++
      } else {
        clearInterval(interval1)
        // Start second line
        let index2 = 0
        setTimeout(() => {
          const interval2 = setInterval(() => {
            if (index2 < text2.length) {
              setLine2(text2.slice(0, index2 + 1))
              index2++
            } else {
              clearInterval(interval2)
              setTimeout(() => setShowSub(true), 200)
              setTimeout(() => setShowButtons(true), 600)
            }
          }, 80)
        }, 200)
      }
    }, 80)

    return () => clearInterval(interval1)
  }, [])

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 bg-deep-navy grid-pattern" />
      <ParticleCanvas />

      {/* Radial glow */}
      <div
        className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full pointer-events-none"
        style={{
          background: 'radial-gradient(circle, rgba(0, 212, 255, 0.08) 0%, transparent 70%)',
        }}
      />

      {/* Content */}
      <div className="relative z-10 text-center max-w-[900px] mx-auto px-4 sm:px-6">
        <h1 className="font-orbitron font-bold text-3xl sm:text-4xl md:text-5xl lg:text-[40px] text-pure-white leading-tight">
          <span className="block min-h-[1.2em]">{line1}</span>
          <span className="block text-neon-cyan min-h-[1.2em] mt-2">{line2}</span>
          <span className="inline-block w-[3px] h-[1em] bg-neon-cyan ml-1 animate-pulse align-middle" />
        </h1>

        <p
          className={`mt-6 text-light-cyan text-base sm:text-lg max-w-[700px] mx-auto leading-relaxed transition-all duration-800 ${
            showSub ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
          }`}
        >
          Struggling to get sales or appearing on the second page of Google? We don't just provide reviews; we build your entire digital presence.
        </p>

        <div
          className={`mt-10 flex flex-col sm:flex-row items-center justify-center gap-4 transition-all duration-600 ${
            showButtons ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-5'
          }`}
        >
          <a href="/#contact" className="btn-primary">
            Get Free Audit
          </a>
          <Link to="/smm-panel" className="btn-outline">
            View SMM Panel
          </Link>
        </div>
      </div>

      {/* Floating badge */}
      <div className="hidden lg:block absolute bottom-[15%] right-[10%] z-10">
        <div className="glass-card-strong px-6 py-4 flex items-center gap-3">
          <span className="w-2.5 h-2.5 rounded-full bg-neon-cyan animate-pulse-glow" />
          <span className="font-syne text-sm text-light-cyan">24/7 Support</span>
        </div>
      </div>

      {/* Scroll indicator */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 z-10 flex flex-col items-center gap-2 opacity-60">
        <span className="text-xs text-muted-gray uppercase tracking-widest">Scroll</span>
        <div className="w-5 h-8 rounded-full border-2 border-neon-cyan/40 flex justify-center pt-1.5">
          <div className="w-1 h-2 bg-neon-cyan rounded-full animate-bounce" />
        </div>
      </div>
    </section>
  )
}
