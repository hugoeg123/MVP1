import { useAuthStore } from '@/store/auth'

export default function Dashboard() {
  const { user } = useAuthStore()
  
  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-4">
        Bem-vindo, {user?.full_name || 'Usuário'}!
      </h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div className="card bg-base-100 shadow hover:shadow-lg transition-shadow">
          <div className="card-body">
            <h3 className="card-title text-gray-700">Consultas Hoje</h3>
            <div className="text-4xl font-bold text-primary">0</div>
          </div>
        </div>
        
        <div className="card bg-base-100 shadow hover:shadow-lg transition-shadow">
          <div className="card-body">
            <h3 className="card-title text-gray-700">Pacientes</h3>
            <div className="text-4xl font-bold text-primary">0</div>
          </div>
        </div>
        
        <div className="card bg-base-100 shadow hover:shadow-lg transition-shadow">
          <div className="card-body">
            <h3 className="card-title text-gray-700">Mensagens</h3>
            <div className="text-4xl font-bold text-primary">0</div>
          </div>
        </div>
      </div>
    </div>
  )
}