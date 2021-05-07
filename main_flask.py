from flask import Flask, redirect, url_for, request, render_template
from main import *

app = Flask(__name__, template_folder='template')

@app.route('/success/<user_id>/<user_product>/<user_qty>',methods = ['GET'])
def success(user_id, user_product, user_qty):
	ret=main_recommend(int(user_id), int(user_product), float(user_qty))
	return render_template('results.html', res=ret)

@app.route('/login',methods = ['POST', 'GET'])
def login():
	if request.method == 'POST':
		user_id = request.form['nm']
		user_product= request.form['pr']
		user_qty = request.form['qty']
		return redirect(url_for('success',user_id = user_id, user_product=user_product, user_qty=user_qty))
	else:
		return render_template('login.html')

if __name__ == '__main__':
   app.run(debug = True)