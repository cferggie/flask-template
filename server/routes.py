from flask import Blueprint, request, jsonify
from .models import Messages, Conversations
from .llm.ollama import Ollama
from utils.logger import setup_logger

routes = Blueprint('routes', __name__)
ollama = Ollama()
logger = setup_logger(__name__)

# health check endpoint
@routes.route('/', methods=['GET'])
def health_check():
    logger.debug("Health check endpoint called")
    return jsonify({'status': 'healthy'})

# create a conversation
@routes.route('/create_conversation', methods=['GET'])
def create_conversation():
    try:
        # Get the user's message from the request
        # this assumes that the request's Content-Type is application/json
        # user_message = request.json.get('message')
        user_message = "This is a test message. Just say hello world."        
        logger.info(f"Creating new conversation with initial message: {user_message[:30]}...")
        
        # Create conversation first
        conversation = Conversations.create(
            summary=user_message,  # TODO: Generate a proper summary using LLM
        )        
        logger.info(f"Created conversation with ID: {conversation.conversation_id}")
        
        # Create the first message in the conversation
        user_message = Messages.create_user_message(
            content=user_message,
            conversation_id=conversation.conversation_id
        )        
        logger.info(f"Created user message with ID: {user_message.message_id}")

        # Generate a response using the LLM
        try:
            logger.info("Generating response from Ollama")
            ollama_response = ollama.generate(user_message.content)

            # Create a new assistant message
            assistant_message = Messages.create_assistant_message(
                content=ollama_response,
                conversation_id=conversation.conversation_id
            )            
            logger.info(f"Created assistant message: {assistant_message.content[:50]}... with ID: {assistant_message.message_id}")
            
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
            logger.error(f"Error generating Ollama response: {str(e)}", exc_info=True)
            # Create a new assistant message to tell the user that there was an error
            assistant_message = Messages.create_assistant_message(
                content="""I'm sorry, but I encountered an internal error while processing your request with the server and 
                couldn't complete it. You can try again in a few moments or simplify your prompt. If the issue persists, please 
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
        logger.error(f"Error creating conversation: {str(e)}", exc_info=True)
        # Create a new assistant message to tell the user that there was an error
        assistant_message = Messages.create_assistant_message(
            content="""I'm sorry, but I encountered an internal error while processing your request with the server and couldn't 
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
        
        logger.info(f"Sending message in conversation ID: {conversation_id}")
        
        # Create a new message
        user_message = Messages.create_user_message(
            content=user_message,
            conversation_id=conversation_id
        )
        
        logger.info(f"Created user message with ID: {user_message.message_id}")
        
        # Get the response from the LLM
        try:
            logger.info("Getting conversation history")
            conversation = Conversations.get_conversation(conversation_id)
            conversation_history = [{'role': message.role, 'content': message.content} for message in conversation]
            
            logger.info("Generating chat response from Ollama")
            ollama_response, appended_chat_history = ollama.chat(conversation_history, user_message.content)

            assistant_message = Messages.create_assistant_message(
                content=ollama_response['content'],
                conversation_id=conversation_id
            )
            
            logger.info(f"Created assistant message: {assistant_message.content[:50]}... with ID: {assistant_message.message_id}")

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
            logger.error(f"Error in chat with Ollama: {str(e)}", exc_info=True)
            # Create a new assistant message to tell the user that there was an error
            assistant_message = Messages.create_assistant_message(
                content="""I'm sorry, but I encountered an internal error while processing your request with the server and couldn't 
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
        logger.error(f"Error sending message: {str(e)}", exc_info=True)
        # Create a new assistant message to tell the user that there was an error
        assistant_message = Messages.create_assistant_message(
            content="""I’m sorry, but I encountered an internal error while processing your request with the server and couldn’t 
            complete it. You can try again in a few moments or simplify your prompt. If the issue persists, please let me know or 
            contact support.""",
            conversation_id=conversation_id
        )
        return jsonify({
            'error': str(e)
        }), 500

@routes.route('/check_convos', methods=['GET'])
def check_convos():
    try:
        logger.info("Checking conversation with ID: 1")
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
        logger.error(f"Error checking conversation: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500
        


