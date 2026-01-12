# Background Processing Optimization

Deferred processing strategies for non-critical tasks on mobile devices.

## Background Task Manager

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

    def _check_device_idleness(self) -> bool:
        """Check if device is currently idle"""
        # Check CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)

        # Check network activity
        network = psutil.net_io_counters()
        network_idle = network.bytes_sent + network.bytes_recv < 1024  # Less than 1KB

        # Check disk activity
        disk_io = psutil.disk_io_counters()
        disk_idle = disk_io.read_bytes + disk_io.write_bytes < 1024  # Less than 1KB

        return cpu_percent < 10 and network_idle and disk_idle
```

## Task Classification

```python
class TaskClassifier:
    def __init__(self):
        self.critical_keywords = [
            "user_action", "ui_response", "critical", "urgent",
            "realtime", "interactive"
        ]
        self.background_keywords = [
            "sync", "cleanup", "cache", "preload", "index",
            "backup", "compress", "analyze"
        ]
        self.charging_keywords = [
            "heavy_processing", "training", "download_large",
            "backup_full", "reindex"
        ]

    def classify_task(self, task: Dict) -> str:
        """Automatically classify task priority"""
        task_description = task.get("description", "").lower()
        task_type = task.get("type", "").lower()

        # Check for critical indicators
        if (any(keyword in task_description for keyword in self.critical_keywords) or
            task_type in ["realtime", "interactive"]):
            return "critical"

        # Check for charging-only indicators
        if (any(keyword in task_description for keyword in self.charging_keywords) or
            task_type in ["training", "heavy_processing"]):
            return "charging_only"

        # Check for background indicators
        if (any(keyword in task_description for keyword in self.background_keywords) or
            task_type in ["sync", "cleanup"]):
            return "background"

        # Default classification
        return "normal"

    def should_defer(self, task: Dict, battery_percent: float) -> bool:
        """Determine if task should be deferred"""
        classification = self.classify_task(task)

        if classification == "critical":
            return False

        if classification == "charging_only":
            return battery_percent < 100  # Only execute when fully charged

        if classification == "background":
            return battery_percent < 50  # Defer when battery < 50%

        # Normal tasks
        return battery_percent < 30  # Defer when battery < 30%
```

## Intelligent Scheduling

```python
class IntelligentScheduler:
    def __init__(self):
        self.scheduling_rules = {
            "battery_threshold": 50,
            "idle_check_interval": 60,  # seconds
            "max_background_batch": 5,
            "charging_only_threshold": 80
        }

    def schedule_task(self, task: Dict) -> Dict:
        """Schedule task intelligently"""
        battery = psutil.sensors_battery()
        is_idle = self._check_device_idleness()

        schedule = {
            "execute_now": False,
            "defer_to_background": False,
            "defer_to_charging": False,
            "scheduled_time": time.time()
        }

        # Critical tasks always execute now
        if self._is_critical_task(task):
            schedule["execute_now"] = True
            return schedule

        # Charging-only tasks
        if task.get("requires_charging", False):
            if battery and battery.power_plugged:
                schedule["execute_now"] = True
            else:
                schedule["defer_to_charging"] = True
            return schedule

        # Background tasks
        if task.get("can_background", False):
            if battery and battery.percent > self.scheduling_rules["battery_threshold"]:
                schedule["execute_now"] = True
            else:
                schedule["defer_to_background"] = True
            return schedule

        # Normal tasks
        if battery:
            if battery.power_plugged or battery.percent > 70:
                schedule["execute_now"] = True
            elif battery.percent > 30:
                if is_idle:
                    schedule["execute_now"] = True
                else:
                    schedule["defer_to_background"] = True
            else:
                schedule["defer_to_background"] = True

        return schedule

    def _is_critical_task(self, task: Dict) -> bool:
        """Check if task is critical"""
        critical_types = ["user_action", "ui_response", "realtime"]
        return task.get("type") in critical_types
```

## Battery-Aware Processing

```python
class BatteryAwareProcessor:
    def __init__(self):
        self.battery_thresholds = {
            "full_performance": 80,
            "reduced_performance": 50,
            "minimal_performance": 30,
            "suspend_non_critical": 20
        }

    def adjust_processing_for_battery(self, task: Dict, battery_percent: float) -> Dict:
        """Adjust task processing based on battery level"""
        config = {
            "batch_size": 16,
            "priority": task.get("priority", "normal"),
            "can_parallel": True,
            "processing_quality": "high"
        }

        if battery_percent >= self.battery_thresholds["full_performance"]:
            # Full performance
            config.update({
                "batch_size": 32,
                "processing_quality": "high"
            })

        elif battery_percent >= self.battery_thresholds["reduced_performance"]:
            # Reduced performance
            config.update({
                "batch_size": 16,
                "processing_quality": "medium"
            })

        elif battery_percent >= self.battery_thresholds["minimal_performance"]:
            # Minimal performance
            config.update({
                "batch_size": 8,
                "processing_quality": "low",
                "can_parallel": False
            })

        else:
            # Critical battery - only critical tasks
            config.update({
                "batch_size": 4,
                "processing_quality": "minimal",
                "can_parallel": False,
                "suspend_non_critical": True
            })

        return config
