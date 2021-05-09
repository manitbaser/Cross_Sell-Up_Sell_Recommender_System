from flask import Flask, redirect, url_for, request, render_template
from blacklist import *
from main import *

app = Flask(__name__, template_folder='template', static_folder='static', static_url_path='')

@app.route('/success/<user_id>/<user_product>/<user_qty>/',methods = ['GET', 'POST'])
def success(user_id, user_product, user_qty):
	if request.method =='POST':
		if(request.form['bc']!=''):
			print(user_qty)
			c2p_blacklist = request.form['bc']
			blacklist_customer_product(int(user_id), int(c2p_blacklist))
			ret=main_recommend(int(user_id), int(user_product), float(user_qty))
			return render_template('results.html', res=ret, user_id=user_id, user_product=user_product, user_qty=user_qty)
			
		if(request.form['bp']!=''):
			print(request.form['bp'])
			p2p_blacklist = request.form['bp']
			print(request.args.get("user_product"))
			blacklist_product_product(int(user_product), int(p2p_blacklist))
			ret=main_recommend(int(user_id), int(user_product), float(user_qty))
			return render_template('results.html', res=ret, user_id=user_id, user_product=user_product, user_qty=user_qty)
	else:
		ret=main_recommend(int(user_id), int(user_product), float(user_qty))
		return render_template('results.html', res=ret, user_id=user_id, user_product=user_product, user_qty=user_qty)

@app.route('/',methods = ['POST', 'GET'])
def login():
	if request.method == 'POST':
		user_id = request.form['nm']
		user_product= request.form['pr']
		user_qty = request.form['qty']
		return redirect(url_for('success',user_id = user_id, user_product=user_product, user_qty=user_qty))
	else:
		return render_template('index.html')

# @app.route('/product_product_blacklist')
# def analysis():
# 	x = show_blacklist_product_product()
# 	return render_template("blacklist_p2p.html", data=x)

if __name__ == '__main__':
   app.run(debug = True)