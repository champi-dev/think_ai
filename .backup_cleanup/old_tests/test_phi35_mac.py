#!/usr/bin/env python3
"""Test Phi-3.5 Mini on macOS without bitsandbytes."""

import asyncio
import torch
import time
from transformers import AutoModelForCausalLM, AutoTokenizer

async def test_phi35_mac():
    """Test Phi-3.5 Mini model on macOS."""
    print("🧪 Testing Phi-3.5 Mini on macOS...")
    print("Note: Using float16 instead of 4-bit quantization due to macOS limitations")
    
    # Load model without quantization for macOS
    print("\n📥 Loading model (first time will download ~7.6GB)...")
    start = time.time()
    
    try:
        # For macOS, we'll use float16 without quantization
        model = AutoModelForCausalLM.from_pretrained(
            "microsoft/Phi-3.5-mini-instruct",
            device_map="auto",
            trust_remote_code=True,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True,
            attn_implementation="eager"  # Avoid flash attention issues
        )
        
        tokenizer = AutoTokenizer.from_pretrained(
            "microsoft/Phi-3.5-mini-instruct",
            trust_remote_code=True
        )
        
        load_time = time.time() - start
        print(f"✅ Model loaded in {load_time:.1f}s")
        
        # Check memory usage
        if torch.backends.mps.is_available():
            print("✅ Using Metal Performance Shaders (MPS)")
        
        # Test generation
        prompts = [
            "What is consciousness?",
            "Write a Python function to calculate factorial:",
            "Explain machine learning in simple terms:"
        ]
        
        for prompt in prompts:
            print(f"\n🔤 Prompt: '{prompt}'")
            
            messages = [{"role": "user", "content": prompt}]
            inputs = tokenizer.apply_chat_template(
                messages, 
                return_tensors="pt", 
                add_generation_prompt=True
            )
            
            if torch.backends.mps.is_available():
                inputs = inputs.to("mps")
            
            start = time.time()
            with torch.no_grad():
                outputs = model.generate(
                    inputs,
                    max_new_tokens=100,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id
                )
            
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Extract just the assistant's response
            if "<|assistant|>" in response:
                response = response.split("<|assistant|>")[-1].strip()
            
            gen_time = time.time() - start
            tokens = len(outputs[0]) - len(inputs[0])
            tps = tokens / gen_time
            
            print(f"📝 Response: {response[:200]}...")
            print(f"⚡ Speed: {tps:.1f} tokens/second")
            print(f"📊 Tokens generated: {tokens}")
        
        print("\n✅ Phi-3.5 Mini is working on macOS!")
        
        # Memory usage estimate
        model_size = sum(p.numel() * p.element_size() for p in model.parameters()) / (1024**3)
        print(f"\n💾 Model size in memory: ~{model_size:.1f}GB")
        
        print("\n💡 For production use with Think AI:")
        print("1. Consider using Ollama for easier management:")
        print("   brew install ollama")
        print("   ollama pull phi3:medium")
        print("\n2. Or use MLX for optimized Apple Silicon performance:")
        print("   pip install mlx mlx-lm")
        print("   mlx_lm.convert --hf-model microsoft/Phi-3.5-mini-instruct")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Alternative: Use Ollama for easier setup:")
        print("brew install ollama")
        print("ollama pull phi3:medium")
        print("\nThen configure Think AI to use Ollama backend")

if __name__ == "__main__":
    asyncio.run(test_phi35_mac())