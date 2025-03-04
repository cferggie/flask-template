from . import db

# conversation model (table)
class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    
    def __repr__(self):
        return f'<Conversation {self.email}>'
    
    @classmethod
    def create(cls, email, password, first_name):
        """Create a new conversation record"""
        conversation = cls(
            email=email,
            password=password,
            first_name=first_name
        )
        db.session.add(conversation)
        db.session.commit()
        return conversation
    
    @classmethod
    def get_by_email(cls, email):
        """Get a conversation by email"""
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def get_by_id(cls, id):
        """Get a conversation by id"""
        return cls.query.get(id)
    
    @classmethod
    def get_all(cls):
        """Get all conversations"""
        return cls.query.all()
    
    def update(self, **kwargs):
        """Update conversation attributes"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
    
    def delete(self):
        """Delete the conversation"""
        db.session.delete(self)
        db.session.commit()

