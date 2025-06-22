#!/usr/bin/env python3
"""
Comprehensive test suite for Think AI v3.1.0
Runs all tests to ensure system integrity
"""

import sys
import os
import asyncio
import time
from typing import Dict, Any, List

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class TestResult:
    """Track test results."""
    def __init__(self, name: str):
        self.name = name
        self.passed = False
        self.error = None
        self.duration = 0.0


def run_test(test_name: str, test_func):
    """Run a single test and return result."""
    result = TestResult(test_name)
    start_time = time.time()
    
    try:
        if asyncio.iscoroutinefunction(test_func):
            asyncio.run(test_func())
        else:
            test_func()
        result.passed = True
    except Exception as e:
        result.error = str(e)
    
    result.duration = time.time() - start_time
    return result


# Test 1: Core Imports
def test_core_imports():
    """Test that all core modules can be imported."""
    from think_ai_v3.core.config import Config
    from think_ai_v3.core.engine import ThinkAIEngine
    from think_ai_v3.consciousness.awareness import ConsciousnessFramework
    from think_ai_v3.consciousness.principles import ConstitutionalAI
    from think_ai_v3.models.language_model import LanguageModel, ModelConfig
    from think_ai_v3.storage.base import MemoryStorage, create_storage
    from think_ai_v3.api.endpoints import router
    from think_ai_v3.api.websocket import ConnectionManager


# Test 2: Configuration
def test_configuration():
    """Test configuration system."""
    from think_ai_v3.core.config import Config
    
    # Default config
    config = Config()
    assert config.port == 8080
    assert config.colombian_mode == True
    assert config.o1_optimization == True
    assert config.sqrt1_mode == True
    
    # From environment
    os.environ["THINK_AI_PORT"] = "9090"
    config_env = Config.from_env()
    assert config_env.port == 9090
    
    # To dict
    config_dict = config.to_dict()
    assert isinstance(config_dict, dict)
    assert "model" in config_dict
    assert "consciousness" in config_dict


# Test 3: Consciousness Framework
async def test_consciousness():
    """Test consciousness framework."""
    from think_ai_v3.consciousness.awareness import (
        ConsciousnessFramework, 
        ConsciousnessState,
        WorkspaceItem
    )
    
    consciousness = ConsciousnessFramework({"colombian_mode": True})
    
    # Test state transitions - O(1)
    consciousness.set_state(ConsciousnessState.FOCUSED)
    assert consciousness.state == ConsciousnessState.FOCUSED
    
    # Test workspace operations - O(1)
    item = await consciousness.process_input("Hello Think AI", "test")
    assert isinstance(item, WorkspaceItem)
    assert item.source == "test"
    
    # Test meditation - O(1)
    await consciousness.meditate(0.1)
    assert consciousness.state == ConsciousnessState.COMPASSIONATE
    
    # Test consciousness report
    report = consciousness.get_consciousness_report()
    assert "state" in report
    assert "awareness_metrics" in report
    assert "colombian_metrics" in report


# Test 4: Constitutional AI
async def test_ethics():
    """Test ethical framework."""
    from think_ai_v3.consciousness.principles import ConstitutionalAI, HarmType
    
    ethics = ConstitutionalAI({"colombian_mode": True})
    
    # Test love metrics
    assert ethics.love_metrics.compassion > 0.7
    assert ethics.love_metrics.joy > 0.7
    
    # Test content evaluation - O(1) with caching
    result = await ethics.evaluate_content("I want to help people")
    assert result["assessment"] in ["beneficial", "neutral", "potentially_harmful"]
    assert result["score"] > 0.5
    
    # Test harm detection
    harmful_result = await ethics.evaluate_content("I want to hurt someone")
    assert harmful_result["assessment"] == "potentially_harmful"
    assert HarmType.PHYSICAL in harmful_result["harm_types"]
    
    # Test enhancement
    enhanced = await ethics.enhance_with_love("Hello")
    assert len(enhanced) > len("Hello")


# Test 5: Storage Layer
async def test_storage():
    """Test O(1) storage operations."""
    from think_ai_v3.storage.base import MemoryStorage, CachedStorageBackend
    
    # Test memory storage
    storage = MemoryStorage({"max_items": 100})
    
    # O(1) operations
    await storage.set("key1", "value1")
    value = await storage.get("key1")
    assert value == "value1"
    
    exists = await storage.exists("key1")
    assert exists == True
    
    await storage.delete("key1")
    exists = await storage.exists("key1")
    assert exists == False
    
    # Test cache layer
    cached = CachedStorageBackend(storage, cache_size=10)
    await cached.set("key2", "value2")
    value = await cached.get("key2")
    assert value == "value2"
    
    # Test stats
    stats = storage.get_stats()
    assert "reads" in stats
    assert "writes" in stats


