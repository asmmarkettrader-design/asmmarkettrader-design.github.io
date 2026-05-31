import { useScrollReveal } from '../../hooks/useScrollReveal'
import { Star, CreditCard, Zap } from 'lucide-react'
import type { LucideIcon } from 'lucide-react'

const features: {
  icon: LucideIcon
  title: string
  description: string
}[] = [
  {
    icon: Star,
    title: 'Awesome Quality',
    description:
      'The quality of SMM services on our panel is fantastic. Every service is tested and verified for maximum reliability.',
  },
  {
    icon: CreditCard,
    title: 'Various Payment Systems',
    description:
      'A great variety of payment options including Easypaisa, JazzCash, and international methods to add funds to your account.',
  },
  {
    icon: Zap,
    title: 'Super Quick Delivery',
    description:
      'You will be surprised at the speed of our order delivery. Most orders start within minutes and complete in record time.',
  },
]

export default function SMMFeatures() {
  const sectionRef = useScrollReveal<HTMLDivElement>({ stagger: 100 })

  return (
    <section className="py-20 md:py-24 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-deep-navy to-electric-blue/3">
      <div className="max-w-7xl mx-auto">
        <div
          ref={sectionRef}
          className="grid grid-cols-1 md:grid-cols-3 gap-6"
        >
          {features.map((feature) => (
            <div
              key={feature.title}
              data-reveal
              className="glass-card glow-border p-8 transition-all duration-400 hover:-translate-y-2"
            >
              <feature.icon size={40} className="text-neon-cyan mb-5" />
              <h4 className="font-orbitron font-semibold text-lg text-pure-white mb-3">
                {feature.title}
              </h4>
              <p className="text-muted-gray text-sm leading-relaxed">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
