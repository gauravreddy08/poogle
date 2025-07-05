import { CheckCircle, Loader2, Brain, Search, Lightbulb } from "lucide-react"

export default function AgentWorkflow(props) {

  const stages = props.stages || [
    { id: 'planning', text: 'Planning', status: 'pending' },
    { id: 'searching', text: 'Spinning up search bots', status: 'pending' },
    { id: 'gathering', text: 'Gathering thoughts', status: 'pending' }
  ];
  console.log("Stages used in AgentWorkflow:", stages);

  const getIcon = (name) => {
    const icons = {
      'planning': Brain,
      'searching': Search,
      'gathering': Lightbulb
    }
    return icons[name] || Brain
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'active':
        return <Loader2 className="h-4 w-4 animate-spin text-blue-500" />
      case 'finished':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'pending':
      default:
        return <div className="h-4 w-4 rounded-full border-2 border-gray-300"></div>
    }
  }

  const getTextStyle = (status) => {
    switch (status) {
      case 'active':
        return 'text-blue-600 font-medium'
      case 'finished':
        return 'text-green-600'
      case 'pending':
      default:
        return 'text-gray-500'
    }
  }

  const AnimatedDots = () => (
    <div className="flex space-x-1 ml-2">
      <div className="w-1 h-1 bg-blue-400 rounded-full animate-bounce" style={{animationDelay: '0ms'}}></div>
      <div className="w-1 h-1 bg-blue-400 rounded-full animate-bounce" style={{animationDelay: '150ms'}}></div>
      <div className="w-1 h-1 bg-blue-400 rounded-full animate-bounce" style={{animationDelay: '300ms'}}></div>
    </div>
  )

  return (
    <div className="bg-white rounded-lg p-4 shadow-sm max-w-md">
      <div className="space-y-3">
        {stages.map((stage, index) => {
          const Icon = getIcon(stage.id)
          
          return (
            <div key={stage.id} className="flex items-center gap-3">
              {getStatusIcon(stage.status)}
              <Icon className="h-4 w-4 text-gray-600" />
              <div className="flex items-center gap-1 flex-1">
                <span className={`text-sm ${getTextStyle(stage.status)}`}>
                  {stage.text}
                </span>
                {stage.status === 'active' && <AnimatedDots />}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
} 