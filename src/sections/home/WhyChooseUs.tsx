import { useScrollReveal } from '../../hooks/useScrollReveal'
import { Cpu, ShieldCheck, TrendingUp, Clock } from 'lucide-react'
import type { LucideIcon } from 'lucide-react'

const reasons: {
  icon: LucideIcon
  title: string
  description: string
}[] = [
  {
    icon: Cpu,
    title: 'Technical Expertise',
    description:
      'We are experts in Software, Networking, and Automation. Our technical depth ensures every solution is built on solid engineering.',
  },
  {
    icon: ShieldCheck,
    title: 'Safe & Secure',
    description:
      'We use professional tools to ensure your accounts stay safe. Your data security and account integrity are our top priorities.',
  },
  {
    icon: TrendingUp,
    title: 'Result Oriented',
    description:
      'We focus on ROI (Return on Investment), not just clicks. Every strategy is measured by the revenue it generates for your business.',
  },
  {
    icon: Clock,
    title: '24/7 Uptime',
    description:
      'Round-the-clock monitoring and support. Our systems run 24/7 so your business never stops growing, even while you sleep.',
  },
]

export default function WhyChooseUs() {
  const sectionRef = useScrollReveal<HTMLDivElement>({ stagger: 100 })

  return (
    <section id="why-us" className="section-padding bg-card-navy/50">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12" data-reveal>
          <h2 className="font-orbitron font-bold text-2xl sm:text-3xl md:text-4xl text-pure-white">
            Why Choose ASM Digital Solutions?
          </h2>
        </div>

        <div
          ref={sectionRef}
          className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6"
        >
          {reasons.map((reason) => (
            <div
              key={reason.title}
              data-reveal
              className="glass-card glow-border p-8 text-center transition-all duration-400 hover:-translate-y-2"
            >
              <div className="w-20 h-20 rounded-full border-2 border-neon-cyan/30 flex items-center justify-center mx-auto animate-float">
                <reason.icon size={36} className="text-neon-cyan" />
              </div>
              <h4 className="font-orbitron font-semibold text-lg text-pure-white mt-5">
                {reason.title}
              </h4>
              <p className="text-muted-gray text-sm leading-relaxed mt-3">
                {reason.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
