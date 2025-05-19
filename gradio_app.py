from dotenv import load_dotenv  # Çevresel değişkenleri yüklemek için dotenv kütüphanesi içe aktarılıyor.
load_dotenv()  # .env dosyasındaki çevresel değişkenler yükleniyor.

import os  # Çevresel değişkenlere erişmek için os modülü içe aktarılıyor.
import gradio as gr  # Gradio kütüphanesi, kullanıcı arayüzü oluşturmak için içe aktarılıyor.

from brain_of_the_doctor import encode_image, analyze_image_with_query  # Görsel işleme ve analiz işlevleri içe aktarılıyor.
from voice_of_the_patient import record_audio, transcribe_with_groq  # Ses kaydı ve sesten metne dönüştürme işlevleri içe aktarılıyor.
from voice_of_the_doctor import text_to_speech_with_gtts  # Metni sese dönüştürme işlevi içe aktarılıyor.

load_dotenv()  # Çevresel değişkenler tekrar yükleniyor.

system_prompt="""Profesyonel bir doktor gibi davranmanı istiyorum, biliyorum gerçek bir doktor değilsin ama bu öğrenme amaçlı.
Bu görselde ne var? Tıbbi açıdan yanlış bir şey buluyor musun?
Bir ayırıcı tanı yaparsan, buna yönelik bazı çözümler de öner.
Yanıtında sayı veya özel karakter kullanma.
Yanıtın tek bir uzun paragraf olmalı.
Yanıt verirken gerçek bir kişiye konuşuyormuşsun gibi cevap ver.
'Bu görselde şunu görüyorum' gibi cümleler kullanma, onun yerine 'Gördüklerime göre sende .... olduğunu düşünüyorum' gibi konuş.
Markdown formatında yazma, bir yapay zekâ gibi değil gerçek bir doktor gibi cevap ver.
Yanıtın kısa olsun (maksimum iki cümle).
Giriş cümlesi kullanmadan doğrudan cevaba başla. """  # Yapay zekâ modeline verilecek sistem komutları tanımlanıyor.

def process_inputs(audio_filepath, image_filepath):  # Kullanıcıdan alınan ses ve görsel girdileri işlemek için bir fonksiyon tanımlanıyor.
    speech_to_text_output = transcribe_with_groq(  # Sesli girdiyi metne dönüştürmek için transcribe_with_groq fonksiyonu çağrılıyor.
        GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),  # Çevresel değişkenlerden alınan API anahtarı kullanılıyor.
        audio_filepath=audio_filepath,  # Ses dosyasının yolu fonksiyona iletiliyor.
        stt_model="whisper-large-v3"  # Sesten metne dönüştürme modeli olarak "whisper-large-v3" kullanılıyor.
    )

    if image_filepath:  # Eğer kullanıcı bir görsel girdisi sağladıysa:
        doctor_response = analyze_image_with_query(  # Görsel ve sesli girdiden elde edilen metin analiz ediliyor.
            query=system_prompt + speech_to_text_output,  # Sistem komutu ve metin birleştirilerek sorgu oluşturuluyor.
            encoded_image=encode_image(image_filepath),  # Görsel encode_image fonksiyonu ile kodlanıyor.
            model="meta-llama/llama-4-scout-17b-16e-instruct"  # Görsel analizi için kullanılan model belirtiliyor.
        )
    else:  # Eğer kullanıcı bir görsel sağlamadıysa:
        doctor_response = "Analiz edebilmem için bana hiçbir görüntü sağlanmadı"  # Kullanıcıya bir hata mesajı döndürülüyor.

    voice_of_doctor = text_to_speech_with_gtts(  # Doktorun yanıtı sese dönüştürülüyor.
        input_text=doctor_response,  # Sese dönüştürülecek metin olarak doktorun yanıtı kullanılıyor.
        output_filepath="final.mp3"  # Ses dosyası "final.mp3" olarak kaydediliyor.
    )

    return speech_to_text_output, doctor_response, voice_of_doctor  # Fonksiyon, metin çıktısını, doktorun yanıtını ve ses dosyasını döndürüyor.

iface = gr.Interface(  # Gradio arayüzü oluşturuluyor.
    fn=process_inputs,  # Kullanıcı girdilerini işlemek için process_inputs fonksiyonu kullanılıyor.
    inputs=[  # Kullanıcıdan alınacak girdiler tanımlanıyor.
        gr.Audio(sources=["microphone"], type="filepath"),  # Mikrofon kaynağından ses girdisi alınacak.
        gr.Image(type="filepath")  # Görsel girdisi dosya yolu olarak alınacak.
    ],
    outputs=[  # Kullanıcıya gösterilecek çıktılar tanımlanıyor.
        gr.Textbox(label="Speech to Text"),  # Sesten metne dönüştürme çıktısı bir metin kutusunda gösterilecek.
        gr.Textbox(label="Doktorun Yanıtı"),  # Doktorun yanıtı bir metin kutusunda gösterilecek.
        gr.Audio("Temp.mp3")  # Sesli yanıt bir ses oynatıcıda gösterilecek.
    ],
    title="AI Doctor with Vision and Voice - Berke Üçyıldız"  # Arayüz başlığı tanımlanıyor.
)

iface.launch(debug=True, share=True)  # Gradio arayüzü başlatılıyor ve hata ayıklama modu etkinleştiriliyor.

#http://127.0.0.1:7860  # Yerel sunucunun çalıştığı URL belirtiliyor.