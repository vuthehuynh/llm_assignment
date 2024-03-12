# Industrial Generative AI Q&A System for Refrigeration Field Engineers

## Local deployment 

- Git clone git@github.com:vuthehuynh/llm_assignment.git
- cd llm_assignment
- Setup environment variables 
  - Specify openai_key for OPENAI_API_KEY in the .env file in the project root folder
  - Specify port for the service in the docker-compose.yaml (default 4000)
- Run `sudo docker-compose up - - build`
- Open the browser, type: http://localhost:4000 to view the app

