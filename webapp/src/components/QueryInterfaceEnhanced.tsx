import { useState } from 'react'
import { motion } from 'framer-motion'
import { useThinkAIStore } from '../lib/store'
import React from 'react'

export default function QueryInterfaceEnhanced() {
  const [query, setQuery] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const { responses, addResponse } = useThinkAIStore()
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim() || isLoading) return
    
    setIsLoading(true)
    
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080'}/api/think`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query,
          enable_consciousness: true,
          temperature: 0.7,
          max_tokens: 50000 // Increased for code generation
        })
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      
      addResponse({
        id: Date.now().toString(),
        query,
        response: data.response,
        consciousness_state: data.consciousness_state,
        has_code: data.has_code || false,
        response_type: data.response_type || 'text',
        timestamp: new Date()
      })
      
      setQuery('')
    } catch (error) {
      console.error('Query failed:', error)
      addResponse({
        id: Date.now().toString(),
        query,
        response: `Error: ${error instanceof Error ? error.message : 'Failed to process query'}`,
        consciousness_state: undefined,
        has_code: false,
        response_type: 'error',
        timestamp: new Date()
      })
    } finally {
      setIsLoading(false)
    }
  }
  
  const renderResponse = (response: string, hasCode: boolean) => {
    if (!hasCode) {
      return <div className="text-gray-200 whitespace-pre-wrap">{response}</div>
    }
    
    // Parse and render code blocks
    const parts = response.split('```')
    return (
      <div className="text-gray-200 space-y-2">
        {parts.map((part, index) => {
          if (index % 2 === 0) {
            // Regular text
            return part.trim() ? (
              <div key={index} className="whitespace-pre-wrap">{part.trim()}</div>
            ) : null
          } else {
            // Code block
            const [language, ...codeLines] = part.split('\n')
            const code = codeLines.join('\n').trim()
            return (
              <div key={index} className="relative group">
                <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
                  <button
                    onClick={() => navigator.clipboard.writeText(code)}
                    className="px-2 py-1 bg-purple-600/20 hover:bg-purple-600/30 text-purple-400 text-xs rounded"
                  >
                    Copy
                  </button>
                </div>
                <pre className="bg-black/50 border border-purple-500/20 rounded-lg p-4 overflow-x-auto">
                  <code className="text-sm text-green-400">{code}</code>
                </pre>
                {language && (
                  <div className="text-xs text-purple-400 mt-1">Language: {language}</div>
                )}
              </div>
            )
          }
        })}
      </div>
    )
  }
  
  return (
    <div className="space-y-4">
      <form onSubmit={handleSubmit} className="relative">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault()
              handleSubmit(e)
            }
          }}
          placeholder="Ask me to code something..."
          className="w-full pl-4 pr-12 py-3 bg-black/30 border border-purple-500/20 rounded-full text-white placeholder-gray-400 focus:outline-none focus:border-purple-500 transition-colors"
          disabled={isLoading}
        />
        
        <motion.button
          type="submit"
          disabled={isLoading || !query.trim()}
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          className="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-purple-400 hover:text-purple-300 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        >
          {isLoading ? (
            <svg className="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          ) : (
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          )}
        </motion.button>
      </form>
      
      {responses.length > 0 && (
        <div className="space-y-3 max-h-96 overflow-y-auto">
          {responses.slice(-5).reverse().map((response, index) => (
            <motion.div
              key={response.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="p-4 bg-black/20 rounded-lg border border-white/10"
            >
              <div className="flex items-center justify-between mb-2">
                <div className="text-sm text-gray-400">
                  {response.timestamp.toLocaleTimeString()}
                </div>
                {response.has_code && (
                  <div className="text-xs px-2 py-1 bg-green-600/20 text-green-400 rounded">
                    Contains Code
                  </div>
                )}
              </div>
              
              <div className="text-purple-400 mb-3 font-medium">Q: {response.query}</div>
              
              <div className="response-content">
                {renderResponse(response.response, response.has_code || false)}
              </div>
              
              {response.consciousness_state && (
                <div className="mt-4 pt-3 border-t border-white/10 text-xs text-gray-400 grid grid-cols-2 gap-2">
                  <div>Attention: {response.consciousness_state.attention_focus}</div>
                  <div>Flow: {response.consciousness_state.consciousness_flow}</div>
                  <div>Awareness: {(response.consciousness_state.awareness_level * 100).toFixed(0)}%</div>
                  <div>Type: {response.consciousness_state.response_type}</div>
                </div>
              )}
            </motion.div>
          ))}
        </div>
      )}
      
      <div className="text-xs text-gray-500 text-center">
        Try: "build a simple API", "create a pizza ordering app", "write CI/CD pipeline"
      </div>
    </div>
  )
}