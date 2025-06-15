import streamlit as st
import speech_recognition as sr
import tempfile
import base64
import os
from gtts import gTTS
import pyttsx3
from pydub import AudioSegment

st.set_page_config(page_title="Text to Speech", layout="centered")
st.title("🗣️ Aplikasi Text-to-Speech Indonesia & Inggris")

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

mode = st.radio("Pilih Mode Input:", ["Ketik Teks", "Ucapkan Teks (Speech to Text)"])

if mode == "Ketik Teks":
    st.session_state.input_text = st.text_area("📝 Ketik teks yang ingin dibacakan:")
else:
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

if st.session_state.input_text.strip() != "":
    st.subheader("📄 Teks Akan Dibacakan:")
    st.info(st.session_state.input_text)

    voice_type = st.selectbox("🗣️ Pilih Suara:", ["Perempuan (Bahasa Indonesia)", "Laki-Laki (English)"])
    speed = st.selectbox("🎚️ Kecepatan Bicara:", ["Lambat", "Normal", "Cepat"])
    speed_map = {"Lambat": 125, "Normal": 175, "Cepat": 225}
    slow_gtts = True if speed == "Lambat" else False

    if st.button("🔁 Konversi ke Suara & Tampilkan"):
        try:
            if voice_type == "Perempuan (Bahasa Indonesia)":
                tts = gTTS(text=st.session_state.input_text, lang='id', slow=slow_gtts)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                    tts.save(f.name)
                    audio_path = f.name

                # Play preview (selalu normal karena gTTS tidak dukung "cepat")
                b64 = base64.b64encode(open(audio_path, "rb").read()).decode()
                st.markdown(f"""
                    <audio controls>
                        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                    </audio>
                """, unsafe_allow_html=True)

                # Siapkan file download
                download_path = audio_path
                if speed == "Cepat":
                    # Proses jadi lebih cepat (pitch/speed up)
                    sound = AudioSegment.from_file(audio_path)
                    faster = sound.speedup(playback_speed=1.4)
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f2:
                        faster.export(f2.name, format="mp3")
                        download_path = f2.name

                st.download_button("💾 Download Suara", open(download_path, "rb"), file_name="hasil_tts.mp3", mime="audio/mp3")

            elif voice_type == "Laki-Laki (English)":
                engine = pyttsx3.init()
                voices = engine.getProperty("voices")
                selected_voice = next((v for v in voices if "david" in v.name.lower() or "mark" in v.name.lower()), None)

                if selected_voice:
                    engine.setProperty("voice", selected_voice.id)
                engine.setProperty("rate", speed_map[speed])

                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                    audio_path = f.name

                engine.save_to_file(st.session_state.input_text, audio_path)
                engine.runAndWait()

                st.audio(open(audio_path, "rb").read(), format="audio/mp3")
                st.download_button("💾 Download Suara", open(audio_path, "rb"), file_name="hasil_tts.mp3", mime="audio/mp3")

        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

st.markdown("""
<hr style='border: 1px solid #ddd;'>
<div style="text-align: center; font-size: 18px; margin-top: 30px;">
    <p><strong>👥 Kelompok C14</strong></p>
    <p>👸🏻 <strong>152022018</strong> - Sadira Amalina F</p>
    <p>👨🏽‍🌾 <strong>152022087</strong> - Abhyasa Gunawan Y</p>
</div>
<hr style='border: 1px solid #ddd;'>
""", unsafe_allow_html=True)
