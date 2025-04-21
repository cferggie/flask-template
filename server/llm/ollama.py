import requests

class Ollama:
    def __init__(self):
        self.url_generate = "http://localhost:11434/api/generate"
        self.url_chat = "http://localhost:11434/api/chat"
        self.model = "gemma3:12b"

    def generate(self, message):
        """
        This function will send a request to the Ollama API and return the response as a JSON object. This should be used for
        one-time generation tasks.

        Args:
            message (str): The users prompt.

        Returns:
            str: The response of the model in JSON format.
        """
        data = {
            "model": self.model,
            "prompt": message,
            "stream": False
        }

        try:
            response = requests.post(self.url_generate, json=data)
            if response.status_code == 200:
                result = response.json()
                model_response = result.get('response')
                return model_response
            else:
                print(f"Error: {response.status_code}, {response.text}")
                return None
        except Exception as e:
            print(f'An error occured: {e}')
            return None
    
    def append_chat_history(self, messages, user_message, model_response):
        """
        This function adds user messages and their model responses to the chat history.

        Args:
            messages (list): A list of messages to send to the model.

        Returns:
            list: A list of messages to send to the model.
        """
        history = messages
        history += [
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": model_response},
        ]
        return history

    def chat(self, messages, user_message):
        """
        This function will start a conversation with the model and return the response as a JSON object. This should be used for 
        chatbot functionality that requires a conversation history.

        Args:
            messages (list): A list of messages to send to the model.
        
        Returns:
            str: The response of the model in JSON format.
        """
        data = {
            "model": self.model,
            "messages": messages + [
                {"role": "user", "content": user_message},
                ],
            "stream": False
        }

        try:
            response = requests.post(self.url_chat, json=data)
            if response.status_code == 200:
                result = response.json()
                model_response = result.get('message')
                appended_chat_history = self.append_chat_history(messages, user_message, model_response['content'])
                return model_response, appended_chat_history
            else:
                print(f"Error: {response.status_code}, {response.text}")
                return None
        except Exception as e:
            print(f'An error occured: {e}')
            return None

    
if __name__ == "__main__":
   # Test the generate function
   print("Testing the generate function...")
   ollama = Ollama()
   result = ollama.generate("Hello, how are you?")
   print(f"Model response: {result}\n")
   
   # Test the chat function
   print(f"Testing the chat function...")
   messages = [{"role": "user", "content": "Is this working?"}, {"role": "assistant", "content": "Yes, it is working."}]
   ollama = Ollama()
   result = ollama.chat(messages, "Is this working?")
   print(f"Model response: {result[0]}")
   print(f"Chat history: {result[1]}")
