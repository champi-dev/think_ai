# `full-system`

The `full-system` crate is the main entry point for the Think AI production application. It integrates all of the other core components of the system into a single, cohesive service.

## Binaries

The `full-system` crate defines the following binaries:

*   `think-ai-full`: The main production binary.
*   `think-ai-full-persistent`: A version of the binary that includes persistent storage.
*   `think-ai-full-tokens`: A version of the binary that includes token-based authentication.

## Dependencies

The `full-system` crate depends on the following core crates:

*   `think-ai-core`
*   `think-ai-knowledge`
*   `think-ai-consciousness`
*   `think-ai-vector`
*   `think-ai-qwen`
*   `think-ai-storage`
*   `think-ai-utils`
