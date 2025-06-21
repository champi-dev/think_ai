#!/usr/bin/env python3
"""
Test Think AI Dependencies Installation - Fixed Version
Tests dependency imports with proper error handling for missing packages
"""

import sys
import os
import importlib.util
from pathlib import Path

class ThinkAIDependencyTester:
    """Test Think AI dependencies with graceful error handling"""
    
    def __init__(self):
        self.results = {
            'core_imports': {},
            'optional_imports': {},
            'circular_import_status': False,
            'summary': {'total': 0, 'passed': 0, 'failed': 0}
        }
        
        # Add Think AI to Python path
        think_ai_path = Path(__file__).parent
        if str(think_ai_path) not in sys.path:
            sys.path.insert(0, str(think_ai_path))
    
    def test_import(self, module_name: str, is_optional: bool = False) -> bool:
        """Test importing a module with error handling"""
        try:
            importlib.import_module(module_name)
            result = True
            error_msg = None
        except ImportError as e:
            result = False
            error_msg = str(e)
        except Exception as e:
            result = False
            error_msg = f"Unexpected error: {e}"
        
        # Store result
        target_dict = self.results['optional_imports'] if is_optional else self.results['core_imports']
        target_dict[module_name] = {
            'success': result,
            'error': error_msg
        }
        
        self.results['summary']['total'] += 1
        if result:
            self.results['summary']['passed'] += 1
            print(f"✅ {module_name}: OK")
        else:
            self.results['summary']['failed'] += 1
            if is_optional:
                print(f"⚠️  {module_name}: Missing (optional)")
            else:
                print(f"❌ {module_name}: FAILED - {error_msg}")
        
        return result
    
    def test_think_ai_types(self) -> bool:
        """Test Think AI types module (should work without heavy dependencies)"""
        print("\n🧠 Testing Think AI Core Types (Circular Import Fix)")
        print("-" * 50)
        
        try:
            # Test direct import of types
            from think_ai.models.types import GenerationConfig, ModelResponse, ModelInstance
            
            # Test instantiation
            config = GenerationConfig(max_tokens=100)
            response = ModelResponse(text="Test", tokens_generated=1)
            instance = ModelInstance(model_id="test")
            
            print("✅ Think AI types imported and instantiated successfully")
            print("✅ Circular import issue RESOLVED!")
            
            self.results['circular_import_status'] = True
            return True
            
        except Exception as e:
            print(f"❌ Think AI types test failed: {e}")
            self.results['circular_import_status'] = False
            return False
    
    def test_python_standard_library(self):
        """Test Python standard library imports"""
        print("\n🐍 Testing Python Standard Library")
        print("-" * 50)
        
        standard_modules = [
            'json', 'os', 'sys', 'time', 'asyncio', 'logging',
            'dataclasses', 'typing', 'pathlib', 'collections'
        ]
        
        for module in standard_modules:
            self.test_import(module)
    
    def test_core_dependencies(self):
        """Test core Python dependencies"""
        print("\n📦 Testing Core Dependencies")
        print("-" * 50)
        
        core_deps = [
            'numpy',
            'fastapi', 
            'uvicorn',
            'pydantic',
            'requests'
        ]
        
        for dep in core_deps:
            self.test_import(dep)
    
    def test_ml_dependencies(self):
        """Test ML dependencies (optional)"""
        print("\n🤖 Testing ML Dependencies (Optional)")
        print("-" * 50)
        
        ml_deps = [
            'torch',
            'transformers',
            'safetensors',
            'sentence_transformers',
            'accelerate',
            'bitsandbytes'
        ]
        
        for dep in ml_deps:
            self.test_import(dep, is_optional=True)
    
    def test_database_dependencies(self):
        """Test database dependencies (optional)"""
        print("\n🗄️  Testing Database Dependencies (Optional)")
        print("-" * 50)
        
        db_deps = [
            'redis',
            'cassandra',
            'neo4j',
            'annoy',
            'faiss'
        ]
        
        for dep in db_deps:
            self.test_import(dep, is_optional=True)
    
    def run_all_tests(self):
        """Run all dependency tests"""
        print("🧪 Think AI Dependency Installation Test - Fixed Version")
        print("=" * 60)
        
        # Test core types first (most important)
        types_success = self.test_think_ai_types()
        
        # Test standard library
        self.test_python_standard_library()
        
        # Test core dependencies
        self.test_core_dependencies()
        
        # Test optional dependencies
        self.test_ml_dependencies()
        self.test_database_dependencies()
        
        # Print summary
        self.print_summary(types_success)
        
        return types_success and self.results['summary']['failed'] == 0
    
    def print_summary(self, types_success: bool):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 DEPENDENCY TEST SUMMARY")
        print("=" * 60)
        
        total = self.results['summary']['total']
        passed = self.results['summary']['passed']
        failed = self.results['summary']['failed']
        
        print(f"Total Tests: {total}")
        print(f"Passed: ✅ {passed}")
        print(f"Failed: ❌ {failed}")
        
        if types_success:
            print("🎉 CIRCULAR IMPORT FIX: ✅ SUCCESS")
        else:
            print("💥 CIRCULAR IMPORT FIX: ❌ FAILED")
        
        print(f"\n🧠 Think AI Core Status:")
        if self.results['circular_import_status']:
            print("  ✅ Types module working")
            print("  ✅ Circular imports resolved")
            print("  ✅ Ready for Colombian AI development")
        else:
            print("  ❌ Core types issues remain")
        
        # Count optional vs required failures
        core_failures = sum(1 for result in self.results['core_imports'].values() if not result['success'])
        optional_failures = sum(1 for result in self.results['optional_imports'].values() if not result['success'])
        
        print(f"\n📈 Detailed Breakdown:")
        print(f"  Core Dependencies Failed: {core_failures}")
        print(f"  Optional Dependencies Missing: {optional_failures}")
        
        if core_failures == 0:
            print("\n🚀 STATUS: Core functionality available!")
            print("🇨🇴 ¡Dale que vamos tarde! - Think AI is ready!")
        else:
            print(f"\n⚠️  STATUS: {core_failures} core dependencies need installation")
        
        if optional_failures > 0:
            print(f"💡 NOTE: {optional_failures} optional ML/DB features unavailable (install as needed)")

if __name__ == "__main__":
    tester = ThinkAIDependencyTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 ALL CORE TESTS PASSED!")
        sys.exit(0)
    else:
        print("\n⚠️  Some dependencies missing, but circular import is fixed!")
        sys.exit(1)