from flask import Flask, redirect, url_for, request, render_template, flash
from blacklist import *
from main import *
import re
import numpy

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def isint(value):
  try:
    int(value)
    return True
  except ValueError:
    return False

app = Flask(__name__, template_folder='template', static_folder='static', static_url_path='')
data1 = list(pd.read_csv('./blacklisted_wholesaler_product.csv')['wholesaler id'])
data2 = list(pd.read_csv('./blacklisted_product_product.csv')['product id'])

prod_info = pd.read_csv('./products_info.csv', index_col="id")
user_info = pd.read_csv('./wholesalers_info.csv', index_col="id")

@app.route('/success/<user_id>/<user_product>/<user_qty>/',methods = ['GET', 'POST'])
def success(user_id, user_product, user_qty):
	if request.method =='POST':
		if request.form['bc']=='' and request.form['bp']=='':
			ret=main_recommend(int(user_id), int(user_product), float(user_qty))
			return render_template('results.html', res=ret, user_id=user_id, user_product=user_product, user_qty=user_qty)
		if(request.form['bc']!=''):
			c2p_blacklist = request.form['bc']
			if c2p_blacklist=='' or isint(c2p_blacklist)==False or int(c2p_blacklist) not in (data2):
				ret=main_recommend(int(user_id), int(user_product), float(user_qty))
				return render_template('results.html', res=ret, user_id=user_id, user_product=user_product, user_qty=user_qty, flash_message="Invalid Product ID provided")
			blacklist_customer_product(int(user_id), int(c2p_blacklist))
			ret=main_recommend(int(user_id), int(user_product), float(user_qty))
			return render_template('results.html', res=ret, user_id=user_id, user_product=user_product, user_qty=user_qty)
			
		if(request.form['bp']!=''):
			p2p_blacklist = request.form['bp']
			if p2p_blacklist=='' or isint(p2p_blacklist)==False or int(p2p_blacklist) not in (data2):
				ret=main_recommend(int(user_id), int(user_product), float(user_qty))
				return render_template('results.html', res=ret, user_id=user_id, user_product=user_product, user_qty=user_qty, flash_message="Invalid Product ID provided")
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
		
		# Error Handling
		
		if user_id=='' or isint(user_id)==False or int(user_id) not in (data1):
			return render_template('index.html', flash_message="Invalid Wholesaler ID provided")
		if user_product=='' or isint(user_product)==False or int(user_product) not in (data2):
			return render_template('index.html', flash_message="Invalid Product ID provided")
		if user_qty=='' or isfloat(user_qty)==False:
			return render_template('index.html', flash_message="Invalid Quantity provided")
		if (float(user_qty)<0):
			return render_template('index.html', flash_message="Invalid Quantity provided")
		if int(user_id) not in list(user_info.index):
			return render_template('index.html', flash_message="Enter Wholesaler ID details in the database ")
		if int(user_product) not in list(prod_info.index):
			return render_template('index.html', flash_message="Enter Product ID details in the database such as brand etc. ")
		return redirect(url_for('success',user_id = user_id, user_product=user_product, user_qty=user_qty))
	else:
		return render_template('index.html')

if __name__ == '__main__':
   app.run(debug = True)
