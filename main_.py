from flask import Flask, render_template, request
import BDsql as bd

app = Flask(__name__)

cn = bd.Conectar()


@app.route('/')
def Index():
    return render_template('index.html')

@app.route('/Control', methods=['POST'])
def ControlPagina():

    return render_template('Control.html')
if __name__ == '__main__':
    app.run(port = 80000,debug= True)