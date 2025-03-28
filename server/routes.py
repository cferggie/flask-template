from flask import Blueprint, request, jsonify
from .models import Messages, Conversations
import requests

routes = Blueprint('routes', __name__)

# health check endpoint
@routes.route('/', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

# create a conversation
@routes.route('/create_conversation', methods=['GET'])
def create_conversation():
    try:
        # Get the user's message from the request
        # this assumes that the request's Content-Type is application/json
        user_message = request.json.get('message')
        # user_message = "Hello, how are you?"
        
        # Create conversation first
        conversation = Conversations.create(
            summary=user_message,  # You might want to generate a proper summary using LLM
        )
        
        # Create the first message in the conversation
        user_message = Messages.create_user_message(
            content=user_message,
            conversation_id=conversation.conversation_id
        )

        # Generate a response using the LLM
        ollama_response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': 'deepseek-r1',
                'prompt': user_message.content,
                'stream': False,
                'keep_alive': 10,
                'format': 'json'
            }
        )
        
        # Parse the LLM response
        ollama_response = ollama_response.json()
        ollama_response_content = ollama_response.get('response', '')

        # TODO: remove the <think> from the response 

        # Create a new message
        return jsonify({
            'conversation_id': conversation.conversation_id,
            'message': {
                'id': user_message.message_id,
                'content': user_message.content,
                'timestamp': user_message.timestamp.isoformat(),
                'sender': user_message.sender
            },
            'ollama_response': {
                'content': ollama_response_content
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# send a message in a conversation
@routes.route('/send_message', methods=['GET'])
def send_message():
    try:
        content = request.json.get('message')
        conversation_id = request.json.get('conversation_id')
        # content = "I am feeling well, thank you for asking"
        # conversation_id = 1
        
        # Create a new message
        message = Messages.create_user_message(
            content=content,
            conversation_id=conversation_id
        )
        
        return jsonify({
            'message': {
                'message_id': message.message_id,
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
        # Get convo by id
        conversation = Conversations.get_by_conversation_id(1)
        
        return jsonify({
            'conversation': {
                'conversation_id': conversation.conversation_id,
                'summary': conversation.summary,
                'messages': [message.content for message in conversation.messages]
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        


