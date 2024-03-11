from flask import Flask, request, jsonify
import openai
import PyPDF2
from openai import OpenAI
import os 
from langchain.chains import RetrievalQA
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
import openai 
import os 
from langchain_openai import OpenAI

app = Flask(__name__)


# Set up your OpenAI API key
# os.environ['OPENAI_API_KEY'] = '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'

print("###################: ",os.environ['OPENAI_API_KEY'])
openai.api_key = os.environ['OPENAI_API_KEY'] 
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", os.environ['OPENAI_API_KEY'] ))


def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text


def extract_text_from_pdf_test(pdf_path):
    text = "Evaluation Criteria:1. Presentation: Are the slides clear, concise, and effectively communicat the solution and its components?"
    return text


# Assuming an in-memory structure for simplicity
# For production, consider using a persistent storage solution
user_histories = {}


@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    
    file.save(os.path.join('./',  file.filename))
    return "File uploaded successfully", 200

@app.route('/generate_response', methods=['POST'])
def generate_response():
    # Get prompt and PDF file path from the request
    prompt = request.form.get('prompt')
    pdf_path = request.form.get('pdf_path')
    user_id = request.form.get('user_id')

    print(f'###################### User_id :{user_id}. Len history:{len(user_histories)}')
    # Read the contents of the PDF file
    # pdf_content = extract_text_from_pdf(pdf_path)
    # pdf_content = extract_text_from_pdf_test(pdf_path)

    # Load pdf content using langchain
    loader = PyPDFLoader(file_path=pdf_path)
    document_content = loader.load()

    # print("####################33", document_content)

    # Init embedding of document user manual using lanchain
    embeddings = OpenAIEmbeddings()
    qa_db = Chroma.from_documents(document_content, embeddings)

     # Check if user history exists and add it to the retriever's documents
    if user_id in user_histories:
        user_histories_str = [str(d) for d in user_histories[user_id]]
        qa_db.add_texts(user_histories_str)

    retriever = qa_db.as_retriever()

    ### IMPORTANT NOTE: there is different chain_type can be use for more accuracy "stuff", "map_reduce", "refine", and "map_rerank".
    # https://brain.d.foundation/Engineering/AI/Workaround+with+OpenAI's+token+limit+with+Langchain
    openai_llm = OpenAI(openai_api_key=os.environ['OPENAI_API_KEY'])
    our_qa = RetrievalQA.from_chain_type(llm=openai_llm, chain_type="stuff", retriever=retriever)

    answer = our_qa.run(prompt)

    # Save the prompt and answer to the user's history
    if user_id not in user_histories:
        user_histories[user_id] = []
    user_histories[user_id].append({'prompt': prompt, 'answer': answer})


    # Return the generated response
    return jsonify({'generated_response': answer, 'user_history': user_histories[user_id]})

if __name__ == '__main__':
    app.run(host='localhost', port=5000)