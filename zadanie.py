import streamlit as st
import audioop
from pydub import AudioSegment
from IPython.display import Audio
from io import BytesIO
from dotenv import dotenv_values
from openai import OpenAI

AUDIO_TRANSCRIBE_MODEL = "whisper-1"

#
# MAIN
#
st.set_page_config(page_title="Generowanie napisów", layout="centered")

st.title("🎬 Generowanie napisów v.2")    

# Wprowadzenie klucza OpenAI z obsługą wyjątków

openai_key = st.text_input("👉 Wprowadź swój klucz OpenAI", type="password")
if not openai_key:
    st.warning("👉 Musisz podać klucz OpenAI, aby kontynuować.")
    st.stop()

try:
    openai_client = OpenAI(api_key=openai_key)

# Testowe wywołanie API - lista modeli służy do weryfikacji klucza

    openai_client.models.list()
    st.success("✅ Klucz API zaakceptowany.")
except Exception as e:
    st.error(f"❌ Nieprawidłowy klucz OpenAI lub błąd połączenia:\n{e}")
    st.stop()

# Ładowanie pliku video

uploaded_files = st.file_uploader(
    "📺 Wybierz pliki wideo", accept_multiple_files=True, type=["mp4"]
)
for uploaded_file in uploaded_files:
    st.video(uploaded_file)

# Generowanie audio z pliku video

for uploaded_file in uploaded_files:
    audio = AudioSegment.from_file(uploaded_file)
    audio_filename = uploaded_file.name.rsplit(".", 1)[0] + ".mp3"
    audio.export(audio_filename, format="mp3")
    st.write(f"🔊 Plik audio wygenerowany: {audio_filename}")
    st.audio(audio_filename)