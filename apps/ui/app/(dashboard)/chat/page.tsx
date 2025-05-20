'use client'

import { SendHorizontal } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'

import { cn } from '@/lib/utils'

import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Input } from '@/components/ui/input'

type Message = {
  id: string
  content: string
  role: 'user' | 'assistant'
  timestamp: Date
}

export default function ChatPage() {
  const [inputValue, setInputValue] = useState('')
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      content:
        'Olá! Sou o Career AI, seu assistente de carreira. Como posso ajudar você hoje?',
      role: 'assistant',
      timestamp: new Date(),
    },
  ])
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const handleSendMessage = () => {
    if (!inputValue.trim()) return

    // Adiciona mensagem do usuário
    const userMessage: Message = {
      id: crypto.randomUUID(),
      content: inputValue,
      role: 'user',
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInputValue('')

    // Simula resposta do assistente
    setTimeout(() => {
      const assistantMessage: Message = {
        id: crypto.randomUUID(),
        content:
          'Estou processando sua solicitação. Em breve implementaremos integrações com IA para respostas mais elaboradas.',
        role: 'assistant',
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, assistantMessage])
    }, 1000)
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  // Rola para o final da conversa quando novas mensagens chegam
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  return (
    <div className='flex h-full flex-col'>
      <div className='mb-4'>
        <h1 className='text-3xl font-bold'>Chat</h1>
        <p className='text-muted-foreground'>
          Converse com o Career AI para obter orientações sobre sua carreira
        </p>
      </div>

      <Card className='flex flex-1 flex-col'>
        <CardContent className='flex h-full flex-col p-4'>
          <div className='flex-1 space-y-4 overflow-y-auto pb-4'>
            {messages.map((message) => (
              <div
                key={message.id}
                className={cn(
                  'flex w-max max-w-[80%] flex-col rounded-lg px-4 py-2',
                  message.role === 'user'
                    ? 'bg-primary text-primary-foreground ml-auto'
                    : 'bg-muted',
                )}
              >
                <p>{message.content}</p>
                <span className='mt-1 text-xs opacity-70'>
                  {message.timestamp.toLocaleTimeString()}
                </span>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          <div className='mt-auto flex items-end gap-2 pt-4'>
            <Input
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder='Digite sua mensagem...'
              className='flex-1'
            />
            <Button
              onClick={handleSendMessage}
              size='icon'
              disabled={!inputValue.trim()}
            >
              <SendHorizontal className='h-5 w-5' />
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
