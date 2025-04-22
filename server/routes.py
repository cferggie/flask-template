from flask import Blueprint, request, jsonify
from .models import Messages, Conversations
from .llm.ollama import Ollama
import requests

routes = Blueprint('routes', __name__)
ollama = Ollama()

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
        # user_message = request.json.get('message')
        user_message = "This is a test message. Just say hello world."
        
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
        try:
            ollama_response = ollama.generate(user_message.content)

            # Create a new assistant message
            assistant_message = Messages.create_assistant_message(
                content=ollama_response,
                conversation_id=conversation.conversation_id
            )
            return jsonify({
                'conversation_id': conversation.conversation_id,
                'user_message': {
                    'message_id': user_message.message_id,
                    'content': user_message.content,
                    'timestamp': user_message.timestamp.isoformat(),
                    'role': user_message.role
                },
                'assistant_message': {
                    'message_id': assistant_message.message_id,
                    'content': assistant_message.content,
                    'timestamp': assistant_message.timestamp.isoformat(),
                    'role': assistant_message.role
                }
            }), 201
        except Exception as e:
            # Create a new assistant message to tell the user that there was an error
            assistant_message = Messages.create_assistant_message(
                content="""I’m sorry, but I encountered an internal error while processing your request with the server and 
                couldn’t complete it. You can try again in a few moments or simplify your prompt. If the issue persists, please 
                let me know or contact support.""",
                conversation_id=conversation.conversation_id
            )
            return jsonify({
                'conversation_id': conversation.conversation_id,
                'user_message': {
                    'message_id': user_message.message_id,
                    'content': user_message.content,
                    'timestamp': user_message.timestamp.isoformat(),
                    'role': user_message.role
                },
                'assistant_message': {
                    'message_id': assistant_message.message_id,
                    'content': assistant_message.content,
                    'timestamp': assistant_message.timestamp.isoformat(),
                    'role': assistant_message.role
                },
                'error': str(e)
            }), 500
        
    except Exception as e:
        # Create a new assistant message to tell the user that there was an error
        assistant_message = Messages.create_assistant_message(
            content="""I’m sorry, but I encountered an internal error while processing your request with the server and couldn’t 
            complete it. You can try again in a few moments or simplify your prompt. If the issue persists, please let me know or 
            contact support.""",
            conversation_id=conversation.conversation_id
        )
        return jsonify({
            'conversation_id': conversation.conversation_id,
            'user_message': {
                'message_id': user_message.message_id,
                'content': user_message.content,
                'timestamp': user_message.timestamp.isoformat(),
                'role': user_message.role
            },
            'assistant_message': {
                'message_id': assistant_message.message_id,
                'content': assistant_message.content,
                'timestamp': assistant_message.timestamp.isoformat(),
                'role': assistant_message.role
            },
            'error': str(e)
        }), 500

# send a message in a conversation
@routes.route('/send_message', methods=['GET'])
def send_message():
    try:
        # user_message = request.json.get('message')
        # conversation_id = request.json.get('conversation_id')
        user_message = "Is conversation 1 working?"
        conversation_id = 1
        
        # Create a new message
        user_message = Messages.create_user_message(
            content=user_message,
            conversation_id=conversation_id
        )
        
        # Get the response from the LLM
        try:
            conversation = Conversations.get_conversation(conversation_id)
            conversation_history = [{'role': message.role, 'content': message.content} for message in conversation]
            ollama_response, appended_chat_history = ollama.chat(conversation_history, user_message.content)

            assistant_message = Messages.create_assistant_message(
                content=ollama_response['content'],
                conversation_id=conversation_id
            )

            return jsonify({
                'conversation_id': conversation_id,
                'chat_history': appended_chat_history,
                'user_message': {
                    'message_id': user_message.message_id,
                    'content': user_message.content,
                    'timestamp': user_message.timestamp.isoformat(),
                    'role': user_message.role
                },
                'assistant_message': {
                    'message_id': assistant_message.message_id,
                    'content': assistant_message.content,
                    'timestamp': assistant_message.timestamp.isoformat(),
                    'role': assistant_message.role
                }
            }), 201
        except Exception as e:
            # Create a new assistant message to tell the user that there was an error
            assistant_message = Messages.create_assistant_message(
                content="""I’m sorry, but I encountered an internal error while processing your request with the server and couldn’t 
                complete it. You can try again in a few moments or simplify your prompt. If the issue persists, please let me know or 
                contact support.""",
                conversation_id=conversation_id
            )
            return jsonify({
                'conversation_id': conversation_id,
                'user_message': {
                    'message_id': user_message.message_id,
                    'content': user_message.content,
                    'timestamp': user_message.timestamp.isoformat(),
                    'role': user_message.role
                },
                'assistant_message': {
                    'message_id': assistant_message.message_id,
                    'content': assistant_message.content,
                    'timestamp': assistant_message.timestamp.isoformat(),
                    'role': assistant_message.role
                },
                'error': str(e)
            }), 500
    except Exception as e:
        # Create a new assistant message to tell the user that there was an error
        assistant_message = Messages.create_assistant_message(
            content="""I’m sorry, but I encountered an internal error while processing your request with the server and couldn’t 
            complete it. You can try again in a few moments or simplify your prompt. If the issue persists, please let me know or 
            contact support.""",
            conversation_id=conversation_id
        )
        return jsonify({
            'conversation_id': conversation_id,
            'user_message': {
                'message_id': user_message.message_id,
                'content': user_message.content,
                'timestamp': user_message.timestamp.isoformat(),
                'role': user_message.role
            },
            'assistant_message': {
                'message_id': assistant_message.message_id,
                'content': assistant_message.content,
                'timestamp': assistant_message.timestamp.isoformat(),
                'role': assistant_message.role
            },
            'error': str(e)
        }), 500

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
        


