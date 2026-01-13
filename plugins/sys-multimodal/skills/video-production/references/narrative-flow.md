# Narrative Flow Understanding

## Overview

The `NarrativeAnalyzer` class understands narrative structure in video, identifying story beats, character arcs, emotional progression, and cinematic techniques for intelligent editing decisions.

## Implementation

```python
from typing import List, Dict, Tuple
import numpy as np

class NarrativeAnalyzer:
    def __init__(self):
        self.emotion_model = None  # Load pre-trained emotion classifier
        self.character_tracker = CharacterTracker()

    def analyze_narrative(self, video_analysis: Dict) -> Dict:
        """Analyze narrative structure from video analysis"""
        return {
            'story_beats': self._identify_story_beats(video_analysis),
            'emotional_arc': self._track_emotional_progression(video_analysis),
            'character_development': self.character_tracker.analyze_arcs(video_analysis),
            'cinematic_techniques': self._identify_cinematic_techniques(video_analysis),
            'narrative_structure': self._determine_structure(video_analysis)
        }
```

## Analysis Components

### 1. Story Beat Identification

**Three-Act Structure:**
```python
def _identify_story_beats(self, analysis: Dict) -> Dict:
    """Identify key story beats (Setup, Confrontation, Resolution)"""
    scenes = analysis['scenes']
    total_duration = sum(scene['duration'] for scene in scenes)

    # Divide into three acts
    setup_end = total_duration * 0.25
    confrontation_end = total_duration * 0.75

    story_beats = {
        'act_1': {'start': 0, 'end': setup_end, 'beats': []},
        'act_2': {'start': setup_end, 'end': confrontation_end, 'beats': []},
        'act_3': {'start': confrontation_end, 'end': total_duration, 'beats': []}
    }

    # Identify beats within each act
    for scene in scenes:
        scene_midpoint = scene['start_time'] + scene['duration'] / 2

        if scene_midpoint < setup_end:
            story_beats['act_1']['beats'].append(scene)
        elif scene_midpoint < confrontation_end:
            story_beats['act_2']['beats'].append(scene)
        else:
            story_beats['act_3']['beats'].append(scene)

    # Identify specific beats
    beats = {
        'inciting_incident': self._find_inciting_incident(scenes),
        'plot_point_1': self._find_plot_point_1(scenes, setup_end),
        'midpoint': self._find_midpoint(scenes, confrontation_end),
        'plot_point_2': self._find_plot_point_2(scenes, confrontation_end),
        'climax': self._find_climax(scenes),
        'resolution': self._find_resolution(scenes)
    }

    story_beats['specific_beats'] = beats
    return story_beats

def _find_inciting_incident(self, scenes: List[Dict]) -> Dict:
    """Find the inciting incident (first major disruption)"""
    for scene in scenes:
        # Look for sudden change in energy, composition, or audio
        if self._is_major_disruption(scene):
            return scene
    return None

def _find_climax(self, scenes: List[Dict]) -> Dict:
    """Find the climax (peak emotional intensity)"""
    max_intensity = 0
    climax_scene = None

    for scene in scenes:
        intensity = self._calculate_emotional_intensity(scene)
        if intensity > max_intensity:
            max_intensity = intensity
            climax_scene = scene

    return climax_scene
```

### 2. Emotional Arc Tracking

**Emotional Progression:**
```python
def _track_emotional_progression(self, analysis: Dict) -> Dict:
    """Track emotional arc throughout video"""
    scenes = analysis['scenes']
    emotional_curve = []

    for scene in scenes:
        emotion = self._analyze_scene_emotion(scene)
        emotional_curve.append({
            'timestamp': scene['start_time'],
            'emotion': emotion['primary'],
            'intensity': emotion['intensity'],
            'valence': emotion['valence'],  # positive/negative
            'arousal': emotion['arousal']    # energy level
        })

    # Analyze the overall arc
    arc_analysis = {
        'emotional_curve': emotional_curve,
        'dominant_emotion': self._find_dominant_emotion(emotional_curve),
        'emotional_variance': self._calculate_variance(emotional_curve),
        'peak_moments': self._find_peak_moments(emotional_curve),
        'emotional_transitions': self._identify_transitions(emotional_curve)
    }

    return arc_analysis

def _analyze_scene_emotion(self, scene: Dict) -> Dict:
    """Analyze emotion in a single scene"""
    # Combine visual and audio cues
    visual_emotion = self._analyze_visual_emotion(scene)
    audio_emotion = self._analyze_audio_emotion(scene)

    # Weighted combination
    combined_emotion = self._combine_emotions(visual_emotion, audio_emotion)

    return combined_emotion

def _analyze_visual_emotion(self, scene: Dict) -> Dict:
    """Analyze emotion from visual cues"""
    # Color analysis (warm vs cool, brightness)
    color_palette = scene.get('color_palette', {})
    lighting = scene.get('lighting', {})

    # Determine emotion from color and lighting
    if lighting.get('color_temperature', 0) > 1.2:
        emotion = 'warm'  # happiness, comfort
    elif lighting.get('shadow_percentage', 0) > 0.5:
        emotion = 'dark'  # sadness, fear
    else:
        emotion = 'neutral'

    return {
        'primary': emotion,
        'intensity': lighting.get('contrast', 0) / 255.0,
        'valence': 0.5,  # Placeholder
        'arousal': lighting.get('brightness', 0) / 255.0
    }
```

### 3. Character Development

