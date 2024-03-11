from flask import Flask, request, jsonify
import openai
import PyPDF2
from openai import OpenAI
import os 

app = Flask(__name__)

# Set up your OpenAI API key
openai.api_key = "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"
client = OpenAI(api_key=os.environ.get("CUSTOM_ENV_NAME", "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"))


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

@app.route('/generate_response', methods=['POST'])
def generate_response():
    # Get prompt and PDF file path from the request
    prompt = request.form.get('prompt')
    pdf_path = request.form.get('pdf_path')

    # print(f"prompt############### :{prompt}")
    # print(f"PDF_path############### :{pdf_path}")

    # Read the contents of the PDF file
    # pdf_content = extract_text_from_pdf(pdf_path)
    pdf_content = extract_text_from_pdf_test(pdf_path)

    
    # Construct the prompt
    prompt_with_pdf = f"{prompt}\n\nPDF Content:\n{pdf_content}"
    # # Set up parameters for the OpenAI API call

    # # Call the OpenAI API to generate a response
    parameters = {
        "model":"gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt_with_pdf
            }
        ]
    }
    response = client.chat.completions.create(**parameters)

    # # Get the generated response
    generated_text = response.choices[0].message.content

    # Return the generated response
    return jsonify({'generated_response': generated_text})

if __name__ == '__main__':
    app.run(host='localhost', port=5000)