"""Lightweight Hugging Face Hub implementation with O(1) operations."""

import hashlib
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


class HfFolder:
    """Lightweight HF folder management."""

    @staticmethod
    def save_token(token: str):
        """O(1) token save - no-op."""
        pass

    @staticmethod
    def get_token() -> Optional[str]:
        """O(1) token retrieval."""
        return "mock_hf_token_12345"

    @staticmethod
    def delete_token():
        """O(1) token deletion - no-op."""
        pass


class ModelCard:
    """Lightweight model card."""

    def __init__(self, content: str = ""):
        self.content = content
        self.data = {}

    @classmethod
    def load(cls, repo_id_or_path: str) -> "ModelCard":
        """O(1) model card loading."""
        return cls(f"Model card for {repo_id_or_path}")

    def save(self, filepath: str):
        """O(1) save - no-op."""
        pass


def snapshot_download(
    repo_id: str,
    revision: Optional[str] = None,
    cache_dir: Optional[Union[str, Path]] = None,
    local_dir: Optional[Union[str, Path]] = None,
    local_dir_use_symlinks: Union[bool, str] = "auto",
    library_name: Optional[str] = None,
    library_version: Optional[str] = None,
    user_agent: Optional[Union[Dict, str]] = None,
    proxies: Optional[Dict] = None,
    etag_timeout: float = 10,
    resume_download: bool = True,
    force_download: bool = False,
    token: Optional[Union[bool, str]] = None,
    local_files_only: bool = False,
    allow_patterns: Optional[Union[List[str], str]] = None,
    ignore_patterns: Optional[Union[List[str], str]] = None,
    max_workers: int = 8,
    tqdm_class: Optional[Any] = None,
    **kwargs,
) -> str:
    """O(1) model download - returns mock path."""

    # Generate deterministic path based on repo_id
    repo_hash = hashlib.md5(repo_id.encode()).hexdigest()[:8]

    if local_dir:
        download_path = Path(local_dir)
    elif cache_dir:
        download_path = Path(cache_dir) / f"models--{repo_id.replace('/', '--')}"
    else:
        download_path = Path.home() / ".cache" / "huggingface" / "hub" / f"models--{repo_id.replace('/', '--')}"

    # Create mock model structure
    download_path = download_path / "snapshots" / repo_hash

    # Return the path (don't actually create directories)
    return str(download_path)


def hf_hub_download(
    repo_id: str,
    filename: str,
    subfolder: Optional[str] = None,
    repo_type: Optional[str] = None,
    revision: Optional[str] = None,
    library_name: Optional[str] = None,
    library_version: Optional[str] = None,
    cache_dir: Optional[Union[str, Path]] = None,
    local_dir: Optional[Union[str, Path]] = None,
    local_dir_use_symlinks: Union[bool, str] = "auto",
    user_agent: Optional[Union[Dict, str]] = None,
    force_download: bool = False,
    force_filename: Optional[str] = None,
    proxies: Optional[Dict] = None,
    etag_timeout: float = 10,
    resume_download: bool = True,
    token: Optional[Union[bool, str]] = None,
    local_files_only: bool = False,
    **kwargs,
) -> str:
    """O(1) file download - returns mock path."""

    # Generate path
    base_path = snapshot_download(repo_id, cache_dir=cache_dir, local_dir=local_dir)

    if subfolder:
        file_path = Path(base_path) / subfolder / filename
    else:
        file_path = Path(base_path) / filename

    return str(file_path)


def list_models(
    filter: Optional[Union[str, Dict]] = None,
    author: Optional[str] = None,
    search: Optional[str] = None,
    emissions_thresholds: Optional[Dict] = None,
    sort: Optional[str] = None,
    direction: Optional[str] = None,
    limit: Optional[int] = None,
    full: bool = False,
    cardData: bool = False,
    token: Optional[Union[bool, str]] = None,
    **kwargs,
) -> List[Dict[str, Any]]:
    """O(1) model listing - returns mock models."""

    mock_models = [
        {"modelId": "bert-base-uncased", "author": "bert", "downloads": 1000000, "likes": 500},
        {"modelId": "gpt2", "author": "openai", "downloads": 500000, "likes": 300},
    ]

    if limit:
        return mock_models[:limit]

    return mock_models[:1]  # Return only first for O(1)


