---
name: mobile-optimization
description: "USE when optimizing AI applications for mobile devices. Implements battery-aware processing, thermal management, adaptive quality settings, and power-efficient inference patterns."
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# Mobile Optimization Protocol

## Purpose

Ensures AI applications run efficiently on mobile devices through intelligent battery management, thermal optimization, and adaptive quality controls.

## Core Responsibilities

### 1. Battery-Aware Processing

**Battery State Monitoring:**

```python
class BatteryMonitor:
    def __init__(self):
        self.battery = psutil.sensors_battery()
        self.power_plan = self._determine_power_plan()
        self.monitoring_interval = 60  # seconds

    def _determine_power_plan(self) -> str:
        """Determine optimal power mode based on battery state"""
        if not self.battery:
            return "AC_POWER"  # Desktop or AC power

        percent = self.battery.percent

        if percent > 75:
            return "HIGH_PERFORMANCE"
        elif percent > 50:
            return "BALANCED"
        elif percent > 20:
            return "POWER_SAVER"
        else:
            return "CRITICAL_POWER_SAVER"

    def get_processing_config(self) -> Dict[str, Any]:
        """Get processing configuration based on battery state"""
        plans = {
            "HIGH_PERFORMANCE": {
                "batch_size": 32,
                "quality": "high",
                "parallel_workers": 4,
                "cache_size_mb": 512
            },
            "BALANCED": {
                "batch_size": 16,
                "quality": "medium",
                "parallel_workers": 2,
                "cache_size_mb": 256
            },
            "POWER_SAVER": {
                "batch_size": 8,
                "quality": "low",
                "parallel_workers": 1,
                "cache_size_mb": 128
            },
            "CRITICAL_POWER_SAVER": {
                "batch_size": 4,
                "quality": "minimal",
                "parallel_workers": 1,
                "cache_size_mb": 64,
                "defer_non_critical": True
            }
        }

        return plans[self.power_plan]
```

### 2. Adaptive Quality Settings

**Dynamic Quality Adjustment:**

```python
class AdaptiveQualityController:
    def __init__(self):
        self.current_quality = "medium"
        self.performance_history = []
        self.quality_thresholds = {
            "high": {"fps": 30, "latency_ms": 100, "cpu_percent": 70},
            "medium": {"fps": 20, "latency_ms": 200, "cpu_percent": 50},
            "low": {"fps": 10, "latency_ms": 500, "cpu_percent": 30}
        }

    def adjust_quality(self, metrics: Dict[str, float]) -> str:
        """Dynamically adjust quality based on performance metrics"""
        current_threshold = self.quality_thresholds[self.current_quality]

        # Check if current quality is sustainable
        if self._is_quality_sustainable(metrics, current_threshold):
            return self.current_quality

        # Determine if we need to reduce quality
        if metrics["cpu_percent"] > current_threshold["cpu_percent"]:
            return self._reduce_quality()
        elif metrics["fps"] < current_threshold["fps"]:
            return self._reduce_quality()

        # Check if we can increase quality
        if (metrics["cpu_percent"] < current_threshold["cpu_percent"] * 0.7 and
            metrics["fps"] > current_threshold["fps"] * 1.2):
            return self._increase_quality()

        return self.current_quality

    def _reduce_quality(self) -> str:
        """Reduce processing quality to save battery"""
        quality_levels = ["high", "medium", "low", "minimal"]
        current_index = quality_levels.index(self.current_quality)
        return quality_levels[min(current_index + 1, len(quality_levels) - 1)]

    def _increase_quality(self) -> str:
        """Increase quality if resources allow"""
        quality_levels = ["high", "medium", "low", "minimal"]
        current_index = quality_levels.index(self.current_quality)
        return quality_levels[max(current_index - 1, 0)]
```

### 3. Thermal Management

**Temperature-Based Throttling:**

