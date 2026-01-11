# Feedback Processing

## Overview

The `FeedbackProcessor` class incorporates user feedback to improve intent classification and parameter mapping over time, creating a learning system for better translation accuracy.

## Implementation

```python
from typing import Dict, List, Optional
import json
import time

class FeedbackProcessor:
    def __init__(self):
        self.feedback_history = []
        self.learning_patterns = {}
        self.confidence_threshold = 0.7

    def process_feedback(self, original_command: str, original_intent: Dict,
                       applied_edits: Dict, user_feedback: Dict) -> Dict:
        """Process user feedback to improve future translations"""
        feedback_entry = {
            'timestamp': time.time(),
            'command': original_command,
            'original_intent': original_intent,
            'applied_edits': applied_edits,
            'user_feedback': user_feedback,
            'analysis': self._analyze_feedback(original_intent, user_feedback)
        }

        self.feedback_history.append(feedback_entry)

        # Update learning patterns
        self._update_patterns(feedback_entry)

        # Generate improvement recommendations
        improvements = self._generate_improvements(feedback_entry)

        return {
            'feedback_recorded': True,
            'improvements_applied': improvements,
            'learning_progress': self._calculate_learning_progress()
        }

    def _analyze_feedback(self, original_intent: Dict, feedback: Dict) -> Dict:
        """Analyze feedback for learning insights"""
        analysis = {
            'was_successful': feedback.get('satisfaction', 0) >= 3,
            'accuracy_score': self._calculate_accuracy(original_intent, feedback),
            'missing_intents': self._identify_missing_intents(feedback),
            'incorrect_parameters': self._identify_parameter_errors(feedback),
            'user_suggestions': feedback.get('suggestions', [])
        }

        return analysis

    def _calculate_accuracy(self, intent: Dict, feedback: Dict) -> float:
        """Calculate translation accuracy score"""
        accuracy_factors = []

        # Intent match accuracy
        matched_intents = intent.get('all_intents', [])
        if matched_intents:
            top_confidence = matched_intents[0]['confidence']
            accuracy_factors.append(top_confidence)

        # User satisfaction
        satisfaction = feedback.get('satisfaction', 0) / 5.0
        accuracy_factors.append(satisfaction)

        # Edit success
        edit_success = 1.0 if feedback.get('edit_applied', False) else 0.0
        accuracy_factors.append(edit_success)

        return sum(accuracy_factors) / len(accuracy_factors)

    def _identify_missing_intents(self, feedback: Dict) -> List[str]:
        """Identify intents that should have been detected"""
        user_intents = feedback.get('intended_intents', [])
        system_intents = feedback.get('detected_intents', [])

        missing = []
        for intent in user_intents:
            if intent not in system_intents:
                missing.append(intent)

        return missing

    def _identify_parameter_errors(self, feedback: Dict) -> List[Dict]:
        """Identify which parameters were incorrect"""
        errors = []

        suggested_params = feedback.get('suggested_parameters', {})
        actual_params = feedback.get('applied_parameters', {})

        for param, suggested_value in suggested_params.items():
            actual_value = actual_params.get(param)
            if suggested_value != actual_value:
                errors.append({
                    'parameter': param,
                    'expected': suggested_value,
                    'actual': actual_value,
                    'severity': self._calculate_error_severity(param, suggested_value, actual_value)
                })

        return errors

    def _calculate_error_severity(self, param: str, expected: any, actual: any) -> str:
        """Calculate severity of parameter error"""
        if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
            diff = abs(expected - actual)
            if diff > 0.5:
                return 'high'
            elif diff > 0.2:
                return 'medium'
            else:
                return 'low'

        if expected != actual:
            return 'high'
        else:
            return 'none'
```

## Learning Mechanisms

### Pattern Learning
```python
def _update_patterns(self, feedback_entry: Dict):
    """Update learning patterns based on feedback"""
    command = feedback_entry['command'].lower()
    analysis = feedback_entry['analysis']

    # Extract successful patterns
    if analysis['was_successful']:
        self._record_successful_pattern(command, feedback_entry)
    else:
        self._record_failed_pattern(command, feedback_entry)

def _record_successful_pattern(self, command: str, entry: Dict):
    """Record pattern that led to successful translation"""
    # Extract keywords from command
    keywords = self._extract_keywords(command)

    # Record pattern
    for keyword in keywords:
        if keyword not in self.learning_patterns:
            self.learning_patterns[keyword] = {'success_count': 0, 'intent_mapping': {}}

        self.learning_patterns[keyword]['success_count'] += 1

        # Update intent mapping
        intents = entry['original_intent'].get('all_intents', [])
        for intent in intents:
            intent_name = intent['intent']
            if intent_name not in self.learning_patterns[keyword]['intent_mapping']:
                self.learning_patterns[keyword]['intent_mapping'][intent_name] = 0
            self.learning_patterns[keyword]['intent_mapping'][intent_name] += 1
```

