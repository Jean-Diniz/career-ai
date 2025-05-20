'use client'

import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useState } from 'react'

import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Checkbox } from '@/components/ui/checkbox'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

export default function RegisterPage() {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setIsLoading(true)

    // Simulação de cadastro
    setTimeout(() => {
      localStorage.setItem('isLoggedIn', 'true')
      router.push('/dashboard')
      setIsLoading(false)
    }, 1000)
  }

  return (
    <div className='flex h-screen w-full items-center justify-center'>
      <Card className='w-full max-w-md'>
        <CardHeader>
          <CardTitle className='text-2xl'>Cadastro</CardTitle>
          <CardDescription>Crie sua conta para começar</CardDescription>
        </CardHeader>
        <form onSubmit={handleSubmit}>
          <CardContent className='space-y-4'>
            <div className='space-y-2'>
              <Label htmlFor='name'>Nome</Label>
              <Input id='name' placeholder='Seu nome completo' required />
            </div>
            <div className='space-y-2'>
              <Label htmlFor='email'>Email</Label>
              <Input
                id='email'
                type='email'
                placeholder='seu@email.com'
                required
              />
            </div>
            <div className='space-y-2'>
              <Label htmlFor='password'>Senha</Label>
              <Input id='password' type='password' required />
            </div>
            <div className='space-y-2'>
              <Label htmlFor='linkedin'>LinkedIn (opcional)</Label>
              <Input id='linkedin' placeholder='URL do seu perfil LinkedIn' />
            </div>
            <div className='flex items-center space-x-2'>
              <Checkbox id='terms' />
              <label
                htmlFor='terms'
                className='text-sm leading-none font-medium peer-disabled:cursor-not-allowed peer-disabled:opacity-70'
              >
                Aceito os termos e condições
              </label>
            </div>
          </CardContent>
          <CardFooter className='mt-4 flex flex-col space-y-4'>
            <Button type='submit' className='w-full' disabled={isLoading}>
              {isLoading ? 'Cadastrando...' : 'Cadastrar'}
            </Button>
            <div className='text-center text-sm'>
              Já tem uma conta?{' '}
              <Link href='/login' className='text-blue-600 hover:underline'>
                Faça login
              </Link>
            </div>
          </CardFooter>
        </form>
      </Card>
    </div>
  )
}
