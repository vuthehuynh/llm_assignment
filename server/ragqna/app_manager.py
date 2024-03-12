from flask import jsonify
import sys 
from pathlib import Path
sys.path.append(Path(__file__).parent.absolute().as_posix())

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

from schemas import QnAInput

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

class AppManager:
    def __init__(self) -> None:
        pass

    async def chat(self, QnAInput):

        prompt = QnAInput.prompt
        pdf_path = QnAInput.pdf_path
        user_id = QnAInput.user_id

        print(f'###################### User_id :{user_id}. Len history:{len(user_histories)}')
        # Read the contents of the PDF file
        # pdf_content = extract_text_from_pdf(pdf_path)
        # pdf_content = extract_text_from_pdf_test(pdf_path)

        # Load pdf content using langchain
        loader = PyPDFLoader(file_path=pdf_path)
        document_content = loader.load()

        # print("####################33", document_content)
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