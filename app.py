import streamlit as st
from gtts import gTTS
import pyttsx3
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import base64
import os
import time
import pandas as pd

st.set_page_config(page_title="TTS Indonesia", layout="centered")
st.title("🗣️ Aplikasi Text-to-Speech dan Speech-to-Text")

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

# Jika ada teks
if st.session_state.input_text.strip() != "":
    st.subheader("📄 Teks Akan Dibacakan:")
    st.info(st.session_state.input_text)

    # Pilih sistem suara
    tts_system = st.radio("🎤 Pilih Sistem Suara:", ["gTTS (Perempuan - Online)", "pyttsx3 (Laki-laki - Offline)"])

    # Pilih kecepatan
    speed = st.selectbox("🎚️ Kecepatan Bicara:", ["Lambat", "Normal", "Cepat"])
    speed_map = {"Lambat": 125, "Normal": 175, "Cepat": 225}

    # Tombol proses
    if st.button("🔁 Konversi ke Suara & Putar"):
        start_time = time.time()

        if tts_system == "gTTS (Perempuan - Online)":
            slow_mode = True if speed == "Lambat" else False
            tts = gTTS(text=st.session_state.input_text, lang='id', slow=slow_mode)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                tts.save(f.name)
                original_path = f.name

            if speed == "Cepat":
                st.info("⚡ Memproses audio untuk mempercepat suara (post-processing)...")
                sound = AudioSegment.from_file(original_path)
                faster_sound = sound.speedup(playback_speed=1.3)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fast_file:
                    faster_sound.export(fast_file.name, format="mp3")
                    audio_path = fast_file.name
            else:
                audio_path = original_path

            # Evaluasi
            file_size_kb = os.path.getsize(audio_path) / 1024
            process_time = time.time() - start_time

            df = pd.DataFrame([{
                "Sistem": "gTTS (Online)",
                "Suara": "Perempuan",
                "Kecepatan": speed,
                "Waktu Proses (s)": round(process_time, 2),
                "Ukuran File (KB)": round(file_size_kb, 2),
                "Status": "✅"
            }])
            st.dataframe(df)

        else:  # pyttsx3 (offline)
            engine = pyttsx3.init()
            voices = engine.getProperty("voices")
            male_voice = None
            for v in voices:
                if 'male' in v.name.lower() or 'male' in str(v).lower():
                    male_voice = v.id
                    break
            if male_voice:
                engine.setProperty("voice", male_voice)
            else:
                st.warning("⚠️ Suara laki-laki tidak ditemukan, gunakan default.")
            engine.setProperty("rate", speed_map[speed])

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                temp_audio_path = f.name
            engine.save_to_file(st.session_state.input_text, temp_audio_path)
            engine.runAndWait()

            audio_path = temp_audio_path

            file_size_kb = os.path.getsize(audio_path) / 1024
            process_time = time.time() - start_time

            df = pd.DataFrame([{
                "Sistem": "pyttsx3 (Offline)",
                "Suara": "Laki-laki",
                "Kecepatan": speed,
                "Waktu Proses (s)": round(process_time, 2),
                "Ukuran File (KB)": round(file_size_kb, 2),
                "Status": "✅"
            }])
            st.dataframe(df)

        # Tampilkan dan unduh audio
        audio_bytes = open(audio_path, "rb").read()
        st.audio(audio_bytes, format="audio/mp3")
        st.download_button("💾 Download Suara", open(audio_path, "rb"), file_name="hasil_tts.mp3", mime="audio/mp3")

# Footer
st.markdown("""
<hr style='border: 1px solid #ddd;'>
<div style="text-align: center; font-size: 18px; margin-top: 30px;">
    <p><strong>👥 Kelompok C14</strong></p>
    <p>👸🏻 <strong>152022018</strong> - Sadira Amalina F</p>
    <p>👨🏽‍🌾 <strong>152022087</strong> - Abhyasa Gunawan Y</p>
</div>
<hr style='border: 1px solid #ddd;'>
""", unsafe_allow_html=True)
