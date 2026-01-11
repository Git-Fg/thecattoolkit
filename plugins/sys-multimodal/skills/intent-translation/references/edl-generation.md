# Edit Decision List Generation

## Overview

The `EDLGenerator` class creates Edit Decision Lists (EDL) from mapped parameters, producing timeline-based editing instructions that can be executed by video editing software.

## Implementation

```python
from typing import Dict, List, Optional
import json
import time

class EDLGenerator:
    def __init__(self):
        self.edl_format = 'standard'  # standard, final_cut_pro, premiere
        self.timeline_resolution = 0.01  # 10ms precision

    def generate_edl(self, parameters: Dict, context: Dict) -> Dict:
        """Generate EDL from parameters and context"""
        timeline = self._build_timeline(parameters, context)
        edits = self._convert_to_edl(timeline)
        metadata = self._generate_metadata(parameters, context)

        return {
            'edl': edits,
            'timeline': timeline,
            'metadata': metadata,
            'format': self.edl_format,
            'version': '1.0'
        }

    def _build_timeline(self, params: Dict, context: Dict) -> List[Dict]:
        """Build timeline from parameters"""
        timeline = []

        # Determine edit points
        edit_points = self._identify_edit_points(context)

        # Generate edits for each point
        for point in edit_points:
            edit = self._create_edit(point, params, context)
            timeline.append(edit)

        return timeline

    def _identify_edit_points(self, context: Dict) -> List[Dict]:
        """Identify where edits should be applied"""
        video_analysis = context.get('video_analysis', {})
        scenes = video_analysis.get('scenes', [])
        audio_analysis = video_analysis.get('audio', {})

        edit_points = []

        # Scene-based edits
        for scene in scenes:
            edit_points.append({
                'type': 'scene',
                'start': scene['start_time'],
                'end': scene['end_time'],
                'scene_data': scene
            })

        # Beat-based edits
        if 'tempo' in audio_analysis:
            beats = self._detect_beats(audio_analysis)
            for beat in beats:
                edit_points.append({
                    'type': 'beat',
                    'timestamp': beat['time'],
                    'beat_data': beat
                })

        # Sort by timestamp
        edit_points.sort(key=lambda x: x.get('start') or x.get('timestamp'))

        return edit_points

    def _create_edit(self, point: Dict, params: Dict, context: Dict) -> Dict:
        """Create individual edit instruction"""
        edit_type = point['type']

        if edit_type == 'scene':
            return self._create_scene_edit(point, params, context)
        elif edit_type == 'beat':
            return self._create_beat_edit(point, params, context)
        else:
            return self._create_timeline_edit(point, params, context)

    def _create_scene_edit(self, point: Dict, params: Dict, context: Dict) -> Dict:
        """Create scene-based edit"""
        scene = point['scene_data']

        edit = {
            'type': 'scene_edit',
            'start_time': point['start'],
            'end_time': point['end'],
            'duration': scene['duration'],
            'operations': []
        }

        # Speed operation
        if params.get('speed', 1.0) != 1.0:
            edit['operations'].append({
                'type': 'speed_change',
                'speed': params['speed'],
                'easing': params.get('easing', 'linear')
            })

        # Color grade operation
        if params.get('color_grade') != 'none':
            edit['operations'].append({
                'type': 'color_grade',
                'grade': params['color_grade'],
                'saturation': params.get('saturation', 1.0),
                'contrast': params.get('contrast', 1.0),
                'color_temp': params.get('color_temp', 'neutral')
            })

        # Background blur
        if params.get('blur_background'):
            edit['operations'].append({
                'type': 'background_blur',
                'amount': 0.5,
                'edge_detection': True
            })

        # Letterbox
        if params.get('letterbox'):
            edit['operations'].append({
                'type': 'letterbox',
                'aspect_ratio': '2.39:1',
                'color': 'black'
            })

        return edit
```

## EDL Format Examples

### Standard EDL Format
```python
edl_standard = {
    'tracks': [
        {
            'name': 'Video Track 1',
            'edits': [
                {
                    'clip_id': 'clip_001',
                    'start_time': 0.0,
                    'end_time': 5.0,
                    'source_start': 0.0,
                    'source_end': 5.0,
                    'effects': [
                        {
                            'type': 'speed_change',
                            'speed': 0.8
                        },
                        {
                            'type': 'color_grade',
                            'grade': 'cinematic'
                        }
                    ]
                }
            ]
        }
    ]
}
```

