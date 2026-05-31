import { useScrollReveal } from '../../hooks/useScrollReveal'
import ServiceCard from './ServiceCard'
import {
  Globe,
  Code,
  Search,
  Share2,
  Target,
  Palette,
  TrendingUp,
} from 'lucide-react'

const services = [
  {
    icon: Globe,
    title: 'Global Reputation Engine & Geo-Targeted Reviews',
    description:
      'Boost trust with verified, geo-targeted reviews. We provide 100% safe, verified, and highly targeted reviews from any location worldwide, specializing in USA, UK, Canada, France, Dubai/UAE, European, and Gulf countries.',
    features: [
      'Geo-Targeted Authority Setup (USA, UK, CA, FR, UAE)',
      'GMB Optimization & Geo-Positioning',
      'Review Infrastructure Management',
      'Localized Citations & Keyword Mapping',
      'Negative Review Mitigation',
      'Automated Positive Review Streams',
    ],
    pricing: [
      { qty: '5 Reviews', price: '$10' },
      { qty: '20 Reviews', price: '$40' },
      { qty: '50 Reviews', price: '$100' },
      { qty: '100 Reviews', price: '$180', badge: 'Best Value' },
    ],
    image: '/assets/hero-globe.png',
    iconBorderColor: 'border-neon-cyan',
  },
  {
    icon: Code,
    title: 'Full-Stack Web Architecture, Domain & Hosting',
    description:
      'End-to-end development and deployment. We build custom, fast, and high-performance websites engineered for 99.9% uptime and seamless user experiences across all devices.',
    features: [
      'Custom Website Development',
      'Domain & Hosting Acquisition',
      'DNS Configuration Management',
      'System Proxies & Latency Optimization',
      'Automated SSL (HTTPS) Sync',
      'Custom Admin Dashboards',
      '99.9% Uptime Guarantee',
      'Dynamic Blog & Image Management',
    ],
    image: '/assets/web-servers.png',
    iconBorderColor: 'border-electric-blue',
    customQuote: true,
    quoteColor: 'bg-electric-blue',
  },
  {
    icon: Search,
    title: 'Omni-Channel Search Engine Optimization (SEO)',
    description:
      'Rank #1 on Google and get organic traffic. Advanced technical on-page and off-page optimization, site architecture refinement, and continuous indexing configurations.',
    features: [
      'Core Website SEO (On-Page & Off-Page)',
      'Technical Audit & Speed Optimization',
      'Keyword Research & Architecture',
      'YouTube SEO Domination',
      'Social Asset Optimization',
      'GMB (Google My Business) Optimization',
      'Local SEO Citations',
      'Search Console Indexing',
    ],
    image: '/assets/seo-ranking.png',
    iconBorderColor: 'border-neon-cyan',
    monthlyPrice: 'Starting from $250/Month',
    priceNote: 'Custom quotes based on website size',
  },
  {
    icon: Share2,
    title: 'Full-Suite Social Media Management (SMM)',
    description:
      'Professional oversight and daily operations of all your major brand handles. Engineering strategic content calendars, interactive audience engagement, and organic growth.',
    features: [
      'Multi-Platform Operations (FB, IG, TikTok, LI)',
      'Organic Growth Engineering',
      'Content Calendar & Scheduling',
      'Audience Engagement Loops',
      'Trend-Driven Hashtag Matrices',
      'SMM Panel Services Available',
      'Influencer Collaboration Outreach',
      'Monthly Analytics Reports',
    ],
    image: '/assets/social-constellation.png',
    iconBorderColor: 'border-pink-500',
    smmLink: true,
  },
  {
    icon: Target,
    title: 'Hyper-Targeted Paid Campaigns (Performance Marketing)',
    description:
      'Get instant leads and sales with targeted ad campaigns. Expert setup and execution of high-converting campaigns across Google, Facebook, Instagram, and TikTok.',
    features: [
      'Google Ads (SEM) Management',
      'YouTube Video Ad Campaigns',
      'Facebook & Instagram Ads',
      'TikTok Ad Campaigns',
      'Programmatic Budget Management',
      'Audience Demographic Targeting',
      'Behavioral & Intent Targeting',
      'ROI-Focused Optimization',
    ],
    image: '/assets/ads-dashboard.png',
    iconBorderColor: 'border-orange-500',
    feePrice: '20% Management Fee of Ad Spend',
    priceNote: 'Min. fee applies',
  },
  {
    icon: Palette,
    title: 'Advanced Creative Studio',
    description:
      'High-retention video editing, premium graphic design, and compelling copywriting. We create content that grabs attention and converts viewers into paying clients.',
    features: [
      'High-Retention Video Editing (Reels, Shorts, TikTok)',
      'YouTube Video Production',
      'Premium Logo & Brand Identity',
      'Website Graphics & Banners',
      'Social Media Post Assets',
      'Compelling Website Copywriting',
      'Authority Blog Posts',
      'High-Conversion Ad Scripts',
    ],
    image: '/assets/creative-palette.png',
    iconBorderColor: 'border-purple-500',
    customQuote: true,
    quoteColor: 'bg-purple-500',
  },
  {
    icon: TrendingUp,
    title: 'Strategic Financial & Business Consultancy',
    description:
      'Expert corporate advice for startups and digital agencies regarding budget planning, ROI forecasting, and market entry strategies. We help you scale efficiently.',
    features: [
      'Digital Business Scaling Strategy',
      'Budget Planning & Allocation',
      'ROI Forecasting & Analysis',
      'Market Entry Strategy',
      'Process Automation Consulting',
      'Software Pipeline Optimization',
      'Expense Reduction Analysis',
      'Profit Margin Multiplication',
    ],
    image: '/assets/growth-chart.png',
    iconBorderColor: 'border-yellow-500',
    customQuote: true,
    quoteColor: 'bg-yellow-500',
  },
]

export default function ServicesOverview() {
  const sectionRef = useScrollReveal<HTMLDivElement>({ stagger: 150 })

  return (
    <section id="services" className="section-padding bg-deep-navy">
      <div className="max-w-7xl mx-auto">
        {/* Section Header */}
        <div className="text-center mb-16" data-reveal>
          <h2 className="font-orbitron font-bold text-2xl sm:text-3xl md:text-4xl text-pure-white">
            Complete Digital Solutions
          </h2>
          <p className="mt-4 text-muted-gray text-base max-w-[600px] mx-auto">
            Everything your business needs to dominate the digital landscape
          </p>
        </div>

        {/* Service Cards */}
        <div ref={sectionRef} className="space-y-8">
          {services.map((service, index) => (
            <div key={service.title} data-reveal>
              <ServiceCard {...service} index={index} />
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
