import { useState } from 'react'
import SMMHero from '../sections/smm/SMMHero'
import ServicesTable from '../sections/smm/ServicesTable'
import HowItWorks from '../sections/smm/HowItWorks'
import SMMFeatures from '../sections/smm/SMMFeatures'
import SMMCTA from '../sections/smm/SMMCTA'

export default function SMMPanelPage() {
  const [searchQuery, setSearchQuery] = useState('')

  return (
    <>
      <SMMHero onSearch={setSearchQuery} />
      <ServicesTable searchQuery={searchQuery} />
      <HowItWorks />
      <SMMFeatures />
      <SMMCTA />
    </>
  )
}
