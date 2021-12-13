import pymysql
import random
from app import app
from db_config import mysql
from flask import flash, session, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from decimal import Decimal




@app.route('/')
def index():
	if 'email' in session:
		username = session['email']
		return redirect('/cart')
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
			if check_password_hash(row[4], _password):
				session['email'] = row[3]
				session['name'] = row[1]
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
	session.clear()
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
		_phone = request.form['inputPhone']
		_email = request.form['inputEmail']
		_password = request.form['inputPassword']
		_confirmpassword = request.form['inputconfirmPassword']
		# validate the received values
	
		if (_password==_confirmpassword) and ('@' in _email) and (len(_phone)==10) and (_phone.isdigit()):
			if _name and _email and _password and _confirmpassword and _phone and request.method == 'POST':
				conn = mysql.connect()
				cursor = conn.cursor()
				sql_check = "SELECT * FROM tbl_user WHERE user_email=%s"
				sql_where = (_email,)
				cursor.execute(sql_check, sql_where)
				row = cursor.fetchone()
				if row:
					flash('Error! User already exists!')
					return render_template('signup.html')
				_hashed_password = generate_password_hash(_password)
				# save edits
				sql = "INSERT INTO tbl_user(user_name, phn_no, user_email, user_password) VALUES(%s, %s, %s, %s)"
				data = (_name, _phone, _email, _hashed_password,)
			
				cursor.execute(sql, data)
				conn.commit()
				flash('User added successfully!')
				return redirect('/login')
		else:
			if (_password!=_confirmpassword):
				flash("Passwords Don't Match")
			if('@' not in _email):
				flash("Invalid Email")
			if(len(_phone)!=10):
				flash("Invalid Phone Number length")
			if not _phone.isdigit():
				flash("Invalid Phone number type")
			return redirect('/signup')

	except Exception as e:
		print(e)
	


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
			conn.commit()
			item_quant = int(row['quantity'])
			itemArray = { row['code'] : {'name' : row['name'], 'code' : row['code'], 'quantity' : _quantity, 'price' : row['price'], 'image' : row['image'], 'total_price': _quantity * row['price']}}
			con = mysql.connect()
			cursor = con.cursor()
			if 'email' in session:
				_email = session['email']
			all_total_price = 0
			all_total_quantity = 0
			
			session.modified = True
			if 'cart_item' in session:
				
				if row['code'] in session['cart_item']:
					c = mysql.connect()
					cur = c.cursor(pymysql.cursors.DictCursor)
					cur.execute("SELECT * FROM cart WHERE product_code=%s", _code)
					cartrow = cur.fetchone()
					cart_quant = int(cartrow['quantity'])
					c.commit()
					cur.close()
					if _quantity < cart_quant + item_quant:
						print("Here")
						sql_update = "UPDATE cart SET quantity= quantity+%s WHERE product_code =%s"
						data = (_quantity, _code,)
						cursor.execute(sql_update, data)
						con.commit()
						for key, value in session['cart_item'].items():
							if row['code'] == key:
								old_quantity = session['cart_item'][key]['quantity']
								total_quantity = old_quantity + _quantity
								session['cart_item'][key]['quantity'] = total_quantity
								session['cart_item'][key]['total_price'] = total_quantity * row['price']
					else:
						flash("Quantity of item requested not available.")


				else:
					if _quantity < item_quant:
						sql_ins = "INSERT INTO cart(email, product_name, product_code, price, quantity) VALUES(%s, %s, %s, %s, %s)"
						data = ( session['email'], row['name'], row['code'], row['price'], _quantity)
						cursor.execute(sql_ins, data)
						con.commit()
						session['cart_item'] = array_merge(session['cart_item'], itemArray)
					else:
						flash("Quantity of item requested not available.")

				for key, value in session['cart_item'].items():
					individual_quantity = int(session['cart_item'][key]['quantity'])
					individual_price = float(session['cart_item'][key]['total_price'])
					all_total_quantity = all_total_quantity + individual_quantity
					all_total_price = all_total_price + individual_price
			else:
				if _quantity < item_quant:
					session['cart_item'] = itemArray
					all_total_quantity = all_total_quantity + _quantity
					all_total_price = all_total_price + _quantity * row['price']
					sql_insert = "INSERT INTO cart(email, product_name, product_code, price, quantity) VALUES(%s, %s, %s, %s, %s)"
					data = (_email, row['name'], row['code'], row['price'], _quantity)
					cursor.execute(sql_insert, data)
					con.commit()
				else:
					flash("Quantity of item requested not available.")
			
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
		con.close()
		
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
	conn = None
	cursor = None
	try:
		session.pop('cart_item', None)
		session.pop('all_total_quantity', None)
		session.pop('all_total_price', None)

		conn = mysql.connect()
		cursor = conn.cursor()
		
		cursor.execute("TRUNCATE TABLE cart")
		conn.commit()
		return redirect(url_for('.products'))
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/checkout_btn')
def checkout_btn():
	try:
		session.pop('cart_item', None)
		session.pop('all_total_quantity', None)
		session.pop('all_total_price', None)

		return render_template('checkout.html')
	except Exception as e:
		print(e)

