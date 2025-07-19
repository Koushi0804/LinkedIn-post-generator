# app.py

import streamlit as st
import requests
import os

TOGETHER_API_KEY = st.secrets["TOGETHER_API_KEY"]
HF_API_KEY = st.secrets["HF_API_KEY"]


st.title("📝 LinkedIn Post Generator")
prompt = st.text_input("Enter a topic (e.g., 'AI in Marketing')")

if st.button("Generate Post"):
    if not prompt:
        st.warning("Please enter a topic.")
    else:
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
            post_text = response.json()["output"]["choices"][0]["text"]
            st.subheader("Generated LinkedIn Post")
            st.write(post_text)

        with st.spinner("Generating image..."):
            image_payload = {
                "inputs": prompt,
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
                st.subheader("Generated Image")
                st.image(image_response.content)
            else:
                st.error("Image generation failed. Try again later.")
