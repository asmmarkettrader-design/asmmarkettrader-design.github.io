import { useScrollReveal } from '../../hooks/useScrollReveal'
import { CheckCircle } from 'lucide-react'

const checklist = [
  'Complete Website Technical Analysis',
  'Competitor Strategy Breakdown',
  'Custom Growth Roadmap',
  'ROI Projection Report',
]

export default function FreeAuditCTA() {
  const sectionRef = useScrollReveal<HTMLDivElement>({ stagger: 100 })

  return (
    <section className="section-padding bg-gradient-to-b from-deep-navy to-electric-blue/5 border-y border-neon-cyan/10">
      <div className="max-w-[800px] mx-auto px-4 sm:px-6 text-center" ref={sectionRef}>
        <h2 className="font-orbitron font-bold text-2xl sm:text-3xl md:text-4xl text-pure-white" data-reveal>
          Get a FREE Business Audit Today!
        </h2>

        {/* Checklist */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-8">
          {checklist.map((item) => (
            <div
              key={item}
              data-reveal
              className="flex items-center gap-3 bg-card-navy/60 border border-neon-cyan/10 rounded-xl px-5 py-4"
            >
              <CheckCircle size={20} className="text-neon-cyan shrink-0" />
              <span className="text-light-cyan text-sm text-left">{item}</span>
            </div>
          ))}
        </div>

        {/* Contact Buttons */}
        <div data-reveal className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
          <a
            href="https://wa.me/923425478683"
            target="_blank"
            rel="noopener noreferrer"
            className="btn-whatsapp"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
              <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z" />
            </svg>
            +92 342 5478683
          </a>
          <a
            href="mailto:Asmmarkettrader@gmail.com"
            className="btn-primary flex items-center gap-2"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <rect width="20" height="16" x="2" y="4" rx="2" />
              <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7" />
            </svg>
            Asmmarkettrader@gmail.com
          </a>
        </div>

        {/* Subtext */}
        <p data-reveal className="text-muted-gray text-sm mt-6">
          Stop losing customers to your competitors. Let's scale your business together.
        </p>
      </div>
    </section>
  )
}
