from flask import Flask

app=Flask(__name__)

@app.route("/",methods=['POST','GET'])
def index():
    return "first ML project"

if __name__=="__main__":
    app.run(debug=True)