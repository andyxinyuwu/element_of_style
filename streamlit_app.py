import streamlit as st
import openai
import os
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.environ.get('OPENAI_API_KEY')


system_prompt = """
"You are an expert on English non-fiction writing. 
Revise my article by focusing on the following elements: 
Aim for clarity and brevity, cutting out unnecessary words. 
Use active voice where possible and prefer concrete language over abstract terms. 
Ensure grammatical parallelism in lists and compound sentences. 
Limit jargon and define any that remains. Check for proper punctuation, 
standard spelling, and grammar. Keep tenses consistent and place modifiers next to the words they modify. 
Examine the overall design and structure, making sure each paragraph starts with a topic sentence. 
Finally, evaluate the tone and style for consistency, and remove needless prepositions and exclamation points.
"""


st.set_page_config(page_title="Chat with the Streamlit docs, powered by LlamaIndex", page_icon="🦙", layout="centered",
                   initial_sidebar_state="auto", menu_items=None)
st.title("StyleCraft, advice from element of style")

advice = """

"""

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    url = "https://docs.google.com/document/d/1GUI4kNnP6HpQvxaZ0ZDJRn_cJVWtf7JKbu9ybxWj6Dw/edit?usp=sharing"
    myurl = "https://xinyuwu.xyz/"
    st.session_state.messages = [
        {"role": "assistant", "content": "Paste your article here and I will help revise your article based on the [rules](%s) from Element of Style. Please contact [me](%s) for any feedbacks. Thanks!" % (url, myurl) }
    ]

if prompt := st.chat_input("Your article"):  # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:  # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Writing..."):

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k-0613",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ]
            )

            result = response.choices[0].message.content
            st.write(result)
            message = {"role": "assistant", "content": result}
            st.session_state.messages.append(message)  # Add response to message history