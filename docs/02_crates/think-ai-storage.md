# `think-ai-storage`

The `think-ai-storage` crate is responsible for managing the system's persistent storage.

## Key Components

*   **`StorageManager`:** The main entry point for the storage crate. It provides a high-level API for interacting with the system's persistent storage.
*   **`StorageBackend`:** A backend for the storage manager. The system includes a default backend that uses the local filesystem.

## Dependencies

The `think-ai-storage` crate depends on the following core crates:

*   `think-ai-utils`
