# Adaptive Quality Settings

Dynamic quality adjustment based on performance metrics and device capabilities.

## Dynamic Quality Adjustment

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

## Quality Levels Configuration

### High Quality
- **Batch Size:** 32
- **FPS Target:** 30
- **Latency:** 100ms
- **CPU Usage:** Up to 70%
- **Memory:** 512MB
- **Use Case:** When device is plugged in or high battery

### Medium Quality (Default)
- **Batch Size:** 16
- **FPS Target:** 20
- **Latency:** 200ms
- **CPU Usage:** Up to 50%
- **Memory:** 256MB
- **Use Case:** Normal mobile usage, balanced performance

### Low Quality
- **Batch Size:** 8
- **FPS Target:** 10
- **Latency:** 500ms
- **CPU Usage:** Up to 30%
- **Memory:** 128MB
- **Use Case:** Low battery or thermal concerns

### Minimal Quality
- **Batch Size:** 4
- **FPS Target:** 5
- **Latency:** 1000ms
- **CPU Usage:** Up to 20%
- **Memory:** 64MB
- **Use Case:** Critical battery saving mode

## Performance Metrics Collection

```python
import psutil
import time

class PerformanceMonitor:
    def __init__(self):
        self.metrics_window = []
        self.window_size = 60  # seconds
        self.last_measurement = time.time()

    def collect_metrics(self) -> Dict[str, float]:
        """Collect current performance metrics"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        battery = psutil.sensors_battery()

        metrics = {
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "memory_available_gb": memory.available / (1024**3),
            "battery_percent": battery.percent if battery else 100,
            "thermal_state": self._get_thermal_state()
        }

        self.metrics_window.append(metrics)
        if len(self.metrics_window) > self.window_size:
            self.metrics_window.pop(0)

        return metrics

    def _get_thermal_state(self) -> str:
        """Get thermal state (simplified)"""
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                cpu_temp = max([t.current for t in temps.get('cpu_thermal', [0])])
                if cpu_temp > 85:
                    return "critical"
                elif cpu_temp > 75:
                    return "warning"
                else:
                    return "normal"
        except:
            pass
        return "unknown"
```

## Quality Adjustment Algorithms

### Hysteresis-Based Adjustment

```python
class HysteresisQualityController:
    def __init__(self):
        self.quality_levels = ["minimal", "low", "medium", "high"]
        self.current_index = 1  # Start at medium
        self.hysteresis_margin = 0.1  # 10% margin

    def should_adjust_quality(self, metrics: Dict[str, float]) -> str:
        """Determine if quality adjustment is needed with hysteresis"""
        current_quality = self.quality_levels[self.current_index]
        threshold = self._get_quality_threshold(current_quality)

        # Check if we need to reduce quality
        if metrics["cpu_percent"] > threshold["cpu_max"] * (1 + self.hysteresis_margin):
            return self._reduce_quality()

        # Check if we can increase quality
        if (metrics["cpu_percent"] < threshold["cpu_min"] * (1 - self.hysteresis_margin) and
            metrics["fps"] > threshold["fps"] * 1.2):
            return self._increase_quality()

        return current_quality

    def _reduce_quality(self):
        """Safely reduce quality"""
        if self.current_index > 0:
            self.current_index -= 1
        return self.quality_levels[self.current_index]

    def _increase_quality(self):
        """Safely increase quality"""
        if self.current_index < len(self.quality_levels) - 1:
            self.current_index += 1
        return self.quality_levels[self.current_index]
```

### ML-Based Quality Prediction

```python
class MLQualityPredictor:
    def __init__(self):
        self.model = None  # In production, load trained model
        self.feature_history = []

    def predict_optimal_quality(self, features: Dict) -> str:
        """Use ML model to predict optimal quality"""
        # Extract features
        feature_vector = self._extract_features(features)

        # Store for training
        self.feature_history.append(feature_vector)

        # In production, use trained model
        # For now, use rule-based fallback
        return self._rule_based_prediction(features)

    def _extract_features(self, metrics: Dict) -> List[float]:
        """Extract features for ML model"""
        return [
            metrics["cpu_percent"],
            metrics["memory_percent"],
            metrics["battery_percent"],
            metrics.get("thermal_state", 0),
            metrics.get("fps", 0)
        ]

    def _rule_based_prediction(self, metrics: Dict) -> str:
        """Fallback rule-based prediction"""
        if metrics["battery_percent"] < 20:
            return "minimal"
        elif metrics["cpu_percent"] > 80 or metrics["thermal_state"] == "critical":
            return "low"
        elif metrics["cpu_percent"] > 50:
            return "medium"
        else:
            return "high"
```

