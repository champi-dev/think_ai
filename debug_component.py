#!/usr/bin/env python3

import subprocess
import time
import signal
import sys

def test_component_initialization():
    print("🔍 Debugging Component Initialization")
    print("=" * 50)
    
    # Start server and immediately capture logs
    print("🚀 Starting server to check component initialization...")
    
    try:
        process = subprocess.Popen(
            ['./target/release/think-ai', 'server'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Read lines for 5 seconds
        start_time = time.time()
        lines_captured = []
        
        while time.time() - start_time < 5:
            try:
                line = process.stdout.readline()
                if line:
                    lines_captured.append(line.strip())
                    print(f"📋 {line.strip()}")
                    
                    # Look for our component initialization
                    if "INITIALIZING MultiLevelResponseComponent" in line:
                        print("✅ FOUND: MultiLevelResponseComponent is being initialized!")
                    elif "Response components initialized" in line:
                        print("✅ FOUND: Component registration complete")
                        
                else:
                    time.sleep(0.1)
            except:
                break
        
        # Terminate the process
        process.terminate()
        process.wait(timeout=2)
        
        print(f"\n📊 Analysis of {len(lines_captured)} log lines:")
        
        # Check what we found
        found_multilevel_init = any("INITIALIZING MultiLevelResponseComponent" in line for line in lines_captured)
        found_component_init = any("Response components initialized" in line for line in lines_captured)
        found_cache_init = any("Initializing multi-level response cache" in line for line in lines_captured)
        
        if found_multilevel_init:
            print("✅ MultiLevelResponseComponent IS being initialized")
        else:
            print("❌ MultiLevelResponseComponent NOT found in initialization")
            
        if found_component_init:
            print("✅ Component registration is happening")
        else:
            print("❌ Component registration not detected")
            
        if found_cache_init:
            print("✅ Cache initialization detected")
        else:
            print("❌ Cache initialization not detected")
        
        if not (found_multilevel_init or found_component_init):
            print("\n🚨 PROBLEM: The component may not be getting registered!")
            print("This explains why it's not being used for queries.")
        else:
            print("\n🤔 Component seems to initialize, but may not be winning scoring.")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
if __name__ == "__main__":
    test_component_initialization()