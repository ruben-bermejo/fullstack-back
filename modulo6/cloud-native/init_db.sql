CREATE TABLE text_t
( 
	id INT(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,
	text_value VARCHAR(100) NOT NULL,
	application VARCHAR(100) NOT NULL,
	text_type INT(5)
);

CREATE TABLE text_properties_t
( 
	id INT(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,
	text_t_id INT(10) NOT NULL, 
	text_size INT(5) NOT NULL,
	style VARCHAR(100) NOT NULL,
	property_type INT(5),
	FOREIGN KEY (text_t_id)
		REFERENCES text_t(id)
);

INSERT INTO text_t (text_value, application, text_type) VALUES ('Texto 1 relational', 'JAVA', 1);
INSERT INTO text_t (text_value, application, text_type) VALUES ('Texto 2 relational', 'JAVA', 2);
INSERT INTO text_t (text_value, application, text_type) VALUES ('Texto 3 relational', 'JAVA', 2);
INSERT INTO text_t (text_value, application, text_type) VALUES ('Texto 4 relational', 'JAVA', 1);

INSERT INTO text_properties_t (text_size, style, property_type, text_t_id) VALUES (25, 'style="color:blue;"', 1, 1);
INSERT INTO text_properties_t (text_size, style, property_type, text_t_id) VALUES (50, 'style="color:red;"', 5, 2);
INSERT INTO text_properties_t (text_size, style, property_type, text_t_id) VALUES (75, 'style="color:yellow;"', 7, 3);
INSERT INTO text_properties_t (text_size, style, property_type, text_t_id) VALUES (100, 'style="color:grey;"', 9, 4);

COMMIT;
