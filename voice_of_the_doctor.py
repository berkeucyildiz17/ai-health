# Step1a: Setup Text to Speech–TTS–model with gTTS
import os  # Çevresel değişkenlere erişmek için os modülü içe aktarılıyor.
from gtts import gTTS  # Google Text-to-Speech (gTTS) kütüphanesi, metni sese dönüştürmek için içe aktarılıyor.

def text_to_speech_with_gtts_old(input_text, output_filepath):  # Eski bir TTS fonksiyonu tanımlanıyor.
    language = "tr"  # Dil Türkçe olarak ayarlanıyor.

    audioobj = gTTS(  # gTTS nesnesi oluşturuluyor.
        text=input_text,  # Sese dönüştürülecek metin.
        lang=language,  # Dil bilgisi.
        slow=False  # Sesin hızlı bir şekilde okunması sağlanıyor.
    )
    audioobj.save(output_filepath)  # Oluşturulan ses dosyası belirtilen dosya yoluna kaydediliyor.

input_text = "Hi this is Ai with Hassan!"  # Örnek bir metin tanımlanıyor.
text_to_speech_with_gtts_old(input_text=input_text, output_filepath="gtts_testing.mp3")  # Eski TTS fonksiyonu çağrılıyor.

# Step2: Use Model for Text output to Voice
import subprocess  # Harici komutları çalıştırmak için subprocess modülü içe aktarılıyor.
import platform  # İşletim sistemi bilgilerini almak için platform modülü içe aktarılıyor.

def text_to_speech_with_gtts(input_text, output_filepath):  # Yeni bir TTS fonksiyonu tanımlanıyor.
    language = "tr"  # Dil Türkçe olarak ayarlanıyor.

    audioobj = gTTS(  # gTTS nesnesi oluşturuluyor.
        text=input_text,  # Sese dönüştürülecek metin.
        lang=language,  # Dil bilgisi.
        slow=False  # Sesin hızlı bir şekilde okunması sağlanıyor.
    )
    audioobj.save(output_filepath)  # Oluşturulan ses dosyası belirtilen dosya yoluna kaydediliyor.

    os_name = platform.system()  # İşletim sistemi bilgisi alınıyor.
    try:
        if os_name == "Darwin":  # Eğer işletim sistemi macOS ise:
            subprocess.run(['afplay', output_filepath])  # macOS için ses dosyası çalınıyor.
        elif os_name == "Windows":  # Eğer işletim sistemi Windows ise:
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])  # Windows için ses dosyası çalınıyor.
        elif os_name == "Linux":  # Eğer işletim sistemi Linux ise:
            subprocess.run(['aplay', output_filepath])  # Linux için ses dosyası çalınıyor. Alternatif: 'mpg123' veya 'ffplay' kullanılabilir.
        else:
            raise OSError("Unsupported operating system")  # Desteklenmeyen bir işletim sistemi durumunda hata fırlatılıyor.
    except Exception as e:  # Eğer bir hata oluşursa:
        print(f"An error occurred while trying to play the audio: {e}")  # Hata mesajı yazdırılıyor.

input_text = "Merhaba Ben Berke, Nasılsın?"  # Örnek bir metin tanımlanıyor.
text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing_autoplay.mp3")  # Yeni TTS fonksiyonu çağrılıyor.