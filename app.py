import streamlit as st
from gtts import gTTS
import speech_recognition as sr
import tempfile
import base64

st.set_page_config(page_title="Text to Speech", layout="centered")
st.title("🗣️ Aplikasi Text-to-Speech Bahasa Indonesia")

# Pilih mode input
mode = st.radio("Pilih Mode Input:", ["Ketik Teks", "Ucapkan Teks (Speech to Text)"])

input_text = ""

if mode == "Ketik Teks":
    input_text = st.text_area("📝 Ketik teks yang ingin dibacakan:")
elif mode == "Ucapkan Teks (Speech to Text)":
    st.info("Klik tombol di bawah dan izinkan mikrofon untuk mengucapkan teks.")
    if st.button("🎤 Rekam Sekarang"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("🎙️ Silakan bicara...")
            audio_data = recognizer.listen(source)
            st.write("⏳ Memproses...")
            try:
                input_text = recognizer.recognize_google(audio_data, language="id-ID")
                st.success(f"Teks Terdeteksi: {input_text}")
            except:
                st.error("❌ Tidak dapat mengenali suara. Coba lagi.")

# Preview teks
if input_text.strip() != "":
    st.subheader("📄 Teks Akan Dibacakan:")
    st.info(input_text)

    # Pilih kecepatan bicara
    speed = st.selectbox("🎚️ Kecepatan Bicara:", ["Lambat", "Normal"])
    slow = True if speed == "Lambat" else False

    # Tombol konversi
    if st.button("🔁 Konversi ke Suara & Putar"):
        tts = gTTS(text=input_text, lang='id', slow=slow)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            tts.save(f.name)
            audio_bytes = f.read()
            b64 = base64.b64encode(open(f.name, "rb").read()).decode()
            audio_html = f"""
                <audio autoplay>
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
            """
            st.markdown(audio_html, unsafe_allow_html=True)

            # Download tombol
            st.download_button("💾 Download Suara", open(f.name, "rb"), file_name="hasil_tts.mp3", mime="audio/mp3")