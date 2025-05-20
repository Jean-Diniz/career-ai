'use client'

import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

import { Sidebar } from '@/components/sidebar'

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const router = useRouter()

  useEffect(() => {
    const isLoggedIn = localStorage.getItem('isLoggedIn')
    if (!isLoggedIn) {
      router.push('/login')
    }
  }, [router])

  return (
    <div className='flex h-screen'>
      <Sidebar />
      <main className='flex-1 overflow-y-auto p-4 md:p-8'>{children}</main>
    </div>
  )
}
