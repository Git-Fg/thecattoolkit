# Audio Analysis

## Overview

The `AudioAnalyzer` class provides comprehensive audio analysis for video understanding, detecting tempo, key, speech segments, energy levels, and music vs speech classification.

## Implementation

```python
import librosa
import numpy as np
from typing import List, Dict

class AudioAnalyzer:
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.n_fft = 2048
        self.hop_length = 512

    def analyze_audio(self, audio_path: str) -> Dict:
        """Comprehensive audio analysis"""
        y, sr = librosa.load(audio_path, sr=self.sample_rate)

        return {
            'tempo': self._detect_tempo(y, sr),
            'key_signature': self._detect_key(y, sr),
            'energy_levels': self._analyze_energy(y),
            'speech_detection': self._detect_speech_segments(y, sr),
            'music_vs_speech': self._classify_audio_content(y, sr),
            'silence_detection': self._detect_silence(y),
            'audio_features': self._extract_features(y, sr)
        }
```

## Analysis Components

### 1. Tempo Detection

**BPM Analysis:**
```python
def _detect_tempo(self, y: np.ndarray, sr: int) -> float:
    """Detect BPM of audio"""
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    return float(tempo)
```

**Output:**
- Tempo in beats per minute (BPM)
- Used for video editing synchronization
- Helps identify rhythm changes

### 2. Key Signature Detection

**Musical Key Analysis:**
```python
def _detect_key(self, y: np.ndarray, sr: int) -> Dict:
    """Detect musical key signature"""
    chroma = librosa.feature.chroma_stft(y=y, sr=sr, hop_length=self.hop_length)
    chroma_mean = np.mean(chroma, axis=1)

    # Map to key names
    keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    key_index = np.argmax(chroma_mean)
    confidence = float(chroma_mean[key_index])

    return {
        'key': keys[key_index],
        'confidence': confidence,
        'chroma_profile': chroma_mean.tolist()
    }
```

**Output:**
- Musical key (C, D, E, etc.)
- Confidence score (0.0 to 1.0)
- Chroma feature vector

### 3. Speech Detection

**Segment Classification:**
```python
def _detect_speech_segments(self, y: np.ndarray, sr: int) -> List[Dict]:
    """Detect speech segments in audio"""
    # Use onset detection and spectral features
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr, hop_length=self.hop_length)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=self.hop_length)

    # Classify segments
    speech_segments = []
    for i, onset_time in enumerate(onset_times):
        segment_start = onset_time
        segment_end = onset_times[i + 1] if i + 1 < len(onset_times) else len(y) / sr

        # Extract segment
        start_sample = int(segment_start * sr)
        end_sample = int(segment_end * sr)
        segment = y[start_sample:end_sample]

        # Classify using spectral features
        segment_type = self._classify_segment(segment, sr)
        if segment_type == 'speech':
            speech_segments.append({
                'start': segment_start,
                'end': segment_end,
                'duration': segment_end - segment_start,
                'energy': float(np.mean(segment**2))
            })

    return speech_segments
```

**Output:**
- List of speech segments with timestamps
- Duration of each segment
- Energy levels for each segment

### 4. Energy Analysis

**Dynamic Range Detection:**
```python
def _analyze_energy(self, y: np.ndarray) -> Dict:
    """Analyze audio energy levels over time"""
    # Calculate RMS energy in windows
    frame_length = int(0.025 * self.sample_rate)  # 25ms frames
    hop_length = int(0.010 * self.sample_rate)   # 10ms hop

    rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
    times = librosa.frames_to_time(np.arange(len(rms)), sr=self.sample_rate, hop_length=hop_length)

    return {
        'rms_curve': rms.tolist(),
        'timestamps': times.tolist(),
        'avg_energy': float(np.mean(rms)),
        'peak_energy': float(np.max(rms)),
        'dynamic_range': float(np.max(rms) - np.min(rms))
    }
```

**Output:**
- RMS energy curve over time
- Average energy level
- Peak energy level
- Dynamic range

### 5. Music vs Speech Classification

**Content Type Detection:**
```python
def _classify_audio_content(self, y: np.ndarray, sr: int) -> Dict:
    """Classify audio as music or speech"""
    # Extract spectral features
    spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

    # Simple heuristic classification
    avg_centroid = np.mean(spectral_centroids)
    avg_rolloff = np.mean(spectral_rolloff)

    # Classify based on features
    if avg_centroid > 2000 and avg_rolloff > 3000:
        content_type = 'music'
        confidence = 0.8
    else:
        content_type = 'speech'
        confidence = 0.7

    return {
        'content_type': content_type,
        'confidence': confidence,
        'spectral_centroid': float(avg_centroid),
        'spectral_rolloff': float(avg_rolloff)
    }
```

### 6. Silence Detection

**Quiet Segment Identification:**
```python
def _detect_silence(self, y: np.ndarray) -> List[Dict]:
    """Detect silence segments in audio"""
    # Calculate energy in small windows
    window_size = int(0.1 * self.sample_rate)  # 100ms windows
    hop_length = window_size // 2

    silence_segments = []
    for i in range(0, len(y) - window_size, hop_length):
        window = y[i:i + window_size]
        energy = np.mean(window ** 2)

        # Threshold for silence (adjust based on audio)
        if energy < 0.01:
            silence_segments.append({
                'start': i / self.sample_rate,
                'end': (i + window_size) / self.sample_rate,
                'duration': window_size / self.sample_rate
            })

    return silence_segments
```

### 7. Audio Features Extraction

**Comprehensive Feature Set:**
```python
def _extract_features(self, y: np.ndarray, sr: int) -> Dict:
    """Extract comprehensive audio features"""
    # Spectral features
    spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]

    # Zero crossing rate
    zcr = librosa.feature.zero_crossing_rate(y)[0]

    # MFCCs
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

    return {
        'spectral_centroid': float(np.mean(spectral_centroids)),
        'spectral_rolloff': float(np.mean(spectral_rolloff)),
        'spectral_bandwidth': float(np.mean(spectral_bandwidth)),
        'zero_crossing_rate': float(np.mean(zcr)),
        'mfccs': np.mean(mfccs, axis=1).tolist(),
        'rms_energy': float(np.sqrt(np.mean(y**2)))
    }
```

## Usage

```python
analyzer = AudioAnalyzer()

# Analyze audio file
analysis = analyzer.analyze_audio("audio.mp3")

print(analysis)
# Output:
# {
#     'tempo': 120.5,
#     'key_signature': {'key': 'C', 'confidence': 0.85, ...},
#     'energy_levels': {...},
#     'speech_detection': [...],
#     'music_vs_speech': {'content_type': 'music', ...},
#     'silence_detection': [...],
#     'audio_features': {...}
# }
```

## Integration Points

- Used by `MultimodalAnalyzer` for audio understanding
- Synchronized with video frame analysis
- Supports EDL generation for video editing

## Applications

1. **Scene Detection**: Audio changes indicate scene boundaries
2. **Music Matching**: Key and tempo for soundtrack selection
3. **Speech Recognition**: Speech segments for transcription
4. **Energy-Based Editing**: Sync edits to energy peaks
5. **Silence Removal**: Automatic gap detection
