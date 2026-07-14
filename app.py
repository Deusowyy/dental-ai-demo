import streamlit as st
from groq import Groq

# Pobieranie klucza API ze Streamlit Secrets
try:
    api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("Brak klucza GROQ_API_KEY. Skonfiguruj go w ustawieniach Secrets na platformie Streamlit.")
    st.stop()

# Inicjalizacja klienta Groq
client = Groq(api_key=api_key)

st.set_page_config(page_title="Dental AI Demo", page_icon="🦷")
st.title("🦷 SmilePerfect Texas - AI Assistant")
st.caption("Wersja demonstracyjna (Zasilana darmowym API Groq i modelem Llama 3.3).")

if "messages" not in st.session_state:
    system_prompt = """
    You are a friendly and professional virtual receptionist for 'SmilePerfect Dental Clinic' located in Austin, Texas.
    Your job is to answer basic patient questions and encourage them to book an appointment.
    
    Key Information:
    - Open: Monday to Friday, 8 AM to 5 PM.
    - Services: General dentistry, teeth whitening ($150), implants, emergency extraction.
    - Location: 123 Longhorn Blvd, Austin, TX.
    - Booking: Always tell users they can book by calling 555-0199 or leaving their email here.
    
    Rules:
    - Keep responses short, concise, and helpful.
    - Do NOT provide medical diagnoses.
    - ALWAYS reply in English.
    """
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
    st.session_state.messages.append({"role": "assistant", "content": "Howdy! Welcome to SmilePerfect Dental. How can I help you smile brighter today? 😁"})

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

user_input = st.chat_input("Type your message here...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                stream=True,
            )
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"API Error: {e}")
```

### Ważna uwaga:
Jeśli po wklejeniu tego na GitHubie nadal będzie błąd, zerknij na to w edytorze GitHuba:
*   Wszystkie linie zaczynające się od `if`, `with`, `for`, `try` muszą mieć odpowiednie wcięcia (zazwyczaj 4 spacje).
*   **W edytorze GitHuba wciśnij "Tab"** przed linią `try:` jeśli zobaczysz, że jest "za krótka" w stosunku do `with` linijkę wyżej.

Zrób ten "clean paste", zapisz commit i daj znać – to musi zadziałać, bo kod jest teraz czysty jak łza. Jak to ruszy, od razu przechodzimy do Dnia 3: **Skrypt do pozyskiwania klientów**!