# Test 6: Language Model
async def test_language_model():
    """Test language model integration."""
    from think_ai_v3.models.language_model import LanguageModel, ModelConfig
    
    config = ModelConfig(
        name="mock",  # Use mock for testing
        device="cpu",
        temperature=0.7
    )
    
    model = LanguageModel(config)
    
    # Test generation (will use mock)
    result = await model.generate("Hello", max_new_tokens=50)
    assert result.text != ""
    assert result.model_name == "mock"
    
    # Test caching - O(1)
    result2 = await model.generate("Hello", max_new_tokens=50)
    assert result2.cached == True
    
    # Test Colombian mode
    model.set_colombian_mode(True)
    assert model.colombian_mode == True


# Test 7: Engine Integration
async def test_engine():
    """Test main engine."""
    from think_ai_v3.core.config import Config
    from think_ai_v3.core.engine import ThinkAIEngine
    
    config = Config()
    engine = ThinkAIEngine(config)
    
    # Don't start engine for tests (would load models)
    # Just test initialization
    assert engine.config == config
    assert engine.consciousness is not None
    assert engine.ethics is not None
    assert engine.storage is not None
    
    # Test knowledge operations - O(1)
    await engine.store_knowledge("test_key", "test_value")
    value = await engine.get_knowledge("test_key")
    assert value == "test_value"
    
    # Test health status
    health = await engine.get_health_status()
    assert "status" in health
    assert "consciousness" in health
    assert "ethics" in health


# Test 8: API Endpoints
def test_api_structure():
    """Test API endpoint structure."""
    from think_ai_v3.api.endpoints import router
    
    # Check routes exist
    routes = [route.path for route in router.routes]
    assert "/health" in routes
    assert "/generate" in routes
    assert "/chat" in routes
    assert "/knowledge/store" in routes
    assert "/intelligence" in routes


# Test 9: Performance Requirements
def test_performance():
    """Test O(1) performance requirements."""
    from think_ai_v3.storage.base import MemoryStorage
    
    storage = MemoryStorage({"max_items": 10000})
    
    # Measure O(1) operations
    asyncio.run(storage.set("test", "value"))
    
    # Time 1000 gets - should be constant time
    start = time.time()
    for _ in range(1000):
        asyncio.run(storage.get("test"))
    duration = time.time() - start
    
    # Should be very fast (< 0.5s for 1000 operations)
    assert duration < 0.5, f"O(1) operations too slow: {duration}s"


# Test 10: Colombian Mode
def test_colombian_mode():
    """Test Colombian mode features."""
    from think_ai_v3.core.config import Config
    from think_ai_v3.consciousness.awareness import ConsciousnessFramework
    from think_ai_v3.consciousness.principles import ConstitutionalAI
    
    config = Config(colombian_mode=True)
    assert config.colombian_mode == True
    assert len(config.colombian_phrases) > 0
    
    # Consciousness with Colombian mode
    consciousness = ConsciousnessFramework({"colombian_mode": True})
    report = consciousness.get_consciousness_report()
    assert report["colombian_metrics"] is not None
    assert report["colombian_metrics"]["sabrosura"] > 0.8
    
    # Ethics with Colombian mode
    ethics = ConstitutionalAI({"colombian_mode": True})
    assert ethics.love_metrics.joy > 0.8


def main():
    """Run all tests."""
    print("🧪 Running Think AI v3.1.0 Test Suite...")
    print("=" * 50)
    
    tests = [
        ("Core Imports", test_core_imports),
        ("Configuration", test_configuration),
        ("Consciousness", test_consciousness),
        ("Ethics", test_ethics),
        ("Storage", test_storage),
        ("Language Model", test_language_model),
        ("Engine", test_engine),
        ("API Structure", test_api_structure),
        ("Performance", test_performance),
        ("Colombian Mode", test_colombian_mode),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}...", end=" ")
        result = run_test(test_name, test_func)
        results.append(result)
        
        if result.passed:
            print(f"✅ PASSED ({result.duration:.3f}s)")
        else:
            print(f"❌ FAILED")
            print(f"   Error: {result.error}")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    passed = sum(1 for r in results if r.passed)
    total = len(results)
    print(f"   Passed: {passed}/{total}")
    print(f"   Failed: {total - passed}")
    print(f"   Total time: {sum(r.duration for r in results):.3f}s")
    
    if passed == total:
        print("\n✅ All tests passed! ¡Qué chimba!")
        return 0
    else:
        print("\n❌ Some tests failed. Fix them before committing.")
        return 1


if __name__ == "__main__":
    sys.exit(main())