import streamlit as st
from pydub import AudioSegment
from io import BytesIO
from dotenv import dotenv_values
from openai import OpenAI

AUDIO_TRANSCRIBE_MODEL = "whisper-1"

#
# TITLE
#

st.set_page_config(page_title="GenNapAI", page_icon="🎬", layout="wide")

st.title("🎬 GenNapAI ver. 0.5")    
st.markdown("*Proste narzędzie AI do generowania napisów!*")

#
# SIDEBAR
#

with st.sidebar:


    st.header("ℹ️ Informacje o aplikacji")

    st.divider()

    st.info("👷 **Używany model AI:** OpenAI Whisper-1") # zmień ikonkrę

    st.divider()

    # Instrukcja obsługi aplikacji
    with st.expander("📖 **Instrukcja obsługi**"):
        st.markdown("""
    1. Wprowadź poniżej w formularzu swój klucz OpenAI.
    2. Wybierz plik wideo.  
    3. Wygeneruje się film oraz ścieżka audio. Odtwórz je, by sprawdzić czy działają.  
    4. W międzyczasie generują się automatycznie napisy.  
    5. Edytuj napisy jeśli trzeba.  
    6. Zapisz napisy z poprawkami czy bez.
    7. Pobierz na dysk w formacie `.srt`.
    """)
            
    st.divider()

    # Wprowadzenie klucza OpenAI z obsługą wyjątków

    openai_key = st.text_input("🔑 Wprowadź swój klucz OpenAI", placeholder="sk-proj-...", type="password")
    if not openai_key:
        st.warning("🔑 Podaj klucz OpenAI, aby kontynuować.")

        with st.expander("📖 Nie posiadasz klucza?"):
            st.markdown("""
        1. Wejdź na [platform.openai.com](https://platform.openai.com/)
        2. Stwórz konto lub zaloguj się
        3. Przejdź do **API Keys** w menu
        4. Kliknij **Create new secret key**
        5. Skopiuj klucz i wklej go tutaj w polu klucza
        """)
        st.stop()

    try:
        openai_client = OpenAI(api_key=openai_key)

    # Testowe wywołanie API - lista modeli służy do weryfikacji klucza

        openai_client.models.list()
        st.success("✅ Klucz API zaakceptowany.")
    except Exception as e:
        st.error(f"❌ Nieprawidłowy klucz OpenAI lub błąd połączenia:\n{e}")
       
        st.stop()

#
# MAIN
#

# Ładowanie pliku video

st.markdown("📹 Wybierz plik wideo")
uploaded_files = st.file_uploader(
    "📺 Wybierz pliki wideo do 200 MB", accept_multiple_files=True, type=["mp4", "mov", "avi", "mkv"]
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

    spinner = st.spinner("Trwa generowanie napisów...")
    with spinner: 

        transcript = openai_client.audio.transcriptions.create(
            file=audio_buffer,
            model=AUDIO_TRANSCRIBE_MODEL,
            response_format="srt"
        )
        
        # Wyświetl pole tekstowe z napisami do edycji
        subtitles= st.text_area(
            label=f"📝 Sprawdź i popraw napisy dla: {uploaded_file.name}",
            value=transcript,
            height=300
        ) 
        save_button = st.button("💾 Zapisz napisy")

        if save_button:
            transcript = subtitles
            
            st.download_button(
                label="⬇️ Pobierz napisy",
                data=transcript,
                file_name=uploaded_file.name.rsplit(".", 1)[0] + ".srt",
            )

