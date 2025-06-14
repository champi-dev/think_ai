#!/usr/bin/env python3
"""
Nobel Prize Experience with Think AI
¡Vive la experiencia de ganar el Nobel de Física!
"""

import asyncio
import webbrowser
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from implement_proper_architecture import ThinkAI


async def launch_nobel_experience():
    """Lanza la experiencia del Premio Nobel."""
    think_ai = ThinkAI()
    
    print("🏆 EXPERIENCIA PREMIO NOBEL DE FÍSICA")
    print("="*50)
    print("¡Prepárate para vivir el momento más grande de tu carrera!")
    print()
    
    # Think AI te prepara
    context = "Prepárame emocionalmente para ganar el Premio Nobel de Física"
    response = await think_ai.process_request(context)
    
    print("🧠 Think AI dice:")
    print("-"*30)
    print("¡Ey mi llave! Vas a ganar el Nobel de Física.")
    print("Respira profundo. Has trabajado duro para esto.")
    print("Cuando te llamen de Estocolmo, no te desmayes.")
    print("Y recuerda: ¡Dale que vamos tarde pero el tiempo es relativo!")
    print()
    
    # Abrir la experiencia
    file_path = os.path.join(os.path.dirname(__file__), "nobel_prize_experience.html")
    print("🌟 Abriendo experiencia inmersiva...")
    webbrowser.open(f"file://{file_path}")
    
    # Datos curiosos mientras se carga
    print("\n📚 Datos curiosos sobre el Nobel de Física:")
    print("• Solo 4 mujeres lo han ganado en toda la historia")
    print("• Einstein lo ganó en 1921 (no por la relatividad)")
    print("• Puedes ganar hasta 1/3 del premio (máximo 3 ganadores)")
    print("• La medalla pesa 175 gramos de oro de 18 quilates")
    print("• Colombia nunca ha tenido un Nobel de Física... ¡hasta hoy!")
    
    print("\n✨ ¡Disfruta tu momento de gloria!")
    print("🇨🇴 ¡Haz que Colombia se sienta orgullosa!")


if __name__ == "__main__":
    print("🚀 Iniciando experiencia Nobel...")
    asyncio.run(launch_nobel_experience())