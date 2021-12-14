# FRONT END
The front end for the system has a main index page in the beginning which can redirect to sign up and login of the merchant as well as user interfaces.

## USER
#### USER AUTHENTICATION:
1. Login page  
    - users will be verified from database 

2. Register page
    - registers the users and stores new users in 'tbl_user' table in hotpink database.

3. Forgot Password page
    - users are redirected to this page if they click on the button which enables them to change password

#### USER PROFILE
1. Products page 
    - users can add items present on this page to the cart, remove them, clear the cart, or check out once      done.
2. Checkout page
    - upon checking out the users are directed to a page where they need to add details like address, name      and payment options.
3. Order Confirmation page
    - once the order is stored in the database, you are redirected to the order confirmation page

#### MERCHANT AUTHENTICATION:
1. Login page  
    - merchants will be verified from database 

2. Register page
    - registers the merchants and stores new users in 'tbl_user' table in hotpink database.

3. Forgot Password page
    - merchants are redirected to this page which enables them to change password

#### MERCHANT PROFILE
1. Home page 
    - Merchants can be directed to either the add product page or edit product page.
2. Add product page
    - Merchants can fill in a little information to add a new product to the products table under their         name
3. Edit product page
    - This page helps us edit product information such as price and quantity. There is also an option to delete the product here.

# BACK END
Connecting the front end to database and adding a python flask functionality in the website.

## FUNCTIONALITY
We added functionality into the website using python.
All forms are validated as needed and we check for wrong inputs wherever input is necessary.
The website is well connected.

## DATABASE
The data storing in the database for the website called 'hotpink' is fully consistent.
Within the Database 'hotpink', we have tables for different requirements:

1. tbl_user:  
      - Unique email id
      - Table for User's personal information- name phone number
      - encrypted password 

2. User_information:
    - user addresses and misc information. It contains the various addresses saved by the user.

3. Product table:  
      - Unique product id
      - Product information like product name, price, quantity available
      - Merchant unique id (email id)

4. Cart table:
    - products currently in cart
    - information of products like MRP, quantity

5. Orders table:
    - unique id (email) of the person ordering
    - information of the product like quantity, mrp etc. 

6. tbl_merchant:
    - Unique email id
    - Table for User's personal information- name phone number
    - encrypted password 

### ER diagram and table schema diagram


![2](https://user-images.githubusercontent.com/89929088/146004380-2ccbe00e-f205-4a57-8738-1354e97c112f.png)


![1](https://user-images.githubusercontent.com/89929088/146004352-2f3551a4-1dbf-4053-b05a-f12feef6c00f.png)

