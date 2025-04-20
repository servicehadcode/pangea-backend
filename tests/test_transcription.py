import requests
import os
import sys
import time
import pyaudio
import wave
import tempfile
from datetime import datetime

def record_audio(output_file, record_seconds=5, sample_rate=44100, channels=1, chunk=1024):
    """
    Record audio from the microphone and save it to a WAV file.

    Args:
        output_file: Path to save the recorded audio
        record_seconds: Duration of recording in seconds
        sample_rate: Audio sample rate
        channels: Number of audio channels (1 for mono, 2 for stereo)
        chunk: Audio chunk size

    Returns:
        True if recording was successful, False otherwise
    """
    try:
        print(f"\nPreparing to record {record_seconds} seconds of audio...")
        print("Get ready to speak in 3 seconds...")
        time.sleep(1)
        print("2...")
        time.sleep(1)
        print("1...")
        time.sleep(1)

        # Initialize PyAudio
        audio = pyaudio.PyAudio()

        # Open audio stream
        stream = audio.open(
            format=pyaudio.paInt16,
            channels=channels,
            rate=sample_rate,
            input=True,
            frames_per_buffer=chunk
        )

        print("\n🎙️ Recording... Speak now!")

        # Record audio
        frames = []
        for i in range(0, int(sample_rate / chunk * record_seconds)):
            data = stream.read(chunk)
            frames.append(data)
            # Print progress bar
            progress = i / int(sample_rate / chunk * record_seconds)
            bar_length = 30
            bar = '█' * int(bar_length * progress) + '░' * (bar_length - int(bar_length * progress))
            sys.stdout.write(f"\r[{bar}] {int(progress * 100)}%")
            sys.stdout.flush()

        print("\n\n✅ Recording complete!")

        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # Save the recorded audio to a WAV file
        with wave.open(output_file, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(frames))

        print(f"Audio saved to {output_file}")
        return True

    except Exception as e:
        print(f"Error recording audio: {str(e)}")
        return False

def transcribe_audio(audio_file_path, language="en-US"):
    """
    Send the audio file to the transcription API and get the result.

    Args:
        audio_file_path: Path to the audio file
        language: Language code for transcription

    Returns:
        API response as JSON or None if an error occurred
    """
    # API endpoint
    url = "http://localhost:5000/api/v1/transcribe"

    # Prepare the files and data
    files = {
        'audio': (os.path.basename(audio_file_path), open(audio_file_path, 'rb'), 'audio/wav')
    }

    data = {
        'language': language
    }

    print(f"\nSending request to {url} with file {audio_file_path}...")

    try:
        # Send the request
        response = requests.post(url, files=files, data=data)

        # Print the response status
        print(f"Status code: {response.status_code}")

        # Return the response JSON
        return response.json()

    except Exception as e:
        print(f"Error: {str(e)}")
        return None
    finally:
        # Close the file
        files['audio'][1].close()

def format_transcription_result(result):
    """
    Format the transcription result for display.

    Args:
        result: The API response JSON
    """
    if not result:
        print("\n❌ No result received from the API")
        return

    if result.get('success', False):
        data = result.get('data', {})
        transcription = data.get('transcription', '')
        confidence = data.get('confidence', 0.0)
        processing_time = data.get('processingTime', 0.0)
        word_count = data.get('wordCount', 0)

        print("\n✨ Transcription Result ✨")
        print("=" * 50)
        print(f"📝 Text: {transcription}")
        print(f"🎯 Confidence: {confidence:.2f}")
        print(f"⏱️ Processing Time: {processing_time:.2f} ms")
        print(f"🔤 Word Count: {word_count}")
        print("=" * 50)
    else:
        error = result.get('error', {})
        print("\n❌ Transcription Failed")
        print(f"Error Code: {error.get('code', 'UNKNOWN')}")
        print(f"Message: {error.get('message', 'Unknown error')}")
        if 'details' in error and error['details']:
            print(f"Details: {error['details']}")

def main():
    """
    Main function to run the audio recording and transcription test.

    Usage:
        python test_transcription.py [record_seconds]
    """
    # Parse command line arguments
    record_seconds = 5  # Default recording duration
    if len(sys.argv) > 1:
        try:
            record_seconds = int(sys.argv[1])
        except ValueError:
            print(f"Invalid recording duration: {sys.argv[1]}. Using default: 5 seconds.")

    # Create a temporary directory for the audio file
    with tempfile.TemporaryDirectory() as temp_dir:
        # Generate a unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_file_path = os.path.join(temp_dir, f"recording_{timestamp}.wav")

        print("\n🎤 Audio Recording and Transcription Test 🎤")
        print("=" * 50)
        print(f"Recording Duration: {record_seconds} seconds")
        print("=" * 50)

        # Record audio
        if record_audio(audio_file_path, record_seconds):
            # Transcribe the recorded audio
            result = transcribe_audio(audio_file_path)

            # Format and display the result
            format_transcription_result(result)
        else:
            print("\n❌ Failed to record audio. Exiting.")

if __name__ == "__main__":
    main()
