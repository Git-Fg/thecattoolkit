---
name: multimodal-understanding
description: "Analyzes video content with vision and audio models. Use when analyzing video content, combining frame analysis, audio processing, scene detection, and narrative flow understanding for intelligent video editing."
context: fork
agent: video-editor
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# Multimodal Understanding Protocol

## Purpose

Analyzes video content through combined vision and audio models to understand narrative flow, visual composition, and semantic content for AI-assisted editing.

## Core Responsibilities

### 1. Frame-by-Frame Visual Analysis

**Composition and Lighting Analysis**

- Rule-of-thirds assessment and visual balance
- Color palette extraction (k-means clustering)
- Lighting analysis (brightness, contrast, mood)
- Subject detection and depth cues
- Motion vector analysis

**Analysis Components:**
- Composition scoring (rule of thirds, symmetry, leading lines)
- Color temperature detection (warm vs cool)
- Shadow percentage and mood classification
- Depth estimation from blur and texture variance

**Reference:** [frame-analysis.md](references/frame-analysis.md) for complete implementation

### 2. Audio Analysis

**Comprehensive Audio Understanding**

- Tempo detection (BPM analysis)
- Key signature detection (musical key and confidence)
- Speech vs music classification
- Speech segment identification
- Energy level tracking and dynamic range

**Audio Features:**
- Spectral analysis (centroids, bandwidth, rolloff)
- MFCC extraction for audio fingerprinting
- Zero crossing rate for voiced/unvoiced detection
- RMS energy curves over time

**Reference:** [audio-processing.md](references/audio-processing.md) for feature extraction algorithms

### 3. Scene Detection

**Intelligent Cut Detection**

- Hard cut detection (>95% accuracy)
- Fade and dissolve detection
- Story beat identification
- Three-act structure recognition
- Minimum scene length enforcement

**Detection Methods:**
- Histogram difference analysis
- Structural similarity (SSIM)
- Edge change ratio
- Color distribution comparison
- Gradual transition detection

**Accuracy Metrics:**
- Hard Cut Detection: >95% accuracy
- False Positive Rate: <2%
- Fade Detection: >90% for fades >0.5 seconds

**Reference:** [scene-detection.md](references/scene-detection.md) for detection algorithms

### 4. Narrative Flow Understanding

**Story Structure Analysis**

- Three-act structure identification (Setup, Confrontation, Resolution)
- Emotional arc tracking throughout video
- Character development analysis
- Cinematic technique detection
- Narrative structure classification

**Analysis Components:**
- Story beat identification (inciting incident, climax, resolution)
- Emotional progression tracking (valence, arousal)
- Character arc analysis (growth, decline, stable)
- Camera movement detection (pan, dolly, static)
- Editing pattern recognition (quick cuts, long takes)

**Reference:** [narrative-flow.md](references/narrative-flow.md) for narrative analysis algorithms

## Implementation Patterns

### Pattern 1: Complete Video Analysis
```python
# Full analysis pipeline
analyzer = MultimodalAnalyzer()

# Analyze entire video
analysis = analyzer.analyze_video("footage.mp4")

# Output includes all analysis results
result = {
    'frames': frame_analysis,    # Per-frame visual analysis
    'audio': audio_analysis,      # Audio features and segments
    'scenes': scenes,             # Scene boundaries and types
    'narrative': narrative        # Story structure and beats
}
```

### Pattern 2: Real-Time Analysis
```python
# Real-time processing for live editing
analyzer = MultimodalAnalyzer()

# Stream processing
for frame in video_stream:
    analysis = analyzer.analyze_frame(frame, timestamp)

    if analysis['scene_change']:
        # Trigger scene boundary detection
        detect_scene_boundary()

    if analysis['lighting']['mood'] == 'dramatic':
        # Suggest color grading
        suggest_cinematic_grade()
```

## Quality Gates

✓ Scene detection accuracy > 95% on standard cuts
✓ Audio analysis detects speech/music with > 90% accuracy
✓ Narrative structure identification matches manual analysis
✓ Frame analysis completes in < 100ms per frame
✓ Color palette extraction identifies 5 dominant colors accurately
✓ Real-time processing at 30fps capability
✓ Story beat detection > 85% accuracy

## Files Generated

- `frame_analyzer.py`: Visual composition and lighting analysis
- `audio_analyzer.py`: Audio feature extraction and classification
- `scene_detector.py`: Intelligent cut detection and scene classification
- `narrative_analyzer.py`: Story beat detection and three-act structure
- `multimodal_fusion.py`: Combined vision + audio understanding

## Integration Points

- Used by `video-editor` agent for autonomous editing
- Referenced by `intent-translation` for natural language commands
- Supports EDL generation for timeline-based editing

## Next Steps

1. Integrate with `intent-translation` for natural language editing commands
2. Add support for specific video formats (4K, HDR, etc.)
3. Implement real-time processing for live video streams
4. Add object tracking across scenes
5. Build recommendation engine for editing suggestions
6. Optimize GPU acceleration for frame analysis
