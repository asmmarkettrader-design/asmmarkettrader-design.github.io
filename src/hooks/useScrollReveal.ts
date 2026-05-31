import { useEffect, useRef } from 'react'

interface ScrollRevealOptions {
  threshold?: number
  rootMargin?: string
  stagger?: number
}

export function useScrollReveal<T extends HTMLElement>(
  options: ScrollRevealOptions = {}
) {
  const ref = useRef<T>(null)
  const { threshold = 0.2, rootMargin = '0px', stagger = 100 } = options

  useEffect(() => {
    const element = ref.current
    if (!element) return

    const children = element.querySelectorAll('[data-reveal]')
    const targets = children.length > 0 ? children : [element]

    targets.forEach((target, index) => {
      const el = target as HTMLElement
      el.style.opacity = '0'
      el.style.transform = 'translateY(30px)'
      el.style.transition = `opacity 0.6s ease-out ${index * stagger}ms, transform 0.6s ease-out ${index * stagger}ms`
    })

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const el = entry.target as HTMLElement
            el.style.opacity = '1'
            el.style.transform = 'translateY(0)'
            observer.unobserve(el)
          }
        })
      },
      { threshold, rootMargin }
    )

    targets.forEach((target) => observer.observe(target))

    return () => {
      targets.forEach((target) => observer.unobserve(target))
    }
  }, [threshold, rootMargin, stagger])

  return ref
}
