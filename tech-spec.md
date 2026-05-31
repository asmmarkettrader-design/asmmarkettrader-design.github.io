# Tech Spec - ASM Digital Solutions

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| vite | ^6 | Build tool, dev server, static site generation |
| @vitejs/plugin-react | ^4 | React support for Vite |
| react | ^19 | UI framework |
| react-dom | ^19 | React DOM renderer |
| react-router-dom | ^7 | Client-side routing (Home + SMM Panel pages) |
| gsap | ^3.12 | Animation engine (scroll reveals, counters, typewriter) |
| lucide-react | ^0.460 | Icon library (all UI icons) |
| tailwindcss | ^4 | Utility-first CSS |
| @tailwindcss/vite | ^4 | Tailwind Vite integration |
| typescript | ^5.6 | Type safety |
| @types/react | ^19 | React type definitions |
| @types/react-dom | ^19 | React DOM type definitions |

No shadcn/ui - all components are custom-built with Tailwind to match the unique cyberpunk design language.

---

## Component Inventory

### Layout (shared across pages)

| Component | Source | Notes |
|-----------|--------|-------|
| Navbar | Custom | Fixed top, glassmorphism, mobile hamburger |
| Footer | Custom | 4-column grid, social icons |
| WhatsAppFloat | Custom | Fixed bottom-right, pulse animation |
| ScrollToTop | Custom | Fixed, appears after 300px scroll |
| ParticleCanvas | Custom | Full-page canvas, vanilla JS via ref |

### Home Page Sections

| Component | Source | Notes |
|-----------|--------|-------|
| HeroSection | Custom | Typewriter headline, particle bg, dual CTAs |
| StatsBar | Custom | 4 animated counters |
| ServicesOverview | Custom | 7 service cards with alternating layouts |
| ServiceCard | Custom | Reusable two-column card (icon+features / decorative visual) |
| WhyChooseUs | Custom | 4-card advantage grid |
| FreeAuditCTA | Custom | Checklist + dual contact buttons |
| ContactSection | Custom | 3 contact cards + LinkedIn |

### SMM Panel Page Sections

| Component | Source | Notes |
|-----------|--------|-------|
| SMMHero | Custom | Compact hero with stats + search |
| CategoryFilter | Custom | Horizontal scrollable filter bar |
| ServicesTable | Custom | Full data table with filtering logic |
| ServiceRow | Custom | Individual table row |
| HowItWorks | Custom | 3-step process cards |
| SMMFeatures | Custom | 3 benefit cards |
| SMMCTA | Custom | Final call-to-action |

### Hooks

| Hook | Purpose |
|------|---------|
| useScrollReveal | IntersectionObserver-based scroll reveal (shared across all sections) |
| useCounter | Animated number counter with ease-out |
| useTypewriter | Character-by-character typing effect with callback |
| useParticleCanvas | Canvas lifecycle: init, animate, cleanup, mouse interaction |

---

## Animation Implementation

| Animation | Library | Approach | Complexity |
|-----------|---------|----------|------------|
| Particle Network | Canvas API (vanilla) | requestAnimationFrame loop, particle class with drift/bounce/collision logic, mouse repel via distance calculation. 60 particles desktop, 30 mobile. | **High** |
| Typewriter Effect | Custom hook | setInterval at 80ms/char, second line delays 200ms after first completes, cleanup on unmount | Medium |
| Scroll Reveal | GSAP + ScrollTrigger | translateY(30px)+opacity tween, triggered at viewport 80%, 100ms sibling stagger | Low |
| Counter Animation | GSAP | gsap.to with snap for integer values, 2000ms duration, ease-out, 200ms stagger between stats | Low |
| Button Hover | CSS | Tailwind transition + scale + box-shadow, no JS needed | Low |
| Card Hover | CSS | Tailwind transition + translateY + border-color change | Low |
| WhatsApp Pulse | CSS | @keyframes scale+opacity, 2s infinite | Low |
| Page Transition | CSS | opacity transition on route change, 200ms out / 300ms in | Low |
| Icon Float | CSS | @keyframes translateY, 3s infinite alternate | Low |
| Category Filter | CSS | opacity transition on row visibility change | Low |
| Checklist Stagger | GSAP + ScrollTrigger | Individual reveals with 100ms stagger | Low |

---

## State & Logic Plan

### Routing
React Router v7 with two routes: `/` (Home) and `/smm-panel` (SMM Panel). Hash-based routing for GitHub Pages compatibility.

### Particle Canvas Global State
The particle canvas runs as an imperative background element. It is NOT driven by React state - all animation runs via requestAnimationFrame in a useRef-managed canvas context. Mouse position tracked via ref (not state) to avoid 60fps re-renders. Component cleanup cancels the animation frame on unmount.

### Services Table Filtering
Category filter + search input both filter the same dataset. Use useMemo to derive filtered rows from `activeCategory` and `searchQuery` state. Debounce search input at 300ms via setTimeout ref (no library needed).

### Page Transition
Wrap route outlet in AnimatePresence (or manual CSS transition). On route change: fade out current (200ms), unmount, mount new, fade in (300ms). Transition state managed at router outlet level.

### Order Button Flow
Each "Order" button constructs a WhatsApp URL with pre-encoded message text containing service name and ID. Opens in new tab. No backend, no state - pure static link generation.