@app.route('/checkout', methods=['POST'])
def checkout():
	_name = request.form['firstname']
	_address = request.form['address']
	_city = request.form['city']
	_state = request.form['state']
	_zip = request.form['zip']
	_email = session['email']
	if _email and _name and _address and _city and _state and _zip and request.method == 'POST':	
		conn = mysql.connect()
		cursor = conn.cursor()
		sql = "INSERT INTO user_information( name, user_email,  user_address, user_city, user_state, user_zipcode) VALUES( %s, %s, %s, %s, %s, %s)"
		sql_where = ( _email, _name, _address, _city, _state, _zip, )
		cursor.execute(sql, sql_where)	
		conn.commit()
		return redirect(url_for('.checkoutcomp'))
	else:
		flash('Fill all fields please!')
		return redirect(url_for('.checkout_btn'))



@app.route('/checkoutcomp')
def checkoutcomp():
	cursor = None
	_email = session['email']
	_name = session['name']
	r=random.randint(1,1000000)
	s = random.randint(1,1000000)
	_orderno = _name + _email[0:5] + str(r) + str(s)
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM cart WHERE email=%s", _email)
		rows = cursor.fetchall()
		cursor.close() 
		conn.close()

		for row in rows:
			con = mysql.connect()
			cur = con.cursor()
			_productname = row[1]
			_productcode = row[2]
			_productprice = row[3]
			_productquantity = int(row[4])
			sql = "INSERT INTO orders( OrderID, user_email, user_name, product_name, product_code, product_price, product_quantity) VALUES(%s, %s, %s, %s, %s, %s, %s)"
			data = (_orderno, _email, _name, _productname,_productcode, _productprice, _productquantity)
			cur.execute(sql, data)
			con.commit()
			cur.close()
			print('Reached here')
			c = mysql.connect()
			cur1 = c.cursor()
			sql_update = "UPDATE product SET quantity = quantity-%s WHERE code =%s"
			data_val = (_productquantity, _productcode,)
			cur1.execute(sql_update, data_val)
			c.commit()
			cur1.close()
		c_conn = mysql.connect()
		c_cursor = c_conn.cursor()
		
		c_cursor.execute("TRUNCATE TABLE cart")
		c_conn.commit()
		return render_template('thank.html')
		
	except Exception as e:
		print(e)
		
		
	
	
	

@app.route('/delete/<string:code>')
def delete_product(code):
	conn = None
	cursor = None
	try:
		all_total_price = 0
		all_total_quantity = 0
		session.modified = True
		conn = mysql.connect()
		cursor = conn.cursor()
		
		cursor.execute("DELETE FROM cart WHERE product_code=%s", (code,))
		conn.commit()

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
	
		session['all_total_quantity'] = all_total_quantity
		session['all_total_price'] = all_total_price
		# if all_total_quantity == 0:
		# 	session.clear()
		# else:
			# session['all_total_quantity'] = all_total_quantity
			# session['all_total_price'] = all_total_price
		
		
		return redirect(url_for('.products'))
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
	
		
		
def array_merge( first_array , second_array ):
	if isinstance( first_array , list ) and isinstance( second_array , list ):
		return first_array + second_array
	elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
		return dict( list( first_array.items() ) + list( second_array.items() ) )
	elif isinstance( first_array , set ) and isinstance( second_array , set ):
		return first_array.union( second_array )
	return False		

@app.route('/edit')
def edit_view():
	return render_template('edit.html')
	

