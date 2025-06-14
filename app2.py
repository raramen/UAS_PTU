import streamlit as st
from TTS.api import TTS
import os

# Inisialisasi model Bahasa Indonesia
@st.cache_resource
def load_tts_model():
    return TTS(model_name="tts_models/id/css10/vits", progress_bar=False, gpu=False)

tts = load_tts_model()

# Tampilan Streamlit
st.set_page_config(page_title="Text-to-Speech Indonesia", layout="centered")
st.title("🗣️ Aplikasi Text-to-Speech Bahasa Indonesia")

st.markdown("Masukkan teks berbahasa Indonesia dan konversikan menjadi suara secara natural.")

# Input teks
text_input = st.text_area("Tulis teks di bawah ini:", height=150)

# Pilihan kecepatan bicara
speed = st.selectbox("Pilih kecepatan bicara:", ["Lambat", "Normal", "Cepat"])

# Konversi ke angka
speed_map = {
    "Lambat": 0.5,
    "Normal": 1.0,
    "Cepat": 1.5
}
selected_speed = speed_map[speed]

# Pilihan gender suara
gender = st.selectbox("Pilih gender suara (opsional):", ["Perempuan (default)"])

# Tombol proses
if st.button("🔊 Konversi Teks ke Suara"):
    if text_input.strip() == "":
        st.warning("Silakan masukkan teks terlebih dahulu.")
    else:
        # Proses TTS
        output_path = "output/result.mp3"
        os.makedirs("output", exist_ok=True)

        # Konversi dan simpan file audio
        tts.tts_to_file(text=text_input, file_path=output_path, speaker_wav=None, speed=selected_speed)

        # Tampilkan audio
        audio_file = open(output_path, "rb")
        audio_bytes = audio_file.read()

        st.audio(audio_bytes, format="audio/mp3")
        st.success("Konversi selesai! Suara berhasil diputar.")
        st.download_button(label="📥 Download Suara (.mp3)", data=audio_bytes, file_name="tts_output.mp3", mime="audio/mp3")