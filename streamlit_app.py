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
            "content": '''You are a university professor specializing in medical biology.
            You are preparing a final exam for advanced medical students. 

            Ask a detailed and relevant exam question based on clinical cases, 
            human physiology, molecular biology, pharmacology, or endocrinology.

            Take inspiration from competitions and the annals of the “Concours d'internat de pharmacie” in France.

            Ensure the question tests the student's understanding of complex medical concepts 
            and encourages critical thinking. The question should be appropriate for a written exam 
            and require a comprehensive explanation as the answer. 

            Give me the choice between random topics.
            
            Translate it in French and make the question answerable with 100 words. 
            Give me only the French version and THEN wait for my answer.''',
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