@app.route('/update', methods=['POST'])
def update_user():
	
	try:		
		_name = request.form['inputName']
		_email = request.form['inputEmail']
		_password = request.form['inputPassword']
		con = mysql.connect()
		cur = con.cursor()
		cur.execute("SELECT * FROM tbl_user WHERE user_email=%s", (_email,))
		row = cur.fetchone()
		con.commit()
		cur.close()
		if row:
			if _name and _email and _password and request.method == 'POST':
				_hashed_password = generate_password_hash(_password)
				print(_hashed_password)
			# save edits
				sql = "UPDATE tbl_user SET user_password=%s WHERE user_email=%s"
				data = (_hashed_password, _email,)
				conn = mysql.connect()
				cursor = conn.cursor()
				cursor.execute(sql, data)
				conn.commit()
				flash('User updated successfully!')
				return redirect('/')
			else:
				flash('User update error! Fill all the fields and try again')
				return redirect(url_for('.edit_view'))
		
		else:
			flash("The user does not exist! Try again!")
			return redirect(url_for('.edit_view'))

		
	except Exception as e:
		print(e)
	

	# -------------------------------------------------------------------------------------------------------------------------
# merchant files

@app.route('/merch_login')
def login_merchant():
    return render_template('merch_login.html')

@app.route('/merch_signup')
def signup_merchant():
    return render_template('merch_signup.html')

@app.route('/new_merch_signup',methods=['POST'])
def merch_signup_submit():
	try:
		cursor=None
		conn=None
		_namemerch = request.form['inputName_merch']
		_phonemerch = request.form['inputPhone_merch']
		_emailmerch = request.form['inputEmail_merch']
		_passwordmerch = request.form['inputPassword_merch']
		_confirmpasswordmerch = request.form['inputconfirmPassword_merch']
		print(_namemerch,_phonemerch,_emailmerch,_passwordmerch)

		if (_passwordmerch==_confirmpasswordmerch) and ('@' in _emailmerch) and (len(_phonemerch)==10) and (_phonemerch.isdigit()):
			if _namemerch and _emailmerch and _passwordmerch and _confirmpasswordmerch and _phonemerch and request.method=='POST':
					conn = mysql.connect() 
					cursor = conn.cursor()
					sql_check = "SELECT * FROM tbl_merchant WHERE merchant_email=%s"
					sql_where = (_emailmerch,)
					cursor.execute(sql_check,sql_where)
					row = cursor.fetchone()
					if row:
						flash("Error! User already exists!")
						return render_template("merch_signup.html")
					_hashed_password = generate_password_hash(_passwordmerch)
					sql = "INSERT into tbl_merchant(merchant_name, merchant_phn_no, merchant_email, merchant_password) VALUES(%s, %s, %s, %s)"
					data = (_namemerch, _phonemerch, _emailmerch, _hashed_password,)
					cursor.execute(sql, data)
					conn.commit()
					flash("User added successfully !")
					return redirect('/merch_login')
		else:
			if(_passwordmerch!=_confirmpasswordmerch):
				flash("Passwords Don't match")
			if('@' not in _emailmerch):
				flash("Invalid Email")
			if(len(_phonemerch)!=10):
				flash("Invalid Phone Number Length")
			if not _phonemerch.isdigit():
				flash("Invalid Phone Number type")
			return redirect('/merch_signup')
	except Exception as e:
		print(e)

@app.route('/merch_submit',methods=['POST'])
def merch_login_submit():
	_emailmerch = request.form['inputEmail_merch']
	_passwordmerch = request.form['inputPassword_merch']
	# validate the received values
	if _emailmerch and _passwordmerch and request.method == 'POST':
		#check user exists
		conn = mysql.connect()
		cursor = conn.cursor()
		sql = "SELECT * FROM tbl_merchant WHERE merchant_email=%s"
		sql_where = (_emailmerch,)
		cursor.execute(sql, sql_where)
		temp = cursor.fetchone()
		if temp:
			

			if check_password_hash(temp[4], _passwordmerch):
				# print("equal passwords")
			# 	return "Its done"
				session['merchant_email'] = temp[3]
				# print(session['merchant_email'])
				cursor.close() 
				conn.close()
				return render_template("merch_home.html")
			else:
				flash('Invalid password!')
				return redirect('/merch_login')
		else:
			flash('Invalid email/password!')
			return redirect('/merch_login')
		# return "done"

@app.route('/merch_home')
def merch_homepage():
	print("Hello")
	if 'merchant_email' in session:
		print("Hello")
		username = session['merchant_email']
		return render_template('merch_home.html')

@app.route('/merch_logout')
def merch_logout():
	session.clear()
	# return render_template('merch_login.html')
	return redirect('/')



@app.route('/product_add')
def merch_product_add():
    return render_template('merch_product_add.html')

