import { Link } from 'react-router-dom'
import { Facebook, Instagram, Linkedin, MessageCircle, Mail, Globe, Phone } from 'lucide-react'

const quickLinks = [
  { name: 'Home', path: '/' },
  { name: 'Services', path: '/#services' },
  { name: 'SMM Panel', path: '/smm-panel' },
  { name: 'Why Us', path: '/#why-us' },
  { name: 'Contact', path: '/#contact' },
]

const services = [
  'SEO Optimization',
  'Paid Marketing',
  'SMM Services',
  'Web Development',
  'Creative Studio',
  'Business Consultancy',
]

const socialLinks = [
  { icon: Facebook, href: '#', label: 'Facebook' },
  { icon: Instagram, href: '#', label: 'Instagram' },
  { icon: Linkedin, href: 'https://linkedin.com/in/asm-market-traders', label: 'LinkedIn' },
  { icon: MessageCircle, href: 'https://wa.me/923425478683', label: 'WhatsApp' },
]

export default function Footer() {
  return (
    <footer className="bg-deep-navy border-t border-neon-cyan/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-10">
          {/* Brand Column */}
          <div className="space-y-6">
            <Link to="/" className="flex items-center gap-0">
              <span className="font-orbitron font-bold text-xl text-neon-cyan">ASM</span>
              <span className="font-orbitron font-normal text-xl text-pure-white ml-1">DIGITAL</span>
            </Link>
            <p className="text-muted-gray text-sm leading-relaxed">
              Your All-in-One Business Growth Partner. We build your entire digital presence.
            </p>
            <div className="flex gap-3">
              {socialLinks.map((social) => (
                <a
                  key={social.label}
                  href={social.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-10 h-10 rounded-full border border-neon-cyan/30 flex items-center justify-center text-neon-cyan hover:bg-neon-cyan hover:text-deep-navy transition-all duration-300"
                  aria-label={social.label}
                >
                  <social.icon size={18} />
                </a>
              ))}
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="font-orbitron font-semibold text-pure-white text-sm uppercase tracking-wider mb-6">
              Quick Links
            </h4>
            <ul className="space-y-3">
              {quickLinks.map((link) => (
                <li key={link.name}>
                  <Link
                    to={link.path}
                    className="text-muted-gray text-sm hover:text-neon-cyan transition-colors"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Services */}
          <div>
            <h4 className="font-orbitron font-semibold text-pure-white text-sm uppercase tracking-wider mb-6">
              Services
            </h4>
            <ul className="space-y-3">
              {services.map((service) => (
                <li key={service}>
                  <span className="text-muted-gray text-sm">{service}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h4 className="font-orbitron font-semibold text-pure-white text-sm uppercase tracking-wider mb-6">
              Contact Us
            </h4>
            <ul className="space-y-4">
              <li className="flex items-center gap-3">
                <Phone size={16} className="text-neon-cyan shrink-0" />
                <a
                  href="https://wa.me/923425478683"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-muted-gray text-sm hover:text-neon-cyan transition-colors"
                >
                  +92 342 5478683
                </a>
              </li>
              <li className="flex items-center gap-3">
                <Mail size={16} className="text-neon-cyan shrink-0" />
                <a
                  href="mailto:Asmmarkettrader@gmail.com"
                  className="text-muted-gray text-sm hover:text-neon-cyan transition-colors"
                >
                  Asmmarkettrader@gmail.com
                </a>
              </li>
              <li className="flex items-center gap-3">
                <Globe size={16} className="text-neon-cyan shrink-0" />
                <a
                  href="https://asmveo.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-muted-gray text-sm hover:text-neon-cyan transition-colors"
                >
                  Asmveo.com
                </a>
              </li>
              <li className="flex items-center gap-3">
                <Linkedin size={16} className="text-neon-cyan shrink-0" />
                <a
                  href="https://linkedin.com/in/asm-market-traders"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-muted-gray text-sm hover:text-neon-cyan transition-colors"
                >
                  ASM Market Traders
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="mt-12 pt-8 border-t border-neon-cyan/10 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-muted-gray text-xs text-center sm:text-left">
            &copy; {new Date().getFullYear()} ASM Digital Solutions. All rights reserved.
          </p>
          <p className="text-muted-gray text-xs">
            Powered by Technical Expertise
          </p>
        </div>
      </div>
    </footer>
  )
}
