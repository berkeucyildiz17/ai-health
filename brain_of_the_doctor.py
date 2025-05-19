# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv  # Çevresel değişkenleri yüklemek için dotenv kütüphanesi içe aktarılıyor.
# load_dotenv()  # .env dosyasındaki çevresel değişkenler yükleniyor.

# Step1: Setup GROQ API key
import os  # Çevresel değişkenlere erişmek için os modülü içe aktarılıyor.

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")  # Çevresel değişkenlerden GROQ API anahtarı alınıyor.

# Step2: Convert image to required format
import base64  # Görselleri Base64 formatına dönüştürmek için base64 kütüphanesi içe aktarılıyor.

# image_path="acne.jpg"  # Örnek bir görsel yolu (kullanılmıyor).

def encode_image(image_path):  # Görselleri Base64 formatına dönüştürmek için bir fonksiyon tanımlanıyor.
    image_file = open(image_path, "rb")  # Görsel dosyası okunmak üzere açılıyor.
    return base64.b64encode(image_file.read()).decode('utf-8')  # Görsel Base64 formatına dönüştürülüp döndürülüyor.

# Step3: Setup Multimodal LLM
from groq import Groq  # GROQ API'sini kullanmak için Groq kütüphanesi içe aktarılıyor.

query = "Yüzümde bir sorun mu var?"  # Görsel analizi için kullanılacak örnek bir sorgu tanımlanıyor.
model = "meta-llama/llama-4-scout-17b-16e-instruct"  # Görsel analizi için kullanılacak model belirtiliyor.
# model="llama-3.2-90b-vision-preview" #Deprecated  # Eski bir model (kullanılmıyor).

def analyze_image_with_query(query, model, encoded_image):  # Görsel ve sorguyu analiz etmek için bir fonksiyon tanımlanıyor.
    client = Groq()  # GROQ API istemcisi oluşturuluyor.
    messages = [  # API'ye gönderilecek mesajlar tanımlanıyor.
        {
            "role": "user",  # Mesajın kullanıcı tarafından gönderildiği belirtiliyor.
            "content": [  # Mesaj içeriği tanımlanıyor.
                {
                    "type": "text",  # Mesajın bir metin olduğu belirtiliyor.
                    "text": query  # Kullanıcının sorgusu mesaj olarak ekleniyor.
                },
                {
                    "type": "image_url",  # Mesajın bir görsel içerdiği belirtiliyor.
                    "image_url": {  # Görselin Base64 formatındaki URL'si tanımlanıyor.
                        "url": f"data:image/jpeg;base64,{encoded_image}",  # Görsel Base64 formatında API'ye gönderiliyor.
                    },
                },
            ],
        }]
    chat_completion = client.chat.completions.create(  # GROQ API'si üzerinden bir sohbet tamamlama isteği oluşturuluyor.
        messages=messages,  # Mesajlar API'ye gönderiliyor.
        model=model  # Kullanılacak model belirtiliyor.
    )

    return chat_completion.choices[0].message.content  # API'den dönen yanıtın içeriği döndürülüyor.
