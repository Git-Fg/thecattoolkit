# Frame-by-Frame Visual Analysis

## Overview

The `FrameAnalyzer` class provides comprehensive visual analysis of individual video frames, analyzing composition, lighting, color, subjects, depth, and motion for intelligent video editing.

## Implementation

```python
import cv2
import numpy as np
from typing import List, Dict, Tuple

class FrameAnalyzer:
    def __init__(self):
        self.scene_boundary_threshold = 0.3
        self.frame_skip = 5  # Analyze every 5th frame for efficiency

    def analyze_frame(self, frame: np.ndarray, frame_number: int) -> Dict:
        """Comprehensive visual analysis of a single frame"""
        return {
            'frame_number': frame_number,
            'composition': self._analyze_composition(frame),
            'lighting': self._analyze_lighting(frame),
            'color_palette': self._extract_color_palette(frame),
            'subject_detection': self._detect_subjects(frame),
            'depth_cues': self._analyze_depth(frame),
            'motion_vectors': self._analyze_motion(frame)
        }
```

## Analysis Components

### 1. Composition Analysis

**Rule of Thirds Assessment:**
```python
def _analyze_composition(self, frame: np.ndarray) -> Dict:
    """Analyze visual composition and rule-of-thirds"""
    height, width = frame.shape[:2]
    thirds_x = [width // 3, 2 * width // 3]
    thirds_y = [height // 3, 2 * height // 3]

    # Detect subjects using edge detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Score based on subject placement
    subjects_on_thirds = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > (width * height) * 0.01:
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])

                # Check if subject is on thirds
                if (cx in thirds_x or cy in thirds_y or
                    abs(cx - thirds_x[0]) < 50 or abs(cx - thirds_x[1]) < 50 or
                    abs(cy - thirds_y[0]) < 50 or abs(cy - thirds_y[1]) < 50):
                    subjects_on_thirds += 1

    return {
        'rule_of_thirds_score': subjects_on_thirds / max(len(contours), 1),
        'balance': self._calculate_visual_balance(contours, width, height),
        'leading_lines': self._detect_leading_lines(edges),
        'symmetry': self._measure_symmetry(frame)
    }
```

**Metrics:**
- **Rule of Thirds Score**: 0.0 to 1.0 (higher is better)
- **Visual Balance**: Symmetry and weight distribution
- **Leading Lines**: Detection of lines that guide the eye
- **Symmetry**: Mirror symmetry measurement

### 2. Lighting Analysis

**Mood and Atmosphere Detection:**
```python
def _analyze_lighting(self, frame: np.ndarray) -> Dict:
    """Analyze lighting conditions and mood"""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

    # Calculate lighting metrics
    brightness = np.mean(hsv[:, :, 2])
    contrast = np.std(hsv[:, :, 2])
    shadow_mask = hsv[:, :, 2] < 30
    shadow_percentage = np.sum(shadow_mask) / shadow_mask.size

    # Color temperature analysis
    b_mean = np.mean(frame[:, :, 0])
    r_mean = np.mean(frame[:, :, 2])
    color_temperature = r_mean / (b_mean + 1e-6)

    return {
        'brightness': float(brightness),
        'contrast': float(contrast),
        'shadow_percentage': float(shadow_percentage),
        'color_temperature': float(color_temperature),
        'mood': self._classify_mood(brightness, contrast, color_temperature)
    }
```

**Lighting Metrics:**
- **Brightness**: 0-255 scale
- **Contrast**: Standard deviation of brightness
- **Shadow Percentage**: Percentage of frame in shadow
- **Color Temperature**: Warm vs cool detection
- **Mood Classification**: Based on lighting characteristics

### 3. Color Palette Extraction

**Dominant Colors:**
```python
def _extract_color_palette(self, frame: np.ndarray) -> Dict:
    """Extract dominant colors using k-means clustering"""
    # Reshape frame to list of pixels
    data = frame.reshape((-1, 3))
    data = np.float32(data)

    # Apply k-means clustering
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    _, labels, centers = cv2.kmeans(data, 8, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Convert back to uint8
    centers = np.uint8(centers)

    # Calculate color percentages
    labels = labels.flatten()
    percentages = np.bincount(labels) / len(labels)

    # Create palette
    palette = []
    for i, (center, percentage) in enumerate(zip(centers, percentages)):
        palette.append({
            'color': center.tolist(),
            'percentage': float(percentage)
        })

    # Sort by percentage
    palette.sort(key=lambda x: x['percentage'], reverse=True)

    return {
        'palette': palette,
        'dominant_color': palette[0]['color'],
        'color_harmony': self._analyze_color_harmony(centers)
    }
```

### 4. Subject Detection

**Object and People Detection:**
```python
def _detect_subjects(self, frame: np.ndarray) -> Dict:
    """Detect main subjects in frame"""
    # Use deep learning model for object detection
    # Or use contour analysis for simpler detection

    # Simplified contour-based detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find significant subjects
    subjects = []
    height, width = frame.shape[:2]
    frame_area = height * width

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > frame_area * 0.05:  # Significant subject
            x, y, w, h = cv2.boundingRect(contour)
            subjects.append({
                'bbox': [x, y, w, h],
                'area': area,
                'aspect_ratio': w / h
            })

    return {
        'subjects': subjects,
        'subject_count': len(subjects),
        'main_subject': subjects[0] if subjects else None
    }
```

### 5. Depth Analysis

**3D Depth Cues:**
```python
def _analyze_depth(self, frame: np.ndarray) -> Dict:
    """Analyze depth cues from 2D frame"""
    # Use various techniques to estimate depth
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Blur-based depth estimation
    depth_cues = {
        'sharpness_map': cv2.Laplacian(gray, cv2.CV_64F).var(),
        'texture_variance': self._calculate_texture_variance(gray),
        'atmospheric_perspective': self._analyze_atmospheric_perspective(frame)
    }

    return depth_cues

def _calculate_texture_variance(self, gray: np.ndarray) -> float:
    """Calculate local variance to estimate texture complexity"""
    kernel = np.ones((5, 5), np.float32) / 25
    mean = cv2.filter2D(gray, -1, kernel)
    variance = cv2.filter2D((gray - mean) ** 2, -1, kernel)
    return float(np.mean(variance))
```

### 6. Motion Analysis

**Optical Flow and Movement:**
```python
def _analyze_motion(self, frame: np.ndarray) -> Dict:
    """Analyze motion vectors in frame"""
    # Calculate optical flow
    # (Requires previous frame for comparison)

    return {
        'motion_intensity': 0.0,  # Placeholder
        'motion_direction': None,  # Placeholder
        'stable_regions': []  # Regions with low motion
    }
```

## Usage

```python
analyzer = FrameAnalyzer()

# Analyze a single frame
frame = cv2.imread("frame_001.jpg")
analysis = analyzer.analyze_frame(frame, frame_number=1)

print(analysis)
# Output:
# {
#     'frame_number': 1,
#     'composition': {...},
#     'lighting': {...},
#     'color_palette': {...},
#     'subject_detection': {...},
#     'depth_cues': {...},
#     'motion_vectors': {...}
# }
```

## Integration Points

- Used by `MultimodalAnalyzer` for comprehensive video analysis
- Referenced by scene detection algorithms
- Supports real-time frame analysis for live editing

## Performance Optimization

1. **Frame Skipping**: Analyze every Nth frame
2. **ROI Analysis**: Focus on regions of interest
3. **Parallel Processing**: Multi-threaded frame analysis
4. **Hardware Acceleration**: GPU support for OpenCV operations
