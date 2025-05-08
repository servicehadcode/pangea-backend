import os
import speech_recognition as sr
from werkzeug.utils import secure_filename
import openai
import json
import re


openai.api_key = os.environ.get("OPENAI_API_KEY")

class FeedbackService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.allowed_formats = {'wav'}
        self.max_file_size = 10 * 1024 * 1024  # 10MB limit

    def build_prompt(self, mode, question, text):
        if mode == "pr":
            return f"""
            You are an expert code reviewer providing actionable, concise feedback for a pull request.

            PR Submission:
            {text}

            Provide clear, constructive feedback in plain text with recommendations for improvement.
            """
        elif mode == "transcribe":
            return f"""
            You are an interviewer providing feedback on a candidate's answer.

            Question: {question}
            Answer: {text}

            Provide a score between 0 and 100, strengths, improvements, and overall feedback.
            Format your response as a JSON object with the following keys:
            score: (integer)
            strengths: (list of strings)
            improvements: (list of strings)
            overallFeedback: (string)
            """

    def generate_feedback(self, prompt):
        """
        Generates feedback using OpenAI's GPT model.
        """
        try:

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful interviewer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,  # Lower temperature for more consistent outputs
            )

            feedback_text = response.choices[0].message.content.strip()
            return feedback_text

        except Exception as e:
            print(f"Error calling OpenAI: {e}")
            return {"error": "Feedback generation failed. Please try again later."}

    def clean_json_response(self, response_text):
        """
        Clean up a JSON string response from OpenAI to ensure it's properly formatted.

        Args:
            response_text (str): The raw response from OpenAI

        Returns:
            dict: Parsed JSON object
        """
        # Try to extract JSON if it's wrapped in other text
        json_match = re.search(r'(\{.*\})', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            json_str = response_text

        # Remove escape characters
        json_str = json_str.replace('\\n', ' ').replace('\\', '')

        try:
            # Parse the JSON
            return json.loads(json_str)
        except json.JSONDecodeError:
            # If parsing fails, return a default structure
            return {
                "feedback": [
                    {
                        "id": "feedback-error",
                        "comment": "Could not parse feedback. Original response: " + response_text[:100] + "...",
                        "author": "System",
                        "resolved": False
                    }
                ]
            }