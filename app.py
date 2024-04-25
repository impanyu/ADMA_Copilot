from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_community.llms import OpenAI
from langchain_community.callbacks import get_openai_callback
import time

def stream_data(stream):
    for word in stream.split(" "):
        yield word + " "
        time.sleep(0.05)

def main():
    load_dotenv(".venv")
    #set the page title and icon
    #the icon is a green leaf
    st.set_page_config(page_title="ADMA Copilot", page_icon="🍃")
    st.header("ADMA Copilot",divider="green")

    prompt = st.sidebar.title("Control Panel")

    
    # upload file
    files = st.sidebar.file_uploader("Upload Your File",accept_multiple_files=True)
    for file in files:
        st.write(file.name)

    # Initialize the session state for chat history if it does not exist
    if 'chat_history' not in st.session_state:
      st.session_state['chat_history'] = []
    
    # Display chat history
    for message in st.session_state['chat_history']:
      if message['role'] == "user":
          # avatar is a emoji
          st.chat_message("user",avatar="👨‍🎓").write(message['message'])
      elif message['role'] == "assistant":
          st.chat_message("assistant", avatar="💻").write(message['message'])

  

    if prompt := st.chat_input("Ask Me Anything About Your AgData"):
      # Update chat history with user message
      user_message = {"role": "user",  "message": f"{prompt}"}
      st.session_state['chat_history'].append(user_message)
      st.chat_message("user",avatar="👦").write(prompt)

      # Generate a response and simulate some processing delay or logic
      response = "I am processing your request... Generators are a type of iterable, like lists or tuples, but they do not store their contents in memory; instead, they generate the items on the fly and only hold one item at a time. This makes them very memory efficient when dealing with large datasets or potentially infinite streams."
      bot_message = {"role": "assistant","message": response}
      st.session_state['chat_history'].append(bot_message)
      st.chat_message("assistant", avatar="💻").write(stream_data(response))

    
    

if __name__ == '__main__':
    main()

