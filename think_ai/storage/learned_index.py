"""Learned index structures for O(1) key-value access in Think AI."""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any, Union
import pickle
import json
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
import hashlib

from ..utils.logging import get_logger


logger = get_logger(__name__)


class LearnedIndex:
    """Base class for learned index structures."""
    
    def __init__(self, error_bound: int = 100):
        self.error_bound = error_bound
        self.trained = False
        self.key_positions: Dict[str, int] = {}
        self.sorted_keys: List[str] = []
    
    def train(self, keys: List[str], positions: List[int]) -> None:
        """Train the learned index."""
        raise NotImplementedError
    
    def predict(self, key: str) -> Tuple[int, int]:
        """Predict position range for a key."""
        raise NotImplementedError
    
    def _hash_key(self, key: str) -> float:
        """Convert key to numeric representation."""
        # Use SHA256 hash and take first 8 bytes as float
        hash_bytes = hashlib.sha256(key.encode()).digest()[:8]
        return float(int.from_bytes(hash_bytes, 'big'))


class LinearLearnedIndex(LearnedIndex):
    """Linear regression-based learned index."""
    
    def __init__(self, error_bound: int = 100):
        super().__init__(error_bound)
        self.model = LinearRegression()
        self.min_hash = 0.0
        self.max_hash = 1.0
    
    def train(self, keys: List[str], positions: List[int]) -> None:
        """Train linear model on key-position pairs."""
        if not keys:
            return
        
        # Convert keys to numeric features
        X = np.array([self._hash_key(k) for k in keys]).reshape(-1, 1)
        y = np.array(positions)
        
        # Normalize features
        self.min_hash = X.min()
        self.max_hash = X.max()
        X_norm = (X - self.min_hash) / (self.max_hash - self.min_hash + 1e-10)
        
        # Train model
        self.model.fit(X_norm, y)
        
        # Store keys for verification
        self.sorted_keys = sorted(keys)
        self.key_positions = {k: i for i, k in enumerate(self.sorted_keys)}
        self.trained = True
        
        logger.info(f"Trained linear index on {len(keys)} keys")
    
    def predict(self, key: str) -> Tuple[int, int]:
        """Predict position range for key."""
        if not self.trained:
            raise ValueError("Index not trained")
        
        # Convert key to normalized feature
        X = self._hash_key(key)
        X_norm = (X - self.min_hash) / (self.max_hash - self.min_hash + 1e-10)
        
        # Predict position
        pred_pos = int(self.model.predict([[X_norm]])[0])
        
        # Return range with error bound
        start = max(0, pred_pos - self.error_bound)
        end = min(len(self.sorted_keys), pred_pos + self.error_bound)
        
        return start, end


class NeuralLearnedIndex(LearnedIndex):
    """Neural network-based learned index."""
    
    def __init__(self, error_bound: int = 50, hidden_layers: Tuple[int, ...] = (64, 32)):
        super().__init__(error_bound)
        self.model = MLPRegressor(
            hidden_layer_sizes=hidden_layers,
            activation='relu',
            max_iter=1000,
            early_stopping=True,
            validation_fraction=0.1
        )
        self.scaler = StandardScaler()
        self.feature_dim = 8
    
    def train(self, keys: List[str], positions: List[int]) -> None:
        """Train neural network on key-position pairs."""
        if len(keys) < 100:
            # Fall back to linear for small datasets
            logger.warning("Too few keys for neural index, using linear")
            return LinearLearnedIndex(self.error_bound).train(keys, positions)
        
        # Extract features from keys
        X = self._extract_features(keys)
        y = np.array(positions)
        
        # Normalize features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model.fit(X_scaled, y)
        
        # Store keys
        self.sorted_keys = sorted(keys)
        self.key_positions = {k: i for i, k in enumerate(self.sorted_keys)}
        self.trained = True
        
        logger.info(f"Trained neural index on {len(keys)} keys")
    
    def predict(self, key: str) -> Tuple[int, int]:
        """Predict position range for key."""
        if not self.trained:
            raise ValueError("Index not trained")
        
        # Extract features
        X = self._extract_features([key])
        X_scaled = self.scaler.transform(X)
        
        # Predict position
        pred_pos = int(self.model.predict(X_scaled)[0])
        
        # Return range with error bound
        start = max(0, pred_pos - self.error_bound)
        end = min(len(self.sorted_keys), pred_pos + self.error_bound)
        
        return start, end
    
    def _extract_features(self, keys: List[str]) -> np.ndarray:
        """Extract multiple features from keys."""
        features = []
        
        for key in keys:
            # Hash-based features
            hash1 = self._hash_key(key)
            hash2 = self._hash_key(key + "salt1")
            hash3 = self._hash_key(key + "salt2")
            
            # Length feature
            length = float(len(key))
            
            # Character-based features
            first_char = float(ord(key[0]) if key else 0)
            last_char = float(ord(key[-1]) if key else 0)
            
            # Entropy feature
            char_counts = {}
            for char in key:
                char_counts[char] = char_counts.get(char, 0) + 1
            entropy = -sum(
                (count/length) * np.log2(count/length)
                for count in char_counts.values()
                if count > 0
            ) if length > 0 else 0.0
            
            # Alphanumeric ratio
            alnum_ratio = sum(1 for c in key if c.isalnum()) / max(length, 1)
            
            features.append([
                hash1, hash2, hash3, length,
                first_char, last_char, entropy, alnum_ratio
            ])
        
        return np.array(features)


