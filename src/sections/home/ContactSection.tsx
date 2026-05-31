import { useScrollReveal } from '../../hooks/useScrollReveal'
import { MessageCircle, Mail, Globe, Linkedin } from 'lucide-react'
import type { LucideIcon } from 'lucide-react'

const contacts: {
  icon: LucideIcon
  title: string
  value: string
  link: string
}[] = [
  {
    icon: MessageCircle,
    title: 'WhatsApp',
    value: '+92 342 5478683',
    link: 'https://wa.me/923425478683',
  },
  {
    icon: Mail,
    title: 'Email',
    value: 'Asmmarkettrader@gmail.com',
    link: 'mailto:Asmmarkettrader@gmail.com',
  },
  {
    icon: Globe,
    title: 'Website',
    value: 'Asmveo.com',
    link: 'https://asmveo.com',
  },
]

export default function ContactSection() {
  const sectionRef = useScrollReveal<HTMLDivElement>({ stagger: 100 })

  return (
    <section id="contact" className="section-padding bg-deep-navy">
      <div className="max-w-[900px] mx-auto">
        <div className="text-center mb-12" data-reveal>
          <h2 className="font-orbitron font-bold text-2xl sm:text-3xl md:text-4xl text-pure-white">
            Contact Us
          </h2>
        </div>

        <div
          ref={sectionRef}
          className="grid grid-cols-1 sm:grid-cols-3 gap-6"
        >
          {contacts.map((contact) => (
            <a
              key={contact.title}
              href={contact.link}
              target="_blank"
              rel="noopener noreferrer"
              data-reveal
              className="glass-card glow-border p-8 text-center transition-all duration-300 hover:-translate-y-1 group"
            >
              <contact.icon
                size={40}
                className="text-neon-cyan mx-auto group-hover:scale-110 transition-transform"
              />
              <h4 className="font-orbitron font-semibold text-lg text-pure-white mt-4">
                {contact.title}
              </h4>
              <p className="text-light-cyan text-sm mt-2 break-all">
                {contact.value}
              </p>
            </a>
          ))}
        </div>

        {/* LinkedIn */}
        <div className="text-center mt-10" data-reveal>
          <a
            href="https://linkedin.com/in/asm-market-traders"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 text-neon-cyan hover:underline font-syne"
          >
            <Linkedin size={20} />
            Connect on LinkedIn - ASM Market Traders
          </a>
        </div>
      </div>
    </section>
  )
}
