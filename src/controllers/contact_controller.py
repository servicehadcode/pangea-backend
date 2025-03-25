from flask import Blueprint, request, jsonify
from models.contact import Contact
from services.email_service import EmailService

contact_blueprint = Blueprint('contact', __name__)
email_service = EmailService()

@contact_blueprint.route('/contact', methods=['POST'])
def handle_contact():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'subject', 'message']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Create contact object
        contact = Contact(
            name=data['name'],
            email=data['email'],
            subject=data['subject'],
            message=data['message']
        )

        # Send email
        if email_service.send_email_support(contact):
            return jsonify({'message': 'Email sent successfully'}), 200
        else:
            return jsonify({'error': 'Failed to send email'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500