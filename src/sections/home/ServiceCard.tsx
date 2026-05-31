import { Link } from 'react-router-dom'
import { CheckCircle } from 'lucide-react'
import type { LucideIcon } from 'lucide-react'

interface PricingItem {
  qty: string
  price: string
  badge?: string
}

interface ServiceCardProps {
  icon: LucideIcon
  title: string
  description: string
  features: string[]
  image: string
  iconBorderColor: string
  pricing?: PricingItem[]
  monthlyPrice?: string
  priceNote?: string
  feePrice?: string
  customQuote?: boolean
  quoteColor?: string
  smmLink?: boolean
  index: number
}

export default function ServiceCard({
  icon: Icon,
  title,
  description,
  features,
  image,
  iconBorderColor,
  pricing,
  monthlyPrice,
  priceNote,
  feePrice,
  customQuote,
  quoteColor = 'bg-neon-cyan',
  smmLink,
  index,
}: ServiceCardProps) {
  const isReversed = index % 2 !== 0

  return (
    <div className="glass-card glow-border overflow-hidden transition-all duration-400 hover:-translate-y-2">
      <div
        className={`flex flex-col ${
          isReversed ? 'lg:flex-row-reverse' : 'lg:flex-row'
        }`}
      >
        {/* Content Column */}
        <div className="flex-1 p-6 sm:p-8 lg:p-10">
          {/* Icon */}
          <div
            className={`w-16 h-16 rounded-full border-2 ${iconBorderColor} flex items-center justify-center mb-6`}
          >
            <Icon size={32} className="text-neon-cyan" />
          </div>

          {/* Title */}
          <h3 className="font-orbitron font-semibold text-lg sm:text-xl md:text-2xl text-pure-white mb-4">
            {title}
          </h3>

          {/* Description */}
          <p className="text-muted-gray text-sm sm:text-base leading-relaxed mb-6">
            {description}
          </p>

          {/* Features Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-6">
            {features.map((feature) => (
              <div key={feature} className="flex items-start gap-2">
                <CheckCircle size={16} className="text-neon-cyan shrink-0 mt-0.5" />
                <span className="text-light-cyan text-sm">{feature}</span>
              </div>
            ))}
          </div>

          {/* Pricing Section */}
          {pricing && (
            <div className="mt-4">
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                {pricing.map((item) => (
                  <div
                    key={item.qty}
                    className={`relative bg-card-navy border rounded-lg p-3 text-center ${
                      item.badge
                        ? 'border-success-green/40'
                        : 'border-neon-cyan/15'
                    }`}
                  >
                    {item.badge && (
                      <span className="absolute -top-2 left-1/2 -translate-x-1/2 bg-success-green text-deep-navy text-[10px] font-orbitron font-bold px-2 py-0.5 rounded-full">
                        {item.badge}
                      </span>
                    )}
                    <div className="font-orbitron font-bold text-neon-cyan text-sm">
                      {item.price}
                    </div>
                    <div className="text-muted-gray text-xs mt-1">{item.qty}</div>
                  </div>
                ))}
              </div>
              <a
                href="https://wa.me/923425478683"
                target="_blank"
                rel="noopener noreferrer"
                className="btn-primary text-xs mt-4 inline-block"
              >
                Order Now
              </a>
            </div>
          )}

          {monthlyPrice && (
            <div className="mt-4">
              <div className="font-orbitron font-bold text-neon-cyan text-lg">
                {monthlyPrice}
              </div>
              {priceNote && (
                <p className="text-muted-gray text-sm mt-1">{priceNote}</p>
              )}
              <a
                href="/#contact"
                className="btn-primary text-xs mt-4 inline-block"
              >
                Get Quote
              </a>
            </div>
          )}

          {feePrice && (
            <div className="mt-4">
              <div className="font-orbitron font-bold text-neon-cyan text-lg">
                {feePrice}
              </div>
              {priceNote && (
                <p className="text-muted-gray text-sm mt-1">{priceNote}</p>
              )}
              <a
                href="/#contact"
                className="btn-primary text-xs mt-4 inline-block"
              >
                Get Quote
              </a>
            </div>
          )}

          {customQuote && (
            <div className="mt-4">
              <span
                className={`inline-block ${quoteColor} text-deep-navy font-orbitron font-bold text-xs px-4 py-2 rounded-full`}
              >
                Custom Quotes
              </span>
              <a
                href="/#contact"
                className="btn-primary text-xs mt-4 inline-block ml-0 sm:ml-4"
              >
                Get Quote
              </a>
            </div>
          )}

          {smmLink && (
            <div className="mt-4">
              <Link
                to="/smm-panel"
                className="btn-outline text-xs mt-4 inline-block"
              >
                Visit SMM Panel
              </Link>
            </div>
          )}
        </div>

        {/* Image Column */}
        <div className="lg:w-[40%] relative min-h-[200px] lg:min-h-0 flex items-center justify-center p-6 lg:p-8">
          <div
            className="absolute inset-0 opacity-30"
            style={{
              background:
                'linear-gradient(135deg, rgba(0, 212, 255, 0.1), transparent)',
            }}
          />
          <img
            src={image}
            alt={title}
            className="relative z-10 w-full max-w-[300px] h-auto object-contain drop-shadow-[0_0_20px_rgba(0,212,255,0.2)]"
            loading="lazy"
          />
        </div>
      </div>
    </div>
  )
}
