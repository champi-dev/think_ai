import { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

export default function Particles() {
  const particlesRef = useRef();
  const particleCount = 300;

  const [positions, colors] = useMemo(() => {
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);

    const color1 = new THREE.Color('#6366f1'); // Primary
    const color2 = new THREE.Color('#8b5cf6'); // Accent 1
    const color3 = new THREE.Color('#06b6d4'); // Accent 2

    for (let i = 0; i < particleCount; i++) {
      // Random position within bounds
      positions[i * 3] = (Math.random() - 0.5) * 120;
      positions[i * 3 + 1] = (Math.random() - 0.5) * 80;
      positions[i * 3 + 2] = (Math.random() - 0.5) * 40;

      // Random color from palette
      const colorChoice = Math.random();
      const color = colorChoice < 0.33 ? color1 : colorChoice < 0.66 ? color2 : color3;

      colors[i * 3] = color.r;
      colors[i * 3 + 1] = color.g;
      colors[i * 3 + 2] = color.b;
    }

    return [positions, colors];
  }, []);

  useFrame((state) => {
    if (!particlesRef.current) return;

    const time = state.clock.getElapsedTime();

    // Gentle drift animation
    for (let i = 0; i < particleCount; i++) {
      const i3 = i * 3;

      particlesRef.current.geometry.attributes.position.array[i3] += Math.sin(time * 0.2 + i) * 0.002;
      particlesRef.current.geometry.attributes.position.array[i3 + 1] += Math.cos(time * 0.15 + i) * 0.002;
    }

    particlesRef.current.geometry.attributes.position.needsUpdate = true;

    // Gentle rotation
    particlesRef.current.rotation.y = time * 0.02;
  });

  return (
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
        size={0.15}
        vertexColors
        transparent
        opacity={0.6}
        sizeAttenuation
        depthWrite={false}
      />
    </points>
  );
}
