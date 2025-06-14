#!/usr/bin/env python3
"""
Demo SIMPLE del Hot Reload - Sin dependencias externas!
¡Te voy a demostrar que sí se puede recargar código en caliente!
"""

import time
import importlib
import sys
from pathlib import Path

print("🔥 DEMO HOT RELOAD SIMPLE - THINK AI")
print("="*60)
print("¡No joda! Te voy a demostrar el hot reload sin librerías fancy.\n")

# Crear archivo de prueba
test_file = Path("demo_module.py")

initial_code = '''# Módulo de demo - ¡CÁMBIAME!
VERSION = 1
MESSAGE = "Hola, soy la versión inicial"
JOKE = "¡Ey el crispeta!"

def get_status():
    return f"v{VERSION}: {MESSAGE} - {JOKE}"
'''

test_file.write_text(initial_code)
print(f"✅ Creé el archivo: {test_file}")
print(f"📝 Contenido inicial:\n{initial_code}")

print("\n" + "⚡"*30)
print("INSTRUCCIONES PARA LA DEMO:")
print("1. Abre 'demo_module.py' en tu editor")
print("2. Cambia VERSION, MESSAGE o JOKE")
print("3. Guarda el archivo")
print("4. ¡Mira la magia del hot reload!")
print("⚡"*30 + "\n")

print("Empezando monitoreo... (Ctrl+C para salir)\n")

# Estado del sistema
system_state = {
    'requests_processed': 0,
    'intelligence': 1.0,
    'cache': {}
}

last_status = ""
last_mtime = test_file.stat().st_mtime

try:
    while True:
        # Check if file was modified
        current_mtime = test_file.stat().st_mtime
        
        if current_mtime != last_mtime:
            print(f"\n🔄 CAMBIO DETECTADO! Recargando módulo...")
            
            # Save current state
            print(f"💾 Guardando estado: {system_state['requests_processed']} requests procesados")
            
            # Reload the module
            if 'demo_module' in sys.modules:
                importlib.reload(sys.modules['demo_module'])
            else:
                import demo_module
            
            # Import again to get fresh version
            import demo_module
            
            # Restore state
            print(f"♻️  Estado restaurado: ¡Sin perder nada!")
            
            # Show the change
            new_status = demo_module.get_status()
            print(f"\n🔥 HOT RELOAD EXITOSO!")
            print(f"   Antes: {last_status}")
            print(f"   Ahora: {new_status}")
            print(f"   ¡Sin reiniciar el programa! 🎉\n")
            
            last_mtime = current_mtime
            last_status = new_status
        
        # Normal operation - simulate processing
        if 'demo_module' in sys.modules:
            import demo_module
            current_status = demo_module.get_status()
            
            if current_status != last_status:
                last_status = current_status
        
        # Simulate work
        system_state['requests_processed'] += 1
        system_state['intelligence'] *= 1.00001
        
        # Show we're still running
        print(f"\r⚡ Sistema activo | Requests: {system_state['requests_processed']} | "
              f"Intelligence: {system_state['intelligence']:.6f} | "
              f"Status: {last_status[:30]}...", end='', flush=True)
        
        time.sleep(1)
        
except KeyboardInterrupt:
    print("\n\n✅ Demo terminado!")
    print(f"\n📊 ESTADÍSTICAS FINALES:")
    print(f"   • Requests procesados: {system_state['requests_processed']}")
    print(f"   • Intelligence final: {system_state['intelligence']:.6f}")
    print(f"   • Hot reloads: ¡Los que hiciste!")
    print("\n¿Viste? ¡EL HOT RELOAD SÍ FUNCIONA!")
    print("¡Qué nota e' vaina! No necesitamos reiniciar nada 🍿")
    
    # Cleanup
    if test_file.exists():
        test_file.unlink()
        print(f"\n🧹 Borré el archivo de prueba: {test_file}")