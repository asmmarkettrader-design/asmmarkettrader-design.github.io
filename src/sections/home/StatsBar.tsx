import { useCounter } from '../../hooks/useCounter'

const stats = [
  { end: 100, suffix: '%', label: 'Client Satisfaction', prefix: '' },
  { end: 500, suffix: 'K+', label: 'Social Media Growth', prefix: '' },
  { end: 5.0, suffix: '', label: 'Average Rating', prefix: '', decimals: 1 },
  { end: 24, suffix: '/7', label: 'Live Support', prefix: '' },
]

function StatItem({
  end,
  suffix,
  prefix,
  label,
  decimals = 0,
  delay = 0,
}: {
  end: number
  suffix: string
  prefix: string
  label: string
  decimals?: number
  delay?: number
}) {
  const { ref, display } = useCounter({ end, suffix, prefix, decimals, duration: 2000 })

  return (
    <div ref={ref} className="text-center" data-reveal style={{ transitionDelay: `${delay}ms` }}>
      <div className="font-orbitron font-bold text-3xl sm:text-4xl text-neon-cyan">
        {display}
      </div>
      <div className="mt-2 font-syne text-xs sm:text-sm uppercase tracking-widest text-muted-gray">
        {label}
      </div>
    </div>
  )
}

export default function StatsBar() {
  return (
    <section className="bg-card-navy border-y border-neon-cyan/10 py-16 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-8 md:gap-4">
        {stats.map((stat, index) => (
          <StatItem
            key={stat.label}
            end={stat.end}
            suffix={stat.suffix}
            prefix={stat.prefix}
            label={stat.label}
            decimals={stat.decimals}
            delay={index * 200}
          />
        ))}
      </div>
    </section>
  )
}
