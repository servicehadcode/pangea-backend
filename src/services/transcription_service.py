import os
import time
import speech_recognition as sr
from pydub import AudioSegment
from typing import Dict, Tuple, Optional
from models.transcription import Transcription
from werkzeug.utils import secure_filename
import tempfile
import io

class TranscriptionService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.allowed_formats = {'wav'}
        self.max_file_size = 10 * 1024 * 1024  # 10MB limit

    def is_valid_file(self, file) -> Tuple[bool, Optional[str]]:
        """Validate the uploaded file."""
        if not file:
            return False, "No file provided"

        # Check if the file has a filename
        if file.filename == '':
            return False, "No selected file"

        # Check file extension
        extension = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        if extension not in self.allowed_formats:
            return False, f"File format not allowed. Allowed formats: {', '.join(self.allowed_formats)}"

        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)  # Reset file pointer

        if file_size > self.max_file_size:
            return False, f"File too large. Maximum size: {self.max_file_size / (1024 * 1024)}MB"

        return True, None

    def transcribe_audio(self, audio_file, language: str = "en-US") -> Tuple[Transcription, Optional[str]]:
        """
        Transcribe the audio file to text.

        Args:
            audio_file: The audio file object
            language: The language code (default: en-US)

        Returns:
            A tuple containing the Transcription object and an error message (if any)
        """
        start_time = time.time()

        try:
            # Save the file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                audio_file.save(temp_file.name)

                # Convert the audio to the format needed by the recognizer
                audio = AudioSegment.from_wav(temp_file.name)

                # Convert to in-memory WAV file (no need for FLAC conversion)
                buffer = io.BytesIO()
                audio.export(buffer, format="wav")
                buffer.seek(0)

                # Use speech_recognition to transcribe
                with sr.AudioFile(buffer) as source:
                    audio_data = self.recognizer.record(source)

                    # Use the simpler recognize_google method without show_all
                    # This avoids the need for FLAC conversion
                    transcription_text = self.recognizer.recognize_google(
                        audio_data,
                        language=language
                    )

                    # Calculate processing time
                    processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds

                    # Since we're not using show_all, we don't get confidence
                    # Set a default confidence value
                    confidence = 0.8

                    # Count words
                    word_count = len(transcription_text.split())

                    # Create and return the transcription object
                    transcription = Transcription(
                        transcription=transcription_text,
                        confidence=confidence,
                        processing_time=processing_time,
                        word_count=word_count,
                        language=language
                    )

                    return transcription, None

        except sr.UnknownValueError:
            return None, "Speech Recognition could not understand audio"
        except sr.RequestError as e:
            return None, f"Could not request results from Speech Recognition service; {str(e)}"
        except Exception as e:
            return None, f"Error transcribing audio: {str(e)}"
        finally:
            # Clean up the temporary file
            if 'temp_file' in locals():
                try:
                    os.unlink(temp_file.name)
                except:
                    pass
