import { useScrollReveal } from '../../hooks/useScrollReveal'
import { Search, MessageCircle, Rocket } from 'lucide-react'
import type { LucideIcon } from 'lucide-react'

const steps: {
  number: string
  title: string
  description: string
  icon: LucideIcon
}[] = [
  {
    number: '01',
    title: 'Choose Your Service',
    description:
      'Browse our extensive catalog of premium services. Use the search bar or category filters to find exactly what you need.',
    icon: Search,
  },
  {
    number: '02',
    title: 'Place Your Order',
    description:
      'Click the Order button on any service. You\'ll be redirected to WhatsApp where our team will process your request instantly.',
    icon: MessageCircle,
  },
  {
    number: '03',
    title: 'Watch It Grow',
    description:
      'Sit back and relax. Our automated systems deliver your order with super quick delivery times. Track progress in real-time.',
    icon: Rocket,
  },
]

export default function HowItWorks() {
  const sectionRef = useScrollReveal<HTMLDivElement>({ stagger: 150 })

  return (
    <section className="section-padding bg-card-navy/50">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12" data-reveal>
          <h2 className="font-orbitron font-bold text-2xl sm:text-3xl md:text-4xl text-pure-white">
            How It Works
          </h2>
        </div>

        <div
          ref={sectionRef}
          className="grid grid-cols-1 md:grid-cols-3 gap-8"
        >
          {steps.map((step) => (
            <div
              key={step.number}
              data-reveal
              className="glass-card glow-border p-10 text-center transition-all duration-400 hover:-translate-y-2"
            >
              <div className="font-orbitron font-bold text-5xl text-neon-cyan/20 mb-4">
                {step.number}
              </div>
              <step.icon
                size={40}
                className="text-neon-cyan mx-auto mb-5"
              />
              <h3 className="font-orbitron font-semibold text-lg text-pure-white mb-3">
                {step.title}
              </h3>
              <p className="text-muted-gray text-sm leading-relaxed">
                {step.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