```python
class ThermalManager:
    def __init__(self):
        self.temperature_threshold = 75  # Celsius
        self.critical_threshold = 85
        self.throttling_active = False
        self.cooldown_period = 300  # 5 minutes

    def monitor_temperature(self) -> Dict[str, Any]:
        """Monitor device temperature and apply throttling if needed"""
        temp = self._get_cpu_temperature()

        if temp > self.critical_threshold:
            return self._emergency_shutdown()
        elif temp > self.temperature_threshold:
            return self._activate_throttling(temp)
        elif self.throttling_active and temp < (self.temperature_threshold - 10):
            return self._deactivate_throttling()
        else:
            return {"status": "normal", "temperature": temp}

    def _activate_throttling(self, temp: float) -> Dict[str, Any]:
        """Reduce processing load to cool device"""
        self.throttling_active = True

        throttling_config = {
            "status": "throttling",
            "temperature": temp,
            "actions": [
                "reduce_batch_size_by_50%",
                "limit_parallel_workers_to_1",
                "disable_non_essential_features",
                "increase_processing_intervals"
            ]
        }

        return throttling_config

    def _emergency_shutdown(self) -> Dict[str, Any]:
        """Critical temperature - shut down non-essential processing"""
        return {
            "status": "emergency_shutdown",
            "actions": [
                "stop_all_non_critical_processing",
                "save_state_and_pause",
                "notify_user_of_thermal_event"
            ]
        }
```

### 4. Power-Efficient Inference

**Batch Processing and Wake Cycle Optimization:**

```python
class PowerEfficientInference:
    def __init__(self):
        self.pending_requests = []
        self.batch_timeout = 2.0  # seconds
        self.wake_lock = None

    def schedule_inference(self, request: Dict) -> None:
        """Schedule inference with power-efficient batching"""
        self.pending_requests.append({
            "data": request,
            "timestamp": time.time(),
            "priority": request.get("priority", "normal")
        })

        # Determine if we should process batch now
        if self._should_process_batch():
            self._process_pending_batch()

    def _should_process_batch(self) -> bool:
        """Determine if batch should be processed now"""
        if len(self.pending_requests) >= 10:
            return True  # Process when batch is full

        if time.time() - self.pending_requests[0]["timestamp"] > self.batch_timeout:
            return True  # Process when timeout reached

        # Check if high-priority request exists
        return any(req["priority"] == "high" for req in self.pending_requests)

    def _process_pending_batch(self) -> List[Dict]:
        """Process all pending requests in a single wake cycle"""
        if not self.pending_requests:
            return []

        # Acquire wake lock to prevent device sleep
        self._acquire_wake_lock()

        try:
            # Combine all requests into batch
            batch_input = self._combine_batch_inputs(self.pending_requests)

            # Single inference for entire batch
            batch_results = self._run_batch_inference(batch_input)

            # Distribute results back to individual requests
            return self._distribute_results(batch_results)
        finally:
            self._release_wake_lock()
            self.pending_requests.clear()
```

### 5. Background Processing Optimization

**Deferred Processing for Non-Critical Tasks:**

```python
class BackgroundTaskManager:
    def __init__(self):
        self.critical_tasks = []
        self.background_tasks = []
        self.charging_only_tasks = []

    def defer_non_critical(self, task: Dict) -> None:
        """Mark task as non-critical and defer if on battery"""
        battery = psutil.sensors_battery()

        if not battery or battery.power_plugged:
            # Execute immediately if on AC power
            self._execute_task(task)
        else:
            # Defer to charging or background processing
            if task.get("requires_charging", False):
                self.charging_only_tasks.append(task)
            else:
                self.background_tasks.append(task)

    def process_background_tasks(self) -> None:
        """Process background tasks during idle time"""
        if not self.background_tasks:
            return

        # Only process if battery > 50% or device is idle
        battery = psutil.sensors_battery()
        is_idle = self._check_device_idleness()

        if (battery and battery.percent > 50) or is_idle:
            task = self.background_tasks.pop(0)
            self._execute_task(task)
```

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

## Next Steps

1. Integrate with `edge-ai-management` for complete mobile optimization
2. Add support for platform-specific optimizations (Android, iOS)
3. Implement machine learning for predictive battery optimization
4. Add charging state awareness for task scheduling
