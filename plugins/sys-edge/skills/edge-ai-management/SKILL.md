---
name: edge-ai-management
description: "USE when managing AI models on mobile/edge devices. Implements lazy loading, quantization strategies, memory pressure handling, and dynamic model management for resource-constrained environments."
context: fork
model: sonnet
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# Edge AI Management Protocol

## Purpose

Optimizes AI model deployment and execution on resource-constrained edge devices through intelligent resource management and quantization strategies.

## Core Responsibilities

### 1. Model Management Strategy

**Lazy Loading Implementation:**
```python
# Model loader with on-demand initialization
class LazyModelLoader:
    def __init__(self, model_paths: Dict[str, str]):
        self.loaded_models = {}
        self.model_paths = model_paths
        self.memory_threshold = 0.8  # 80% memory usage threshold

    def load_model(self, model_name: str) -> Optional[Any]:
        """Load model only when needed"""
        if model_name not in self.loaded_models:
            if self._check_memory_pressure():
                self._unload_least_recently_used()
            self.loaded_models[model_name] = self._load_from_disk(model_name)
        return self.loaded_models[model_name]
```

**Memory Pressure Detection:**
- Monitor RAM usage via `psutil`
- Trigger unload when memory > 80%
- LRU (Least Recently Used) eviction strategy
- Preload frequently used models during idle time

### 2. Quantization Strategy

**Dynamic Quantization Based on Device Capabilities:**

```python
class QuantizationManager:
    def __init__(self):
        self.device_capabilities = self._detect_device_capabilities()

    def _detect_device_capabilities(self) -> Dict[str, Any]:
        return {
            'ram_gb': psutil.virtual_memory().total / (1024**3),
            'cpu_cores': psutil.cpu_count(),
            'device_age': self._estimate_device_age(),
            'gpu_available': torch.cuda.is_available()
        }

    def get_quantization_config(self, model_size: str) -> str:
        """Return optimal quantization based on device"""
        ram = self.device_capabilities['ram_gb']

        if ram < 4:
            return "int4"  # Aggressive quantization for older devices
        elif ram < 8:
            return "int8"  # Balanced for mid-range devices
        else:
            return "fp16"  # Minimal quantization for high-end devices
```

**Quantization Levels:**
- **int4**: 4-bit quantization for devices < 4GB RAM (pre-2020)
- **int8**: 8-bit quantization for devices 4-8GB RAM
- **fp16**: 16-bit floating point for devices > 8GB RAM

### 3. Context Window Management

**Sliding Window with Semantic Chunking:**

```python
class ContextWindowManager:
    def __init__(self, max_tokens: int = 4096):
        self.max_tokens = max_tokens
        self.current_context = []
        self.embedding_cache = {}

    def add_to_context(self, text: str) -> None:
        """Add text with smart context management"""
        tokens = self._tokenize(text)

        if len(tokens) > self.max_tokens:
            # Use semantic chunking to preserve relevant context
            chunks = self._semantic_chunk(tokens)
            self.current_context.extend(chunks)
            self._prune_context()
        else:
            self.current_context.append(text)
            self._prune_context()

    def _semantic_chunking(self, tokens: List[str]) -> List[str]:
        """Chunk preserving semantic coherence"""
        # Use embedding similarity to group related content
        embeddings = self._compute_embeddings(tokens)
        # Group by similarity threshold
        # Keep most recent + most relevant chunks
        return self._select_optimal_chunks(embeddings)
```

### 4. Battery Optimization

**Batch Inference and Throttling:**

```python
class BatteryOptimizer:
    def __init__(self):
        self.battery = psutil.sensors_battery()
        self.batch_queue = []
        self.batch_size = 10
        self.low_battery_mode = False

    def should_batch_inference(self) -> bool:
        """Determine if batching is beneficial"""
        if self.battery.percent < 20:
            self.low_battery_mode = True
            return True  # Always batch in low battery
        return len(self.batch_queue) >= self.batch_size

    def add_inference_request(self, request: Dict) -> None:
        """Queue request for batch processing"""
        self.batch_queue.append(request)

        if self.should_batch_inference():
            self._process_batch()

    def _process_batch(self) -> None:
        """Process queued requests in batch"""
        if not self.batch_queue:
            return

        # Single inference for entire batch
        batch_input = self._combine_batch_inputs(self.batch_queue)
        results = self._run_inference(batch_input)

        # Distribute results
        self._distribute_results(results)
        self.batch_queue.clear()
```

