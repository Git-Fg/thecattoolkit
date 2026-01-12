---
name: mobile-optimization
description: "Implements battery-aware processing, thermal management, adaptive quality settings, and power-efficient inference patterns. Use when optimizing AI applications for mobile devices."
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# Mobile Optimization Protocol

Ensures AI applications run efficiently on mobile devices through intelligent battery management, thermal optimization, and adaptive quality controls.

## Core Responsibilities

### 1. Battery-Aware Processing

**Battery State Monitoring:**

Monitor battery level and adjust processing configuration:

- HIGH_PERFORMANCE (>75% battery): Batch size 32, high quality, 4 workers
- BALANCED (50-75%): Batch size 16, medium quality, 2 workers
- POWER_SAVER (20-50%): Batch size 8, low quality, 1 worker
- CRITICAL_POWER_SAVER (<20%): Batch size 4, minimal quality, 1 worker

**See:** `references/battery-management.md` for complete implementation

### 2. Adaptive Quality Settings

**Dynamic Quality Adjustment:**

Automatically adjust quality based on performance metrics:
- **High:** 30 FPS target, 100ms latency, 70% CPU
- **Medium:** 20 FPS target, 200ms latency, 50% CPU
- **Low:** 10 FPS target, 500ms latency, 30% CPU
- **Minimal:** 5 FPS target, 1000ms latency, 20% CPU

**See:** `references/adaptive-quality.md` for complete implementation

### 3. Thermal Management

**Temperature-Based Throttling:**

Monitor device temperature and apply throttling:
- **Normal** (<75°C): Full performance
- **Warning** (75-85°C): Reduce load by 50%
- **Critical** (>85°C): Emergency shutdown

**See:** `references/thermal-management.md` for complete implementation

### 4. Power-Efficient Inference

**Batch Processing and Wake Cycle Optimization:**

Reduce wake cycles by batching requests:
- Process up to 10 requests per batch
- 2-second timeout for batch formation
- Priority-based processing (high → normal → low)
- Wake lock acquisition during batch processing

**See:** `references/power-efficient-inference.md` for complete implementation

### 5. Background Processing Optimization

**Deferred Processing for Non-Critical Tasks:**

Automatically defer non-critical tasks:
- **Critical tasks:** Execute immediately
- **Background tasks:** Execute when battery >50% or device idle
- **Charging-only tasks:** Execute only when plugged in

**See:** `references/background-processing.md` for complete implementation

## Implementation Patterns

### Pattern 1: Battery-Aware Model Inference
```python
# Initialize mobile optimizer
optimizer = MobileOptimizer()

# Run inference with battery awareness
result = optimizer.run_inference(
    input_data=data,
    quality_adaptive=True,  # Automatically adjust quality
    battery_aware=True      # Conserve battery when low
)

# Automatically adjusts:
# - Processing quality based on battery level
# - Batch size for efficiency
# - Parallel workers to manage CPU usage
```

### Pattern 2: Thermal-Safe Processing
```python
# Monitor and adapt to thermal state
thermal_manager = ThermalManager()

while processing:
    thermal_status = thermal_manager.monitor_temperature()

    if thermal_status["status"] == "throttling":
        # Automatically reduce processing load
        reduce_processing_intensity()
    elif thermal_status["status"] == "emergency_shutdown":
        # Save state and pause
        save_state_and_pause()
        break
```

### Pattern 3: Power-Efficient Scheduling
```python
# Queue requests for batch processing
power_efficient = PowerEfficientInference()

# Multiple requests automatically batched
power_efficient.schedule_inference(request1)
power_efficient.schedule_inference(request2)

# Processed together in single wake cycle
# Reduces wake cycles by 80%
```

## Integration Points

### With Edge AI Management
```python
# Combined edge optimization
edge_manager = EdgeAIManager()
mobile_optimizer = MobileOptimizer()

# Apply both optimizations
config = mobile_optimizer.get_processing_config()
model = edge_manager.load_model(
    model_name="generator",
    constraints={
        **config,
        "battery_percent": get_battery_percent(),
        "thermal_state": get_thermal_state()
    }
)
```

## Quality Gates

- Battery drain < 5% per hour during active use
- Thermal throttling activates before 85°C
- Adaptive quality maintains acceptable user experience
- Background tasks don't impact foreground performance
- Wake cycles reduced by >70% through batching

## Files Generated

- `battery_monitor.py`: Battery state tracking and power plan selection
- `thermal_manager.py`: Temperature monitoring and throttling logic
- `adaptive_quality.py`: Dynamic quality adjustment based on performance
- `power_efficient_scheduler.py`: Batch processing and wake cycle optimization

## Reference Materials

**Implementation Guides:**
- `references/battery-management.md` - Complete battery monitoring and power management
- `references/thermal-management.md` - Temperature monitoring and throttling
- `references/adaptive-quality.md` - Dynamic quality adjustment algorithms
- `references/power-efficient-inference.md` - Batch processing and wake cycle optimization
- `references/background-processing.md` - Deferred processing strategies

## Next Steps

1. Integrate with `edge-ai-management` for complete mobile optimization
2. Add support for platform-specific optimizations (Android, iOS)
3. Implement machine learning for predictive battery optimization
4. Add charging state awareness for task scheduling
