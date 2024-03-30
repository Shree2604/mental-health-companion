# mental-health-companion
Create a basic RAG application focused on mental health consultation that respects user privacy, avoiding the realm of direct medical advice but offering support and companionship, including PII detection (via any pre-trained model available) to ensure only non-sensitive information is processed. 



# Mental Health Companion

This is a privacy-aware chatbot application that offers emotional support and stress-relief exercises. It uses natural language processing and machine learning techniques to understand user queries and provide relevant responses. The application also ensures that no personally identifiable information (PII) is processed or stored by redacting any sensitive data before responding to the user.

## Features

- Real-time data ingestion and indexing from unstructured data sources
- Intelligent query understanding and response generation
- PII detection and redaction to protect user privacy
- Gradio-based user interface for easy interaction

## Prerequisites

- Python 3.9 or later
- Docker (optional)

## Installation

### With Docker (Recommended)

1. Clone the repository:

```
git clone https://github.com/your-username/mental-health-companion.git
cd mental-health-companion
```

2. Create a `.env` file with your OpenAI API key and other configuration settings:

```
OPENAI_API_KEY=your_openai_api_key
DATA_FOLDER_PATH=/path/to/your/data
```

3. Build the Docker image:

```
docker build -t mental-health-companion .
```

4. Run the Docker container:

```
docker run -p 8501:8501 --env-file .env mental-health-companion
```

5. Access the application at `http://localhost:8501`.

### Without Docker

1. Clone the repository:

```
git clone https://github.com/your-username/mental-health-companion.git
cd mental-health-companion
```

2. Create a virtual environment and install the required packages:

```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

3. Create a `.env` file with your OpenAI API key and other configuration settings:

```
OPENAI_API_KEY=your_openai_api_key
DATA_FOLDER_PATH=/path/to/your/data
```

4. Run the application:

```
streamlit run ui.py
```

5. Access the application at `http://localhost:8501`.

## Usage

1. Enter your query or message in the text input box.
2. The application will process your query, retrieve relevant information, and provide a response while redacting any detected PII.
3. You can continue the conversation by entering additional queries or messages.

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix: `git checkout -b my-new-feature`
3. Make your changes and commit them: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request.

## Acknowledgments

- [Pathway](https://pathway.com/)
- [OpenAI](https://openai.com/)
- [Hugging Face Transformers](https://huggingface.co/transformers/)
- [Gradio](https://gradio.app/)
```
