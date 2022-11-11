from flask import Flask

app = Flask(__name__)

@app.route('/') 
def test_message(): 
   return '<h1>Sup2</h1>'

if __name__ == "__main__": 
   app.run(debug=True, host='0.0.0.0', port=8000)