### Final Cut Pro XML
```python
edl_fcp_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<xmeml version="5">
    <project>
        <children>
            <sequence>
                <name>Edited Sequence</name>
                <duration>300</duration>
                <children>
                    <clip>
                        <name>Clip 1</name>
                        <start>0</start>
                        <end>150</duration>
                        <effects>
                            <effect>
                                <name>Speed Change</name>
                                <parameter>
                                    <name>speed</name>
                                    <value>0.8</value>
                                </parameter>
                            </effect>
                        </effects>
                    </clip>
                </children>
            </sequence>
        </children>
    </project>
</xmeml>'''
```

### Adobe Premiere Pro
```python
edl_premiere = {
    'sequence': {
        'name': 'Edited Sequence',
        'frameRate': 30,
        'tracks': [
            {
                'type': 'video',
                'clips': [
                    {
                        'name': 'Clip 1',
                        'start': 0,
                        'end': 150,
                        'speed': 0.8,
                        'effects': [
                            {
                                'type': 'color_correction',
                                'lum_contrast': 20,
                                'saturation': 90
                            }
                        ]
                    }
                ]
            }
        ]
    }
}
```

## Edit Operations

### Speed Change
```python
speed_edit = {
    'type': 'speed_change',
    'speed': 0.8,
    'easing': 'ease-in-out',
    'frame_blending': True
}
```

### Color Grade
```python
color_edit = {
    'type': 'color_grade',
    'grade': 'cinematic',
    'shadows': {'lift': 0.0, 'gamma': 1.0, 'gain': 1.1},
    'midtones': {'saturation': 0.9},
    'highlights': {'temperature': 200}
}
```

### Transition
```python
transition_edit = {
    'type': 'transition',
    'transition_type': 'cut',
    'duration': 0.5,
    'easing': 'linear'
}
```

### Effect Application
```python
effect_edit = {
    'type': 'effect',
    'effect_name': 'Background Blur',
    'parameters': {
        'blur_amount': 0.5,
        'edge_detection': True,
        'falloff': 'gaussian'
    }
}
```

## Timeline Construction

```python
def _convert_to_edl(self, timeline: List[Dict]) -> Dict:
    """Convert timeline to EDL format"""
    edl = {
        'format': self.edl_format,
        'tracks': [
            {
                'type': 'video',
                'edits': []
            },
            {
                'type': 'audio',
                'edits': []
            }
        ]
    }

    for edit in timeline:
        edl['tracks'][0]['edits'].append({
            'clip_id': f"clip_{len(edl['tracks'][0]['edits']):03d}",
            'start_time': edit['start_time'],
            'end_time': edit['end_time'],
            'source_start': edit['start_time'],
            'source_end': edit['end_time'],
            'operations': edit['operations']
        })

    return edl
```

## Usage

```python
generator = EDLGenerator()

# Generate EDL
parameters = {'speed': 0.8, 'color_grade': 'cinematic'}
context = {'video_analysis': {...}}

edl = generator.generate_edl(parameters, context)

print(edl)
# Output:
# {
#     'edl': {...},
#     'timeline': [...],
#     'metadata': {...},
#     'format': 'standard',
#     'version': '1.0'
# }
```

## Export Options

### JSON Export
```python
def export_json(self, edl: Dict, filename: str):
    """Export EDL as JSON"""
    with open(filename, 'w') as f:
        json.dump(edl, f, indent=2)
```

### XML Export
```python
def export_xml(self, edl: Dict, filename: str):
    """Export EDL as XML (Final Cut Pro)"""
    xml = self._convert_to_xml(edl)
    with open(filename, 'w') as f:
        f.write(xml)
```

### Export to Video Editor
```python
def export_to_editor(self, edl: Dict, editor_type: str):
    """Export directly to video editor"""
    if editor_type == 'premiere':
        self._export_to_premiere(edl)
    elif editor_type == 'final_cut':
        self._export_to_final_cut(edl)
    elif editor_type == 'davinci':
        self._export_to_davinci(edl)
```

## Best Practices

1. **Precision**: Use millisecond precision for timing
2. **Compatibility**: Support multiple EDL formats
3. **Metadata**: Include comprehensive metadata
4. **Validation**: Validate EDL before export
5. **Preview**: Generate preview of edits
