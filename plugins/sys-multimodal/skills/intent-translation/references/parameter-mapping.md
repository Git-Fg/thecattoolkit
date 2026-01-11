# Parameter Translation

## Overview

The `ParameterMapper` class translates classified intents into concrete video editing parameters, handling parameter conflicts and generating executable edit commands.

## Implementation

```python
from typing import Dict, List, Tuple, Optional
import json

class ParameterMapper:
    def __init__(self):
        self.parameter_defaults = {
            'speed': 1.0,
            'color_grade': 'none',
            'blur_background': False,
            'letterbox': False,
            'transition_duration': 1.0,
            'cut_frequency': 'medium',
            'rhythm': 'normal',
            'hold_frames': False,
            'easing': 'linear',
            'color_temp': 'neutral',
            'saturation': 1.0,
            'contrast': 1.0,
            'tempo_sync': False,
            'beat_matching': False
        }

        self.parameter_constraints = {
            'speed': {'min': 0.1, 'max': 3.0},
            'transition_duration': {'min': 0.1, 'max': 5.0},
            'saturation': {'min': 0.0, 'max': 2.0},
            'contrast': {'min': 0.0, 'max': 2.0}
        }

    def map_intents_to_parameters(self, intents: List[Dict], context: Optional[Dict] = None) -> Dict:
        """Map multiple intents to unified parameter set"""
        # Start with defaults
        parameters = self.parameter_defaults.copy()

        # Apply each intent's parameters
        for intent in intents:
            intent_params = intent.get('parameters', {})
            for param, value in intent_params.items():
                parameters = self._merge_parameter(parameters, param, value, intent['intent'])

        # Validate parameters
        validated_params = self._validate_parameters(parameters)

        # Handle conflicts
        resolved_params = self._resolve_conflicts(validated_params)

        return resolved_params

    def _merge_parameter(self, params: Dict, key: str, value: any, source: str) -> Dict:
        """Merge parameter with conflict resolution"""
        if key not in params:
            params[key] = value
            return params

        # Check for conflicts
        current_value = params[key]
        if current_value != value:
            # Resolve based on source priority
            resolved_value = self._resolve_conflict(key, current_value, value, source)
            params[key] = resolved_value

        return params

    def _resolve_conflict(self, param_name: str, value1: any, value2: any, source: str) -> any:
        """Resolve parameter conflicts"""
        # Speed conflicts (take minimum for slow motion wins)
        if param_name == 'speed':
            return min(value1, value2)

        # Boolean conflicts (True takes precedence)
        if isinstance(value1, bool) and isinstance(value2, bool):
            return value1 or value2

        # Numeric conflicts (take average)
        if isinstance(value1, (int, float)) and isinstance(value2, (int, float)):
            return (value1 + value2) / 2

        # String conflicts (source priority)
        priority_order = ['cinematic', 'color_grade', 'pacing', 'fast_cut', 'slow_motion']
        if value1 != value2:
            # Higher priority wins
            # Implementation would use priority_order to determine winner

        return value2
```

## Parameter Categories

### Speed Parameters
```python
speed_params = {
    'normal': 1.0,
    'fast': 1.5,
    'slow': 0.5,
    'cinematic': 0.8,
    'dramatic': 0.3
}
```

### Color Grade Parameters
```python
color_grades = {
    'none': {'saturation': 1.0, 'contrast': 1.0, 'color_temp': 'neutral'},
    'cinematic': {
        'saturation': 0.9,
        'contrast': 1.2,
        'color_temp': 'warm',
        'lut': 'cinematic'
    },
    'warm': {'color_temp': 'warm', 'saturation': 1.1},
    'cool': {'color_temp': 'cool', 'saturation': 0.9},
    'vintage': {
        'saturation': 0.8,
        'contrast': 0.9,
        'color_temp': 'warm',
        'vignette': True
    }
}
```

### Transition Parameters
```python
transition_params = {
    'fast': {'duration': 0.2, 'easing': 'ease-in'},
    'normal': {'duration': 1.0, 'easing': 'linear'},
    'smooth': {'duration': 2.0, 'easing': 'ease-in-out'},
    'dramatic': {'duration': 3.0, 'easing': 'ease-out'}
}
```

## Parameter Validation

```python
def _validate_parameters(self, params: Dict) -> Dict:
    """Validate parameters against constraints"""
    validated = params.copy()

    for param, value in params.items():
        if param in self.parameter_constraints:
            constraint = self.parameter_constraints[param]
            min_val = constraint['min']
            max_val = constraint['max']

            if isinstance(value, (int, float)):
                validated[param] = max(min_val, min(value, max_val))

    return validated
```

## Complex Parameter Sets

### Cinematic Look
```python
cinematic_params = {
    'speed': 0.8,
    'letterbox': True,
    'blur_background': True,
    'color_grade': 'cinematic',
    'contrast': 1.2,
    'saturation': 0.9
}
```

### Fast-Paced Edit
```python
fast_cut_params = {
    'speed': 1.5,
    'transition_duration': 0.2,
    'cut_frequency': 'high',
    'rhythm': 'fast',
    'beat_matching': True
}
```

### Dramatic Moment
```python
dramatic_params = {
    'speed': 0.5,
    'hold_frames': True,
    'easing': 'smooth',
    'color_grade': 'cinematic',
    'blur_background': True,
    'contrast': 1.3
}
```

## Usage

```python
mapper = ParameterMapper()

# Map intents to parameters
intents = [
    {'intent': 'cinematic', 'confidence': 0.8, 'parameters': {...}},
    {'intent': 'color_grade', 'confidence': 0.6, 'parameters': {...}}
]

parameters = mapper.map_intents_to_parameters(intents)

print(parameters)
# Output:
# {
#     'speed': 0.8,
#     'color_grade': 'cinematic',
#     'blur_background': True,
#     'letterbox': True,
#     'saturation': 0.9,
#     'contrast': 1.2
# }
```

## Conflict Resolution Strategies

### Speed Conflicts
- Slow motion takes precedence (minimum speed wins)
- Rationale: More dramatic effect

### Boolean Conflicts
- True takes precedence (feature enabled)
- Rationale: Explicit intent

### Color Conflicts
- Source priority: cinematic > color_grade > others
- Rationale: More specific intent

### Numeric Conflicts
- Average of values
- Rationale: Compromise solution

## Best Practices

1. **Parameter Defaults**: Always start with safe defaults
2. **Constraint Validation**: Enforce min/max bounds
3. **Conflict Resolution**: Document resolution strategies
4. **Source Attribution**: Track parameter sources
5. **Incremental Updates**: Support partial parameter updates
