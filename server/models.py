from . import db
from datetime import datetime, timezone, timedelta
import uuid


# conversations model (table)
class Conversations(db.Model):
    """
    This model represents a conversation between a user and an assistant.
    It contains the conversation_id, timestamp, messages, summary, and conversation_url.

    lazy=True means that the messages are not loaded into memory until they are needed.
    cascade='all, delete-orphan' means that when a conversation is deleted, all of the messages associated with it are also deleted.
    """
    # define table attributes
    conversation_id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone(timedelta(hours=-4))))
    messages = db.relationship('Messages', backref='conversation', lazy=True, cascade='all, delete-orphan')
    summary = db.Column(db.String(50), nullable=False)  

    # string representation of the conversation
    def __repr__(self):
        return f'<Conversation {self.conversation_id}>'
    
    @classmethod
    def create(cls, summary):
        """Create a new conversation record"""
        conversation = cls(
            summary=summary[0:50], # for now we are passing in a static summary, but in the future we will use the LLM to generate a summary
        )
        db.session.add(conversation)
        db.session.commit()
        return conversation
    
    @classmethod
    def get_conversation(cls, conversation_id):
        """Get conversation history by conversation_id"""
        conversation = cls.query.get(conversation_id)
        if conversation:
            return conversation.messages
        else:
            return []
    
    @classmethod
    def get_all(cls):
        """Get all conversations"""
        return cls.query.all()
    
    def update(self, **kwargs):
        """Update conversation attributes"""
        # This sort of update is not needed, but I'm keeping it here for now for things like changing the convo summary 
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
    
    def delete(self):
        """Delete the conversation"""
        db.session.delete(self)
        db.session.commit()

class Messages(db.Model):
    # define table attributes
    message_id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.conversation_id'), nullable=False)
    content = db.Column(db.String(4096), nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone(timedelta(hours=-5))))
    role = db.Column(db.String(100), nullable=False) # this will either be "user" or "assistant"
    
    def __repr__(self):
        return f'<Message {self.content}>'
    
    @classmethod
    def create_user_message(cls, content, conversation_id):
        """Create a new user message record"""
        message = cls(
            content=content,
            conversation_id=conversation_id, # implement this by calling the get_by_conversation_id method on the Conversations model in the call u make
            role="user"
        )
        db.session.add(message)
        db.session.commit()
        return message
    
    @classmethod
    def create_assistant_message(cls, content, conversation_id):
        """Create a new assistant message record"""
        message = cls(
            content=content,
            conversation_id=conversation_id,
            role="assistant"
        )
        db.session.add(message)
        db.session.commit()
        return message
    
    @classmethod
    def edit_user_message(cls, message_id, content):
        """Edit a user message record"""
        message = cls.query.get(message_id)
        message.content = content
        db.session.commit()
        return message
