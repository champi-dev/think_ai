"""Wrapper for CLI entry points to handle async execution properly."""

import asyncio
import sys
import os

# Prevent eager imports of heavy modules
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow warnings
os.environ['TOKENIZERS_PARALLELISM'] = 'false'  # Suppress tokenizer warnings


def main():
    """Entry point for think-ai command."""
    # Import only when needed to avoid circular imports
    try:
        # Temporarily modify sys.modules to prevent torch issues
        import sys
        _torch = sys.modules.get('torch', None)
        if _torch is None:
            # Create a minimal torch module stub
            import types
            torch_stub = types.ModuleType('torch')
            torch_stub.Tensor = type('Tensor', (), {})
            sys.modules['torch'] = torch_stub
        
        from .cli.main import main as async_main
        
        # Handle Windows event loop policy
        if sys.platform.startswith("win"):
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
        asyncio.run(async_main())
    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋")
        sys.exit(0)
    except ImportError as e:
        print(f"Import Error: {e}")
        print("\nPlease ensure all dependencies are installed:")
        print("  pip install -e .")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def full_cli():
    """Entry point for think-ai-full command (standalone full CLI)."""
    import subprocess
    import os
    
    # Run the full CLI script
    script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "think_ai_full_cli.py")
    subprocess.run([sys.executable, script_path])


def simple_chat():
    """Entry point for think-ai-chat command (simple chat)."""
    import subprocess
    import os
    
    # Run the simple chat script
    script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "think_ai_simple_chat.py")
    subprocess.run([sys.executable, script_path])


def server():
    """Entry point for think-ai-server command."""
    from .api.server import create_app
    import uvicorn
    
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8080)