### 5. Model Selection Algorithm

**Runtime Model Selection:**

```python
class ModelSelector:
    def __init__(self):
        self.available_models = {
            'small': {'size_mb': 100, 'quality': 0.7, 'speed': 0.9},
            'medium': {'size_mb': 500, 'quality': 0.85, 'speed': 0.7},
            'large': {'size_mb': 2000, 'quality': 0.95, 'speed': 0.4}
        }

    def select_model(self, task_type: str, constraints: Dict) -> str:
        """Select optimal model based on task and constraints"""
        available_ram = constraints.get('available_ram_gb', 4)
        battery_percent = constraints.get('battery_percent', 100)
        priority = constraints.get('priority', 'balanced')  # speed, quality, balanced

        # Filter models that fit in memory
        feasible_models = [
            name for name, specs in self.available_models.items()
            if specs['size_mb'] < (available_ram * 1024 * 0.6)  # Use max 60% of RAM
        ]

        if not feasible_models:
            return 'small'  # Fallback to smallest model

        # Score models based on priority
        scored_models = []
        for model in feasible_models:
            specs = self.available_models[model]
            score = self._calculate_score(specs, priority, battery_percent)
            scored_models.append((model, score))

        # Return highest scoring model
        return max(scored_models, key=lambda x: x[1])[0]

    def _calculate_score(self, specs: Dict, priority: str, battery: int) -> float:
        """Calculate model suitability score"""
        if priority == 'speed':
            return specs['speed'] * (1 if battery > 30 else 0.5)
        elif priority == 'quality':
            return specs['quality'] * (1 if battery > 20 else 0.3)
        else:  # balanced
            return (specs['speed'] + specs['quality']) / 2 * (1 if battery > 25 else 0.4)
```

## Implementation Patterns

### Pattern 1: Resource-Aware Model Loading
```python
# Example usage
manager = EdgeAIManager()

# Load model based on current resources
model = manager.load_model(
    model_name="text_generator",
    constraints={
        'max_memory_mb': 512,
        'battery_percent': 45,
        'priority': 'balanced'
    }
)

# Model automatically quantized and optimized
output = model.generate(input_text)
```

### Pattern 2: Context-Aware Processing
```python
# Context window automatically manages memory
context_manager = ContextWindowManager(max_tokens=2048)

for document in documents:
    context_manager.add_to_context(document)
    # Oldest/least relevant context automatically pruned
```

### Pattern 3: Battery-Smart Inference
```python
# Inference automatically optimized for battery
optimizer = BatteryOptimizer()

# Requests automatically batched in low battery
optimizer.add_inference_request(request1)
optimizer.add_inference_request(request2)
# Processed together when batch threshold reached or battery low
```

## Integration with CatToolkit

**Usage in Builder Workflow:**
```bash
# Use edge-ai-management skill for mobile optimization
"Optimize this model for edge deployment on mobile devices"

# Skill automatically:
# 1. Detects device capabilities
# 2. Applies appropriate quantization
# 3. Configures memory management
# 4. Implements battery optimization
# 5. Generates deployment configuration
```

## Quality Gates

- Model size after quantization < 60% of available RAM
- Battery impact < 10% per hour of active use
- Context window maintains semantic coherence
- Memory pressure never exceeds 80%
- Cold start time < 3 seconds for cached models

## Files Generated

- `model_config.json`: Quantization and optimization settings
- `deployment_config.yaml`: Mobile deployment configuration
- `resource_monitor.py`: Runtime resource tracking
- `battery_optimizer.py`: Battery-aware processing logic

## Next Steps

1. Integrate with `mobile-optimization` skill for complete battery management
2. Connect to `offline-sync` skill for model updates
3. Add support for hardware-specific optimizations (NNAPI, CoreML)
