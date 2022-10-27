from flask import Flask, render_template, request, redirect, url_for, Response
#pip install flask pandas contextily geopandas matplotlib
app = Flask(__name__)
import pandas as pd
import pymssql
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
conn = pymssql.connect(server = '213.140.22.237\SQLEXPRESS', user = 'biagioni.jacopo', password = 'xxx123##', database = 'biagioni.jacopo')

@app.route('/', methods=['GET'])
def home():
    return render_template("home.html") #serve per restituire una stringa

@app.route('/selezione', methods=['GET'])
def selezione():
  scelta = request.args['scelta']
  if scelta == 'esercizio1':
    return redirect(url_for('esercizio1'))
  elif scelta == 'esercizio2':
    return redirect(url_for('esercizio2'))
  else:
    return redirect(url_for('esercizio3'))

@app.route('/esercizio1', methods=['GET'])
def esercizio1(): 
  query = 'SELECT category_name, count(*) as numero_prodotti FROM production.products INNER JOIN production.categories ON production.products.category_id = production.categories.category_id GROUP BY categories.category_name ORDER BY numero_prodotti DESC'
  df = pd.read_sql(query,conn)
  return render_template("esercizio1.html", nomiColonne = df.columns.values, dati = list(df.values.tolist()))

@app.route('/graficoEs1', methods=['GET'])
def graficoEs1():
    #costruzione grafico
    query = 'SELECT category_name, count(*) as numero_prodotti FROM production.products INNER JOIN production.categories ON production.products.category_id = production.categories.category_id GROUP BY categories.category_name ORDER BY numero_prodotti DESC'
    df = pd.read_sql(query,conn)
    fig, ax = plt.subplots(figsize = (6,4))
    fig.autofmt_xdate(rotation=90)
    ax.bar(df.category_name, df.numero_prodotti, color='g')

    #visualizzazione grafico
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)

    return Response(output.getvalue(), mimetype='image/png')


@app.route('/es2', methods=['GET'])     
def esercizio2():
    
    query = 'SELECT store_name, count(*) as numero_ordini from sales.orders inner join sales.stores on stores.store_id = orders.store_id group by store_name'
    global df2
    df2 = pd.read_sql(query,conn)
    return render_template('esercizio2.html', nomiColonne = df2.columns.values, dati = list(df2.values.tolist()))


@app.route('/graficoEs2', methods=['GET'])
def graficoEs2():
    #costruzione grafico
    fig, ax = plt.subplots(figsize = (6,4))
    fig.autofmt_xdate(rotation=90)
    ax.bar(df2.store_name, df2.numero_ordini, color='g')

    #visualizzazione grafico
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)

    return Response(output.getvalue(), mimetype='image/png')



@app.route('/es3', methods=['GET'])     
def esercizio3():

    query = 'SELECT brand_name, count(*) as numero_prodotti FROM production.products inner join production.brands on brands.brand_id = products.brand_id group by brand_name'
    global df3
    df3 = pd.read_sql(query,conn)

    # visualizzare le informazioni
    return render_template('esercizio3.html', nomiColonne = df3.columns.values, dati = list(df3.values.tolist()))



@app.route('/graficoEs3', methods=['GET'])
def graficoEs3():
    fig = plt.figure()
    ax = plt.axes()
    cols = ['c','b','hotpink','yellow','red','brown'] 
    ax.pie(df3.numero_prodotti,colors=cols,labels=df3.brand_name)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)

    return Response(output.getvalue(), mimetype='image/png')



@app.route('/result', methods=['GET'])
def result():
# Collegamento al database
    # Invio query al database e ricezione informazioni
    nomeprodotto = request.args['nomeprodotto']
    query = f"select * from production.products where product_name like '{nomeprodotto}%'" #  f(format) prima di una stringa = 'format' + string = serve per inserire una variabile all interno di una stringa
    dfprodotti = pd.read_sql(query,conn)
    # Visualizzare le informazioni 
    return render_template('result.html', nomiColonne = dfprodotti.columns.values, dati = list( dfprodotti.values.tolist()))


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True) 