import requests
from os import getenv

# Replace with your API key and endpoint
url = getenv('ollama_url')

def summarize_text(paragraph):

    data = {
        "model": "deepseek-r1",
        "prompt": paragraph ,
        # "text": paragraph,
        "system": """
        The user will provide text. The response should ingest the paragraph and provide an unbiased summary of the text. 
        Begin each response with Unbiased Summary:""",
        
        "stream": False
    }

    try:
        response = requests.post(url, json=data)
        
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