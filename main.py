from src.post_likers import getLikersList 
from src.company_follower import getfollowers  
import time 
import requests
from src.Telegrambot import send_to_telegram,NotificationCompanyPost
import pandas as pd
from src.Likers_memory  import get_sent_history ,save_to_history
from src.Pageinfo import Get_post_urn,Get_member_post_urn
from src.data_processor import get_company_id_by_name
from src.analyz import hashtagbul,Textbul
from sentence_transformers import SentenceTransformer
import nltk




class LinkedinOtomation () :
 def __init__(self,bot_token,chat_id,company_id,model,nltk,profile_urls = any):
        self.bot_id=bot_token 
        self.chat_id=chat_id
        self.company_id=company_id
        self.admin_urls=profile_urls
        self.model =model
        self.nltk = nltk


 def Postlikers(self):
       print("Beğenenleri kazıma işlemi başlıyor...")
       zaman_damgasi = time.time() # anlık zamanı alalım Unix timestamp formatında

       try:
         post_urn = Get_post_urn(self.company_id) 
         print("Post_urn alabildik mi ",post_urn)   
         #deneme_urn = 'urn:li:activity:7446876543873683456'
         likers = getLikersList(post_urn, zaman_damgasi)
         print("Beğenenler listesi: " )
         print(likers)
         if not likers:
            print("Veri çekilemedi. Çerezleri veya Post ID'yi kontrol et.")
            return # Veri yoksa devam etme

         print(f"Likers değişkeni ile gelen veriler: {len(likers)} adet.")
         df = pd.DataFrame(data=likers) 

         # 1. Adminleri temizle
         df_filtered = df[~df['profileUrl'].isin(self.admin_urls)].copy()
        
         # 2. Daha önce gönderilenleri hafızadan al (get_sent_history fonksiyonun import edilmiş olmalı)
         sent_notification = get_sent_history()
        
         # 3. Sadece yeni olanlar
         df_new_people = df_filtered[~df_filtered['profileUrl'].isin(sent_notification)].copy()

         if not df_new_people.empty:
            print(f"Yeni {len(df_new_people)} profil tespit edildi.")

            # İlk 5 kişiyi al ve sözlüğe çevir
            ilk_bes_beğenme_listesi = df_new_people.head(5).to_dict('records')

            print(f"Telegram'a gönderiliyor...")
            send_to_telegram(ilk_bes_beğenme_listesi, bot_token, chat_id)

            # Geçmişe kaydet
            for person in ilk_bes_beğenme_listesi:
                save_to_history(person['profileUrl'])
                print(f"Kaydedildi: {person['fullName']}")
         else:
            print("Bildirim gönderilecek yeni bir kişi bulunamadı.")

       except Exception as e:
         print("Çalıştırma Sırasında Hata Oluştu:", e)

 def CompanyFollowers () : 
      try:
        times = time.time()
        followers = getfollowers(company_id, 3, times)

        print("\n--- ÇEKİLEN TAKİPÇİ LİSTESİ ---")
        if followers:
            for index, kisi in enumerate(followers, 1):
                print(f"{index}. İsim: {kisi.get('fullName')} | Ünvan: {kisi.get('jobTitle')}")
                print(f"   Profil: {kisi.get('profileUrl')}")
                print("-" * 30)
            # Eğer takipçileri Telegram'a göndermek İSTEMİYORSAN buraya send_to_telegram ekleme.
        else:
            print("Hiç takipçi verisi çekilemedi.")

      except Exception as e:
        print("Şirket Takipçilerini çekerken bir hata oluştu:", e) 




 def CompanyPipeline (self,text_list,sirketler,hashtag_list) :
    company_id_universal = get_company_id_by_name(sirketler) #universalname ve company id parametrelerini dizi formatında döner bize  
    print("Company datas: ",company_id_universal)

    for companyiduniversal in company_id_universal :
         currentid = companyiduniversal.get('companyid')
         currentname = companyiduniversal.get('universalname')
         posts = Get_member_post_urn(currentid) #Burada verilen şirket id si ile detaylı post analizi (post_urn, text_snippet,hashtag,metrics) verir.
         flag = 0
         for post in posts : 
             posthashtag = post.get('hashtags')
             posthashtag = None
             print( "şu an posthashtags ve text_snippet: ",posthashtag , post.get('text_snippet'))
             #print("postlar :",post) postlar geliyor sorun yok
             if posthashtag :
                 hashtag_analiz = hashtagbul(post,hashtag_list,self.model) #burada post_link ,linkedin_link ve eslesen_kelimeler parametreleri döner.
                 print("Hashtag analiz sonucu : ",hashtag_analiz)
                 if hashtag_analiz :
                     NotificationCompanyPost(hashtag_analiz,self.bot_id,self.chat_id,currentname,flag) 
                     print("currentname: ",currentname)   
          
             elif  post.get('text_snippet') :
                 print("2. elife girdim") 
                 flag=1
                 try :
                     text_analiz = Textbul(post ,text_list,self.model,self.nltk) #hashtagbul fonksiyonu ile aynı parametreler dönmektedir
                     print("Textbul dan  dönen sonuçlar:  ",text_analiz)
                     if text_analiz : 
                         NotificationCompanyPost(text_analiz,self.bot_id,self.chat_id,currentname,flag=1)
                 except Exception as e :
                    print("gelmedi : ", e)

             #NotificationCompanyPost(text_analiz,self.bot_id,self.chat_id,currentname,flag)   

        

bot_token="8786816515:AAH-8OBPkvW3jL2mbtU4Inpe-ZUEH74diFA"
chat_id="7567279308"
company_id = '112230400'


'''
admins = Get_admin_urn(company_id)
print("gelen adminler: ",admins)

#admin linki ekleyerek beğenen kişinin şirketina admini olsa bile engellensin 
base_url = "https://www.linkedin.com/in/"
profile_urls =[]
# Her bir ID'yi url'nin yanına koy ve yeni bir liste yap
if admins : 
   profile_urls = [f"{base_url}{pid}/" for pid in admins if pid]
   print(profile_urls)'''

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
nltk.download('punkt')
obje = LinkedinOtomation (bot_token,chat_id,company_id,model,nltk,profile_urls=any)
#url = input("Şirketin url adresini giriniz: ")

#test = obje.pipeline(url)
# TEST
hash_tag_list =["maviyaka",'İK',"yetkinlik modeli", "isg", "bulut","competncy","lms"]
text_list = ["Mavi Yaka", "İnsan kaynakları","yetkinlik modeli", "isg", "bulut","competncy","dijital dönüşüm","yapay zekâ"]
sirketler = ["talent-astra"] #burada tek bir şirket göndersen bile liste [] parametereleri ile gönderilmeli yoksa fonksiyonda karakter karakter gezmeye çalışır.
obje.CompanyPipeline(text_list,sirketler,hash_tag_list)



