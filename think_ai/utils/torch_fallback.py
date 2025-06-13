"""
Minimal torch fallback for Think AI
Provides basic functionality when torch is not available
"""

import warnings


class MockTensor:
    """Mock tensor for torch fallback"""

    def __init__(self, data=None, dtype=None):
        self.data = data or []
        self.dtype = dtype
        self.shape = [len(data)] if isinstance(data, list) else []

    def float16(self):
        return MockTensor(self.data, "float16")

    def to(self, device):
        return self

    def long(self):
        return MockTensor(self.data, "long")

    def float(self):
        return MockTensor(self.data, "float32")


class MockTorch:
    """Mock torch module for fallback"""

    float16 = "float16"
    float32 = "float32"
    long = "long"

    class backends:
        class mps:
            @staticmethod
            def is_available():
                return False

    class nn:
        """Mock neural network module"""

        class Module:
            """Base class for all neural network modules"""

            def __init__(self):
                pass

            def eval(self):
                return self

            def train(self):
                return self

            def to(self, device):
                return self

            def parameters(self):
                return []

            def state_dict(self):
                return {}

            def load_state_dict(self, state_dict):
                pass

        class Linear(Module):
            """Mock linear layer"""

            def __init__(self, in_features, out_features):
                super().__init__()
                self.in_features = in_features
                self.out_features = out_features

        class LayerNorm(Module):
            """Mock layer normalization"""

            def __init__(self, normalized_shape):
                super().__init__()
                self.normalized_shape = normalized_shape

        class Embedding(Module):
            """Mock embedding layer"""

            def __init__(self, num_embeddings, embedding_dim):
                super().__init__()
                self.num_embeddings = num_embeddings
                self.embedding_dim = embedding_dim

        class CrossEntropyLoss(Module):
            """Mock cross entropy loss"""

            def __init__(self):
                super().__init__()

        class Parameter:
            """Mock parameter class"""

            def __init__(self, data=None):
                self.data = data if data is not None else MockTensor()
                self.requires_grad = True

            def to(self, device):
                return self

            def float16(self):
                return Parameter(
                    self.data.float16() if hasattr(
                        self.data, "float16") else self.data)

            def float(self):
                return Parameter(
                    self.data.float() if hasattr(
                        self.data, "float") else self.data)

    @staticmethod
    def tensor(data, dtype=None):
        return MockTensor(data, dtype)

    @staticmethod
    def LongTensor(data=None):
        """Create a long tensor"""
        return MockTensor(data or [], "long")

    @staticmethod
    def FloatTensor(data=None):
        """Create a float tensor"""
        return MockTensor(data or [], "float32")

    @staticmethod
    def zeros(*shape):
        """Create a tensor filled with zeros"""
        size = 1
        for dim in shape:
            size *= dim
        return MockTensor([0] * size)


# Try to import real torch, fallback to mock if not available
try:
    import torch

    TORCH_AVAILABLE = True
except ImportError:
    warnings.warn(
        "Torch not available, using minimal fallback for Think AI", UserWarning
    )
    torch = MockTorch()
    TORCH_AVAILABLE = False

__all__ = ["torch", "TORCH_AVAILABLE"]
