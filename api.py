import os
from dotenv import load_dotenv
from common.embedder import embeddings, index_embeddings
from common.prompt import prompt
from pathway.xpacks.llm.parsers import ParseUnstructured
from pathway.xpacks.llm.splitters import TokenCountSplitter
from transformers import AutoModelForTokenClassification, AutoTokenizer

load_dotenv()
data_folder_path = os.environ.get("DATA_FOLDER_PATH", "/usr/local/data")

pii_model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
pii_tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")

def detect_and_redact_pii(text):
    inputs = pii_tokenizer(text, return_tensors="pt")
    outputs = pii_model(**inputs)[0]
    redacted_text = text
    for idx, token in enumerate(inputs.tokens()[0]):
        if outputs[0][idx][5] > 0.5:  # 5 is the index for 'PER' entity
            redacted_text = redacted_text.replace(token, "[REDACTED]")
    return redacted_text

def run(host, port):
    # Given a user search query query
    response_writer = pw.io.http.rest_connector(
        host=host, port=port, schema=QueryInputSchema, autocommit_duration_ms=50,
    )

    # Real-time data coming from external unstructured data sources like a PDF file
    input_data = pw.io.fs.read(
        data_folder_path, mode="streaming", format="binary", autocommit_duration_ms=50,
    )

    # Chunk input data into smaller documents
    parser = ParseUnstructured()
    documents = input_data.select(texts=parser(pw.this.data))
    documents = documents.flatten(pw.this.texts)
    documents = documents.select(texts=pw.this.texts[0])
    splitter = TokenCountSplitter()
    documents = documents.select(chunks=splitter(pw.this.texts))
    documents = documents.flatten(pw.this.chunks)
    documents = documents.select(chunk=pw.this.chunks[0])

    # Compute embeddings for each document using the OpenAI Embeddings API
    embedded_data = embeddings(context=documents, data_to_embed=pw.this.chunk)

    # Construct an index on the generated embeddings in real-time
    index = index_embeddings(embedded_data)

    # Generate embeddings for the query from the OpenAI Embeddings API
    embedded_query = embeddings(context=query, data_to_embed=pw.this.query)

    # Build prompt using indexed data
    responses = prompt(index, embedded_query, pw.this.query)

    # Redact PII from the responses
    redacted_responses = [detect_and_redact_pii(response) for response in responses]

    # Feed the prompt to ChatGPT and obtain the generated answer.
    response_writer(redacted_responses)

    # Run the pipeline
    pw.run()

class QueryInputSchema(pw.Schema):
    query: str

if __name__ == "__main__":
    host = os.environ.get("HOST", "localhost")
    port = int(os.environ.get("PORT", 8501))
    run(host, port)
