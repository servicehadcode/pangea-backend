class Contact:
    def __init__(self, name, email, subject, message):
        self.name = name
        self.email = email
        self.subject = subject
        self.message = message

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'subject': self.subject,
            'message': self.message
        }