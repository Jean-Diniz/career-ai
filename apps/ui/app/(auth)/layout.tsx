'use client'

import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const router = useRouter()

  useEffect(() => {
    const isLoggedIn = localStorage.getItem('isLoggedIn')
    if (isLoggedIn) {
      router.push('/dashboard')
    }
  }, [router])

  return (
    <div className='grid min-h-screen grid-cols-1 md:grid-cols-2'>
      <div className='bg-muted hidden md:block'>
        <div className='flex h-full flex-col items-center justify-center'>
          <div className='flex flex-col items-center gap-6 px-6'>
            <h1 className='text-center text-4xl font-bold'>Career AI</h1>
            <p className='text-center text-xl'>
              Sua plataforma completa para evolução profissional
            </p>
          </div>
        </div>
      </div>
      <div className='flex items-center justify-center'>{children}</div>
    </div>
  )
}
