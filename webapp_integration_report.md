# Web App Integration Test Report

**Generated:** 2025-06-22T22:07:51.519578

## Summary

- Total Tests: 15
- Passed: 7
- Failed: 8
- Success Rate: 46.7%

## Evidence

- ✅ PASS server_startup: Server running - Health: {
  "status": "healthy",
  "timestamp": "2025-06-23T03:07:57.058081",
  "components": {
    "storage": {
      "status": "healthy",
      "type": "scylla_with_redis_cache"
    },
    "embedding_model": {
      "status": "healthy",
      "dimension": 384
    }
  },
  "colombian_mode": "active \ud83c\udde8\ud83c\uddf4"
}
- ❌ FAIL think_endpoint: Think endpoint returned 404
- ❌ FAIL intelligence_endpoint: Intelligence endpoint returned 404
- ❌ FAIL code_generation: Code generation returned 404
- ❌ FAIL capabilities_endpoint: Capabilities endpoint returned 404
- ✅ PASS model_loading: Model loaded: SentenceTransformer
- ✅ PASS vector_db_init: Vector DB initialized: O1VectorSearch
- ✅ PASS knowledge_base: Knowledge base loaded: 17 thoughts
- ✅ PASS embedding_generation: Generated embedding shape: (384,)
- ✅ PASS vector_search: Vector search working: 1 results found
- ✅ PASS response_generation: Generated response: Hello! I'm Think AI, ready to help you build amazing things!...
- ❌ FAIL query_test_1: Query failed with status 404
- ❌ FAIL query_test_2: Query failed with status 404
- ❌ FAIL query_test_3: Query failed with status 404
- ❌ FAIL websocket_support: WebSocket endpoint returned 404

## Conclusion

**WORKING AT 46.7% ACCURACY**
