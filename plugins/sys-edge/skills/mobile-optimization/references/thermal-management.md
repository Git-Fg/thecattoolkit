# Thermal Management

Temperature monitoring and throttling strategies for mobile devices.

## Temperature-Based Throttling

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

    def _get_cpu_temperature(self) -> float:
        """Get current CPU temperature"""
        try:
            # Try various methods to get temperature
            if hasattr(psutil, "sensors_temperatures"):
                temps = psutil.sensors_temperatures()
                if temps:
                    # Get average of all CPU cores
                    cpu_temps = [t.current for t in temps.get('cpu_thermal', [])]
                    if not cpu_temps:
                        cpu_temps = [t.current for t in temps.get('coretemp', [])]
                    return sum(cpu_temps) / len(cpu_temps)
        except:
            pass
        return 0.0  # Default if cannot read
```

## Thermal State Machine

```
NORMAL (T < 75°C)
    ↓ (T > 75°C)
THROTTLING (75°C < T < 85°C)
    ↓ (T > 85°C)
EMERGENCY SHUTDOWN (T > 85°C)
    ↓ (T < 65°C)
THROTTLING
    ↓ (T < 55°C)
NORMAL
```

## Temperature Thresholds

| State | Temperature | Action |
|-------|-------------|--------|
| Normal | < 75°C | Full performance |
| Warning | 75-85°C | Reduce load by 50% |
| Critical | > 85°C | Emergency shutdown |

## Advanced Thermal Control

### Adaptive Throttling

```python
class AdaptiveThermalController:
    def __init__(self):
        self.temperature_history = []
        self.throttling_levels = {
            "light": {"reduce_by": 0.25, "actions": ["reduce_batch_size"]},
            "moderate": {"reduce_by": 0.50, "actions": ["reduce_batch_size", "limit_workers"]},
            "heavy": {"reduce_by": 0.75, "actions": ["minimal_processing"]},
            "critical": {"reduce_by": 1.00, "actions": ["shutdown_non_critical"]}
        }

    def calculate_throttling_level(self, temp: float, rate_of_change: float) -> str:
        """Calculate appropriate throttling level based on temp and rate"""
        # Determine base level from temperature
        if temp > 85:
            return "critical"
        elif temp > 80:
            return "heavy"
        elif temp > 75:
            return "moderate"
        elif temp > 70:
            return "light"

        # Adjust based on rate of change
        if rate_of_change > 5:  # Rapid heating
            return self._increase_throttling_level()

        return "none"

    def _increase_throttling_level(self):
        """Increase throttling if temperature rising rapidly"""
        # Implementation for proactive throttling
        pass
```

### Thermal Prediction

```python
class ThermalPredictor:
    def __init__(self):
        self.temperature_history = []
        self.prediction_window = 60  # seconds

    def predict_temperature(self, current_temp: float, load: float) -> float:
        """Predict temperature based on current state and load"""
        # Simple linear prediction
        # In production, use ML model for better prediction

        if len(self.temperature_history) < 10:
            return current_temp

        # Calculate rate of change
        recent_temps = self.temperature_history[-10:]
        rate_of_change = (recent_temps[-1] - recent_temps[0]) / 10

        # Predict temperature in 1 minute
        predicted_temp = current_temp + (rate_of_change * 60)

        return predicted_temp

    def should_preemptively_throttle(self, predicted_temp: float) -> bool:
        """Determine if preemptive throttling is needed"""
        return predicted_temp > 80  # Threshold for preemptive action
```

### Cooling Strategies

```python
class CoolingManager:
    def __init__(self):
        self.active_cooling = False

    def apply_cooling_strategy(self, thermal_manager):
        """Apply active cooling measures"""
        temp = thermal_manager._get_cpu_temperature()

        cooling_actions = []

        if temp > 75:
            cooling_actions.extend([
                "reduce_screen_brightness",
                "limit_network_activity",
                "pause_background_sync",
                "reduce_animation_quality"
            ])

        if temp > 80:
            cooling_actions.extend([
                "enable_cpu_undervolting",
                "limit_gpu_frequency",
                "activate_fan_boost"
            ])

        if temp > 85:
            cooling_actions.extend([
                "emergency_cpu_throttle",
                "disable_non_essential_sensors",
                "force_garbage_collection"
            ])

        return cooling_actions
```

## Integration with Processing Pipeline

```python
class ThermalAwareProcessor:
    def __init__(self):
        self.thermal_manager = ThermalManager()
        self.processor = ModelProcessor()

    def process_with_thermal_awareness(self, input_data):
        """Process with thermal management"""
        thermal_status = self.thermal_manager.monitor_temperature()

        if thermal_status["status"] == "normal":
            # Full processing power
            return self.processor.process_full(input_data)

        elif thermal_status["status"] == "throttling":
            # Reduced processing
            reduced_config = self._get_throttled_config(thermal_status)
            return self.processor.process_with_config(input_data, reduced_config)

        elif thermal_status["status"] == "emergency_shutdown":
            # Save state and pause
            self._save_state()
            raise ThermalEmergencyException("Device too hot, pausing processing")

    def _get_throttled_config(self, thermal_status):
        """Get configuration based on thermal status"""
        return {
            "batch_size": 4,  # Reduced from 32
            "quality": "minimal",
            "parallel_workers": 1,
            "cache_enabled": False
        }
```

## Monitoring and Alerting

### Thermal Event Logging

```python
class ThermalLogger:
    def __init__(self):
        self.events = []

    def log_thermal_event(self, event_type: str, temperature: float, action: str):
        """Log thermal events for analysis"""
        self.events.append({
            "timestamp": time.time(),
            "type": event_type,
            "temperature": temperature,
            "action": action
        })

    def get_thermal_summary(self) -> Dict:
        """Get summary of thermal events"""
        if not self.events:
            return {"total_events": 0}

        return {
            "total_events": len(self.events),
            "max_temperature": max(e["temperature"] for e in self.events),
            "throttling_events": sum(1 for e in self.events if e["type"] == "throttling"),
            "emergency_events": sum(1 for e in self.events if e["type"] == "emergency")
        }
```

## Best Practices

### Do's
GOOD Monitor temperature continuously during processing
GOOD Implement gradual throttling before emergency shutdown
GOOD Save state before critical temperature
GOOD Log all thermal events for analysis
GOOD Predict temperature based on load and history
GOOD Use multiple temperature sensors if available

### Don'ts
BAD Don't wait for critical temperature before acting
BAD Don't disable thermal management to maintain performance
BAD Don't ignore temperature spikes during intensive tasks
BAD Don't resume full processing immediately after cooling
BAD Don't rely on a single temperature reading

### Optimization Tips

1. **Proactive Throttling**
   - Monitor rate of temperature increase
   - Throttle before reaching critical levels
   - Balance performance and temperature

2. **Smart Workload Distribution**
   - Spread intensive tasks over time
   - Allow cooling periods between batches
   - Use thermal-friendly scheduling

3. **Hardware Integration**
   - Use platform-specific thermal APIs
   - Monitor multiple sensors
   - Consider ambient temperature
