from datetime import datetime
from typing import Dict, Optional

class Transcription:
    def __init__(self, 
                 transcription: str, 
                 confidence: float, 
                 processing_time: float, 
                 word_count: int,
                 language: str = "en-US",
                 timestamp: Optional[datetime] = None):
        self.transcription = transcription
        self.confidence = confidence
        self.processing_time = processing_time
        self.word_count = word_count
        self.language = language
        self.timestamp = timestamp or datetime.now()

    def to_dict(self) -> Dict:
        """Convert the transcription object to a dictionary."""
        return {
            'transcription': self.transcription,
            'confidence': self.confidence,
            'processingTime': self.processing_time,
            'wordCount': self.word_count,
            'language': self.language,
            'timestamp': self.timestamp.isoformat()
        }

    @staticmethod
    def from_dict(data: Dict) -> 'Transcription':
        """Create a Transcription object from a dictionary."""
        timestamp = None
        if 'timestamp' in data:
            try:
                timestamp = datetime.fromisoformat(data['timestamp'])
            except (ValueError, TypeError):
                timestamp = datetime.now()
                
        return Transcription(
            transcription=data.get('transcription', ''),
            confidence=data.get('confidence', 0.0),
            processing_time=data.get('processingTime', 0.0),
            word_count=data.get('wordCount', 0),
            language=data.get('language', 'en-US'),
            timestamp=timestamp
        )
