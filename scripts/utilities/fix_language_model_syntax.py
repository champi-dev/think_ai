#!/usr/bin/env python3
"""Fix language_model.py syntax issues"""

import re


def fix_language_model():
    """Fix the language_model.py file"""

    with open("think_ai/models/language_model.py", "r") as f:
        content = f.read()

    # Fix the imports section
    # Find the broken imports and fix them
    content = re.sub(
        r"from transformers import \(\nfrom typing import.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\nAutoModelForCausalLM,\nAutoTokenizer,\nBitsAndBytesConfig,\nTextStreamer,\nStoppingCriteria,\nStoppingCriteriaList\n\)",
        """from typing import List, Dict, Any, Optional
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TextStreamer,
    StoppingCriteria,
    StoppingCriteriaList
)""",
        content,
        flags=re.DOTALL,
    )

    # Fix spacing issues
    content = content.replace(" - > ", " -> ")
    content = content.replace(" = = ", " == ")
    content = content.replace(" ! = ", " != ")
    content = content.replace(" + = ", " += ")
    content = content.replace(" * * ", " ** ")
    content = content.replace("* * ", "** ")
    content = content.replace(" * *", " **")

    # Fix specific method signatures
    content = re.sub(
        r"def get_valid_generation_params\(self\) - > Dict\[str, Any\]:",
        "def get_valid_generation_params(self) -> Dict[str, Any]:",
        content,
    )
    content = re.sub(
        r"def __call__\(self, input_ids: torch\.LongTensor, scores: torch\.FloatTensor, \* \* kwargs\) - > bool:",
        "def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:",
        content,
    )
    content = re.sub(
        r"async def initialize\(self\) - > None:",
        "async def initialize(self) -> None:",
        content,
    )
    content = re.sub(
        r"async def generate\(.*?\) - > ModelResponse:",
        lambda m: m.group(0).replace(" - > ", " -> "),
        content,
    )
    content = re.sub(
        r"async def generate_with_context\(.*?\) - > ModelResponse:",
        lambda m: m.group(0).replace(" - > ", " -> "),
        content,
    )
    content = re.sub(
        r"async def answer_question\(.*?\) - > ModelResponse:",
        lambda m: m.group(0).replace(" - > ", " -> "),
        content,
    )
    content = re.sub(
        r"async def summarize\(self, text: str, max_length: int = 150\) - > ModelResponse:",
        "async def summarize(self, text: str, max_length: int = 150) -> ModelResponse:",
        content,
    )
    content = re.sub(
        r"async def translate\(.*?\) - > ModelResponse:",
        lambda m: m.group(0).replace(" - > ", " -> "),
        content,
    )
    content = re.sub(
        r"def _get_default_prompt\(self, user_input: str\) - > str:",
        "def _get_default_prompt(self, user_input: str) -> str:",
        content,
    )
    content = re.sub(
        r"async def get_model_info\(self\) - > Dict\[str, Any\]:",
        "async def get_model_info(self) -> Dict[str, Any]:",
        content,
    )
    content = re.sub(
        r"def _estimate_parameters\(self\) - > str:",
        "def _estimate_parameters(self) -> str:",
        content,
    )
    content = re.sub(
        r"def _get_memory_usage\(self\) - > Dict\[str, float\]:",
        "def _get_memory_usage(self) -> Dict[str, float]:",
        content,
    )
    content = re.sub(
        r"def _check_and_fix_meta_tensors\(self\) - > Dict\[str, torch\.nn\.Parameter\]:",
        "def _check_and_fix_meta_tensors(self) -> Dict[str, torch.nn.Parameter]:",
        content,
    )
    content = re.sub(
        r"async def _reload_model_properly\(self\) - > Any:",
        "async def _reload_model_properly(self) -> Any:",
        content,
    )
    content = re.sub(
        r"def _validate_model_ready\(self\) - > None:",
        "def _validate_model_ready(self) -> None:",
        content,
    )
    content = re.sub(
        r"def _build_parameter_cache\(self\) - > None:",
        "def _build_parameter_cache(self) -> None:",
        content,
    )
    content = re.sub(
        r"async def get_model_info\(self\) - > Dict\[str, Any\]:",
        "async def get_model_info(self) -> Dict[str, Any]:",
        content,
    )
    content = re.sub(
        r"async def process_multimodal\(.*?\) - > Dict\[str, Any\]:",
        lambda m: m.group(0).replace(" - > ", " -> "),
        content,
    )

    # Fix indentation issues in class definitions
    lines = content.split("\n")
    fixed_lines = []
    in_class = False
    class_indent = 0

    for i, line in enumerate(lines):
        # Skip the already processed imports section
        if i < 30:
            fixed_lines.append(line)
            continue

        stripped = line.strip()

        # Fix class indentation
        if line.startswith(" ") and stripped.startswith("class ") and i > 30:
            # This is an indented class definition that should be at module level
            if (
                "GenerationConfig" in stripped
                or "ModelResponse" in stripped
                or "LoveStoppingCriteria" in stripped
                or "LanguageModel" in stripped
                or "ModelOrchestrator" in stripped
            ):
                fixed_lines.append(stripped)  # Remove extra indentation
                in_class = True
                class_indent = 0
                continue

        # Fix method indentation
        if (
            line.startswith(" ")
            and (stripped.startswith("def ") or stripped.startswith("async def "))
            and not line.startswith("    def")
            and not line.startswith("    async def")
        ):
            if in_class:
                fixed_lines.append("    " + stripped)  # Ensure proper method indentation
            else:
                fixed_lines.append(stripped)
            continue

        # Fix docstring indentation
        if '"""' in line and not line.strip().startswith('"""'):
            # Find the proper indentation level
            if i > 0:
                prev_line = lines[i - 1].strip()
                if prev_line.endswith(":"):
                    # This is a docstring after a function/class definition
                    indent = len(lines[i - 1]) - len(lines[i - 1].lstrip())
                    fixed_lines.append(" " * (indent + 4) + line.strip())
                    continue

        fixed_lines.append(line)

    content = "\n".join(fixed_lines)

    # Fix remaining specific syntax issues
    content = content.replace(
        "torch.cuda.memory_allocated() / 1024** 3",
        "torch.cuda.memory_allocated() / 1024**3",
    )
    content = content.replace(
        "torch.cuda.memory_reserved() / 1024** 3",
        "torch.cuda.memory_reserved() / 1024**3",
    )

    # Write the fixed content
    with open("think_ai/models/language_model.py", "w") as f:
        f.write(content)

    print("Fixed language_model.py")


if __name__ == "__main__":
    fix_language_model()
