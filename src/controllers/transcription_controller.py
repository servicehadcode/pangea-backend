from flask import Blueprint, request, jsonify
from services.transcription_service import TranscriptionService
import time

transcription_blueprint = Blueprint('transcription', __name__)
transcription_service = TranscriptionService()

@transcription_blueprint.route('/v1/transcribe', methods=['POST'])
def transcribe_audio():
    """
    Endpoint to transcribe audio files.
    
    Expects:
    - audio file in multipart/form-data
    - format parameter (optional, defaults to 'wav')
    - language parameter (optional, defaults to 'en-US')
    
    Returns:
    - JSON response with transcription data or error message
    """
    try:
        # Check if the request has the file part
        if 'audio' not in request.files:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'MISSING_FILE',
                    'message': 'No audio file provided',
                    'details': None
                }
            }), 400
            
        audio_file = request.files['audio']
        
        # Validate the file
        is_valid, error_message = transcription_service.is_valid_file(audio_file)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'INVALID_FILE',
                    'message': error_message,
                    'details': None
                }
            }), 400
            
        # Get language parameter (optional)
        language = request.form.get('language', 'en-US')
        
        # Transcribe the audio
        transcription, error = transcription_service.transcribe_audio(audio_file, language)
        
        if error:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'TRANSCRIPTION_FAILED',
                    'message': error,
                    'details': None
                }
            }), 500
            
        # Return the transcription data
        return jsonify({
            'success': True,
            'data': transcription.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'SERVER_ERROR',
                'message': 'An unexpected error occurred',
                'details': str(e)
            }
        }), 500
