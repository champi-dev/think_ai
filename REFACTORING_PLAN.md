# Think AI Refactoring Plan

## Goal: Max 5 files per folder, 40 lines per file

### Current Issues:
- Root directory: 176 files (needs 35+ folders)
- Large files: 6 files over 1000 lines
- Crowded folders: think_ai/storage (11 files), think_ai/models (8 files)

## Phase 1: Root Directory Organization

### Create New Structure:
```
Think_AI/
├── src/              # Source code only
├── scripts/          # All utility scripts
│   ├── deployment/   # Deployment scripts
│   ├── testing/      # Test scripts
│   ├── training/     # Training scripts
│   └── utilities/    # Other utilities
├── configs/          # All configuration files
├── servers/          # API server variants
├── archives/         # Old/unused files
└── examples/         # Example code
```

### File Movement Plan:

#### To `scripts/deployment/`:
- deploy_full_system.sh
- deploy_v2.sh
- publish.sh
- publish_packages.sh
- setup_services.sh
- install_service.sh

#### To `scripts/testing/`:
- test_*.py (62 files)
- run_*.sh files
- FULL_SYSTEM_TEST.py
- EVIDENCE_MODEL_WORKS.py

#### To `scripts/training/`:
- train_*.py files
- self_training_*.py files

#### To `scripts/utilities/`:
- cleanup_*.py
- cache_*.py
- compress_dependencies.py
- reset_intelligence.py

#### To `servers/`:
- api_server*.py files
- simple_api_server.py
- background_worker.py

#### To `configs/`:
- *.yaml, *.yml files
- Dockerfile* files
- docker-compose* files

## Phase 2: Large File Refactoring

### 1. `think_ai/coding/code_generator.py` (2532 lines)
Split into:
- `generator/base.py` (40 lines)
- `generator/templates.py` (40 lines)  
- `generator/validators.py` (40 lines)
- `generator/processors.py` (40 lines)
- `generator/utils.py` (40 lines)

### 2. `think_ai/models/language_model.py` (1012 lines)
Split into:
- `language/base_model.py` (40 lines)
- `language/inference.py` (40 lines)
- `language/tokenizer.py` (40 lines)
- `language/cache.py` (40 lines)
- `language/utils.py` (40 lines)

### 3. `think_ai/storage/` (11 files)
Reorganize into:
- `storage/vector/` (vector_db.py, fast_vector_db.py)
- `storage/cache/` (redis_cache.py, offline.py)
- `storage/distributed/` (scylla.py, indexed_storage.py)
- `storage/base/` (base.py, utils.py)

## Phase 3: Module Reorganization

### think_ai/ structure:
```
think_ai/
├── core/           # Max 5 files
├── models/         # Split into subfolders
│   ├── language/
│   ├── embeddings/
│   └── cache/
├── storage/        # Split into subfolders
│   ├── vector/
│   ├── cache/
│   └── distributed/
├── coding/         # Split into subfolders
│   ├── generator/
│   ├── executor/
│   └── builder/
└── consciousness/  # Keep as is (5 files)
```

## Implementation Steps:

### Step 1: Create Directory Structure
```bash
mkdir -p scripts/{deployment,testing,training,utilities}
mkdir -p servers configs archives examples
mkdir -p think_ai/models/{language,embeddings,cache}
mkdir -p think_ai/storage/{vector,cache,distributed,base}
mkdir -p think_ai/coding/{generator,executor,builder}
```

### Step 2: Move Root Files
```bash
# Move test files
mv test_*.py scripts/testing/
mv run_*.sh scripts/testing/

# Move deployment files
mv deploy*.sh publish*.sh setup*.sh install*.sh scripts/deployment/

# Move training files
mv train_*.py self_training_*.py scripts/training/

# Move utilities
mv cleanup*.py cache*.py compress*.py reset*.py scripts/utilities/

# Move servers
mv api_server*.py simple_api_server.py background_worker.py servers/

# Move configs
mv *.yaml *.yml Dockerfile* docker-compose* configs/
```

### Step 3: Split Large Files
Each file will be split into modules of exactly 40 lines with:
- Clear single responsibility
- Proper imports
- Docstrings
- Type hints

### Step 4: Update Imports
All imports across the codebase need to be updated to reflect new paths.

### Step 5: Test Everything
Run comprehensive tests to ensure nothing breaks.

## Expected Result:
- No folder with more than 5 files
- No file with more than 40 lines
- Clear, organized structure
- All tests passing