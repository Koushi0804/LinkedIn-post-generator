# app.py

import streamlit as st
import requests
import os
from PIL import Image
from io import BytesIO

# Access API keys from Streamlit secrets
TOGETHER_API_KEY = st.secrets["TOGETHER_API_KEY"]
HF_API_KEY = st.secrets["HF_API_KEY"]

st.title("📝 LinkedIn Post Generator")
prompt = st.text_input("Enter a topic (e.g., 'AI in Marketing')")

if st.button("Generate Post"):
    if not prompt:
        st.warning("Please enter a topic.")
    else:
        # --- Generate Text ---
        with st.spinner("Generating text..."):
            headers = {
                "Authorization": f"Bearer {TOGETHER_API_KEY}",
                "Content-Type": "application/json"
            }
            json_data = {
                "model": "mistralai/Mistral-7B-Instruct-v0.1",
                "prompt": f"<s>[INST] Write a short LinkedIn post about: {prompt} [/INST]",
                "temperature": 0.7,
                "max_tokens": 300,
                "top_p": 0.9
            }
            response = requests.post(
                "https://api.together.xyz/inference",
                headers=headers,
                json=json_data
            )
            try:
                post_text = response.json()["output"]["choices"][0]["text"]
                st.subheader("Generated LinkedIn Post")
                st.write(post_text)
            except Exception as e:
                st.error("Failed to generate post text. Please try again.")
                st.stop()

        # --- Generate Image ---
        with st.spinner("Generating image..."):
            image_payload = {
                "inputs": f"A professional LinkedIn-style illustration about: {prompt}"
            }
            hf_headers = {
                "Authorization": f"Bearer {HF_API_KEY}"
            }
            image_response = requests.post(
                "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2",
                headers=hf_headers,
                json=image_payload
            )

            if image_response.status_code == 200:
                try:
                    image = Image.open(BytesIO(image_response.content))
                    st.subheader("Generated Image")
                    st.image(image)
                except Exception as e:
                    st.error("Failed to display the generated image.")
            else:
                st.error("Image generation failed. Please try again later.")
