# Step1: Setup Audio recorder (ffmpeg & portaudio)
# ffmpeg, portaudio, pyaudio
import logging  # Hata ve bilgi mesajlarını kaydetmek için logging modülü içe aktarılıyor.
import speech_recognition as sr  # Mikrofonla ses kaydı almak için SpeechRecognition kütüphanesi içe aktarılıyor.
from pydub import AudioSegment  # Ses dosyalarını işlemek için pydub kütüphanesi içe aktarılıyor.
from io import BytesIO  # Bellekteki bayt verilerini işlemek için BytesIO sınıfı içe aktarılıyor.

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')  # Logging yapılandırması ayarlanıyor.

def record_audio(file_path, timeout=20, phrase_time_limit=None):  # Mikrofonla ses kaydı almak için bir fonksiyon tanımlanıyor.
    """
    Simplified function to record audio from the microphone and save it as an MP3 file.

    Args:
    file_path (str): Path to save the recorded audio file.
    timeout (int): Maximum time to wait for a phrase to start (in seconds).
    phrase_time_limit (int): Maximum time for the phrase to be recorded (in seconds).
    """
    recognizer = sr.Recognizer()  # SpeechRecognition sınıfından bir tanıyıcı nesnesi oluşturuluyor.
    
    try:
        with sr.Microphone() as source:  # Mikrofon kaynağı açılıyor.
            logging.info("Adjusting for ambient noise...")  # Ortam gürültüsüne göre ayarlama yapılıyor.
            recognizer.adjust_for_ambient_noise(source, duration=1)  # Gürültü ayarı için 1 saniye bekleniyor.
            logging.info("Start speaking now...")  # Kullanıcıya konuşmaya başlaması için bilgi veriliyor.
            
            # Record the audio
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)  # Mikrofonla ses kaydı alınıyor.
            logging.info("Recording complete.")  # Kayıt işleminin tamamlandığı bilgisi veriliyor.
            
            # Convert the recorded audio to an MP3 file
            wav_data = audio_data.get_wav_data()  # Kaydedilen ses WAV formatında alınıyor.
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))  # WAV formatındaki ses, pydub ile işleniyor.
            audio_segment.export(file_path, format="mp3", bitrate="128k")  # Ses MP3 formatında belirtilen dosya yoluna kaydediliyor.
            
            logging.info(f"Audio saved to {file_path}")  # Ses dosyasının kaydedildiği bilgisi veriliyor.

    except Exception as e:  # Eğer bir hata oluşursa:
        logging.error(f"An error occurred: {e}")  # Hata mesajı kaydediliyor.

audio_filepath = "patient_voice_test_for_patient.mp3"  # Ses dosyasının kaydedileceği dosya yolu tanımlanıyor.
# record_audio(file_path=audio_filepath)  # Ses kaydı fonksiyonu çağrılıyor (şu anda yorum satırı olarak bırakılmış).

# Step2: Setup Speech to text–STT–model for transcription
import os  # Çevresel değişkenlere erişmek için os modülü içe aktarılıyor.
from groq import Groq  # GROQ API'sini kullanmak için Groq kütüphanesi içe aktarılıyor.

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")  # Çevresel değişkenlerden GROQ API anahtarı alınıyor.
stt_model = "whisper-large-v3"  # Sesten metne dönüştürme modeli olarak "whisper-large-v3" seçiliyor.

def transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY):  # Ses dosyasını metne dönüştürmek için bir fonksiyon tanımlanıyor.
    client = Groq(api_key=GROQ_API_KEY)  # GROQ API istemcisi oluşturuluyor.
    
    audio_file = open(audio_filepath, "rb")  # Ses dosyası okunmak üzere açılıyor.
    transcription = client.audio.transcriptions.create(  # GROQ API'si üzerinden bir transkripsiyon isteği oluşturuluyor.
        model=stt_model,  # Kullanılacak model belirtiliyor.
        file=audio_file,  # Ses dosyası API'ye gönderiliyor.
        language="tr"  # Dil Türkçe olarak ayarlanıyor.
    )

    return transcription.text  # API'den dönen metin çıktısı döndürülüyor.
