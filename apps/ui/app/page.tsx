'use client'

import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export default function Home() {
  const router = useRouter()

  useEffect(() => {
    const isLoggedIn = localStorage.getItem('isLoggedIn')
    if (isLoggedIn) {
      router.push('/dashboard')
    } else {
      router.push('/login')
    }
  }, [router])

  return (
    <div className='flex h-screen flex-col items-center justify-center'>
      <div className='flex flex-col items-center gap-8'>
        <h1 className='text-4xl font-bold'>Career AI</h1>
        <p>Redirecionando...</p>
      </div>
    </div>
  )
}
