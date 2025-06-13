import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { useThinkAIStore } from '../lib/store'

export default function IntelligenceDashboard() {
  const { intelligenceMetrics } = useThinkAIStore()
  const [isTraining, setIsTraining] = useState(false)
  
  const startTraining = async () => {
    setIsTraining(true)
    
    try {
      await fetch('/api/training/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          mode: 'parallel',
          target_iq: 1000000,
          parallel_tests: 5
        })
      })
    } catch (error) {
      console.error('Failed to start training:', error)
      setIsTraining(false)
    }
  }
  
  const stopTraining = async () => {
    try {
      await fetch('/api/training/stop', { method: 'POST' })
      setIsTraining(false)
    } catch (error) {
      console.error('Failed to stop training:', error)
    }
  }
  
  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const response = await fetch('/api/intelligence')
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        const data = await response.json()
        if (data) {
          useThinkAIStore.getState().setIntelligenceMetrics(data)
        }
      } catch (error) {
        console.error('Failed to fetch intelligence metrics:', error)
      }
    }, 5000)
    
    return () => clearInterval(interval)
  }, [])
  
  const formatNumber = (num: number) => {
    return new Intl.NumberFormat('en-US').format(num)
  }
  
  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">Intelligence Metrics</h2>
      
      <div className="grid grid-cols-2 gap-4">
        <motion.div
          whileHover={{ scale: 1.05 }}
          className="p-4 bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-lg border border-purple-500/30"
        >
          <div className="text-sm text-gray-400">Current IQ</div>
          <div className="text-3xl font-bold text-white">
            {formatNumber(intelligenceMetrics.iq)}
          </div>
        </motion.div>
        
        <motion.div
          whileHover={{ scale: 1.05 }}
          className="p-4 bg-gradient-to-br from-blue-500/20 to-cyan-500/20 rounded-lg border border-blue-500/30"
        >
          <div className="text-sm text-gray-400">Knowledge Base</div>
          <div className="text-3xl font-bold text-white">
            {formatNumber(intelligenceMetrics.knowledge_count)}
          </div>
        </motion.div>
        
        <motion.div
          whileHover={{ scale: 1.05 }}
          className="p-4 bg-gradient-to-br from-green-500/20 to-emerald-500/20 rounded-lg border border-green-500/30"
        >
          <div className="text-sm text-gray-400">Training Cycles</div>
          <div className="text-3xl font-bold text-white">
            {formatNumber(intelligenceMetrics.training_cycles)}
          </div>
        </motion.div>
        
        <motion.div
          whileHover={{ scale: 1.05 }}
          className="p-4 bg-gradient-to-br from-orange-500/20 to-red-500/20 rounded-lg border border-orange-500/30"
        >
          <div className="text-sm text-gray-400">Consciousness</div>
          <div className="text-3xl font-bold text-white">
            {(intelligenceMetrics.consciousness_level * 100).toFixed(1)}%
          </div>
        </motion.div>
      </div>
      
      <div className="space-y-4">
        <h3 className="text-lg font-semibold">Self-Training Control</h3>
        
        {!isTraining ? (
          <motion.button
            onClick={startTraining}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="w-full py-3 bg-gradient-to-r from-green-500 to-emerald-500 rounded-lg font-semibold transition-all"
          >
            Start Training
          </motion.button>
        ) : (
          <motion.button
            onClick={stopTraining}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="w-full py-3 bg-gradient-to-r from-red-500 to-orange-500 rounded-lg font-semibold transition-all"
          >
            Stop Training
          </motion.button>
        )}
        
        <div className="p-4 bg-yellow-500/10 border border-yellow-500/30 rounded-lg">
          <div className="text-sm text-yellow-400">
            {isTraining ? '🔄 Training in progress...' : '⏸️ Training paused'}
          </div>
          <div className="text-xs text-gray-400 mt-1">
            Target IQ: 1,000,000 | Mode: Parallel
          </div>
        </div>
      </div>
      
      <div className="mt-6">
        <h3 className="text-lg font-semibold mb-3">IQ Evolution</h3>
        <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
          <motion.div
            className="h-full bg-gradient-to-r from-purple-500 to-pink-500"
            initial={{ width: '0%' }}
            animate={{ width: `${Math.min((intelligenceMetrics.iq / 1000000) * 100, 100)}%` }}
            transition={{ duration: 2, ease: 'easeInOut' }}
          />
        </div>
        <div className="flex justify-between text-xs text-gray-400 mt-1">
          <span>1,000</span>
          <span>1,000,000</span>
        </div>
      </div>
    </div>
  )
}