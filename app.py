from flask import Flask, request, jsonify
from flask_cors import CORS # Arayüz ve Backend çakışmasın diye gerekli
from src.company_follower import getfollowers 
from src.data_processor import get_company_id_by_name
import time 

app = Flask(__name__)
CORS(app) # Frontend'den gelen istekleri engellememesi için

@app.route('/', methods=['GET'])
def Home():

    return "Sunucuya Çikarma islemi basarili"


@app.route('/scrape' , methods = ['GET'])
def scrape () :
 scraper_type = request.args.get('scraperType')
 company_url = request.args.get('companyUrl') 
 companyUniversalName = company_url.strip("/ ").split("/company/")[-1].split("/")[0]


 if scraper_type == '1' :
    try :
      company_id= get_company_id_by_name (companyUniversalName)
      followerNumber = int(request.args.get('followerNumber', 10))
      followers = getfollowers(company_id,followerNumber,time.time())
      return followers
    
    except Exception as e : 
       return("Follower Error ",e)




if __name__ == '__main__':
    # debug=True sayesinde kodda hata yaparsan sunucu kapanmaz, hatayı söyler
    app.run(host='0.0.0.0', port=5000, debug=True)