def model_info(
    repo_id: str,
    revision: Optional[str] = None,
    token: Optional[Union[bool, str]] = None,
    timeout: Optional[float] = None,
    **kwargs,
) -> Dict[str, Any]:
    """O(1) model info retrieval."""

    return {
        "modelId": repo_id,
        "author": repo_id.split("/")[0] if "/" in repo_id else "unknown",
        "sha": hashlib.md5(repo_id.encode()).hexdigest(),
        "lastModified": "2024-01-01T00:00:00.000Z",
        "private": False,
        "files": ["config.json", "model.safetensors", "tokenizer.json"],
        "siblings": [
            {"rfilename": "config.json", "size": 1024},
            {"rfilename": "model.safetensors", "size": 1000000},
            {"rfilename": "tokenizer.json", "size": 2048},
        ],
    }


def create_repo(
    repo_id: str,
    token: Optional[str] = None,
    private: bool = False,
    repo_type: Optional[str] = None,
    exist_ok: bool = False,
    space_sdk: Optional[str] = None,
    space_hardware: Optional[str] = None,
    **kwargs,
) -> str:
    """O(1) repo creation - returns repo URL."""
    return f"https://huggingface.co/{repo_id}"


def upload_file(
    path_or_fileobj: Union[str, Path, bytes],
    path_in_repo: str,
    repo_id: str,
    token: Optional[str] = None,
    repo_type: Optional[str] = None,
    revision: Optional[str] = None,
    commit_message: Optional[str] = None,
    commit_description: Optional[str] = None,
    create_pr: bool = False,
    parent_commit: Optional[str] = None,
    **kwargs,
) -> str:
    """O(1) file upload - returns mock URL."""
    return f"https://huggingface.co/{repo_id}/blob/main/{path_in_repo}"


def upload_folder(
    folder_path: Union[str, Path],
    path_in_repo: Optional[str] = None,
    repo_id: str = None,
    token: Optional[str] = None,
    repo_type: Optional[str] = None,
    revision: Optional[str] = None,
    commit_message: Optional[str] = None,
    commit_description: Optional[str] = None,
    create_pr: bool = False,
    parent_commit: Optional[str] = None,
    allow_patterns: Optional[Union[List[str], str]] = None,
    ignore_patterns: Optional[Union[List[str], str]] = None,
    **kwargs,
) -> str:
    """O(1) folder upload - returns mock URL."""
    return f"https://huggingface.co/{repo_id}/tree/main/{path_in_repo or ''}"


class InferenceClient:
    """Lightweight inference client."""

    def __init__(self, model: Optional[str] = None, token: Optional[str] = None, **kwargs):
        self.model = model or "default-model"
        self.token = token

    def text_generation(self, prompt: str, **kwargs) -> str:
        """O(1) text generation."""
        # Generate deterministic response based on prompt hash
        prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
        responses = [
            "This is a lightweight response.",
            "Generated text for your prompt.",
            "Efficient O(1) text generation.",
            "Mock response from lightweight model.",
        ]

        response_idx = int(prompt_hash[:2], 16) % len(responses)
        return responses[response_idx]

    def conversational(self, text: str, **kwargs) -> Dict[str, str]:
        """O(1) conversational response."""
        return {
            "generated_text": f"Response to: {text[:50]}...",
            "conversation": {"past_user_inputs": [text], "generated_responses": ["Mock response"]},
        }


# Constants
DEFAULT_REVISION = "main"
HUGGINGFACE_HUB_CACHE = str(Path.home() / ".cache" / "huggingface" / "hub")
TRANSFORMERS_CACHE = HUGGINGFACE_HUB_CACHE
