import streamlit as st
from streamlit_chat import message

from langchain.chat_models import ChatOpenAI as COAI
from langchain.document_loaders import PyMuPDFLoader as PL
from langchain.embeddings import HuggingFaceEmbeddings as HFE
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain as CRC

class FileIngestorGPT :

    def __init__(self , path) : self.path = path

    def handlefileandingestGPT(self) : 

        db = FAISS.from_documents(
            PL(file_path = self.path).load() , 
            HFE(
                model_name = 'sentence-transformers/all-MiniLM-L6-v2'
                )
            )
        db.save_local('vectorstore/db_faiss')

        chain = CRC.from_llm(
            llm = COAI(
                model = 'gpt-3.5-turbo' ,
                openai_api_key = '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', 
            ) , 
            retriever = db.as_retriever()
        )


        def conversational_chat(query) : 
            
            result = chain(
                {
                    'question' : query , 
                    'chat_history' : st.session_state['history']
                }
            )
            
            st.session_state['history'].append(
                (
                    query , 
                    result['answer']))

            return result["answer"]


        if 'history' not in st.session_state : st.session_state['history'] = []
        if 'generated' not in st.session_state : st.session_state['generated'] = ['Hello ! Ask me(LLAMA2) about the PDF uploaded 🤗']
        if 'past' not in st.session_state : st.session_state['past'] = ['Hey ! 👋']

        response_container = st.container()
        container = st.container()

        with container : 

            with st.form(
                key = 'my_form' , 
                clear_on_submit = True) :
                user_input = st.text_input(
                    'Query:' , 
                    placeholder = 'Talk to PDF data 🧮' , 
                    key='input')
                submit_button = st.form_submit_button(label = 'Send')

            if submit_button and user_input : 
                
                output = conversational_chat(user_input)
                
                st.session_state['past'].append(user_input)
                st.session_state['generated'].append(output)

        if st.session_state['generated'] : 
            
            with response_container : 
                
                for index in range(len(st.session_state['generated'])) : 
                    
                    message(
                        st.session_state['past'][index] , 
                        is_user = True , 
                        key = str(index) + '_user' , 
                        avatar_style = 'big-smile')
                    message(
                        st.session_state['generated'][index] , 
                        key=str(index) , 
                        avatar_style = 'thumbs')

