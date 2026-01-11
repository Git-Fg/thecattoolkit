# Intent Classification

## Overview

The `IntentClassifier` class translates natural language commands into structured intent classifications with confidence scores and parameter mappings.

## Implementation

```python
from typing import Dict, List, Tuple
import re

class IntentClassifier:
    def __init__(self):
        self.intent_patterns = {
            'cinematic': {
                'keywords': ['cinematic', 'movie-like', 'film', 'dramatic'],
                'parameters': {
                    'speed': 0.8,
                    'color_grade': 'cinematic_lut',
                    'blur_background': True,
                    'letterbox': True
                }
            },
            'fast_cut': {
                'keywords': ['quick', 'fast', 'rapid', 'snappy'],
                'parameters': {
                    'transition_duration': 0.2,
                    'cut_frequency': 'high',
                    'rhythm': 'fast'
                }
            },
            'slow_motion': {
                'keywords': ['slow', 'dramatic', 'pause', 'slo-mo'],
                'parameters': {
                    'speed': 0.5,
                    'hold_frames': True,
                    'easing': 'smooth'
                }
            },
            'color_grade': {
                'keywords': ['warm', 'cool', 'vintage', 'mood', 'atmosphere'],
                'parameters': {
                    'color_temp': 'auto',
                    'saturation': 'adaptive',
                    'contrast': 'enhanced'
                }
            },
            'pacing': {
                'keywords': ['faster', 'slower', 'rhythm', 'beat'],
                'parameters': {
                    'tempo_sync': True,
                    'beat_matching': True
                }
            }
        }

    def classify_intent(self, command: str) -> Dict:
        """Classify user intent from natural language"""
        command_lower = command.lower()
        matched_intents = []

        for intent, pattern in self.intent_patterns.items():
            if any(keyword in command_lower for keyword in pattern['keywords']):
                confidence = self._calculate_confidence(command_lower, pattern['keywords'])
                matched_intents.append({
                    'intent': intent,
                    'confidence': confidence,
                    'parameters': pattern['parameters']
                })

        # Sort by confidence
        matched_intents.sort(key=lambda x: x['confidence'], reverse=True)

        return {
            'command': command,
            'primary_intent': matched_intents[0]['intent'] if matched_intents else None,
            'all_intents': matched_intents,
            'requires_context': self._requires_context(command)
        }
```

## Intent Categories

### 1. Cinematic Intent
**Keywords**: cinematic, movie-like, film, dramatic
**Parameters**:
- Speed: 0.8 (20% slowdown)
- Color grade: Cinematic LUT
- Background blur: Enabled
- Letterbox: Enabled

**Examples**:
- "Make it cinematic" → Cinematic parameters
- "Film look" → Cinematic parameters
- "Dramatic effect" → Cinematic parameters

### 2. Fast Cut Intent
**Keywords**: quick, fast, rapid, snappy
**Parameters**:
- Transition duration: 0.2 seconds
- Cut frequency: High
- Rhythm: Fast

**Examples**:
- "Quick cuts" → Fast cut parameters
- "Make it snappy" → Fast cut parameters
- "Rapid transitions" → Fast cut parameters

### 3. Slow Motion Intent
**Keywords**: slow, dramatic, pause, slo-mo
**Parameters**:
- Speed: 0.5 (50% slowdown)
- Hold frames: Enabled
- Easing: Smooth

**Examples**:
- "Slow motion" → Slow motion parameters
- "Dramatic pause" → Slow motion parameters
- "Slo-mo effect" → Slow motion parameters

### 4. Color Grade Intent
**Keywords**: warm, cool, vintage, mood, atmosphere
**Parameters**:
- Color temperature: Auto
- Saturation: Adaptive
- Contrast: Enhanced

**Examples**:
- "Warm colors" → Color grade parameters
- "Cool atmosphere" → Color grade parameters
- "Vintage look" → Color grade parameters

### 5. Pacing Intent
**Keywords**: faster, slower, rhythm, beat
**Parameters**:
- Tempo sync: Enabled
- Beat matching: Enabled

**Examples**:
- "Match the beat" → Pacing parameters
- "Faster rhythm" → Pacing parameters
- "Sync to music" → Pacing parameters

## Confidence Calculation

```python
def _calculate_confidence(self, command: str, keywords: List[str]) -> float:
    """Calculate confidence score for intent match"""
    matches = sum(1 for keyword in keywords if keyword in command)
    keyword_ratio = matches / len(keywords)

    # Bonus for exact keyword matches
    exact_matches = sum(1 for keyword in keywords if f' {keyword} ' in f' {command} ')
    exact_bonus = exact_matches * 0.2

    confidence = min(keyword_ratio + exact_bonus, 1.0)
    return confidence
```

## Context Requirements

```python
def _requires_context(self, command: str) -> bool:
    """Determine if command requires video context"""
    contextual_keywords = ['this', 'that', 'here', 'current', 'scene']
    return any(keyword in command.lower() for keyword in contextual_keywords)
```

## Usage

```python
classifier = IntentClassifier()

# Classify command
result = classifier.classify_intent("Make this video cinematic with warm colors")

print(result)
# Output:
# {
#     'command': 'Make this video cinematic with warm colors',
#     'primary_intent': 'cinematic',
#     'all_intents': [
#         {'intent': 'cinematic', 'confidence': 0.8, 'parameters': {...}},
#         {'intent': 'color_grade', 'confidence': 0.6, 'parameters': {...}}
#     ],
#     'requires_context': True
# }
```

## Integration Points

- Used by `IntentTranslator` for command processing
- Referenced by parameter mapping system
- Supports custom intent patterns

## Extensibility

To add new intent patterns:

```python
self.intent_patterns['new_intent'] = {
    'keywords': ['keyword1', 'keyword2'],
    'parameters': {
        'param1': value1,
        'param2': value2
    }
}
```

## Best Practices

1. **Keyword Coverage**: Include common synonyms
2. **Confidence Scoring**: Use weighted confidence for accuracy
3. **Context Awareness**: Detect when context is needed
4. **Pattern Updates**: Regularly update patterns based on usage
5. **Multi-Intent Support**: Handle commands with multiple intents
