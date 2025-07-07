import { CheckCircle, Loader2, Brain, Search, Lightbulb, ExternalLink} from "lucide-react"

export default function AgentWorkflow() {

  console.log("Props in AgentWorkflow:", props.stages);

  const stages = props.stages || [
    { id: 'planning-011', type: 'planning', text: 'Planning', status: 'pending', queries: [] },
    { id: 'searching-012', type: 'searching', text: 'Spinning up search bots', status: 'pending', queries: ['Hello Word4', 'Hello Word5', 'Hello Word6'] },
    { id: 'gathering-013', type: 'gathering', text: 'Gathering thoughts', status: 'pending', queries: [] }
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

  const getIconStyle = (status) => {
    switch (status) {
      case 'active':
        return 'h-4 w-4 text-blue-600'
      case 'finished':
        return 'h-4 w-4 text-green-600'
      case 'pending':
      default:
        return 'h-4 w-4 text-gray-600'
    }
  }

  

  const getQueries = ( queries ) => {
    if (queries.length === 0) {
      return null
    }
  
    return (
      <div className="flex flex-wrap gap-1 mt-1">
        {queries.map((query, index) => (
          <div key={index} className="flex items-center border border-gray-600" style={{
            padding: '1px 4px',
            fontSize: '10px',
            gap: '2px',
            borderRadius: '4px'
          }}>
            <Search className="text-gray-500" style={{
              width: '8px',
              height: '8px',
              minWidth: '8px'
            }} />
            <a 
              href={`https://www.google.com/search?q=${encodeURIComponent(query)}`}
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-600 font-mono truncate hover:text-blue-600 hover:underline"
              style={{
                maxWidth: '150px',
                lineHeight: '1.2'
              }} 
              title={query}
            >
              {query}
            </a>
          </div>
        ))}
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg p-4 shadow-sm max-w-md">
      <div className="space-y-1">
        {stages.map((stage, index) => {
          const Icon = getIcon(stage.type)
          
          return (
            <div key={stage.id} className="mb-3"> {/* or mb-[14px] */}
              <div className="flex items-center gap-3">
                {getStatusIcon(stage.status)}
                <Icon className={getIconStyle(stage.status)} />
                <div className="flex items-center gap-1 flex-1">
                  <span className={`text-sm ${getTextStyle(stage.status)}`}>
                    {stage.text}
                  </span>
                </div>
              </div>
              {getQueries(stage.queries)}
            </div>
          )
        })}
      </div>
    </div>
  )
} 