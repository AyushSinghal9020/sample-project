import shutil
import tempfile
import os
from ingestor_and_gpt import FileIngestorGPT
import openai
import streamlit as st
from openai import OpenAI
from helper import get_image_base64_str
import base64

def RAG() :

    def load_openai_api_key():

        api_key = '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'

        client = OpenAI(api_key = api_key)

        return st.session_state.get('openai_api_key')


    openai_api_key = load_openai_api_key()


    def save_uploaded_file(uploaded_file) : 

        if 'file_paths' not in st.session_state : st.session_state['file_paths'] = {}

        with tempfile.NamedTemporaryFile(
            delete = False , 
            suffix = '.pdf') as tmp_file : 

            shutil.copyfileobj(uploaded_file, tmp_file)
            st.session_state['file_paths'][uploaded_file.name] = tmp_file.name

        return st.session_state['file_paths'][uploaded_file.name]


    uploaded_file = st.file_uploader(
        'Upload File' , 
        type = 'pdf')

    if uploaded_file :

        file_path = save_uploaded_file(uploaded_file)

        ingestor = FileIngestorGPT(file_path)
        ingestor.handlefileandingestGPT()

    def clean_up_files():
        
        if 'file_paths' in st.session_state : 
            for file_path in st.session_state['file_paths'].values() : 
                if os.path.exists(file_path) : os.remove(file_path)

def report() : 

    st.markdown(open('Main/Assets/Report/Mark_1.txt').read())

    bar_dict = {
        'token_length' : {
            'GPT 3.5 Turbo' : 32768 , 
            'LLAMA 2 3B' : 16000 , 
            'Gemma' : 8192 ,
            'GPT 3' : 4096 , 
            'LLAMA 2 7B' : 4096 , 
            'BERT' : 512 
        } , 
        'model_size' : {
            'BERT' : 550000000 , 
            'Gemma' : 1000000000 , 
            'LLAMA 2 3B' : 3000000000 , 
            'LLAMA 2 7B' : 7000000000 , 
            'GPT 3.5 Turbo' : 22000000000 , 
            'GPT 3' : 170000000000 , 
        } , 
        'training_size' : {
            'GPT 3.5 Turbo' : 570 , 
            'LLAMA 2 3B' : 100 , 
            'Gemma' : 100 ,
            'GPT 3' : 570 , 
            'LLAMA 2 7B' : 100 , 
            'BERT' : 136
        }
    }

    st.bar_chart(bar_dict['token_length'])
    st.markdown(open('Main/Assets/Report/Mark_2.txt').read())
    st.bar_chart(bar_dict['model_size']) 
    st.bar_chart(bar_dict['training_size'])

    st.markdown(open('Main/Assets/Report/Mark_5.txt').read())
    st.markdown(open('Main/Assets/Report/Mark_6.txt').read())
    st.markdown(f'''<img src="data:image/jpeg;base64,{get_image_base64_str('Main/Assets/Report/Images/MLM_1.webp')}" width="400" height="200">''' , unsafe_allow_html = True)
    st.markdown(open('Main/Assets/Report/Mark_7.txt').read())
    st.markdown(f'''<img src="data:image/jpeg;base64,{get_image_base64_str('Main/Assets/Report/Images/MLM_2.webp')}" width="400" height="200">''' , unsafe_allow_html = True)
    st.markdown(open('Main/Assets/Report/Mark_8.txt').read())
    st.markdown(f'''<img src="data:image/jpeg;base64,{get_image_base64_str('Main/Assets/Report/Denoising-Autoencoders.webp')}" width="400" height="200">''' , unsafe_allow_html = True)
    st.markdown(open('Main/Assets/Report/Mark_9.txt').read())

def understanding() : pass
def questions() : pass




st.sidebar.title('Navigation')

option = st.sidebar.selectbox(
    'Go to' , 
    [
        'RAG' , 
        'Report' , 
        'Understanding' , 
        'Questions'
    ])

if option == 'RAG' : RAG()
elif option == 'Report' : report()
elif option == 'Understanding' : understanding()
elif option == 'Questions' : questions()
