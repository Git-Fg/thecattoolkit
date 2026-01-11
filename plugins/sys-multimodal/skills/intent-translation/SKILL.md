---
name: intent-translation
description: "USE when translating natural language editing commands into concrete video editing parameters. Converts user intent like 'make this cinematic' into specific cuts, transitions, color grades, and effects."
context: fork
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# Intent Translation Protocol

## Purpose

Translates natural language editing commands into precise, executable video editing parameters and workflows. Bridges the gap between user intent and technical implementation.

## Core Responsibilities

### 1. Natural Language Understanding

**Intent Classification**

- Keyword-based intent detection
- Confidence scoring for intent matches
- Multi-intent command support
- Context-aware classification

**Intent Categories:**
- **Cinematic**: Speed 0.8x, cinematic LUT, background blur, letterbox
- **Fast Cut**: Quick transitions, high cut frequency, fast rhythm
- **Slow Motion**: 0.5x speed, smooth easing, frame holds
- **Color Grade**: Temperature adjustment, saturation, contrast
- **Pacing**: Tempo sync, beat matching, rhythm control

**Reference:** [intent-classification.md](references/intent-classification.md) for classification algorithms

### 2. Parameter Translation

**Command to Parameter Mapping**

- Intent parameter extraction
- Parameter conflict resolution
- Constraint validation
- Semantic parameter merging

**Parameter Categories:**
- Speed parameters (0.1x to 3.0x range)
- Color grade settings (warm, cool, vintage, cinematic)
- Transition timing (0.1s to 5.0s range)
- Effect intensity (0.0 to 2.0 range)

**Resolution Strategies:**
- Speed conflicts: Minimum wins (slow motion precedence)
- Boolean conflicts: True takes precedence
- Numeric conflicts: Average of values
- Color conflicts: Source priority-based

**Reference:** [parameter-mapping.md](references/parameter-mapping.md) for mapping strategies

### 3. Edit Decision List Generation

**EDL Creation**

- Timeline-based edit construction
- Multiple format support (Standard, Final Cut Pro, Premiere)
- Effect application sequencing
- Metadata generation

**EDL Components:**
- Video track edits with timestamps
- Effect operations (speed, color, blur, etc.)
- Audio track modifications
- Transition specifications

**Export Formats:**
- JSON (standard format)
- XML (Final Cut Pro)
- Native Premiere Pro
- DaVinci Resolve

**Reference:** [edl-generation.md](references/edl-generation.md) for EDL formats and generation

### 4. Feedback Incorporation

**Learning System**

- User feedback collection and analysis
- Intent classification refinement
- Parameter mapping improvements
- Success rate tracking

**Feedback Types:**
- Satisfaction ratings (1-5 scale)
- Edit quality scores
- Intent accuracy validation
- Parameter correctness feedback

**Learning Mechanisms:**
- Pattern recognition from successful translations
- Missing intent detection
- Parameter error identification
- Continuous improvement tracking

**Reference:** [feedback-processing.md](references/feedback-processing.md) for learning algorithms

## Implementation Patterns

### Pattern 1: Natural Language to Edit
```python
# Full translation pipeline
translator = IntentTranslator()

# Translate command
result = translator.translate(
    command="Make this video cinematic with warm colors",
    context={'video_analysis': {...}}
)

# Generate EDL
edl = result['edl']
# Output: Executable edit decision list
```

### Pattern 2: Feedback Loop
```python
# Incorporate feedback
feedback_result = translator.process_feedback(
    original_command="Make it cinematic",
    user_feedback={
        'satisfaction': 4,
        'suggestions': ['Make colors warmer']
    }
)

# Refined translation on next use
```

### Pattern 3: Batch Processing
```python
# Process multiple commands
commands = [
    "Cinematic opening",
    "Fast cut transition",
    "Warm color grade"
]

for command in commands:
    edl = translator.translate(command, context)
    apply_edits(edl)
```

## Quality Gates

✓ Intent classification accuracy > 90% for common commands
✓ Parameter translation maintains semantic meaning
✓ EDL generation produces valid, executable actions
✓ Feedback incorporation adjusts parameters correctly
✓ Processing time < 500ms per command
✓ Multi-intent command support
✓ Conflict resolution handles all edge cases

## Files Generated

- `intent_classifier.py`: Natural language intent recognition
- `parameter_translator.py`: Command to parameter mapping
- `edl_generator.py`: Edit Decision List creation
- `feedback_processor.py`: Adaptive parameter adjustment
- `semantic_analyzer.py`: Context and semantic analysis

## Integration Points

- Used by `video-editor` agent for autonomous editing
- Integrates with `multimodal-understanding` for context-aware translation
- Supports EDL export to major video editing software
- Connects to feedback learning system

## Next Steps

1. Integrate with `multimodal-understanding` for context-aware translation
2. Add support for complex multi-step commands
3. Implement learning from user behavior patterns
4. Build command suggestion engine
5. Add visual parameter preview system
6. Support custom parameter ranges
7. Add voice command support
