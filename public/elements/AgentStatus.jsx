import { CheckCircle, Loader2, Brain, Search, Lightbulb } from "lucide-react"
import { useState, useEffect } from "react"

export default function AgentStatus() {
  const [isAnimating, setIsAnimating] = useState(true)

  const getIcon = (type) => {
    
    const icons = {
      'planning': Brain,
      'searching': Search,
      'gathering': Lightbulb
    }
    return icons[type] 
  }

  const getGradientClass = (type, status) => {
    if (status === 'finished') {
      return 'text-green-600'
    }
    
    const gradients = {
      'planning': 'bg-gradient-to-r from-blue-400 to-purple-500',
      'searching': 'bg-gradient-to-r from-orange-400 to-red-500', 
      'gathering': 'bg-gradient-to-r from-green-400 to-blue-500'
    }
    return gradients[type] || gradients['planning']
  }

  const AnimatedText = ({ text, isActive }) => {
    if (!isActive) {
      return <span className="text-gray-700">{text}</span>
    }

    return (
      <span className="inline-flex">
        {text.split('').map((char, index) => (
          <span
            key={index}
            className="animate-pulse"
            style={{
              animationDelay: `${index * 0.1}s`,
              animationDuration: '1.5s'
            }}
          >
            {char === ' ' ? '\u00A0' : char}
          </span>
        ))}
      </span>
    )
  }

  const type = props.type || 'planning'
  const status = props.status || 'active'
  const text = props.text || 'Processing...'
  const Icon = getIcon(type)

  return (
    <div className="flex items-center gap-2 px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg max-w-fit">
      {status === 'active' ? (
        <Loader2 className="h-4 w-4 animate-spin text-blue-500" />
      ) : (
        <CheckCircle className="h-4 w-4 text-green-500" />
      )}
      
      <Icon className="h-4 w-4 text-gray-600" />
      
      <div className="text-sm font-medium">
        {status === 'active' ? (
          <div className="flex items-center gap-1">
            <span 
              className={`bg-clip-text text-transparent ${getGradientClass(type, status)} animate-pulse`}
            >
              {text}
            </span>
            <div className="flex space-x-1">
              <div className="w-1 h-1 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0ms'}}></div>
              <div className="w-1 h-1 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '150ms'}}></div>
              <div className="w-1 h-1 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '300ms'}}></div>
            </div>
          </div>
        ) : (
          <span className="text-gray-700">{text}</span>
        )}
      </div>
    </div>
  )
} 