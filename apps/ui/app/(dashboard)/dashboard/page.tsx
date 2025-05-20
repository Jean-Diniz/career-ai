import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

export default function DashboardPage() {
  return (
    <div className='space-y-6'>
      <h1 className='text-3xl font-bold'>Dashboard</h1>
      <div className='grid gap-6 md:grid-cols-2 lg:grid-cols-3'>
        <Card>
          <CardHeader>
            <CardTitle>Perfil Profissional</CardTitle>
            <CardDescription>Análise do seu perfil LinkedIn</CardDescription>
          </CardHeader>
          <CardContent>
            <p>
              Conecte seu LinkedIn para realizar uma análise completa do seu
              perfil profissional.
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Trilha de Estudos</CardTitle>
            <CardDescription>Sua trilha personalizada</CardDescription>
          </CardHeader>
          <CardContent>
            <p>
              Com base no seu perfil e objetivos, criamos uma trilha de estudos
              personalizada.
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Simulação de Entrevista</CardTitle>
            <CardDescription>Prepare-se para entrevistas</CardDescription>
          </CardHeader>
          <CardContent>
            <p>
              Pratique com simulações de entrevista baseadas nas vagas que você
              deseja.
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
