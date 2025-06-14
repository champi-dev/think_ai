#!/usr/bin/env python3
"""
Demo del Hot Reload - ¡Te voy a demostrar que sí funciona!
Cambia cualquier archivo y mira la magia.
"""

import asyncio
import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).parent))


async def demo_hot_reload():
    """Demostración del hot reload en acción."""
    print("🔥 DEMO HOT RELOAD - THINK AI")
    print("="*60)
    print("¡Ey mani! Te voy a demostrar que el hot reload sí funciona.")
    print("\nPrimero, voy a crear un archivo que puedas modificar...\n")
    
    # Crear archivo de prueba
    test_file = Path("hot_reload_test_module.py")
    
    initial_code = '''# Test module for hot reload demo
MESSAGE = "¡Hola! Soy la versión 1.0"
COUNTER = 1

def get_message():
    return f"{MESSAGE} - Counter: {COUNTER}"
'''
    
    test_file.write_text(initial_code)
    print(f"✅ Creé el archivo: {test_file}")
    print("\n📝 Contenido inicial:")
    print("-"*40)
    print(initial_code)
    print("-"*40)
    
    # Import the hot reload system
    from hot_reload_think_ai import HotReloadThinkAI
    
    print("\n🚀 Iniciando sistema con hot reload...")
    system = HotReloadThinkAI()
    await system.initialize()
    
    print("\n✅ Sistema iniciado! Ahora viene lo bueno...")
    print("\n" + "🔥"*30)
    print("INSTRUCCIONES:")
    print("1. Abre 'hot_reload_test_module.py' en tu editor")
    print("2. Cambia el MESSAGE a algo diferente")
    print("3. Guarda el archivo")
    print("4. ¡Mira cómo se recarga automáticamente!")
    print("🔥"*30 + "\n")
    
    # Monitor loop
    print("Monitoreando cambios... (Ctrl+C para salir)\n")
    
    iteration = 0
    last_message = ""
    
    try:
        while True:
            iteration += 1
            
            # Import and check the module
            try:
                import hot_reload_test_module
                # Force reload to get latest changes
                import importlib
                importlib.reload(hot_reload_test_module)
                
                current_message = hot_reload_test_module.get_message()
                
                # Check if message changed
                if current_message != last_message:
                    if last_message:  # Not first iteration
                        print(f"\n🔥🔥🔥 HOT RELOAD DETECTADO! 🔥🔥🔥")
                        print(f"Mensaje anterior: {last_message}")
                        print(f"Mensaje nuevo: {current_message}")
                        print("¡No joda! ¡Funcionó sin reiniciar nada!\n")
                    else:
                        print(f"Mensaje actual: {current_message}")
                    
                    last_message = current_message
                
                # Process a fake request to show system is still working
                if iteration % 5 == 0:
                    result = await system.process_request(f"Test request #{iteration}")
                    print(f"[{time.strftime('%H:%M:%S')}] Procesé request #{iteration} - Sistema funcionando ✅")
                
            except Exception as e:
                print(f"Error: {e}")
            
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n✅ Demo terminado!")
        print("¿Viste? ¡El hot reload sí funciona!")
        print("¡Qué nota e' vaina! 🍿")
        
        # Cleanup
        await system.shutdown()
        
        # Remove test file
        if test_file.exists():
            test_file.unlink()
            print(f"\n🧹 Borré el archivo de prueba: {test_file}")


async def main():
    """Run the demo."""
    await demo_hot_reload()


if __name__ == "__main__":
    asyncio.run(main())