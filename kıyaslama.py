import nltk
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
import re

# Model ve NLTK kurulumu
nltk.download('punkt')
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

metin = "Birlikte Üretiyor, Birlikte Dijitalleşiyoruz  Coşkunöz Holding ile mavi yaka çalışanlar için yürüttüğümüz yetkinlik ve eğitim yolculuğunun ardından, şimdi de beyaz yaka eğitim süreçlerini uçtan uca yönetecek LMS modülümüzü devreye alıyoruz.  Ulutek’teki ofisimizde bir araya gelerek son kontrollerimizi birlikte yaptık ve canlıya geçiş için geri sayıma başladık. Artık eğitim taleplerinin toplanmasından bütçelenmesine, planlamadan ölçümlemeye kadar tüm süreçler anlık ve bütünsel bir şekilde yönetilebilecek.  Bu sürecin en kıymetli yanı ise aynı hedefe inanan, birlikte düşünen ve birlikte üreten güçlü bir ekip ile çalışıyor olmak. Uyumları, enerjileri ve katkılarıyla süreci çok daha anlamlı hale getiren Coşkunöz Holding eğitim birimine gönülden teşekkür ederiz.  Teknolojinin gücüyle zaman kazandırmak ve süreçleri kolaylaştırmak en büyük motivasyonumuz 🚀"

text_list = [
    "beyaz yaka", "eğitim yönetimi", "yazılım devreye alma", 
    "insan kaynakları", "fabrika üretimi", "yapay zeka", "LMS"
]

def metin_temizle_soft(cumle):
    cumle = re.sub(r'http\S+', '', cumle)
    cumle = re.sub(r'[^\w\s.,!?]', ' ', cumle) 
    return re.sub(r'\s+', ' ', cumle).strip()

# 1. Hazırlık
cumleler = sent_tokenize(metin, language='turkish')
metinler_temiz = [metin_temizle_soft(c) for c in cumleler]

# 2. Embedding (Normalizasyon Aktif)
embedding_targets = model.encode(text_list, convert_to_tensor=True, normalize_embeddings=True)
embedding_sentences = model.encode(metinler_temiz, convert_to_tensor=True, normalize_embeddings=True)

# 3. Benzerlik Hesapla
similarity = model.similarity(embedding_targets, embedding_sentences)

# --- FİLTRELEME VE LİSTEYE ATMA BÖLÜMÜ ---
analiz_sonuclari = [] # Tüm başarılı eşleşmeleri burada toplayacağız

print(f"{'HEDEF':<20} | {'SKOR':<8} | {'EŞLEŞEN CÜMLE'}")
print("-" * 80)

for idx_i, target in enumerate(text_list):
    for idx_j, cumle in enumerate(metinler_temiz):
        skor = similarity[idx_i][idx_j].item() # Sayısal değeri al
        
        # %30 (0.30) Üzerindeki Skorları Yakala
        if skor >= 0.30:
            veri = {
                "hedef_kelime": target,
                "eslesen_cumle": cumle,
                "skor": round(skor, 4)
            }
            analiz_sonuclari.append(veri)
            print(f"{target:<20} | {skor:<8.4f} | {cumle[:50]}...")

# Final listesini kontrol et
print("\nFinal Listesi Eleman Sayısı:", len(analiz_sonuclari))