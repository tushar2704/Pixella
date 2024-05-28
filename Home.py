##© 2024 Tushar Aggarwal. All rights reserved.(https://tushar-aggarwal.com)
##Pixella[Towards-GenAI] (https://github.com/Towards-GenAI)
##################################################################################################
#Importing dependencies

from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
import os
import logging
import streamlit as st
from pathlib import Path
import base64
import sys
import os
import warnings
from dotenv import load_dotenv
from typing import Any, Dict
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import HumanMessage
from langchain_community.tools import DuckDuckGoSearchRun
search_tool = DuckDuckGoSearchRun()
from fpdf import FPDF
#From src
# from src.agents import *
# from src.task import *
# from src.crew import *
from src.crew import writing_crew_1
from src.components.navigation import *






















##################################################################################################
#Setting up Llama3 via Ollama server @http://localhost:11434/v1 
os.environ["OPENAI_API_KEY"] = "NA"

llm = ChatOpenAI(
    model = "crewai-llama3",
    base_url = "http://localhost:11434/v1")
##################################################################################################
#Streamlit Page Setup
page_config("Botimmus", "🤖", "wide")
custom_style()
st.sidebar.image('./src/logo.png')


class CustomHandler(BaseCallbackHandler):
    def __init__(self, agent_name: str) -> None:
        super().__init__()
        self.agent_name = agent_name

    def on_chain_start(self, serialized: Dict[str, Any], outputs: Dict[str, Any], **kwargs: Any) -> None:
        st.session_state.messages.append({"role": "assistant", "content": outputs['input']})
        st.chat_message("assistant").write(outputs['input'])

    def on_agent_action(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any) -> None:
        st.session_state.messages.append({"role": "assistant", "content": inputs['input']})
        st.chat_message("assistant").write(inputs['input'])

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        st.session_state.messages.append({"role": self.agent_name, "content": outputs['output']})
        st.chat_message(self.agent_name).write(outputs['output'])
    
    
def main():
    st.title("🤖Pixella🤖")
    st.markdown('''
            <style>
                div.block-container{padding-top:0px;}
                font-family: 'Roboto', sans-serif; /* Add Roboto font */
                color: blue; /* Make the text blue */
            </style>
                ''',
            unsafe_allow_html=True)
    st.markdown(
        """
        ### Write Structured blogs with AI Agents, powered by Llamma3 via Ollama & CrewAI  [Towards-GenAI](https://github.com/Towards-GenAI)
        """
    )
    
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    col1, col2 = st.columns(2)
    # Input for blog topic
    with col1:
        blog_topic = st.text_input("Enter the blog topic:")

    # Dropdown for selecting the type of content
    with col2:
        
        content_type = st.selectbox("Select the type of content:", ["Blog Post", "Research Paper", "Technical Report"])
    
    
    
    
    
    
    if st.button("Start Blogging Crew"):
        if blog_topic:
            result = writing_crew_1.kickoff(inputs={
                "topic": blog_topic,}
               )
            st.write(result)
            
            # Create a PDF and write the output to it
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            for line in result.split("\n"):
                pdf.write(5, line)
                pdf.ln()  # move to next line

            # Save the PDF file
            pdf.output("blog.pdf")
            file_path = './blog.pdf'
            with open(file_path, 'rb') as file:
                file_content = file.read()

            # Create download button
            st.download_button(
                label="Download blog.pdf",
                data=file_content,
                file_name="blog.pdf",
                mime="application/pdf"
            )
                
            
        else:
            st.error("Please enter a blog topic.")
            
    

if __name__ == "__main__":
    main()
    with st.sidebar:
        
        footer()












