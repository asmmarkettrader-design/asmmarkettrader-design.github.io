import { useState, useEffect, useCallback } from 'react'

interface TypewriterOptions {
  text: string
  speed?: number
  delay?: number
  onComplete?: () => void
}

export function useTypewriter({
  text,
  speed = 80,
  delay = 0,
  onComplete,
}: TypewriterOptions) {
  const [displayText, setDisplayText] = useState('')
  const [isComplete, setIsComplete] = useState(false)
  const [hasStarted, setHasStarted] = useState(false)

  const start = useCallback(() => {
    setHasStarted(true)
  }, [])

  useEffect(() => {
    if (!hasStarted) return

    const timeout = setTimeout(() => {
      let index = 0
      const interval = setInterval(() => {
        if (index < text.length) {
          setDisplayText(text.slice(0, index + 1))
          index++
        } else {
          clearInterval(interval)
          setIsComplete(true)
          onComplete?.()
        }
      }, speed)

      return () => clearInterval(interval)
    }, delay)

    return () => clearTimeout(timeout)
  }, [hasStarted, text, speed, delay, onComplete])

  return { displayText, isComplete, start, hasStarted }
}
