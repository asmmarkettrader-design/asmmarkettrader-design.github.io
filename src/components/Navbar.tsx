import { useState, useEffect } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Menu, X } from 'lucide-react'

const navLinks = [
  { name: 'Home', path: '/' },
  { name: 'Services', path: '/#services' },
  { name: 'SMM Panel', path: '/smm-panel' },
  { name: 'Why Us', path: '/#why-us' },
  { name: 'Contact', path: '/#contact' },
]

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false)
  const [scrolled, setScrolled] = useState(false)
  const location = useLocation()

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  useEffect(() => {
    setIsOpen(false)
  }, [location])

  const isActive = (path: string) => {
    if (path === '/') return location.pathname === '/'
    if (path.startsWith('/#')) {
      return location.pathname === '/' && location.hash === path.slice(1)
    }
    return location.pathname === path
  }

  const handleNavClick = (path: string) => {
    if (path.startsWith('/#')) {
      const sectionId = path.slice(2)
      if (location.pathname === '/') {
        const el = document.getElementById(sectionId)
        if (el) {
          el.scrollIntoView({ behavior: 'smooth' })
        }
      }
    }
    setIsOpen(false)
  }

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled
          ? 'bg-deep-navy/95 backdrop-blur-xl border-b border-neon-cyan/10'
          : 'bg-transparent'
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-[72px]">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-0 shrink-0">
            <span className="font-orbitron font-bold text-xl text-neon-cyan">ASM</span>
            <span className="font-orbitron font-normal text-xl text-pure-white ml-1">DIGITAL</span>
          </Link>

          {/* Desktop Nav Links */}
          <div className="hidden md:flex items-center gap-8">
            {navLinks.map((link) => (
              <Link
                key={link.name}
                to={link.path}
                onClick={() => handleNavClick(link.path)}
                className={`nav-link ${isActive(link.path) ? 'active' : ''}`}
              >
                {link.name}
              </Link>
            ))}
          </div>

          {/* CTA Button */}
          <div className="hidden md:block">
            <Link
              to="/#contact"
              onClick={() => handleNavClick('/#contact')}
              className="btn-primary text-xs py-2.5 px-6"
            >
              Get Started
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden text-pure-white p-2"
            onClick={() => setIsOpen(!isOpen)}
            aria-label="Toggle menu"
          >
            {isOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      <div
        className={`md:hidden absolute top-[72px] left-0 right-0 bg-deep-navy/98 backdrop-blur-xl border-b border-neon-cyan/10 transition-all duration-300 ${
          isOpen ? 'opacity-100 visible' : 'opacity-0 invisible'
        }`}
      >
        <div className="px-4 py-6 space-y-4">
          {navLinks.map((link) => (
            <Link
              key={link.name}
              to={link.path}
              onClick={() => handleNavClick(link.path)}
              className={`block font-syne font-medium text-base uppercase tracking-wider transition-colors ${
                isActive(link.path) ? 'text-neon-cyan' : 'text-muted-gray hover:text-neon-cyan'
              }`}
            >
              {link.name}
            </Link>
          ))}
          <Link
            to="/#contact"
            onClick={() => handleNavClick('/#contact')}
            className="btn-primary text-sm inline-block mt-4"
          >
            Get Started
          </Link>
        </div>
      </div>
    </nav>
  )
}