class RecursiveModelIndex(LearnedIndex):
    """Recursive Model Index (RMI) implementation."""
    
    def __init__(self, stages: int = 2, models_per_stage: List[int] = None):
        super().__init__(error_bound=10)  # RMI has tighter bounds
        self.stages = stages
        self.models_per_stage = models_per_stage or [1, 100]
        self.models: List[List[LinearRegression]] = []
        self.stage_data: List[Dict[int, Tuple[List[str], List[int]]]] = []
    
    def train(self, keys: List[str], positions: List[int]) -> None:
        """Train recursive model index."""
        if not keys:
            return
        
        self.sorted_keys = sorted(keys)
        self.key_positions = {k: i for i, k in enumerate(self.sorted_keys)}
        
        # Initialize stages
        self.models = []
        self.stage_data = []
        
        # Stage 0: Single root model
        root_model = LinearRegression()
        X = np.array([self._hash_key(k) for k in keys]).reshape(-1, 1)
        y = np.array(positions)
        root_model.fit(X, y)
        self.models.append([root_model])
        
        # Subsequent stages
        current_keys = keys
        current_positions = positions
        
        for stage in range(1, self.stages):
            stage_models = []
            stage_assignments = {}
            
            num_models = self.models_per_stage[min(stage, len(self.models_per_stage)-1)]
            
            # Assign keys to models in this stage
            for i, key in enumerate(current_keys):
                # Use previous stage to determine assignment
                prev_pred = self._predict_stage(key, stage-1)
                model_idx = int(prev_pred * num_models / len(current_keys))
                model_idx = min(model_idx, num_models - 1)
                
                if model_idx not in stage_assignments:
                    stage_assignments[model_idx] = ([], [])
                
                stage_assignments[model_idx][0].append(key)
                stage_assignments[model_idx][1].append(current_positions[i])
            
            # Train models for this stage
            for model_idx in range(num_models):
                if model_idx in stage_assignments:
                    model_keys, model_positions = stage_assignments[model_idx]
                    if model_keys:
                        model = LinearRegression()
                        X = np.array([self._hash_key(k) for k in model_keys]).reshape(-1, 1)
                        y = np.array(model_positions)
                        model.fit(X, y)
                        stage_models.append(model)
                    else:
                        stage_models.append(None)
                else:
                    stage_models.append(None)
            
            self.models.append(stage_models)
            self.stage_data.append(stage_assignments)
        
        self.trained = True
        logger.info(f"Trained RMI with {self.stages} stages on {len(keys)} keys")
    
    def predict(self, key: str) -> Tuple[int, int]:
        """Predict position using recursive models."""
        if not self.trained:
            raise ValueError("Index not trained")
        
        # Traverse through stages
        position = 0
        
        for stage in range(self.stages):
            if stage == 0:
                # Root model
                position = self._predict_stage(key, stage)
            else:
                # Determine which model to use
                prev_position = position
                model_idx = int(prev_position * len(self.models[stage]) / len(self.sorted_keys))
                model_idx = min(model_idx, len(self.models[stage]) - 1)
                
                if self.models[stage][model_idx] is not None:
                    X = np.array([[self._hash_key(key)]])
                    position = int(self.models[stage][model_idx].predict(X)[0])
        
        # Tight bounds for RMI
        start = max(0, position - self.error_bound)
        end = min(len(self.sorted_keys), position + self.error_bound)
        
        return start, end
    
    def _predict_stage(self, key: str, stage: int) -> float:
        """Predict using model at specific stage."""
        if stage >= len(self.models):
            return 0.0
        
        if stage == 0:
            # Root model
            X = np.array([[self._hash_key(key)]])
            return float(self.models[0][0].predict(X)[0])
        
        return 0.0


