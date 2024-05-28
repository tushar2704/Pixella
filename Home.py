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




















topic=input("Enter the topic: ")


results = writing_crew_1.kickoff(inputs={"topic": topic})