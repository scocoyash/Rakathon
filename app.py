from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import pickle
import operator
from operator import itemgetter
from indicoio.custom import Collection
import json
import requests
import base64

import indicoio
from indicoio.custom import Collection
indicoio.config.api_key = 'b1885d01b85e70a8f36452cbc4e66a6a'

app = Flask(__name__)
CORS(app)
path = os.getcwd()

myip = 'http://10.99.7.158:8000'

pants = {'label1': '1.jpg','label2': '2.jpg' , 'label3': '3.jpg',
'label4': '4.jpg', 'label5': '5.jpg', 'label6': '6.jpg', 'label': '7.jpg'}

pant_links = {
            '7.jpg': 'https://www.thesouledstore.com/product/solids-black-joggers',
              '6.jpg' : 'https://www.thesouledstore.com/product/solids-navy-blue-joggers',
              '3.jpg' : 'https://www.thesouledstore.com/product/superman-logo-joggers',
              '4.jpg' : 'https://www.thesouledstore.com/product/harry-potter-mischief-managed-joggers',
              '5.jpg' : 'https://www.thesouledstore.com/product/harry-potter-deathly-hallows-joggers',
              '1.jpg'  : 'https://www.amazon.com/Southpole-Active-Basic-Jogger-Fleece/dp/B00LGRZSSA?ref_=fsclp_pl_dp_1',
              '2.jpg' :  'https://www.amazon.com/Southpole-Fleece-Basic-Jogger-Colorblock/dp/B07719FGWN?ref_=fsclp_pl_dp_2',
             }

# Run inference
@app.route('/api/infer', methods=['POST'])
def infer():
    #print request.form.to_dict()
    person_img = request.form.to_dict()['person']
    clothing_url = request.form.to_dict()['clothing']
    #clothing_img = request.files['clothing']
    #print clothing_url
    #print person_img

    person_img = person_img[person_img.find(",")+1:]
    
    imgdata = base64.b64decode(person_img)
    filename = './inputs/input_person.jpg'
    with open(filename, 'wb') as f:
        f.write(imgdata)

    r = requests.get(clothing_url, allow_redirects=True)
    open('./inputs/input_clothing.jpg', 'wb').write(r.content)
    
    file = open('predict_matching', 'rb')
    collection = pickle.load(file)
    file.close()
    sort_key = itemgetter(1)
    recomm_tuple = sorted(collection.predict('./inputs/input_clothing.jpg').items(), key=sort_key)
    recomm_tuple = recomm_tuple[-3:]
    d_keys = [str(item) for item in dict(recomm_tuple).keys()]
    #print(d_keys)

    # return url of recommended pants
    result_pants = []
    for key in d_keys:
        pants_recomm_path = myip + '/matching_clothes/training_pants/'
        file_path_list = pants_recomm_path + pants[key]
        d = dict()
        d['image_link'] = file_path_list
        d['store_link'] = pant_links[pants[key]]
        result_pants.append(d)

    os.system('./run_smartfit.sh ./inputs/input_person.jpg ./inputs/input_clothing.jpg')

    # Check that files exists (i.e. smartfit didn't crash)
    if not os.path.isfile('output/output.png'):
        return jsonify(error = '500: Internal server error')

    output_path = myip + '/output/output.png'
    response = dict()
    response['output'] = output_path
    response['recommendations'] = result_pants
    print response
    return jsonify(response)


if __name__ == '__main__':
   app.run('0.0.0.0', ssl_context=('cert.pem', 'key.pem'))
