'use client'

import { LayoutDashboard, LogOut, MessageSquare, User } from 'lucide-react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useState } from 'react'

import { cn } from '@/lib/utils'

import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Button } from '@/components/ui/button'
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from '@/components/ui/sheet'

const routes = [
  {
    href: '/dashboard',
    label: 'Dashboard',
    icon: LayoutDashboard,
  },
  {
    href: '/chat',
    label: 'Chat',
    icon: MessageSquare,
  },
  {
    href: '/profile',
    label: 'Perfil',
    icon: User,
  },
]

export function Sidebar() {
  const pathname = usePathname()
  const [isOpen, setIsOpen] = useState(false)

  const handleLogout = () => {
    localStorage.removeItem('isLoggedIn')
    window.location.href = '/login'
  }

  return (
    <>
      {/* Sidebar para desktop */}
      <div className='bg-background hidden h-screen w-64 flex-col border-r p-4 md:flex'>
        <div className='flex items-center gap-2 py-4'>
          <h1 className='text-xl font-bold'>Career AI</h1>
        </div>
        <div className='mt-8 flex flex-1 flex-col gap-2'>
          {routes.map((route) => (
            <Button
              key={route.href}
              variant={pathname === route.href ? 'default' : 'ghost'}
              className={cn('flex w-full justify-start gap-2')}
              asChild
            >
              <Link href={route.href}>
                <route.icon className='h-5 w-5' />
                {route.label}
              </Link>
            </Button>
          ))}
        </div>
        <div className='mt-auto border-t pt-4'>
          <div className='mb-4 flex items-center gap-3'>
            <Avatar>
              <AvatarImage src='/placeholder-avatar.jpg' />
              <AvatarFallback>US</AvatarFallback>
            </Avatar>
            <div>
              <p className='text-sm font-medium'>Usuário</p>
              <p className='text-muted-foreground text-xs'>usuario@email.com</p>
            </div>
          </div>
          <Button
            variant='outline'
            className='flex w-full justify-start gap-2'
            onClick={handleLogout}
          >
            <LogOut className='h-5 w-5' />
            Sair
          </Button>
        </div>
      </div>

      {/* Sidebar móvel */}
      <Sheet open={isOpen} onOpenChange={setIsOpen}>
        <SheetTrigger asChild className='md:hidden'>
          <Button variant='outline' size='icon' className='fixed top-4 left-4'>
            <span className='sr-only'>Abrir menu</span>
            <svg
              width='15'
              height='15'
              viewBox='0 0 15 15'
              fill='none'
              xmlns='http://www.w3.org/2000/svg'
              className='h-5 w-5'
            >
              <path
                d='M1.5 3C1.22386 3 1 3.22386 1 3.5C1 3.77614 1.22386 4 1.5 4H13.5C13.7761 4 14 3.77614 14 3.5C14 3.22386 13.7761 3 13.5 3H1.5ZM1 7.5C1 7.22386 1.22386 7 1.5 7H13.5C13.7761 7 14 7.22386 14 7.5C14 7.77614 13.7761 8 13.5 8H1.5C1.22386 8 1 7.77614 1 7.5ZM1 11.5C1 11.2239 1.22386 11 1.5 11H13.5C13.7761 11 14 11.2239 14 11.5C14 11.7761 13.7761 12 13.5 12H1.5C1.22386 12 1 11.7761 1 11.5Z'
                fill='currentColor'
                fillRule='evenodd'
                clipRule='evenodd'
              ></path>
            </svg>
          </Button>
        </SheetTrigger>
        <SheetContent side='left' className='w-64 p-0'>
          <SheetHeader className='border-b p-4'>
            <SheetTitle className='text-left'>Career AI</SheetTitle>
          </SheetHeader>
          <div className='flex flex-1 flex-col gap-2 p-4'>
            {routes.map((route) => (
              <Button
                key={route.href}
                variant={pathname === route.href ? 'default' : 'ghost'}
                className={cn('flex w-full justify-start gap-2')}
                asChild
                onClick={() => setIsOpen(false)}
              >
                <Link href={route.href}>
                  <route.icon className='h-5 w-5' />
                  {route.label}
                </Link>
              </Button>
            ))}
          </div>
          <div className='border-t p-4'>
            <div className='mb-4 flex items-center gap-3'>
              <Avatar>
                <AvatarImage src='/placeholder-avatar.jpg' />
                <AvatarFallback>US</AvatarFallback>
              </Avatar>
              <div>
                <p className='text-sm font-medium'>Usuário</p>
                <p className='text-muted-foreground text-xs'>
                  usuario@email.com
                </p>
              </div>
            </div>
            <Button
              variant='outline'
              className='flex w-full justify-start gap-2'
              onClick={handleLogout}
            >
              <LogOut className='h-5 w-5' />
              Sair
            </Button>
          </div>
        </SheetContent>
      </Sheet>
    </>
  )
}
