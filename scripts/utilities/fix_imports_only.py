#!/usr/bin/env python3
"""Fix just the import section in language_model.py"""


def fix_imports():
    with open("think_ai/models/language_model.py", "r") as f:
        content = f.read()

# Fix the broken imports section
# Find the problematic part
        broken_imports = """from transformers import (
from typing import List, Dict, Any, Optional
import torch

from ..consciousness.principles import ConstitutionalAI
from ..core.config import ModelConfig
from ..utils.complexity_detector import detect_complexity
from ..utils.logging import get_logger
from .response_cache import response_cache

        AutoModelForCausalLM,
        AutoTokenizer,
        BitsAndBytesConfig,
        TextStreamer,
        StoppingCriteria,
        StoppingCriteriaList
        )"""

        fixed_imports = """from typing import List, Dict, Any, Optional
import torch
from transformers import (
        AutoModelForCausalLM,
        AutoTokenizer,
        BitsAndBytesConfig,
        TextStreamer,
        StoppingCriteria,
        StoppingCriteriaList
        )

from ..consciousness.principles import ConstitutionalAI
from ..core.config import ModelConfig
from ..utils.complexity_detector import detect_complexity
from ..utils.logging import get_logger
from .response_cache import response_cache"""

# Replace the broken section
        content = content.replace(broken_imports, fixed_imports)

# Fix other syntax issues
        content = content.replace(" - > ", " -> ")
        content = content.replace(" = = ", " == ")
        content = content.replace(" ! = ", " != ")
        content = content.replace(" + = ", " += ")
        content = content.replace(" * * ", " ** ")
        content = content.replace("* * ", "** ")
        content = content.replace(" < = ", " <= ")
        content = content.replace(" > = ", " >= ")
        content = content.replace(
        "torch.cuda.memory_allocated() / 1024* * 3",
        "torch.cuda.memory_allocated() / 1024 ** 3",
        )
        content = content.replace(
        "torch.cuda.memory_reserved() / 1024* * 3",
        "torch.cuda.memory_reserved() / 1024 ** 3",
        )

# Write back
        with open("think_ai/models/language_model.py", "w") as f:
            f.write(content)

            print("Fixed imports and basic syntax in language_model.py")


            if __name__ == "__main__":
                fix_imports()