### Intent Refinement
```python
def refine_intent_classification(self, command: str) -> Dict:
    """Refine intent classification using learned patterns"""
    keywords = self._extract_keywords(command)

    # Get pattern-based adjustments
    adjustments = self._get_pattern_adjustments(keywords)

    # Apply adjustments to classification
    refined_intents = self._apply_adjustments(command, adjustments)

    return refined_intents

def _get_pattern_adjustments(self, keywords: List[str]) -> Dict:
    """Get intent adjustments from learned patterns"""
    adjustments = {
        'boost_intents': [],
        'new_intents': [],
        'parameter_weights': {}
    }

    for keyword in keywords:
        if keyword in self.learning_patterns:
            pattern = self.learning_patterns[keyword]

            # Boost frequently successful intents
            for intent, count in pattern['intent_mapping'].items():
                if count > 2:  # Threshold for pattern recognition
                    adjustments['boost_intents'].append({
                        'intent': intent,
                        'boost': min(count * 0.1, 0.5)  # Max 50% boost
                    })

    return adjustments
```

## Feedback Types

### Satisfaction Feedback
```python
satisfaction_feedback = {
    'type': 'satisfaction',
    'satisfaction': 4,  # 1-5 scale
    'comment': 'Good cinematic effect, but could be warmer'
}
```

### Edit Feedback
```python
edit_feedback = {
    'type': 'edit_quality',
    'edit_applied': True,
    'quality_score': 3,
    'issues': ['Too slow', 'Color too cool']
}
```

### Intent Feedback
```python
intent_feedback = {
    'type': 'intent_accuracy',
    'intended_intents': ['cinematic', 'color_grade'],
    'detected_intents': ['cinematic'],
    'missing_intents': ['color_grade'],
    'incorrect_intents': []
}
```

### Parameter Feedback
```python
parameter_feedback = {
    'type': 'parameter_accuracy',
    'suggested_parameters': {
        'speed': 0.7,
        'color_temp': 'warm'
    },
    'applied_parameters': {
        'speed': 0.8,
        'color_temp': 'neutral'
    }
}
```

## Learning Progress Tracking

```python
def _calculate_learning_progress(self) -> Dict:
    """Calculate learning progress metrics"""
    total_feedback = len(self.feedback_history)
    successful_translations = sum(1 for f in self.feedback_history
                                  if f['analysis']['was_successful'])

    if total_feedback == 0:
        return {'progress': 0, 'total_feedback': 0}

    success_rate = successful_translations / total_feedback

    # Calculate improvement trend
    recent_success_rate = self._calculate_recent_success_rate(10)

    return {
        'total_feedback': total_feedback,
        'overall_success_rate': success_rate,
        'recent_success_rate': recent_success_rate,
        'trend': 'improving' if recent_success_rate > success_rate else 'stable',
        'patterns_learned': len(self.learning_patterns)
    }

def _calculate_recent_success_rate(self, window: int) -> float:
    """Calculate success rate for recent feedback"""
    recent = self.feedback_history[-window:] if len(self.feedback_history) >= window else self.feedback_history
    successful = sum(1 for f in recent if f['analysis']['was_successful'])
    return successful / len(recent) if recent else 0
```

## Usage

```python
processor = FeedbackProcessor()

# Process user feedback
result = processor.process_feedback(
    original_command="Make it cinematic",
    original_intent={...},
    applied_edits={...},
    user_feedback={
        'satisfaction': 4,
        'comment': 'Good but needs warmer colors',
        'suggestions': ['Make colors warmer']
    }
)

print(result)
# Output:
# {
#     'feedback_recorded': True,
#     'improvements_applied': [...],
#     'learning_progress': {...}
# }
```

## Continuous Learning

1. **Collect Feedback**: Gather feedback on every translation
2. **Analyze Patterns**: Identify successful and failed patterns
3. **Refine Classification**: Improve intent classification accuracy
4. **Update Parameters**: Adjust default parameters based on feedback
5. **Track Progress**: Monitor learning progress over time

## Best Practices

1. **Frequent Updates**: Update patterns after each feedback
2. **Weight Recent Feedback**: Give more weight to recent feedback
3. **Pattern Validation**: Validate patterns before applying
4. **User Privacy**: Anonymize feedback data
5. **Gradual Improvement**: Make small, incremental adjustments
