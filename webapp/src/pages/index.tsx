import { Canvas } from '@react-three/fiber'
import { OrbitControls, Stars, Float } from '@react-three/drei'
import { EffectComposer, Bloom, ChromaticAberration } from '@react-three/postprocessing'
import { Vector2 } from 'three'
import { motion } from 'framer-motion'
import { useEffect, useState, useRef } from 'react'
import ConsciousnessVisualization from '../components/ConsciousnessVisualization'
import NeuralNetwork from '../components/NeuralNetwork'
import QueryInterfaceEnhanced from '../components/QueryInterfaceEnhanced'
import IntelligenceDashboard from '../components/IntelligenceDashboard'
import { useThinkAIStore } from '../lib/store'

export default function Home() {
  const [socket, setSocket] = useState<WebSocket | null>(null)
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null)
  const { setConsciousnessState, setIntelligenceMetrics } = useThinkAIStore()

  // Log intelligence metrics periodically
  useEffect(() => {
    const logInterval = setInterval(async () => {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080'}/api/v1/intelligence`)
        if (response.ok) {
          const data = await response.json()
          console.log('🧠 Intelligence Metrics:', {
            iq: data.iq,
            knowledge: data.knowledge_count,
            training_cycles: data.training_cycles,
            consciousness: `${(data.consciousness_level * 100).toFixed(1)}%`
          })
        }
      } catch (error) {
        // Silently fail - don't clutter console with errors
      }
    }, 5000)
    
    return () => clearInterval(logInterval)
  }, [])

  useEffect(() => {
    let ws: WebSocket | null = null
    let reconnectAttempts = 0
    const maxReconnectAttempts = 5
    
    const connectWebSocket = () => {
      console.log('Connecting to WebSocket...')
      
      // Connect to the API server WebSocket endpoint
      const wsUrl = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8080/api/v1/ws'
      
      ws = new WebSocket(wsUrl)
      
      ws.onopen = () => {
        console.log('WebSocket connected')
        setSocket(ws)
        reconnectAttempts = 0
      }
      
      ws.onmessage = async (event) => {
        try {
          let messageData;
          
          // Handle both text and blob data
          if (event.data instanceof Blob) {
            const text = await event.data.text()
            messageData = JSON.parse(text)
          } else {
            messageData = JSON.parse(event.data)
          }
          
          // Handle consciousness state updates (direct format from Python API)
          if (messageData.attention_focus && messageData.consciousness_flow) {
            setConsciousnessState(messageData)
          } 
          // Handle wrapped messages
          else if (messageData.type === 'consciousness_update') {
            setConsciousnessState(messageData.payload || messageData.data)
          } else if (messageData.type === 'intelligence_update') {
            setIntelligenceMetrics(messageData.payload || messageData.data)
          }
          // Handle intelligence data
          else if (messageData.iq && messageData.consciousness_level) {
            setIntelligenceMetrics(messageData)
          }
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error)
        }
      }
      
      ws.onerror = (error) => {
        console.error('WebSocket error:', error)
      }
      
      ws.onclose = () => {
        console.log('WebSocket disconnected')
        setSocket(null)
        
        // Attempt to reconnect
        if (reconnectAttempts < maxReconnectAttempts) {
          reconnectAttempts++
          console.log(`Reconnecting... (attempt ${reconnectAttempts}/${maxReconnectAttempts})`)
          const delay = Math.min(5000 * reconnectAttempts, 30000) // Exponential backoff up to 30 seconds
          reconnectTimeoutRef.current = setTimeout(connectWebSocket, delay)
        }
      }
    }
    
    connectWebSocket()
    
    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current)
      }
      if (ws) {
        ws.close()
      }
    }
  }, [setConsciousnessState, setIntelligenceMetrics])

  return (
    <div className="min-h-screen bg-black text-white overflow-hidden">
      <div className="fixed inset-0 z-0">
        <Canvas
          camera={{ position: [0, 0, 30], fov: 75 }}
          gl={{ antialias: true, alpha: true }}
        >
          <color attach="background" args={['#000000']} />
          <fog attach="fog" args={['#000000', 10, 100]} />
          
          <ambientLight intensity={0.1} />
          <pointLight position={[10, 10, 10]} intensity={0.5} />
          <pointLight position={[-10, -10, -10]} intensity={0.5} color="#6366f1" />
          
          <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />
          
          <Float speed={1} rotationIntensity={1} floatIntensity={2}>
            <ConsciousnessVisualization />
          </Float>
          
          <NeuralNetwork />
          
          <OrbitControls
            enablePan={true}
            enableZoom={true}
            enableRotate={true}
            zoomSpeed={0.6}
            panSpeed={0.5}
            rotateSpeed={0.4}
          />
          
          <EffectComposer>
            <Bloom
              intensity={0.5}
              luminanceThreshold={0.2}
              luminanceSmoothing={0.9}
              height={300}
            />
            <ChromaticAberration
              offset={new Vector2(0.0005, 0.0012)}
              radialModulation={false}
              modulationOffset={0}
            />
          </EffectComposer>
        </Canvas>
      </div>

      <div className="relative z-10">

        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 0.8, y: 0 }}
          transition={{ delay: 0.5, duration: 1 }}
          className="fixed bottom-0 left-0 right-0 p-4"
        >
          <div className="max-w-2xl mx-auto">
            <div className="bg-black/40 backdrop-blur-sm rounded-lg p-3 border border-white/10">
              <QueryInterfaceEnhanced />
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}