class LearnedIndexManager:
    """Manages multiple learned indexes for different key patterns."""
    
    def __init__(self, index_dir: Optional[Path] = None):
        self.index_dir = index_dir or Path.home() / ".think_ai" / "learned_indexes"
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.indexes: Dict[str, LearnedIndex] = {}
        self.index_stats: Dict[str, Dict[str, Any]] = {}
    
    def create_index(
        self,
        name: str,
        keys: List[str],
        positions: List[int],
        index_type: str = "auto"
    ) -> LearnedIndex:
        """Create and train a learned index."""
        # Choose index type
        if index_type == "auto":
            if len(keys) < 1000:
                index_type = "linear"
            elif len(keys) < 10000:
                index_type = "neural"
            else:
                index_type = "rmi"
        
        # Create index
        if index_type == "linear":
            index = LinearLearnedIndex()
        elif index_type == "neural":
            index = NeuralLearnedIndex()
        elif index_type == "rmi":
            index = RecursiveModelIndex()
        else:
            raise ValueError(f"Unknown index type: {index_type}")
        
        # Train index
        index.train(keys, positions)
        
        # Store index
        self.indexes[name] = index
        self.index_stats[name] = {
            "type": index_type,
            "num_keys": len(keys),
            "error_bound": index.error_bound,
            "created_at": np.datetime64('now')
        }
        
        # Save to disk
        self.save_index(name)
        
        return index
    
    def get_index(self, name: str) -> Optional[LearnedIndex]:
        """Get a learned index by name."""
        if name in self.indexes:
            return self.indexes[name]
        
        # Try to load from disk
        if self.load_index(name):
            return self.indexes[name]
        
        return None
    
    def predict(self, name: str, key: str) -> Tuple[int, int]:
        """Predict position range using named index."""
        index = self.get_index(name)
        if not index:
            raise ValueError(f"Index {name} not found")
        
        return index.predict(key)
    
    def save_index(self, name: str) -> bool:
        """Save index to disk."""
        if name not in self.indexes:
            return False
        
        try:
            index_path = self.index_dir / f"{name}.pkl"
            stats_path = self.index_dir / f"{name}_stats.json"
            
            # Save index
            with open(index_path, 'wb') as f:
                pickle.dump(self.indexes[name], f)
            
            # Save stats
            with open(stats_path, 'w') as f:
                json.dump(self.index_stats[name], f, default=str)
            
            logger.info(f"Saved learned index {name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save index {name}: {e}")
            return False
    
    def load_index(self, name: str) -> bool:
        """Load index from disk."""
        try:
            index_path = self.index_dir / f"{name}.pkl"
            stats_path = self.index_dir / f"{name}_stats.json"
            
            if not index_path.exists():
                return False
            
            # Load index
            with open(index_path, 'rb') as f:
                self.indexes[name] = pickle.load(f)
            
            # Load stats
            if stats_path.exists():
                with open(stats_path, 'r') as f:
                    self.index_stats[name] = json.load(f)
            
            logger.info(f"Loaded learned index {name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load index {name}: {e}")
            return False
    
    def get_stats(self, name: str) -> Dict[str, Any]:
        """Get statistics for an index."""
        return self.index_stats.get(name, {})
    
    def list_indexes(self) -> List[str]:
        """List all available indexes."""
        # In-memory indexes
        indexes = set(self.indexes.keys())
        
        # On-disk indexes
        for path in self.index_dir.glob("*.pkl"):
            indexes.add(path.stem)
        
        return sorted(list(indexes))