'use client'

import { useState } from 'react'

import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

export default function ProfilePage() {
  const [isEditing, setIsEditing] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [formData, setFormData] = useState({
    name: 'Usuário',
    email: 'usuario@email.com',
    linkedin: 'https://linkedin.com/in/usuario',
  })

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    // Simulação de atualização de perfil
    setTimeout(() => {
      setIsLoading(false)
      setIsEditing(false)
    }, 1000)
  }

  return (
    <div className='space-y-6'>
      <h1 className='text-3xl font-bold'>Perfil</h1>

      <Card>
        <CardHeader>
          <div className='flex items-center gap-4'>
            <Avatar className='h-16 w-16'>
              <AvatarImage src='/placeholder-avatar.jpg' />
              <AvatarFallback>US</AvatarFallback>
            </Avatar>
            <div>
              <CardTitle>{formData.name}</CardTitle>
              <CardDescription>{formData.email}</CardDescription>
            </div>
          </div>
        </CardHeader>

        <form onSubmit={handleSubmit}>
          <CardContent className='space-y-4'>
            <div className='space-y-2'>
              <Label htmlFor='name'>Nome</Label>
              <Input
                id='name'
                name='name'
                value={formData.name}
                onChange={handleInputChange}
                disabled={!isEditing}
              />
            </div>

            <div className='space-y-2'>
              <Label htmlFor='email'>Email</Label>
              <Input
                id='email'
                name='email'
                type='email'
                value={formData.email}
                onChange={handleInputChange}
                disabled={!isEditing}
              />
            </div>

            <div className='space-y-2'>
              <Label htmlFor='linkedin'>LinkedIn</Label>
              <Input
                id='linkedin'
                name='linkedin'
                value={formData.linkedin}
                onChange={handleInputChange}
                disabled={!isEditing}
              />
            </div>
          </CardContent>

          <CardFooter className='flex justify-between'>
            {isEditing ? (
              <>
                <Button
                  type='button'
                  variant='outline'
                  onClick={() => setIsEditing(false)}
                  disabled={isLoading}
                >
                  Cancelar
                </Button>
                <Button type='submit' disabled={isLoading}>
                  {isLoading ? 'Salvando...' : 'Salvar alterações'}
                </Button>
              </>
            ) : (
              <Button type='button' onClick={() => setIsEditing(true)}>
                Editar perfil
              </Button>
            )}
          </CardFooter>
        </form>
      </Card>
    </div>
  )
}
