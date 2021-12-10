

-- Create table 'tbl_user'

CREATE TABLE `tbl_user`

(   `user_id` bigint(20) AUTO_INCREMENT,

    `user_name` varchar(45) NOT NULL,

    `phn_no` varchar(15) NOT NULL,  

    `user_email` varchar(45) NOT NULL,

    `user_password` varchar(255) NOT NULL,

     PRIMARY KEY (`user_id`) );

CREATE TABLE user_information

(
    name varchar(45) NOT NULL,

    user_email varchar(45) NOT NULL,

    user_address varchar(400) DEFAULT NULL,
    
    user_city varchar(50) DEFAULT NULL,
 
    user_state varchar(50) DEFAULT NULL,
 
    user_zipcode varchar(15) DEFAULT NULL);


--  Create table cart
 CREATE TABLE cart(email varchar(30), 
                   
  product_name varchar(30),
                   
  product_code varchar(30),
                   
  price varchar(15), 
                   
  quantity int(4), 
                   
  PRIMARY KEY (`product_code`));
                   
                   
                   
 CREATE TABLE Orders (

    OrderID varchar(40) NOT NULL,

    user_email varchar(40) NOT NULL,
     
    user_name varchar(40) NOT NULL,
     
    product_name varchar(50) not null,
     
    product_code varchar(30) not null,
     
    product_price int unsigned NOT null,
    
    product_quantity varchar(10) NOT NULL
     
    

);