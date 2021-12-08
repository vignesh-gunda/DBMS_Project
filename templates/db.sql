

-- Create table 'tbl_user'

CREATE TABLE `tbl_user`

(   `user_id` bigint(20) AUTO_INCREMENT,

    `user_name` varchar(45) NOT NULL,

    `phn_no` varchar(10) NOT NULL,  

    `user_email` varchar(45) NOT NULL,

    `user_password` varchar(255) NOT NULL,

PRIMARY KEY (`user_id`) );

--  Create table cart
 CREATE TABLE cart(email varchar(30), 
                   
                   product_name varchar(30),
                   
                   product_code varchar(30),
                   
                   price varchar(10), 
                   
                   quantity int(4), 
                   
                   PRIMARY KEY (`product_code`));
