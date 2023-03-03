#import libs
import openai 
import streamlit as st
import io
import docx
import pandas as pd
from transformers import GPT2TokenizerFast\


# pip install streamlit-chat  
from streamlit_chat import message

openai.api_key = st.secrets['openai-secret']

#add title to 
st.title("chatBot : OpenAI")

#Initialising session
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'history' not in st.session_state:
    st.session_state['history'] = []

if 'uploadKey' not in st.session_state:
    st.session_state['uploadKey'] = 1

def generate_response(prompt):
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages= prompt
        )
        return chat['choices'][0]['message']['content']

#Form for user input
def update():
    st.session_state.text += st.session_state.text_value


uploaded_file = st.file_uploader("Choose a CSV file", key=st.session_state['uploadKey'])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df)

user_input = st.text_input('Enter your prompt and click on submit', value="", key='text_value')

#Get user response
if uploaded_file is not None and user_input != "":
    #Get user response
    user_input = user_input + df.to_json()
    st.session_state['uploadKey'] += 1

if user_input:
        
    #Store the input
    st.session_state.history.append({"role": "user", "content": user_input})

    #Generate the response
    output = generate_response(st.session_state['history'])

    #Store the chat
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)
    st.session_state.history.append({"role": "assistant", "content": output})

# Create an instance of a word document
def list_to_word_doc(items, doc_name):
    doc = docx.Document()
    for item in items:
        doc.add_paragraph(item)
    return doc

#Chat history downloader
doc_download = list_to_word_doc(st.session_state['history'], 'chat_history')

bio = io.BytesIO()
doc_download.save(bio)
if doc_download:
    st.download_button(
        label="Download Chat History",
        data=bio.getvalue(),
        file_name="chat_history.docx",
        mime="docx"
    )

#display no of tokens
#tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
#number_of_tokens = len(tokenizer(''.join(st.session_state['history']))['input_ids'])

#st.text('Number of tokens left: '+ str(max_tokens - number_of_tokens))

if st.session_state['generated']:
    
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