## Context-Aware Quality

```python
class ContextAwareQualityController:
    def __init__(self):
        self.context = {
            "user_activity": "normal",
            "charging": False,
            "thermal_state": "normal",
            "app_importance": "normal"
        }

    def adjust_quality_with_context(self, metrics: Dict) -> str:
        """Adjust quality based on context and metrics"""
        base_quality = self._get_base_quality(metrics)

        # Adjust based on context
        if self.context["charging"]:
            base_quality = self._increase_quality(base_quality)

        if self.context["thermal_state"] == "warning":
            base_quality = self._decrease_quality(base_quality)

        if self.context["user_activity"] == "intensive":
            base_quality = self._increase_quality(base_quality)

        if self.context["app_importance"] == "critical":
            base_quality = self._increase_quality(base_quality)

        return base_quality

    def update_context(self, new_context: Dict):
        """Update context information"""
        self.context.update(new_context)
```

## Quality Transition Smoothing

```python
class SmoothQualityTransition:
    def __init__(self):
        self.current_quality = "medium"
        self.target_quality = "medium"
        self.transition_speed = 0.1  # 10% per adjustment cycle

    def set_target_quality(self, new_quality: str):
        """Set target quality for smooth transition"""
        if new_quality != self.target_quality:
            self.target_quality = new_quality

    def get_smooth_quality(self) -> str:
        """Get quality with smooth transitions"""
        if self.current_quality == self.target_quality:
            return self.current_quality

        # Gradually move towards target
        quality_levels = ["minimal", "low", "medium", "high"]
        current_idx = quality_levels.index(self.current_quality)
        target_idx = quality_levels.index(self.target_quality)

        if abs(target_idx - current_idx) == 1:
            # Adjacent levels - can transition
            self.current_quality = self.target_quality
        else:
            # Jump multiple levels - gradual transition
            step = 1 if target_idx > current_idx else -1
            self.current_quality = quality_levels[current_idx + step]

        return self.current_quality
```

## Quality Metrics Dashboard

```python
class QualityMetricsDashboard:
    def __init__(self):
        self.metrics_history = []

    def record_quality_adjustment(self, old_quality: str, new_quality: str,
                                 metrics: Dict, reason: str):
        """Record quality adjustment with context"""
        self.metrics_history.append({
            "timestamp": time.time(),
            "old_quality": old_quality,
            "new_quality": new_quality,
            "metrics": metrics,
            "reason": reason
        })

    def get_quality_statistics(self) -> Dict:
        """Get statistics on quality adjustments"""
        if not self.metrics_history:
            return {}

        recent = self.metrics_history[-100:]  # Last 100 adjustments

        return {
            "total_adjustments": len(recent),
            "quality_distribution": self._calculate_distribution(recent),
            "average_adjustment_interval": self._calculate_interval(recent),
            "common_reasons": self._calculate_reasons(recent)
        }

    def _calculate_distribution(self, history: List) -> Dict:
        """Calculate distribution of quality levels"""
        qualities = [h["new_quality"] for h in history]
        return {
            q: qualities.count(q) / len(qualities)
            for q in set(qualities)
        }
```

## Best Practices

### Do's
✅ Use smooth transitions between quality levels
✅ Consider context (charging, user activity) in decisions
✅ Monitor long-term performance trends
✅ Implement hysteresis to prevent oscillation
✅ Log quality adjustments for analysis
✅ Test quality changes under various conditions

### Don'ts
❌ Don't change quality too frequently
❌ Don't ignore battery and thermal context
❌ Don't jump between distant quality levels
❌ Don't forget to restore quality when conditions improve
❌ Don't use only CPU metrics - include battery and thermal
❌ Don't transition quality during critical operations

### Optimization Tips

1. **Gradual Transitions**
   - Change quality levels gradually
   - Allow system to stabilize
   - Monitor for oscillation

2. **Context Awareness**
   - Check if device is charging
   - Consider user activity patterns
   - Factor in app importance

3. **Multi-Metric Decisions**
   - Don't rely on single metric
   - Consider CPU, memory, battery, thermal
   - Weight metrics appropriately

4. **User Experience**
   - Prioritize user-perceived quality
   - Smooth transitions over abrupt changes
   - Communicate quality changes when critical
