import streamlit as st
import os
import requests

# Show title and description
st.title("💬🩺 Nouky ")
st.write(
    """
🎓✨ Voici Nouky, ton compagnon de préparation aux concours de l'internat !! 📚💡\n
 Tout vos retours sont les bienvenues à cette adresse : redouane.elbadaoui@yahoo.com 📧 \n
Bonne révision ! 🚀🎉
"""
)

# Set SambaNova API key and base URL
api_key = os.environ.get("SAMBANOVA_API_KEY", "78133d14-3cff-41c7-bcac-29a3dce289d0")  
base_url = "https://api.sambanova.ai/v1"  # Base URL for SambaNova API

# Session state to store chat messages across reruns
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": '''You are a university-level expert in medical biology.
You specialize in human physiology, molecular biology, pharmacology, and endocrinology.
Rely on authoritative and reputable pharmaceutical and biomedical literature as sources.
Before providing your final answer, verify its accuracy.
Be objective in your response and do not necessarily try to go in my direction.
Once certain that the information is correct, translate your answer into French.

            .''',
        }
    ]

# Display the chat messages
for message in st.session_state.messages:
    if message["role"] != "system":  # Skip displaying system messages
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Create a chat input field
if prompt := st.chat_input("Je t'écoute"):
    # Store and display the user's prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare the request to SambaNova API
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": "Meta-Llama-3.1-70B-Instruct",  # Assuming the model is available in SambaNova
        "messages": [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
        "temperature": 0.1,
        "top_p": 0.1
    }

    # Send the request to SambaNova API
    try:
        response = requests.post(f"{base_url}/chat/completions", headers=headers, json=payload)
        response.raise_for_status()  # Ensure we catch any HTTP errors
        assistant_reply = response.json()["choices"][0]["message"]["content"]

        # Stream the response to the chat
        with st.chat_message("assistant"):
            st.markdown(assistant_reply)

        # Append the assistant's response to the session state
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with SambaNova API: {e}")
