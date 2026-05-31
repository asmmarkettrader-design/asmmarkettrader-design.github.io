import { useState, useMemo } from 'react'
import { useScrollReveal } from '../../hooks/useScrollReveal'
import { categories, smmServices } from '../../data/smmServicesData'

interface ServicesTableProps {
  searchQuery: string
}

export default function ServicesTable({ searchQuery }: ServicesTableProps) {
  const [activeCategory, setActiveCategory] = useState('All')
  const sectionRef = useScrollReveal<HTMLDivElement>({ stagger: 50 })

  const filteredServices = useMemo(() => {
    let filtered = smmServices

    if (activeCategory !== 'All') {
      filtered = filtered.filter((s) => s.category === activeCategory)
    }

    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase()
      filtered = filtered.filter((s) => s.name.toLowerCase().includes(q))
    }

    return filtered
  }, [activeCategory, searchQuery])

  const handleOrder = (serviceName: string, serviceId: string) => {
    const message = `Hi ASM Digital Solutions, I want to order ${serviceName} (ID: ${serviceId}). Please assist me.`
    const encoded = encodeURIComponent(message)
    window.open(`https://wa.me/923425478683?text=${encoded}`, '_blank')
  }

  return (
    <section className="section-padding bg-deep-navy" id="services-table">
      <div className="max-w-7xl mx-auto" ref={sectionRef}>
        {/* Category Filter */}
        <div data-reveal className="mb-8 overflow-x-auto pb-2">
          <div className="flex gap-2 min-w-max">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setActiveCategory(cat)}
                className={`px-4 py-2 rounded-full text-xs sm:text-sm font-syne font-medium whitespace-nowrap transition-all duration-200 border ${
                  activeCategory === cat
                    ? 'bg-neon-cyan text-deep-navy border-neon-cyan'
                    : 'bg-transparent text-muted-gray border-neon-cyan/15 hover:border-neon-cyan/40'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        {/* Services Table */}
        <div data-reveal className="overflow-x-auto">
          <table className="w-full min-w-[700px]">
            <thead>
              <tr className="bg-neon-cyan/10">
                <th className="text-left px-4 py-4 text-xs uppercase tracking-wider text-muted-gray font-syne font-medium w-16">
                  ID
                </th>
                <th className="text-left px-4 py-4 text-xs uppercase tracking-wider text-muted-gray font-syne font-medium">
                  Service
                </th>
                <th className="text-left px-4 py-4 text-xs uppercase tracking-wider text-muted-gray font-syne font-medium w-28">
                  Price
                </th>
                <th className="text-left px-4 py-4 text-xs uppercase tracking-wider text-muted-gray font-syne font-medium w-24 hidden sm:table-cell">
                  Min Order
                </th>
                <th className="text-left px-4 py-4 text-xs uppercase tracking-wider text-muted-gray font-syne font-medium w-24 hidden sm:table-cell">
                  Max Order
                </th>
                <th className="text-left px-4 py-4 text-xs uppercase tracking-wider text-muted-gray font-syne font-medium w-28 hidden md:table-cell">
                  Avg Time
                </th>
                <th className="text-right px-4 py-4 text-xs uppercase tracking-wider text-muted-gray font-syne font-medium w-24">
                  Action
                </th>
              </tr>
            </thead>
            <tbody>
              {filteredServices.length === 0 ? (
                <tr>
                  <td
                    colSpan={7}
                    className="text-center py-12 text-muted-gray font-syne"
                  >
                    No services found matching your criteria.
                  </td>
                </tr>
              ) : (
                filteredServices.map((service, index) => (
                  <tr
                    key={service.id}
                    className={`border-b border-neon-cyan/5 transition-colors hover:bg-neon-cyan/5 ${
                      index % 2 === 0 ? 'bg-transparent' : 'bg-card-navy/30'
                    }`}
                  >
                    <td className="px-4 py-4 text-muted-gray text-xs font-mono">
                      {service.id}
                    </td>
                    <td className="px-4 py-4">
                      <span
                        className="text-pure-white text-sm font-medium block truncate max-w-[300px] sm:max-w-[400px]"
                        title={service.name}
                      >
                        {service.name}
                      </span>
                    </td>
                    <td className="px-4 py-4">
                      <div className="font-orbitron font-bold text-neon-cyan text-sm">
                        ${service.markedPrice.toFixed(2)}
                      </div>
                      <div className="text-muted-gray text-[10px]">Per 1000</div>
                    </td>
                    <td className="px-4 py-4 text-light-cyan text-sm hidden sm:table-cell">
                      {service.minOrder.toLocaleString()}
                    </td>
                    <td className="px-4 py-4 text-light-cyan text-sm hidden sm:table-cell">
                      {service.maxOrder.toLocaleString()}
                    </td>
                    <td className="px-4 py-4 text-muted-gray text-sm hidden md:table-cell">
                      {service.avgTime}
                    </td>
                    <td className="px-4 py-4 text-right">
                      <button
                        onClick={() => handleOrder(service.name, service.id)}
                        className="bg-neon-cyan text-deep-navy font-orbitron font-semibold text-xs px-4 py-2 rounded-full hover:scale-105 hover:shadow-neon transition-all"
                      >
                        Order
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Results count */}
        <p className="text-muted-gray text-xs mt-4 text-center">
          Showing {filteredServices.length} of {smmServices.length} services
          {activeCategory !== 'All' && ` in ${activeCategory}`}
        </p>
      </div>
    </section>
  )
}