@app.route('/product_add_submit',methods=['POST'])
def merch_product_add_submit():
	_name=request.form['product_name']
	_code=request.form['product_code']
	_category=request.form['product_category']
	_quantity=int(request.form['product_quantity'])
	_price = Decimal(request.form['product_price'])
	_image = request.form['product_image']
	_merch = session['merchant_email']

	if _name and _code and _category and _quantity and _price and request.method=='POST':
		_image = request.form['product_image']
		filename='product-images/{}'.format(_image)
		conn = mysql.connect()
		cursor = conn.cursor()

		sql_check = "SELECT * FROM product WHERE code = %s"
		sql_where = (_code,)
		cursor.execute(sql_check, sql_where)

		row = cursor.fetchone()
		if row:
			flash('Product already exists!')
			return redirect('/merch_home')
		
		sql = "INSERT INTO product (name, code, image, price, quantity, category, merchant_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
		data = (_name, _code, filename, _price, _quantity, _category, _merch)
		cursor.execute(sql,data)
		conn.commit()
		cursor.close()
		flash("product added successfully")
		return redirect('/merch_home')

@app.route('/edit_merch')
def edit_merch():
	return render_template('forgot_merch.html')
	

@app.route('/merchforgot', methods=['POST'])
def merchforgot():
	
	try:		
		_name = request.form['inputName']
		_email = request.form['inputEmail']
		_password = request.form['inputPassword']
		con = mysql.connect()
		cur = con.cursor()
		cur.execute("SELECT * FROM tbl_merchant WHERE merchant_email=%s", (_email,))
		row = cur.fetchone()
		con.commit()
		cur.close()
		print('reached here')
		if row:
			if _name and _email and _password and request.method == 'POST':
			#do not save password as a plain text
				_hashed_password = generate_password_hash(_password)
				print(_hashed_password)
			# save edits
				sql = "UPDATE tbl_merchant SET merchant_password=%s WHERE merchant_email=%s"
				data = (_hashed_password, _email,)
				conn = mysql.connect()
				cursor = conn.cursor()
				cursor.execute(sql, data)
				conn.commit()
				cursor.close() 
				flash('Merchant password updated successfully!')
				return redirect('/merch_login')
			else:
				flash('Error! Fill all the fields and try again!')
				return redirect(url_for('.edit_merch'))
		
		else:
			flash("The merchant email does not exist! Try again!")
			return redirect(url_for('.edit_merch'))
		
	except Exception as e:
		print(e)
		

@app.route('/product_edit/')
def merch_product_edit():

	conn=mysql.connect()
	cursor = conn.cursor()
	_merch = session['merchant_email']
	sql = "SELECT * FROM product WHERE merchant_id=%s"
	data = (_merch,)
	cursor.execute(sql,data)
	rows = cursor.fetchall()
	return render_template('merch_product_edit.html',rows=rows)

@app.route('/product_edit_submit/<int:id>',methods=['POST'])
def merch_product_edit_submit(id):
		conn = mysql.connect()
		cursor = conn.cursor()
		_id = id
		sql = "SELECT * FROM product WHERE id=%s"
		data = (_id,)
		cursor.execute(sql,data)
		result = cursor.fetchone()
		if request.method == 'POST':
			return render_template("edit_product.html",result=result)

@app.route('/update_product/<int:id>',methods=['POST'])
def update_product(id):
	_price = request.form['product_price']
	_quantity = request.form['product_quantity']
	_merch = session['merchant_email']
	_id = id
	if request.method == 'POST':
		conn = mysql.connect()
		cursor = conn.cursor()
		print(_price,_quantity,_merch)
		sql_1 = "UPDATE product SET price = %s, quantity = %s WHERE merchant_id=%s AND id=%s"
		data_1 = (_price,_quantity,_merch,_id)
		cursor.execute(sql_1,data_1)
		conn.commit()
		return redirect('/product_edit/')

#------------------------------------------------------------------------------------------------------------------------------
# delete 
# @app.route('/delete_product/<int:id>',methods=['POST'])
# def delete_product(id):
# 	_id = id
# 	if request.method == 'POST':
# 		conn = mysql.connect()
# 		cursor = conn.cursor()
# 		# print(_price,_quantity,_merch)
# 		sql_2 = "DELETE FROM product WHERE id=%s"
# 		data_2 = (_id,)
# 		cursor.execute(sql_1,data_1)
# 		conn.commit()
# 		return redirect('/product_edit/')
#-------------------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    app.run(debug=True)

