from flask import Blueprint, request, jsonify
from services.feedback_service import FeedbackService
import json

feedback_blueprint = Blueprint('feedback', __name__)
feedback_service = FeedbackService()

@feedback_blueprint.route('/v1/feedback/transcribe', methods=['POST'])
def evaluate_transcription():
    try:
        data = request.get_json()
        question = data.get('question')
        transcribed_text = data.get('transcribedText')

        if not question or not transcribed_text:
            return jsonify({"error": "Missing question or transcribedText"}), 400

        prompt = feedback_service.build_prompt(mode="transcribe", question=question, text=transcribed_text)
        feedback = feedback_service.generate_feedback(prompt)

        try:
            feedback = json.loads(feedback)
            feedback['score'] = int(feedback['score'])
            return jsonify(feedback)
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Error parsing OpenAI response: {e}")
            return jsonify({
                "score": 0,
                "strengths": [],
                "improvements": ["Could not generate feedback at this time."],
                "overallFeedback": "Evaluation failed. Please try again."
                })

    except Exception as e:
        print(f"Error in evaluate_answer: {e}")
        return jsonify({"error": "Internal server error"}), 500

@feedback_blueprint.route('/v1/feedback/pr', methods=['POST'])
def generate_pr_feedback():
    try:
        data = request.get_json()
        pr_text = data.get('prText')

        if not pr_text:
            return jsonify({"error": "Missing prText"}), 400

        prompt = feedback_service.build_prompt(mode="pr", question="", text=pr_text)
        feedback_text = feedback_service.generate_feedback(prompt)

        # Clean and parse the JSON response
        cleaned_feedback = feedback_service.clean_json_response(feedback_text)
        return jsonify(cleaned_feedback)

    except Exception as e:
        print(f"Error in evaluate_answer: {e}")
        return jsonify({"error": "Internal server error"}), 500

