import requests

url = 'http://localhost:8686/generate_response'
# url = 'http://0.0.0.0:5000/generate_response'



prompt = 'What is the main content of that file pdf'
pdf_path = '/home/vuthede/Downloads/Alcolizer-White-Paper-The-Use-Of-Fuel-Cell-Technology-in-Breathalysers-v1.pdf'

files = {
    'prompt': (None, prompt),
    'pdf_path': (None, pdf_path)
}

response = requests.post(url, files=files)
if response.status_code == 200:
    print("Response received successfully:")
    print(response.json())
else:
    print("Error: Failed to receive response. Status code:", response.status_code)