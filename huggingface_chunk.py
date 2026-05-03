from groq import Groq
import json


api_key = "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"
post_metni = "Birlikte Üretiyor, Birlikte Dijitalleşiyoruz\
Coşkunöz Holding ile mavi yaka çalışanlar için yürüttüğümüz yetkinlik ve eğitim yolculuğunun ardından, şimdi de beyaz yaka eğitim süreçlerini uçtan uca yönetecek LMS modülümüzü devreye alıyoruz.\
Ulutek’teki ofisimizde bir araya gelerek son kontrollerimizi birlikte yaptık ve canlıya geçiş için geri sayıma başladık. Artık eğitim taleplerinin toplanmasından bütçelenmesine, planlamadan ölçümlemeye kadar tüm süreçler anlık ve bütünsel bir şekilde yönetilebilecek.\
Bu sürecin en kıymetli yanı ise aynı hedefe inanan, birlikte düşünen ve birlikte üreten güçlü bir ekip ile çalışıyor olmak. Uyumları, enerjileri ve katkılarıyla süreci çok daha anlamlı hale getiren Coşkunöz Holding eğitim birimine gönülden teşekkür ederiz.\
Teknolojinin gücüyle zaman kazandırmak ve süreçleri kolaylaştırmak en büyük motivasyonumuz 🚀"

def Iliskilipost(post,anahtar_kelimeler) :
    client =Groq(api_key=api_key)
    completion =client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
           {
    "role": "system",
    "content": """Sen bir içerik analiz asistanısın.
     Sana bir LinkedIn postu ve anahtar kelime listesi verilecek.

     Görevin:
     1. Her anahtar kelimeyi tek tek incele
     2. Kelime birebir geçmese bile ANLAMSAL olarak alakalıysa eşleşmiş say
     (örnek: "yazılım" kelimesi için "kod", "uygulama", "sistem" da eşleşir)
     3. Eşleşen en az 1 kelime varsa "alakali": true yaz
     4. Skoru şöyle hesapla: eşleşen kelime sayısı / toplam kelime sayısı
     5. Sadece JSON döndür, başka hiçbir şey yazma"""
    },
     {
     "role": "user",
     "content": f"""Post: {post}

     Anahtar Kelimeler: {anahtar_kelimeler}

     Şu formatta cevap ver:
     {{
      "alakali": true/false,
      "skor": 0.0-1.0,
      "neden": "kısa açıklama",
      "eslesenler": ["kelime1", "kelime2"]
     }}"""
     }
        ],
        temperature=0.1, #modeli deterministlik oranı belirleniyor yani 0 olması durumunda değişkenlik hiç göstermez
        max_completion_tokens=1024,
        stream=False,
    )
    
    content = completion.choices[0].message.content
    print(completion.usage.total_tokens)
    return (json.loads(content) ,completion)

# Kullanım
sonuc,hamsonuc= Iliskilipost(
    post=post_metni,
    anahtar_kelimeler = [
    "eğitim teknolojisi",
    "dijitalleşme",
    "kurumsal yazılım",
    "mikrodenetleyici",
    "yapay zeka"
]
)

print("gelen ham sonuclar : ",hamsonuc)
print("Ayıklanmıs veri : ",sonuc)

