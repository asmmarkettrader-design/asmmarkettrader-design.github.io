import { useEffect, useRef, useState } from 'react'

interface CounterOptions {
  end: number
  duration?: number
  suffix?: string
  prefix?: string
  decimals?: number
}

export function useCounter({
  end,
  duration = 2000,
  suffix = '',
  prefix = '',
  decimals = 0,
}: CounterOptions) {
  const [count, setCount] = useState(0)
  const [hasStarted, setHasStarted] = useState(false)
  const ref = useRef<HTMLDivElement>(null)
  const frameRef = useRef<number | null>(null)

  useEffect(() => {
    const element = ref.current
    if (!element) return

    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && !hasStarted) {
          setHasStarted(true)
        }
      },
      { threshold: 0.5 }
    )

    observer.observe(element)
    return () => observer.disconnect()
  }, [hasStarted])

  useEffect(() => {
    if (!hasStarted) return

    const startTime = performance.now()
    const startValue = 0

    const animate = (currentTime: number) => {
      const elapsed = currentTime - startTime
      const progress = Math.min(elapsed / duration, 1)
      
      // Ease-out function
      const easeOut = 1 - Math.pow(1 - progress, 3)
      const current = startValue + (end - startValue) * easeOut

      setCount(Number(current.toFixed(decimals)))

      if (progress < 1) {
        frameRef.current = requestAnimationFrame(animate)
      }
    }

    frameRef.current = requestAnimationFrame(animate)

    return () => {
      if (frameRef.current) {
        cancelAnimationFrame(frameRef.current)
      }
    }
  }, [hasStarted, end, duration, decimals])

  const display = `${prefix}${count}${suffix}`

  return { ref, display, hasStarted }
}
