import HeroSection from '../sections/home/HeroSection'
import StatsBar from '../sections/home/StatsBar'
import ServicesOverview from '../sections/home/ServicesOverview'
import WhyChooseUs from '../sections/home/WhyChooseUs'
import FreeAuditCTA from '../sections/home/FreeAuditCTA'
import ContactSection from '../sections/home/ContactSection'

export default function HomePage() {
  return (
    <>
      <HeroSection />
      <StatsBar />
      <ServicesOverview />
      <WhyChooseUs />
      <FreeAuditCTA />
      <ContactSection />
    </>
  )
}
