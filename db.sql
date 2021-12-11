
-- products table

CREATE TABLE `product` (
	`id` int unsigned COLLATE utf8mb4_unicode_ci NOT NULL AUTO_INCREMENT,
	`name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
	`code` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
	`image` text COLLATE utf8mb4_unicode_ci NOT NULL,
	`price` double COLLATE utf8mb4_unicode_ci NOT NULL,
    quantity int,
    category varchar(40),
	PRIMARY KEY (`id`)
);

-- products insert
INSERT INTO `product` (`id`, `name`, `code`, `image`, `price`, `quantity`, `category` ) VALUES
(1, 'American Tourist', 'AMTR01', 'product-images/bag.jpg', 12000.00, 1000, 'bags'),
(2, 'EXP Portable Hard Drive', 'USB02', 'product-images/external-hard-drive.jpg', 5000.00, 20, 'tech'),
(3, 'Shoes', 'SH03', 'product-images/shoes.jpg', 1000.00, 30, 'shoes'),
(4, 'XP 1155 Intel Core Laptop', 'LPN4', 'product-images/laptop.jpg', 80000.00, 5, 'tech'),
(5, 'FinePix Pro2 3D Camera', '3DCAM01', 'product-images/camera.jpg', 150000.00),
(6, 'Simple Mobile', 'MB06', 'product-images/mobile.jpg', 3000.00),
(7, 'Luxury Ultra thin Wrist Watch', 'WristWear03', 'product-images/watch.jpg', 3000.00),
(8, 'Headphone', 'HD08', 'product-images/headphone.jpg', 400.00);


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
