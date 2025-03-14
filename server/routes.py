from flask import Blueprint, request, jsonify
from .models import Messages, Conversations
import uuid

routes = Blueprint('routes', __name__)

# health check endpoint
@routes.route('/', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

from flask import jsonify
from .models import Messages, Conversations

@routes.route('/create_conversation', methods=['GET'])
def create_conversation():
    try:
        # Get the user's message from the request
        user_message = request.json.get('message')
       
        # Generate unique conversation URL
        conversation_url = str(uuid.uuid4())
        
        # Create conversation first
        conversation = Conversations.create(
            summary=user_message,  # You might want to generate a proper summary using LLM
            conversation_url=conversation_url
        )
        
        # Create the first message in the conversation
        user_message = Messages.create_user_message(
            content=user_message,
            conversation_id=conversation.conversation_id  # Use the actual integer ID
        )
        
        return jsonify({
            'conversation_id': conversation.conversation_id,
            'conversation_url': conversation_url,
            'message': {
                'id': user_message.message_id,
                'content': user_message.content,
                'timestamp': user_message.timestamp.isoformat(),
                'sender': user_message.sender
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/send_message', methods=['GET'])
def send_message():
    try:
        content = "Test Message"
        
        # Get conversation ID from request parameters or by URL search params
        conversation_id = 1
        
        # Create a new message
        message = Messages.create_user_message(
            content=content,
            conversation_id=conversation_id
        )
        
        return jsonify({
            'message': {
                'id': message.message_id,
                'content': message.content,
                'timestamp': message.timestamp.isoformat(),
                'sender': message.sender
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@routes.route('/check_convos', methods=['GET'])
def check_convos():
    try:
        # Get all conversations
        conversation = Conversations.get_by_conversation_id(1)
        
        return jsonify({
            'conversation': {
                'id': conversation.conversation_id,
                'summary': conversation.summary,
                'messages': [message.content for message in conversation.messages]
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        


