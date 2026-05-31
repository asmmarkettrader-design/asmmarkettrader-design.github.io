import { useState } from 'react'
import { Search } from 'lucide-react'
import { useCounter } from '../../hooks/useCounter'
import ParticleCanvas from '../../components/ParticleCanvas'

const stats = [
  { end: 50, suffix: 'K+', label: 'Happy Clients' },
  { end: 2, suffix: 'M+', label: 'Completed Orders' },
  { end: 24, suffix: '/7', label: 'Fastest Support' },
  { end: 5, suffix: '%', label: 'Deposit Bonus' },
]

interface SMMHeroProps {
  onSearch: (query: string) => void
}

export default function SMMHero({ onSearch }: SMMHeroProps) {
  const [searchValue, setSearchValue] = useState('')

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value
    setSearchValue(value)
    onSearch(value)
  }

  return (
    <section className="relative min-h-[60vh] flex items-center justify-center overflow-hidden pt-[72px]">
      {/* Background */}
      <div className="absolute inset-0 bg-deep-navy grid-pattern" />
      <ParticleCanvas />

      {/* Radial glow */}
      <div
        className="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] rounded-full pointer-events-none"
        style={{
          background: 'radial-gradient(circle, rgba(0, 212, 255, 0.06) 0%, transparent 70%)',
        }}
      />

      <div className="relative z-10 text-center max-w-[900px] mx-auto px-4 sm:px-6 py-16">
        {/* Badge */}
        <div className="inline-flex items-center gap-2 bg-neon-cyan/10 border border-neon-cyan/30 rounded-full px-4 py-1.5 mb-6">
          <span className="text-neon-cyan text-xs font-syne">#1 SMM Panel</span>
        </div>

        <h1 className="font-orbitron font-bold text-2xl sm:text-3xl md:text-4xl lg:text-[40px] text-pure-white leading-tight">
          World's Most Trusted
          <span className="block text-neon-cyan">Premium SMM Panel</span>
        </h1>

        <p className="mt-4 text-light-cyan text-base max-w-[700px] mx-auto leading-relaxed">
          Providing Top-Tier Social Media Services. Buy real followers, likes & views instantly. Our team of experts ensures all services are of the cheapest and beyond quality standards.
        </p>

        {/* Stats */}
        <div className="flex flex-wrap items-center justify-center gap-6 sm:gap-10 mt-10">
          {stats.map((stat) => (
            <StatItem
              key={stat.label}
              end={stat.end}
              suffix={stat.suffix}
              label={stat.label}
            />
          ))}
        </div>

        {/* Search Bar */}
        <div className="mt-10 max-w-[600px] mx-auto relative">
          <Search
            size={20}
            className="absolute left-5 top-1/2 -translate-y-1/2 text-muted-gray"
          />
          <input
            type="text"
            value={searchValue}
            onChange={handleSearch}
            placeholder="Search services..."
            className="w-full bg-card-navy/80 border border-neon-cyan/15 rounded-full py-4 pl-14 pr-6 text-light-cyan placeholder-muted-gray outline-none focus:border-neon-cyan/40 transition-colors"
          />
        </div>
      </div>
    </section>
  )
}

function StatItem({
  end,
  suffix,
  label,
}: {
  end: number
  suffix: string
  label: string
}) {
  const { ref, display } = useCounter({ end, suffix, duration: 2000 })

  return (
    <div ref={ref} className="text-center">
      <div className="font-orbitron font-bold text-2xl sm:text-3xl text-neon-cyan">
        {display}
      </div>
      <div className="mt-1 text-muted-gray text-xs uppercase tracking-wider">
        {label}
      </div>
    </div>
  )
}
