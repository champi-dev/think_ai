#!/usr/bin/env python3
"""
Nobel Prize Experience - Versión Simple
¡Vive la experiencia de ganar el Nobel de Física!
"""

import asyncio
import webbrowser
import os
import time


async def launch_nobel_experience():
    """Lanza la experiencia del Premio Nobel."""
    
    print("🏆 EXPERIENCIA PREMIO NOBEL DE FÍSICA")
    print("="*50)
    print("¡Prepárate para vivir el momento más grande de tu carrera!")
    print()
    
    # Preparación mental
    print("🧠 Preparación Mental:")
    print("-"*30)
    print("¡Ey mi llave! Vas a ganar el Nobel de Física.")
    print("Respira profundo. Has trabajado duro para esto.")
    print("Cuando te llamen de Estocolmo, no te desmayes.")
    print("Y recuerda: ¡Dale que vamos tarde pero el tiempo es relativo!")
    print()
    
    await asyncio.sleep(2)
    
    # Abrir la experiencia
    file_path = os.path.join(os.path.dirname(__file__), "nobel_prize_experience.html")
    print("🌟 Abriendo experiencia inmersiva...")
    
    # Abrir en browser
    webbrowser.open(f"file://{file_path}")
    
    await asyncio.sleep(1)
    
    # Datos curiosos mientras se carga
    print("\n📚 Datos curiosos sobre el Nobel de Física:")
    print("• Solo 4 mujeres lo han ganado en toda la historia")
    print("• Einstein lo ganó en 1921 (no por la relatividad)")
    print("• Puedes ganar hasta 1/3 del premio (máximo 3 ganadores)")
    print("• La medalla pesa 175 gramos de oro de 18 quilates")
    print("• Colombia nunca ha tenido un Nobel de Física... ¡hasta hoy!")
    
    await asyncio.sleep(3)
    
    print("\n🎬 FASES DE TU EXPERIENCIA NOBEL:")
    print("="*40)
    
    phases = [
        "🔬 Fase 1: Tu descubrimiento revolucionario",
        "📞 Fase 2: La llamada de Estocolmo", 
        "📺 Fase 3: El anuncio mundial",
        "🏛️ Fase 4: La ceremonia en Suecia",
        "🎤 Fase 5: Tu conferencia Nobel",
        "🇨🇴 Fase 6: Celebración en Colombia",
        "⭐ Fase 7: Tu legado eterno"
    ]
    
    for phase in phases:
        print(f"   {phase}")
        await asyncio.sleep(0.5)
    
    print("\n✨ Tips para tu experiencia:")
    print("• Escribe un descubrimiento creativo")
    print("• Prepara un discurso épico")
    print("• ¡Disfruta cada momento!")
    print("• No olvides agradecer a Colombia")
    
    print("\n🌟 ¡La experiencia ya está cargada en tu navegador!")
    print("¡Disfruta tu momento de gloria, futuro Nobel! 🏆")
    print("\n¡Dale que eres un genio! 🧠✨")


if __name__ == "__main__":
    print("🚀 Iniciando experiencia Nobel...")
    asyncio.run(launch_nobel_experience())