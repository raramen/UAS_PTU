import streamlit as st
from gtts import gTTS
import speech_recognition as sr
import tempfile
import base64

st.set_page_config(page_title="Text to Speech", layout="centered")
st.title("🗣️ Aplikasi Text-to-Speech Bahasa Indonesia")

# Inisialisasi session state
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# Pilih mode input
mode = st.radio("Pilih Mode Input:", ["Ketik Teks", "Ucapkan Teks (Speech to Text)"])

if mode == "Ketik Teks":
    st.session_state.input_text = st.text_area("📝 Ketik teks yang ingin dibacakan:")
elif mode == "Ucapkan Teks (Speech to Text)":
    st.info("Klik tombol di bawah dan izinkan mikrofon untuk mengucapkan teks.")
    if st.button("🎤 Rekam Sekarang"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("🎙️ Silakan bicara...")
            audio_data = recognizer.listen(source)
            st.write("⏳ Memproses...")
            try:
                detected_text = recognizer.recognize_google(audio_data, language="id-ID")
                st.session_state.input_text = detected_text
                st.success(f"Teks Terdeteksi: {detected_text}")
            except:
                st.error("❌ Tidak dapat mengenali suara. Coba lagi.")

# Jika ada teks yang siap dibacakan
if st.session_state.input_text.strip() != "":
    st.subheader("📄 Teks Akan Dibacakan:")
    st.info(st.session_state.input_text)

    # Pilihan bahasa/suara
    voice_option = st.selectbox("🗣️ Pilih Suara:", ["Bahasa Indonesia", "Bahasa Sunda", "English (US)", "India (Hindi)"])
    lang_map = {
        "Bahasa Indonesia": "id",
        "Bahasa Sunda": "su",
        "English (US)": "en",
        "India (Hindi)": "hi"
    }
    lang_code = lang_map[voice_option]

    # Pilihan kecepatan
    speed = st.selectbox("🎚️ Kecepatan Bicara:", ["Lambat", "Normal"])
    slow = True if speed == "Lambat" else False

    # Tombol konversi
    if st.button("🔁 Konversi ke Suara & Putar"):
        try:
            tts = gTTS(text=st.session_state.input_text, lang=lang_code, slow=slow)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                tts.save(f.name)
                b64 = base64.b64encode(open(f.name, "rb").read()).decode()
                audio_html = f"""
                    <audio autoplay>
                        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                    </audio>
                """
                st.markdown(audio_html, unsafe_allow_html=True)

                # Tombol unduh
                st.download_button("💾 Download Suara", open(f.name, "rb"), file_name="hasil_tts.mp3", mime="audio/mp3")
        except ValueError as e:
            st.error(f"Terjadi kesalahan: {e}")
