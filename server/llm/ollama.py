import requests

class Ollama:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = "gemma3:12b"

    def summarize_text(self, paragraph):
        """
        This function will send a request to the Ollama API and return the summary of the text.

        Args:
            paragraph (str): The text to summarize.

        Returns:
            str: The summary of the text in JSON format.
        """
        data = {
            "model": self.model,
            "prompt": paragraph,
            "format": "json",
            # can add system prompt here using "system": """""",
            "stream": False
        }

        try:
            response = requests.post(self.url, json=data)
            if response.status_code == 200:
                result = response.json()
                summary = result.get('response')
                return summary
            else:
                print(f"Error: {response.status_code}, {response.text}")
                return None
        except Exception as e:
            print(f'An error occured: {e}')
            return None


    
if __name__ == "__main__":
   ollama = Ollama()
   result = ollama.summarize_text("Hello, how are you?")
   print(result)
   print(type(result))
