from flask import Flask, render_template, request 
#pip install flask pandas contextily geopandas matplotlib
app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    return render_template("search.html") #serve per restituire una stringa

@app.route('/result', methods=['GET'])
def result():
# Collegamento al database
    import pandas as pd
    import pymssql
    conn = pymssql.connect(server = '213.140.22.237\SQLEXPRESS',user = 'dilecce.gabriele',password = 'xxx123##',database = 'dilecce.gabriele')
    # Invio query al database e ricezione informazioni
    nomeprodotto = request.args['nomeprodotto']
    query = f"select * from production.products where product_name like '{nomeprodotto}%'" #  f(format) prima di una stringa = 'format' + string = serve per inserire una variabile all interno di una stringa
    dfprodotti = pd.read_sql(query,conn)
    # Visualizzare le informazioni 
    return render_template('result.html', nomiColonne = dfprodotti.columns.values, dati = list( dfprodotti.values.tolist()))

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True) 