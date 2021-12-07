

-- Create table 'tbl_user'

CREATE TABLE `tbl_user`

(   `user_id` bigint(20) NOT NULL AUTO_INCREMENT,

    `user_name` varchar(45) COLLATE utf8_unicode_ci DEFAULT NOT NULL,

    `phn_no` varchar(10)  COLLATE utf8mb3_unicode_ci NOT NULL,  

    `user_email` varchar(45) unique COLLATE utf8_unicode_ci DEFAULT NOT NULL,

    `user_password` varchar(255) COLLATE utf8_unicode_ci DEFAULT NOT NULL,

PRIMARY KEY (`user_id`) ) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

 
