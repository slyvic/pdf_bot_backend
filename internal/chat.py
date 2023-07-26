import os
from llama_index import SimpleDirectoryReader, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain.chat_models import ChatOpenAI
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

os.environ['OPENAI_API_KEY'] = "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"

def extract_info (text):
  # BEGINS PDF TO TEXT SECTION ###################
  if text != "":
    extracted_text = text
    
    # WRITING TEXT FILE TO FOLDER ##############
    directory_name = 'converted_pdf_to_text'
    if not os.path.exists(directory_name):
      os.mkdir(directory_name)
    file_name = 'document_in_txt_format.txt'
    file_path = os.path.join(directory_name, file_name)
    with open(file_path, 'w', encoding = 'UTF-8') as f:
      f.write(str(extracted_text))
    if os.path.isfile(file_path):
      print(f'{file_name} created successfully in {directory_name}.')
    else:
      print(f"{file_name} creation in {directory_name} failed.")
    
    # BEGINS LLM SECTION ##########
    max_input_size = 4096
    num_outputs = 500
    max_chunk_overlap = 200
    chunk_size_limit = 4000
    
    llm_predictor = LLMPredictor(
        llm = ChatOpenAI(temperature = 0, model_name = 'gpt-3.5-turbo', max_tokens = num_outputs))
    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit = chunk_size_limit)
    
    documents = SimpleDirectoryReader(directory_name).load_data()
    global index
    index = GPTSimpleVectorIndex(documents, llm_predictor = llm_predictor, prompt_helper = prompt_helper)
    # Remove json file if it exists to make sure it's not using a previous index file as source
    if os.path.exists("index.json"):
      os.remove("index.json")
      print("The file 'index.json' has been deleted.")
    else:
      print("The file 'index.json' does not exist.")
    
    # Save json index to disk from current information
    index.save_to_disk('index.json')
    
    # Remove directory with initial text file
    # shutil.rmtree(directory_name)
    return "Success! You can now click on the 'Knowledge bot' tab to interact with your document"

def chat (user_input):
  bot_response = index.query(user_input)
  response = ''
  # Show each letter progressively
  for letter in ''.join(bot_response.response):
    response += letter + ""
  return response
