# Docker Bake configuration for parallel builds with maximum caching

variable "REGISTRY" {
  default = "localhost:5000"
}

variable "DEPENDENCY_HASH" {
  default = "latest"
}

group "default" {
  targets = ["think-ai", "think-ai-gpu", "think-ai-cache"]
}

target "docker-metadata-action" {}

target "think-ai" {
  dockerfile = "Dockerfile.hypercache"
  context = "."
  tags = [
    "${REGISTRY}/think-ai:latest",
    "${REGISTRY}/think-ai:${DEPENDENCY_HASH}",
  ]
  cache-from = [
    "type=local,src=/tmp/docker-cache",
    "type=registry,ref=${REGISTRY}/think-ai:cache",
    "type=registry,ref=${REGISTRY}/think-ai:latest",
    "type=gha",
  ]
  cache-to = [
    "type=local,dest=/tmp/docker-cache,mode=max",
    "type=registry,ref=${REGISTRY}/think-ai:cache,mode=max",
    "type=inline",
    "type=gha,mode=max",
  ]
  platforms = ["linux/amd64", "linux/arm64"]
  args = {
    BUILDKIT_INLINE_CACHE = "1"
    DEPENDENCY_HASH = "${DEPENDENCY_HASH}"
  }
  output = ["type=registry,push=true"]
}

target "think-ai-gpu" {
  inherits = ["think-ai"]
  dockerfile = "Dockerfile.hypercache"
  target = "runtime-gpu"
  tags = [
    "${REGISTRY}/think-ai:gpu",
    "${REGISTRY}/think-ai:gpu-${DEPENDENCY_HASH}",
  ]
}

target "think-ai-cache" {
  inherits = ["think-ai"]
  target = "cache-warmer"
  tags = ["${REGISTRY}/think-ai:cache-warmer"]
}