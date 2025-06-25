import { useRef, useMemo } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";
import { getPerformanceSettings, createFrameLimiter } from "../lib/performance";

interface Node {
  position: THREE.Vector3;
  connections: number[];
}

export default function NeuralNetwork() {
  const groupRef = useRef<THREE.Group>(null);
  const linesRef = useRef<THREE.LineSegments>(null);
  const perfSettings = getPerformanceSettings();
  const frameLimiter = useMemo(
    () => createFrameLimiter(perfSettings.targetFPS),
    [perfSettings.targetFPS],
  );

  const { nodes, linePositions } = useMemo(() => {
    const layerSizes = [5, 8, 12, 8, 5];
    const nodes: Node[] = [];
    const connections: [number, number][] = [];

    let nodeIndex = 0;
    layerSizes.forEach((size, layerIndex) => {
      const layerZ = (layerIndex - 2) * 4;

      for (let i = 0; i < size; i++) {
        const angle = (i / size) * Math.PI * 2;
        const radius = 8;

        nodes.push({
          position: new THREE.Vector3(
            Math.cos(angle) * radius,
            Math.sin(angle) * radius,
            layerZ,
          ),
          connections: [],
        });

        if (layerIndex > 0) {
          const prevLayerStart = nodeIndex - layerSizes[layerIndex - 1];
          const prevLayerSize = layerSizes[layerIndex - 1];

          for (let j = 0; j < prevLayerSize; j++) {
            if (Math.random() > 1 - perfSettings.neuralNetworkConnections) {
              connections.push([nodeIndex, prevLayerStart + j]);
              nodes[nodeIndex].connections.push(prevLayerStart + j);
            }
          }
        }

        nodeIndex++;
      }
    });

    const linePositions = new Float32Array(connections.length * 6);
    connections.forEach(([a, b], i) => {
      const i6 = i * 6;
      linePositions[i6] = nodes[a].position.x;
      linePositions[i6 + 1] = nodes[a].position.y;
      linePositions[i6 + 2] = nodes[a].position.z;
      linePositions[i6 + 3] = nodes[b].position.x;
      linePositions[i6 + 4] = nodes[b].position.y;
      linePositions[i6 + 5] = nodes[b].position.z;
    });

    return { nodes, linePositions };
  }, []);

  useFrame((state) => {
    frameLimiter(() => {
      if (groupRef.current) {
        groupRef.current.rotation.z += 0.001 * perfSettings.animationSpeed;
      }

      if (linesRef.current && perfSettings.animationSpeed > 0) {
        const time = state.clock.elapsedTime;
        const material = linesRef.current.material as THREE.LineBasicMaterial;

        const hue =
          (Math.sin(time * 0.5 * perfSettings.animationSpeed) + 1) * 0.5;
        material.color.setHSL(hue, 0.7, 0.5);
      }
    });
  });

  return (
    <group ref={groupRef} position={[0, 0, -10]}>
      {nodes.map((node, i) => (
        <mesh key={i} position={node.position}>
          <sphereGeometry
            args={[
              0.3,
              perfSettings.sphereSegments,
              perfSettings.sphereSegments,
            ]}
          />
          <meshPhongMaterial
            color="#ffffff"
            emissive="#6366f1"
            emissiveIntensity={0.5}
          />
        </mesh>
      ))}

      <lineSegments ref={linesRef}>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            count={linePositions.length / 3}
            array={linePositions}
            itemSize={3}
          />
        </bufferGeometry>
        <lineBasicMaterial
          color="#6366f1"
          transparent
          opacity={0.3}
          blending={THREE.AdditiveBlending}
        />
      </lineSegments>
    </group>
  );
}
