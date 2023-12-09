from flask import Flask
from housing.logger import logging

app=Flask(__name__)

@app.route("/",methods=['POST','GET'])
def index():
    logging.info("We are testing logging module")
    return "first ML project"

if __name__=="__main__":
    app.run(debug=True) 