**Character Arc Analysis:**
```python
class CharacterTracker:
    def __init__(self):
        self.characters = {}

    def analyze_arcs(self, video_analysis: Dict) -> Dict:
        """Analyze character development arcs"""
        scenes = video_analysis['scenes']
        character_arcs = {}

        for scene in scenes:
            # Detect characters in scene
            detected_characters = self._detect_characters(scene)

            for char in detected_characters:
                char_id = char['id']
                char_emotion = char['emotion']

                if char_id not in character_arcs:
                    character_arcs[char_id] = []

                character_arcs[char_id].append({
                    'timestamp': scene['start_time'],
                    'emotion': char_emotion,
                    'screen_time': char.get('screen_time', 0)
                })

        # Analyze each character's arc
        arc_analysis = {}
        for char_id, appearances in character_arcs.items():
            arc_analysis[char_id] = self._analyze_character_arc(appearances)

        return arc_analysis

    def _analyze_character_arc(self, appearances: List[Dict]) -> Dict:
        """Analyze individual character arc"""
        emotions = [a['emotion'] for a in appearances]

        # Determine arc type
        if self._is_rising_arc(emotions):
            arc_type = 'growth'  # Character develops positively
        elif self._is_falling_arc(emotions):
            arc_type = 'decline'  # Character deteriorates
        elif self._is_flat_arc(emotions):
            arc_type = 'stable'  # Character remains consistent
        else:
            arc_type = 'complex'  # Complex, multi-dimensional arc

        return {
            'arc_type': arc_type,
            'appearances': appearances,
            'emotional_journey': emotions,
            'peak_moment': self._find_peak_emotion(emotions)
        }
```

### 4. Cinematic Technique Identification

**Film Language Detection:**
```python
def _identify_cinematic_techniques(self, analysis: Dict) -> Dict:
    """Identify cinematic techniques used"""
    scenes = analysis['scenes']
    techniques = {
        'camera_movements': [],
        'editing_patterns': [],
        'visual_effects': [],
        'sound_design': []
    }

    for scene in scenes:
        # Detect camera movements from motion vectors
        camera_move = self._detect_camera_movement(scene)
        if camera_move:
            techniques['camera_movements'].append({
                'timestamp': scene['start_time'],
                'technique': camera_move
            })

        # Detect editing patterns
        editing_pattern = self._detect_editing_pattern(scene)
        if editing_pattern:
            techniques['editing_patterns'].append({
                'timestamp': scene['start_time'],
                'pattern': editing_pattern
            })

        # Detect visual effects
        vfx = self._detect_visual_effects(scene)
        if vfx:
            techniques['visual_effects'].append({
                'timestamp': scene['start_time'],
                'effect': vfx
            })

    return techniques

def _detect_camera_movement(self, scene: Dict) -> str:
    """Detect camera movement type"""
    motion_vectors = scene.get('motion_vectors', {})

    if not motion_vectors:
        return None

    # Analyze motion patterns
    motion_intensity = motion_vectors.get('motion_intensity', 0)

    if motion_intensity > 0.8:
        return 'fast_pan' or 'dolly'
    elif motion_intensity > 0.5:
        return 'slow_pan'
    else:
        return 'static' or 'handheld'

def _detect_editing_pattern(self, scene: Dict) -> str:
    """Detect editing pattern (rhythm, pacing)"""
    cut_frequency = self._calculate_cut_frequency(scene)

    if cut_frequency > 2.0:  # cuts per second
        return 'quick_cuts'
    elif cut_frequency > 0.5:
        return 'normal_rhythm'
    else:
        return 'long_takes'
```

### 5. Narrative Structure Determination

**Structure Classification:**
```python
def _determine_structure(self, analysis: Dict) -> Dict:
    """Determine overall narrative structure"""
    story_beats = analysis['story_beats']
    emotional_arc = analysis['emotional_arc']

    # Analyze pacing
    scene_durations = [scene['duration'] for scene in analysis['scenes']]
    avg_duration = np.mean(scene_durations)
    pacing_variance = np.var(scene_durations)

    # Determine structure type
    structure = {
        'type': self._classify_structure(story_beats, emotional_arc),
        'pacing': 'fast' if avg_duration < 3 else 'slow' if avg_duration > 10 else 'normal',
        'pacing_consistency': 'consistent' if pacing_variance < 5 else 'variable',
        'emotional_complexity': self._assess_emotional_complexity(emotional_arc)
    }

    return structure

def _classify_structure(self, story_beats: Dict, emotional_arc: Dict) -> str:
    """Classify narrative structure type"""
    # Classic three-act
    if self._has_three_acts(story_beats):
        return 'three_act'

    # Hero's journey
    elif self._is_heros_journey(story_beats):
        return 'heros_journey'

    # Documentary style
    elif self._is_documentary_style(story_beats):
        return 'documentary'

    # Music video (emotion-driven)
    elif self._is_music_video(emotional_arc):
        return 'music_video'

    # Experimental
    else:
        return 'experimental'
```

## Usage

```python
analyzer = NarrativeAnalyzer()

# Analyze narrative
narrative = analyzer.analyze_narrative(video_analysis)

print(narrative)
# Output:
# {
#     'story_beats': {...},
#     'emotional_arc': {...},
#     'character_development': {...},
#     'cinematic_techniques': {...},
#     'narrative_structure': {...}
# }
```

## Applications

1. **Intelligent Editing**: Edit based on narrative understanding
2. **Story Visualization**: Visualize narrative flow
3. **Highlight Extraction**: Extract most important moments
4. **Emotional Targeting**: Target specific emotions
5. **Character Focus**: Track character development
