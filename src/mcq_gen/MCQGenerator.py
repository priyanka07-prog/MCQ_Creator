import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import LLMChain, SequentialChain
import PyPDF2
from src.mcq_gen.logger import logging
from src.mcq_gen.utills import read_file,get_table_data

load_dotenv()



key =os.getenv("My_key")


llm = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash", temperature=0.7,google_api_key=os.getenv("My_key"))

template= """
Text: {text}
You are an expert MCQ maker.
Create {number_of_questions} MCQs based on the above text for the subject {subject}. 
The tone of the questions should be {tone}.
Make sure the questions are not repeated and are unique and check all the questions to be conforming the text as well .
The output should be in the following JSON format:
{response_json}

"""

quiz_generator_prompt = PromptTemplate(
    input_variables=["text","number_of_questions", "subject", "tone", "response_json"],
    template=TEMPLATE
)

quiz_chain = LLMChain(llm=llm, prompts=quiz_generator_prompt, output_key="quiz", verbose=True)

template2 ="""
You are an expert MCQ maker.
Give a multiple choice question based on the subject {subject}.
Make sure the question is not repeated and is unique and check the question to be conforming the text as well .
If the quiz is not at per with the above instructions, then regenerate the quiz.
QUIZ_MCQs:
{quiz}

Check from an expert writer of the above quiz:
"""

quiz_evalaution_prompt= PromptTemplate(input_variable=["subject", "quiz"], template=template2)

review_chains=LLMChain(llm=llm, prompt=quiz_evalaution_prompt, output_key="review", verbose=True)

generate_evaluate_chain=SequentialChain(chains=[quiz_chain, review_chains], input_variables=["text","number_of_questions", "subject", "tone", "response_json"],
                                        output_variables=["quiz", "review"], verbose=True)


def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader=PyPDF2.PdffileReader(file)
            text=""
            for page in pdf_reader.pages:
                text =page.extract_text()
            return text
        
        except Exception as e:
            raise Exception("error reading the pdf file")
        
    elif file.name.readswith(".txt"):
        return file.read().decode("utf.8")
    
    else:
        raise Exception(
            "unsupported file format only pdf and text file supported"
        )
              