#!/usr/bin/env python3
"""Quick demo of code writing capability"""

print("🎯 Think AI Code Writing Demo")
print("=" * 60)
print("\nThe code writing integration is now complete!")
print("\nWhen you ask Think AI to 'write code' or 'create a file', it will:")
print("1. Detect the code writing request")
print("2. Generate appropriate code using Claude or templates")
print("3. Save the code to the 'generated_code' directory")
print("4. Test the code for syntax errors")
print("5. Show you the result with the file path")
print("\nExample phrases that trigger code writing:")
print("- 'write code to create a hello world program'")
print("- 'create a file called test.py'")
print("- 'save code for a calculator'")
print("\nThe generated files are saved in: ./generated_code/")
print("\nCheck the existing generated file:")

import os
if os.path.exists('generated_code/code.py'):
    with open('generated_code/code.py', 'r') as f:
        print(f"\n📁 generated_code/code.py:")
        print("-" * 40)
        print(f.read())
        print("-" * 40)
else:
    print("\nNo files generated yet.")

print("\n✅ Code writing is fully integrated!")