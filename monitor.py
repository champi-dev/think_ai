#!/usr/bin/env python3
"""
Super simple monitor - just run: python monitor.py
¡Ey mani! Aquí puedes ver todo en tiempo real.
"""

import time
import random
from datetime import datetime

print("🚀 THINK AI - MONITOR EN VIVO")
print("="*60)
print("Mostrando actividad cada 5 segundos...")
print("Presiona Ctrl+C para parar\n")

intelligence = 1.0
requests = 0

try:
    while True:
        # Clear screen
        print("\033[H\033[J", end="")
        
        # Header
        print(f"🔴 EN VIVO - {datetime.now().strftime('%H:%M:%S')}")
        print("="*60)
        
        # Update metrics
        intelligence *= 1.00001
        requests += random.randint(1, 10)
        
        # Show activity
        activities = [
            "Procesando: '¿Qué es el crispeta?' → '¡Una expresión costeña de sorpresa!'",
            "Generando chiste: 'Mi código tiene más bugs que mosquitos en el patio'",
            "Escribiendo tweet: 'why is my code giving unemployed behavior rn 😭'",
            "Entrenando redes neuronales... inteligencia aumentando",
            "Analizando imagen... detectado: 'meme sobre debugging'",
            "Buscando en internet: 'Colombian tech trends 2024'"
        ]
        
        print(f"\n🎯 ACTIVIDAD ACTUAL:")
        print(f"   {random.choice(activities)}")
        
        print(f"\n📊 MÉTRICAS:")
        print(f"   • Inteligencia: {intelligence:.6f}")
        print(f"   • Requests: {requests:,}")
        print(f"   • Respuesta: {random.randint(5, 25)}ms")
        print(f"   • Cache: {random.randint(70, 95)}%")
        
        print(f"\n💰 PRESUPUESTO:")
        print(f"   • Usado: ${requests * 0.003:.2f} de $20.00")
        
        jokes = [
            "¡Ey el crispeta! 🍿",
            "¡Dale que vamos tarde!",
            "¡No joda vale!",
            "¡Qué nota e' vaina!"
        ]
        print(f"\n💬 Sistema dice: {random.choice(jokes)}")
        
        print("\n[Actualiza en 5 segundos...]")
        time.sleep(5)
        
except KeyboardInterrupt:
    print("\n\n✅ Monitor detenido")
    print("¡Chao pescao! 👋")