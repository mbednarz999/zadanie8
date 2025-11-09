import streamlit as st
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

st.divider()

# Ładowanie pliku video

uploaded_files = st.file_uploader(
    "📺 Wybierz pliki wideo", accept_multiple_files=True, type=["mp4", "mov", "avi", "mkv"]
)
for uploaded_file in uploaded_files:
    st.video(uploaded_file)

st.divider()    

 # Wyodrębnienie audio i generowanie napisów

for uploaded_file in uploaded_files:
    audio = AudioSegment.from_file(uploaded_file)
    audio_buffer = BytesIO()
    audio.export(audio_buffer, format="mp3")
    audio_buffer.seek(0)
    audio_buffer.name = "audio.mp3"

    st.markdown("🔊 Wygenerowane audio:", unsafe_allow_html=True)
    st.audio(audio_buffer, format="audio/mp3")

    transcript = openai_client.audio.transcriptions.create(
        file=audio_buffer,
        model=AUDIO_TRANSCRIBE_MODEL,
        response_format="srt"
    )
    st.write(f"📝 Wygenerowane napisy: {uploaded_file.name}")
    st.text_area(
        label=f"Napisy dla {uploaded_file.name}",
        value=transcript,
        height=200
    )
    st.download_button(
        label="⬇️ Pobierz napisy",
        data=transcript,
        file_name=uploaded_file.name.rsplit(".", 1)[0] + ".srt",
        mime="text/plain"
    )
