import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import { useThinkAIStore } from '../lib/store'

export default function ConsciousnessVisualization() {
  const meshRef = useRef<THREE.Mesh>(null)
  const particlesRef = useRef<THREE.Points>(null)
  const { consciousnessState } = useThinkAIStore()
  
  const particleCount = 1000
  
  const [positions, colors] = useMemo(() => {
    const positions = new Float32Array(particleCount * 3)
    const colors = new Float32Array(particleCount * 3)
    
    for (let i = 0; i < particleCount; i++) {
      const theta = Math.random() * Math.PI * 2
      const phi = Math.acos(2 * Math.random() - 1)
      const radius = 5 + Math.random() * 5
      
      positions[i * 3] = radius * Math.sin(phi) * Math.cos(theta)
      positions[i * 3 + 1] = radius * Math.sin(phi) * Math.sin(theta)
      positions[i * 3 + 2] = radius * Math.cos(phi)
      
      colors[i * 3] = Math.random()
      colors[i * 3 + 1] = Math.random() * 0.5
      colors[i * 3 + 2] = Math.random() * 0.8 + 0.2
    }
    
    return [positions, colors]
  }, [])
  
  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.x += 0.001
      meshRef.current.rotation.y += 0.002
      
      const scale = 1 + Math.sin(state.clock.elapsedTime) * 0.1
      meshRef.current.scale.set(scale, scale, scale)
    }
    
    if (particlesRef.current) {
      particlesRef.current.rotation.y += 0.0005
      
      const positions = particlesRef.current.geometry.attributes.position.array as Float32Array
      const time = state.clock.elapsedTime
      
      for (let i = 0; i < particleCount; i++) {
        const i3 = i * 3
        const x = positions[i3]
        const y = positions[i3 + 1]
        const z = positions[i3 + 2]
        
        const wave = Math.sin(time + i * 0.01) * 0.1
        positions[i3 + 1] = y + wave
      }
      
      particlesRef.current.geometry.attributes.position.needsUpdate = true
    }
  })
  
  return (
    <group>
      <mesh ref={meshRef}>
        <icosahedronGeometry args={[3, 4]} />
        <meshPhongMaterial
          color="#6366f1"
          emissive="#4338ca"
          emissiveIntensity={0.5}
          wireframe
          transparent
          opacity={0.3}
        />
      </mesh>
      
      <points ref={particlesRef}>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            count={particleCount}
            array={positions}
            itemSize={3}
          />
          <bufferAttribute
            attach="attributes-color"
            count={particleCount}
            array={colors}
            itemSize={3}
          />
        </bufferGeometry>
        <pointsMaterial
          size={0.1}
          vertexColors
          transparent
          opacity={0.8}
          blending={THREE.AdditiveBlending}
        />
      </points>
    </group>
  )
}