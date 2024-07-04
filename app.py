from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import io
import base64
from PIL import Image
import google.generativeai as genai
import pdf2image
import poppler

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content,input_prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,pdf_content[0],input_prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    #convert the pdf to image
    if uploaded_file is not None:
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        #convert into bytes
        img_byte_arr= io.BytesIO()
        first_page.save(img_byte_arr,format="JPEG")
        img_byte_arr=img_byte_arr.getval()

        pdf_part=[
            {
                "mime_type":"image/jpeg",
                "data":base64.b64encocde(img_byte_arr).decode() #encode to base64
            }
        ]
        return pdf_part
    else:
        raise FileNotFoundError("NO file Uploaded")
    
    ##streamlit APp

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking sytem")
input_text=st.text_area("Job Description:",key="input")
uploaded_file=st.file_uploader("Upload resume",type=["pdf"])

if uploaded_file is not None:
    st.write("PDF uploaded successfully")
submit1=st.button('tell me about the resume')
submit2= st.button(" how can i improvise my skill")
submit3 = st.button("percentage match")

input_promt1=""" 
You are and experience telnical human resource manager in data science, fullstack web development, big data engneering and deveops your task is to evaluate people and highlight strengths and weakness"""

input_promt3=""" your are a skilled ATS applicant tracker and deep understand and tell me the percentage match for prvided context """

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_promt1,pdf_content,input)
        st.subheader("the response is")
        st.write(response)
    else:
        st.write("Please upload the resume")


    