import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import os
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()  # load all the environmental variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = "Get the transcripts and summarize in points of 250 words: "

def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

def extract_transcript(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript_text
    except Exception as e:
        raise e

# Streamlit app
st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter URL")
if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get detailed notes"):
    transcript_text = extract_transcript(youtube_link)
    if transcript_text:
        transcript_text = ' '.join([item['text'] for item in transcript_text])  # Convert transcript to text
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("## Summary")
        st.write(summary)
