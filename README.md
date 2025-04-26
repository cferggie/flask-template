# Flask Template

A lightweight and modern Ollama Flask server template, perfect for building RESTful APIs and web applications that require prompting to LLMs.

## Features

- Clean project structure
- Ready for API development
- Easy to extend and customize

## Requirements

- [Ollama](https://ollama.com/) - LLM server that needs to be installed locally
- This application uses the `gemma3:12b` model

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/flask-template.git
cd flask-template
```

2. Install and run Ollama:
   - Download from [https://ollama.com/download](https://ollama.com/download)
   - After installation, pull the Gemma 3 12B model:
   ```bash
   ollama pull gemma3:12b
   ```

3. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the development server:
```bash
python run.py
```

The server will start at `http://localhost:5000`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
