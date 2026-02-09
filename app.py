import streamlit as st
import google.generativeai as genai

st.title("🔍 Model Diagnostic Tool")

# 1. Setup API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    st.success("API Key found.")
else:
    st.error("API Key missing in Secrets.")
    st.stop()

# 2. Ask Google what models are available
st.write("### The models available to your API Key are:")

try:
    count = 0
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            # We only care about chat models
            model_id = m.name.replace("models/", "")
            st.code(f'model_name="{model_id}"')
            count += 1
            
    if count == 0:
        st.error("Your API Key connects, but it has access to 0 chat models. You might need to enable the API in Google Cloud Console.")
        
except Exception as e:
    st.error(f"Connection Error: {e}")
