from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_community.llms import OpenAI
from langchain_community.callbacks import get_openai_callback


def main():
    load_dotenv(".venv")
    #set the page title and icon
    #the icon is a green leaf
    st.set_page_config(page_title="ADMA Copilot", page_icon="🍃")
    st.header("ADMA Copilot: Ask Me Anything About Your AgData💬",divider="green")

    st.sidebar.title("Control Panel")
    
    # upload file
    pdf = st.sidebar.file_uploader("Upload your PDF", type="pdf")
    
    # extract the text
    if pdf is not None:
      pdf_reader = PdfReader(pdf)
      text = ""
      for page in pdf_reader.pages:
        text += page.extract_text()
        
      # split into chunks
      text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
      )
      chunks = text_splitter.split_text(text)
      
      # create embeddings
      embeddings = OpenAIEmbeddings()
      knowledge_base = FAISS.from_texts(chunks, embeddings)
      
      # show user input
      user_question = st.text_input("Ask a question about your PDF:")
      if user_question:
        docs = knowledge_base.similarity_search(user_question)
        
        llm = OpenAI()
        chain = load_qa_chain(llm, chain_type="stuff")
        with get_openai_callback() as cb:
          response = chain.run(input_documents=docs, question=user_question)
          print(cb)
           
        st.write(response)
    

if __name__ == '__main__':
    main()
