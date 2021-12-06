import pymysql
from app import app
from db_config import mysql
from flask import flash, session, render_template, request, redirect, url_for
#from werkzeug import generate_password_hash, check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash



@app.route('/')
def index():
	if 'email' in session:
		username = session['email']
		return render_template('home.html')
	return render_template('index.html')

	
@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/submit', methods=['POST'])
def login_submit():
	_email = request.form['inputEmail']
	_password = request.form['inputPassword']
	# validate the received values
	if _email and _password and request.method == 'POST':
		#check user exists			
		conn = mysql.connect()
		cursor = conn.cursor()
		sql = "SELECT * FROM tbl_user WHERE user_email=%s"
		sql_where = (_email,)
		cursor.execute(sql, sql_where)
		row = cursor.fetchone()
		if row:
			if check_password_hash(row[3], _password):
				session['email'] = row[1]
				cursor.close() 
				conn.close()
				return redirect('/')
			else:
				flash('Invalid password!')
				return redirect('/login')
		else:
			flash('Invalid email/password!')
			return redirect('/login')
		
@app.route('/logout')
def logout():
	session.pop('email', None)
	return render_template('index.html')


@app.route('/signup')
def add_user_view():
	return render_template('signup.html')
		
@app.route('/new_user', methods=['POST'])
def add_user():
	conn = None
	cursor = None
	try:		
		_name = request.form['inputName']
		_email = request.form['inputEmail']
		_password = request.form['inputPassword']
		# validate the received values
		if _name and _email and _password and request.method == 'POST':
			#do not save password as a plain text
			_hashed_password = generate_password_hash(_password)
			# save edits
			sql = "INSERT INTO tbl_user(user_name, user_email, user_password) VALUES(%s, %s, %s)"
			data = (_name, _email, _hashed_password,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			flash('User added successfully!')
			return redirect('/')
		else:
			return 'Error while adding user'
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		


@app.route('/add', methods=['POST'])
def add_product_to_cart():
	cursor = None
	try:
		_quantity = int(request.form['quantity'])
		_code = request.form['code']
		# validate the received values
		if _quantity and _code and request.method == 'POST':
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT * FROM product WHERE code=%s", _code)
			row = cursor.fetchone()
			
			itemArray = { row['code'] : {'name' : row['name'], 'code' : row['code'], 'quantity' : _quantity, 'price' : row['price'], 'image' : row['image'], 'total_price': _quantity * row['price']}}
			
			all_total_price = 0
			all_total_quantity = 0
			
			session.modified = True
			if 'cart_item' in session:
				if row['code'] in session['cart_item']:
					for key, value in session['cart_item'].items():
						if row['code'] == key:
							#session.modified = True
							#if session['cart_item'][key]['quantity'] is not None:
							#	session['cart_item'][key]['quantity'] = 0
							old_quantity = session['cart_item'][key]['quantity']
							total_quantity = old_quantity + _quantity
							session['cart_item'][key]['quantity'] = total_quantity
							session['cart_item'][key]['total_price'] = total_quantity * row['price']
				else:
					session['cart_item'] = array_merge(session['cart_item'], itemArray)

				for key, value in session['cart_item'].items():
					individual_quantity = int(session['cart_item'][key]['quantity'])
					individual_price = float(session['cart_item'][key]['total_price'])
					all_total_quantity = all_total_quantity + individual_quantity
					all_total_price = all_total_price + individual_price
			else:
				session['cart_item'] = itemArray
				all_total_quantity = all_total_quantity + _quantity
				all_total_price = all_total_price + _quantity * row['price']
			
			session['all_total_quantity'] = all_total_quantity
			session['all_total_price'] = all_total_price
			
			return redirect(url_for('.products'))
		else:			
			return 'Error while adding item to cart'
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/cart')
def products():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM product")
		rows = cursor.fetchall()
		return render_template('cart.html', products=rows)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/empty')
def empty_cart():
	try:
		session.clear()
		return redirect(url_for('.products'))
	except Exception as e:
		print(e)

@app.route('/delete/<string:code>')
def delete_product(code):
	try:
		all_total_price = 0
		all_total_quantity = 0
		session.modified = True
		
		for item in session['cart_item'].items():
			if item[0] == code:				
				session['cart_item'].pop(item[0], None)
				if 'cart_item' in session:
					for key, value in session['cart_item'].items():
						individual_quantity = int(session['cart_item'][key]['quantity'])
						individual_price = float(session['cart_item'][key]['total_price'])
						all_total_quantity = all_total_quantity + individual_quantity
						all_total_price = all_total_price + individual_price
				break
		
		if all_total_quantity == 0:
			session.clear()
		else:
			session['all_total_quantity'] = all_total_quantity
			session['all_total_price'] = all_total_price
		
		#return redirect('/')
		return redirect(url_for('.products'))
	except Exception as e:
		print(e)
		
def array_merge( first_array , second_array ):
	if isinstance( first_array , list ) and isinstance( second_array , list ):
		return first_array + second_array
	elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
		return dict( list( first_array.items() ) + list( second_array.items() ) )
	elif isinstance( first_array , set ) and isinstance( second_array , set ):
		return first_array.union( second_array )
	return False		
		
if __name__ == "__main__":
    app.run(debug=True)