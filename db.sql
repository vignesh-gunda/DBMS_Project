
-- products table

CREATE TABLE `product`(
	`id` int unsigned COLLATE utf8mb4_unicode_ci NOT NULL AUTO_INCREMENT,
	`name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
	`code` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
	`image` text COLLATE utf8mb4_unicode_ci NOT NULL,
	`price` double COLLATE utf8mb4_unicode_ci NOT NULL,
    	quantity int,
    	category varchar(40),
	merchant_id varchar(40),
	PRIMARY KEY (`id`));

-- products insert

 INSERT INTO `product` (`id`, `name`, `code`, `image`, `price`, quantity, category, merchant_id)
VALUES
 (1, 'Hat', 'RDDR', 'product-images/hats.jpg', 4200.00, 30, 'clothes', 'drishti@gmail.com'),

 (2, 'spl aviator-sunglasses', 'SASG', 'product-images/aviator-sunglasses.jpg', 2900.00, 20, 'accessories', 'mihika@gmail.com'),

 (3, 'Shoes', 'SH01', 'product-images/shoes.jpg', 1000.00, 40, 'shoes', 'drishti@gmail.com'),

 (4, 'hot pink scarf', 'HPS', 'product-images/scarf.jpg', 400.00, 40, 'clothes', 'vignesh@gmail.com'),

 (5, 'set of 3 ties', '3TS01', 'product-images/ties.jpg', 1200.00, 60, 'accessories', 'vignesh@gmail.com'),

 (6, 'Simple wallet xd', 'WLT06', 'product-images/wallets.jpg', 1500.00, 50, 'accessories', 'drishti@gmail.com'),

 (7, 'LU1V handbag', 'IV04', 'product-images/handbag.jpg', 12000.00, 8, 'accessories', 'mihika@gmail.com'),

 (8, 'UXI bandana', 'UXB', 'product-images/bandanas.jpg', 400.00, 10, 'accessories', 'drishti@gmail.com'),

 (9, 'CLK gloves', 'CGLK', 'product-images/gloves.jpg', 1400.00, 60, 'accessories', 'vignesh@gmail.com'),

 (10, 'scarves', 'SC01', 'product-images/scarves.jpg', 5400.00, 40, 'clothes', 'vignesh@gmail.com'),

 (11, 'Black Sash', 'SH004', 'product-images/sashes.jpg', 6400.00, 8, 'accessories', 'drishti@gmail.com'),

 (12, 'Brown Bag', 'WHL02', 'product-images/weekender.jpg', 5600.00, 8, 'accessories', 'vignesh@gmail.com'),

 (13, 'Denim jacket', 'DJKT1', 'product-images/denimjacket.jpg', 4400.00, 40, 'clothes', 'mihika@gmail.com'),

 (14, 'Cologne', 'DJKT2', 'product-images/cologne.jpg', 4400.00, 40, 'clothes', 'mihika@gmail.com'),

 (15, 'Boots', 'BO08', 'product-images/boots.jpg', 7800.00, 20, 'shoes', 'vignesh@gmail.com'),

 (16, 'Blue Print Dress', 'BPD7', 'product-images/D2.jpg', 2500.00, 20, 'clothes', 'drishti@gmail.com'),

 (17, 'Black Dress', 'LBD19', 'product-images/D3.jpeg', 2350.00, 20, 'clothes', 'vignesh@gmail.com'),

 (18, 'White Dress', 'DW440', 'product-images/D4.jpg', 2100.00, 20, 'clothes', 'mihika@gmail.com'),

 (19, 'Red Coat', 'REDC', 'product-images/C2.jpg', 3700.00, 20, 'clothes', 'drishti@gmail.com'),

 (20, 'White Coat', 'WH12', 'product-images/C1.jpg', 4300.00, 20, 'clothes', 'mihika@gmail.com');


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
    
    product_quantity int NOT NULL,
     product_total_price int NOT NULL);
    
--     merchant table- personal info of merchants
    CREATE TABLE `tbl_merchant`
(   
    `merchant_id` bigint(20) AUTO_INCREMENT,

    `merchant_name` varchar(45) NOT NULL,

    `merchant_phn_no` varchar(15) NOT NULL,  

    `merchant_email` varchar(45) NOT NULL,

    `merchant_password` varchar(255) NOT NULL,

    PRIMARY KEY (`merchant_id`) 
);
