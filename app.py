from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)

@app.route('/',methods=['GET'])
@cross_origin()
def home_page():
    return render_template("index.html")

@app.route('/productreview',methods=['POST','GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace("","")
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            uClient = uReq(flipkart_url)
            flipkartPage = uClient.read()
            uClient.close()
            flipkart_html = bs(flipkartPage, "html.parser")
            bigboxes = flipkart_html.findAll("div",{"class" : "_1AtVbE col-12-12"})
            del bigboxes[0:3]
            box = bigboxes[0]
            productLink = "https://www.flipkart.com" + box.div.div.div.a['href']
            prodRes = requests.get(productLink)
            prodRes.encoding = 'utf-8'
            prod_html = bs(prodRes.text, "html.parser")
            # print(prod_html)
            commentboxes = prod_html.find_all('div', {'class': "_16PBlm"})

            review_list = []
            for comment in commentboxes:
                try:
                    name = comment.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text
                except:
                    name = "No Name"

                try:
                    rating = comment.div.div.div.div.text
                except:
                    rating = "No rating"

                try:
                    commentHead = comment.div.div.div.p.text
                except:
                    commentHead = "No Comment Heading"

                try:
                    comtag = comment.div.div.find_all('div', {'class': ''})
                    cusComment = comtag[0].div.text
                except:
                    comtag = "No Comment Tag"

                myDict = {"Product":searchString, "Name":name, "Rating":rating, "CommentHead":commentHead, "Comments":cusComment}
                review_list.append(myDict)
            return render_template('results.html',review_list = review_list[0:len(review_list) - 1])

        except Exception as e:
            print(e)

    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)