```

## Background Sync Optimization

```python
class BackgroundSyncManager:
    def __init__(self):
        self.sync_queues = {
            "high_priority": [],
            "normal_priority": [],
            "low_priority": []
        }
        self.last_sync_time = {}

    def queue_for_sync(self, data: Dict, priority: str = "normal"):
        """Queue data for background synchronization"""
        sync_item = {
            "data": data,
            "timestamp": time.time(),
            "retry_count": 0,
            "max_retries": 3
        }

        self.sync_queues[priority].append(sync_item)

    def process_sync_queue(self, battery_percent: float, is_charging: bool) -> List[Dict]:
        """Process synchronization queue based on conditions"""
        results = []

        # Only sync high priority items when battery is low
        if battery_percent < 30 and not is_charging:
            queue_to_process = ["high_priority"]
        # Process normal and high priority when on battery but sufficient
        elif battery_percent < 50 and not is_charging:
            queue_to_process = ["high_priority", "normal_priority"]
        # Process all queues when charging
        else:
            queue_to_process = ["high_priority", "normal_priority", "low_priority"]

        for priority in queue_to_process:
            while self.sync_queues[priority]:
                item = self.sync_queues[priority].pop(0)
                try:
                    result = self._sync_item(item)
                    results.append(result)
                except Exception as e:
                    item["retry_count"] += 1
                    if item["retry_count"] < item["max_retries"]:
                        # Re-queue for retry
                        self.sync_queues[priority].append(item)
                    else:
                        # Max retries reached
                        results.append({"error": str(e), "item": item})

        return results

    def _sync_item(self, item: Dict) -> Dict:
        """Sync individual item"""
        # Implementation depends on sync target
        return {"status": "synced", "timestamp": time.time()}
```

## Predictive Deferred Processing

```python
class PredictiveDeferredProcessor:
    def __init__(self):
        self.usage_patterns = []
        self.prediction_window = 3600  # 1 hour

    def learn_usage_pattern(self, timestamp: float, activity_level: float):
        """Learn device usage patterns"""
        self.usage_patterns.append({
            "timestamp": timestamp,
            "activity": activity_level
        })

        # Keep only recent patterns
        cutoff = time.time() - self.prediction_window
        self.usage_patterns = [
            p for p in self.usage_patterns if p["timestamp"] > cutoff
        ]

    def predict_optimal_processing_time(self) -> float:
        """Predict when device will be idle/charging"""
        if not self.usage_patterns:
            return time.time() + 3600  # Default: 1 hour from now

        # Find time of day with lowest activity
        hourly_activity = {}
        for pattern in self.usage_patterns:
            hour = time.localtime(pattern["timestamp"]).tm_hour
            if hour not in hourly_activity:
                hourly_activity[hour] = []
            hourly_activity[hour].append(pattern["activity"])

        # Calculate average activity per hour
        avg_activity = {
            hour: sum(activities) / len(activities)
            for hour, activities in hourly_activity.items()
        }

        # Find hour with lowest activity
        optimal_hour = min(avg_activity, key=avg_activity.get)

        # Schedule for next occurrence of optimal hour
        now = time.time()
        optimal_time = time.mktime(
            time.strptime(
                f"{time.localtime(now).tm_year} {time.localtime(now).tm_mon} "
                f"{time.localtime(now).tm_mday} {optimal_hour} 0 0",
                "%Y %m %d %H %M %S"
            )
        )

        # If optimal hour has passed today, schedule for tomorrow
        if optimal_time <= now:
            optimal_time += 86400  # Add 24 hours

        return optimal_time
```

## Resource-Constrained Processing

```python
class ResourceConstrainedProcessor:
    def __init__(self):
        self.memory_threshold = 0.8  # 80%
        self.cpu_threshold = 0.7  # 70%
        self.disk_threshold = 0.9  # 90%

    def check_resources(self) -> Dict[str, bool]:
        """Check if resources are available for processing"""
        resources = {
            "memory_ok": self._check_memory(),
            "cpu_ok": self._check_cpu(),
            "disk_ok": self._check_disk()
        }

        return resources

    def _check_memory(self) -> bool:
        """Check if sufficient memory is available"""
        memory = psutil.virtual_memory()
        return memory.percent < (self.memory_threshold * 100)

    def _check_cpu(self) -> bool:
        """Check if CPU load is acceptable"""
        cpu_percent = psutil.cpu_percent(interval=1)
        return cpu_percent < (self.cpu_threshold * 100)

    def _check_disk(self) -> bool:
        """Check if disk space is sufficient"""
        disk = psutil.disk_usage('/')
        return disk.percent < (self.disk_threshold * 100)

    def get_processing_recommendation(self) -> str:
        """Get recommendation for processing"""
        resources = self.check_resources()

        if all(resources.values()):
            return "process_now"
        elif not resources["cpu_ok"]:
            return "defer_cpu_intensive"
        elif not resources["memory_ok"]:
            return "defer_memory_intensive"
        elif not resources["disk_ok"]:
            return "defer_disk_intensive"
        else:
            return "defer_all_non_critical"
```

## Best Practices

### Do's
✅ Classify tasks by criticality automatically
✅ Defer non-critical tasks during low battery
✅ Process background tasks during idle periods
✅ Queue synchronization items intelligently
✅ Learn usage patterns for predictive scheduling
✅ Monitor resource availability before processing
✅ Implement exponential backoff for retries

### Don'ts
❌ Don't process heavy tasks on low battery
❌ Don't ignore device idleness signals
❌ Don't queue too many background tasks
❌ Don't retry failed tasks indefinitely
❌ Don't process during active user interaction
❌ Don't forget to clean up completed tasks
❌ Don't defer critical user-initiated tasks

### Optimization Strategies

1. **Smart Classification**
   - Use keywords and patterns to auto-classify tasks
   - Consider user behavior patterns
   - Allow manual override for specific tasks

2. **Predictive Scheduling**
   - Learn when device is typically idle
   - Schedule heavy tasks during charging
   - Use historical data to optimize timing

3. **Resource Awareness**
   - Monitor CPU, memory, and disk usage
   - Defer tasks when resources are constrained
   - Process tasks when resources are abundant

4. **Battery-First Design**
   - Always consider battery impact
   - Prioritize charging time for heavy processing
   - Use adaptive processing based on battery level
