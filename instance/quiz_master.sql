PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE subject (
	id INTEGER NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	description TEXT, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
INSERT INTO subject VALUES(1,'Python','A simple and easy to understand Programming Language.');
INSERT INTO subject VALUES(2,'Machine Learning ','A subset of Artificial Intelligence where we teach machines to learn by recognizing patterns.');
INSERT INTO subject VALUES(3,'Application Development 1','App Dev 1');
INSERT INTO subject VALUES(4,'Neural Networks','An overview of gradient descent in the context of neural networks.');
CREATE TABLE score (
	id INTEGER NOT NULL, 
	quiz_id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	time_stamp_of_attempt DATETIME NOT NULL, 
	total_scored INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(quiz_id) REFERENCES quiz (id), 
	FOREIGN KEY(user_id) REFERENCES "user" (id)
);
INSERT INTO score VALUES(1,1,2,'2025-03-26 23:04:25.236855',5);
INSERT INTO score VALUES(2,2,2,'2025-03-27 00:04:07.587461',3);
INSERT INTO score VALUES(3,2,3,'2025-03-27 01:11:14.519544',3);
INSERT INTO score VALUES(4,2,3,'2025-03-27 23:25:45.608596',1);
INSERT INTO score VALUES(5,1,2,'2025-03-28 23:01:42.463175',1);
INSERT INTO score VALUES(6,2,2,'2025-03-29 01:12:56.349356',4);
CREATE TABLE chapter (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	description TEXT, 
	num_questions INTEGER NOT NULL, 
	subject_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(subject_id) REFERENCES subject (id)
);
INSERT INTO chapter VALUES(1,'Linear Regression','Linear Regression',2,2);
INSERT INTO chapter VALUES(3,'Flask','Python module to create applications',5,3);
INSERT INTO chapter VALUES(4,'OOPs in Python','Object Oriented Programming in python',3,1);
INSERT INTO chapter VALUES(5,'Gradient Descend','An overview of gradient descent in the context of neural networks.',5,4);
CREATE TABLE IF NOT EXISTS "question" (
	id INTEGER NOT NULL, 
	quiz_id INTEGER NOT NULL, 
	question_statement TEXT NOT NULL, 
	"chapter_id" INTEGER NOT NULL,
	"option_a" VARCHAR(255) NOT NULL, 
	"option_b" VARCHAR(255) NOT NULL, 
	"option_c" VARCHAR(255) NOT NULL, 
	"option_d" VARCHAR(255) NOT NULL, 
	correct_option INTEGER NOT NULL, `title` TEXT NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(quiz_id) REFERENCES quiz (id),
	FOREIGN KEY ("chapter_id") REFERENCES subject(id)
);
INSERT INTO question VALUES(1,1,'What is the primary objective of Linear Regression?',1,' To classify data into categories',' To find the relationship between dependent and independent variables','To cluster similar data points',' To reduce dimensionality','B','Basic Linear Regression');
INSERT INTO question VALUES(2,1,'What is the main purpose of Linear Regression?',1,' To classify data into different categories','To find the relationship between dependent and independent variables','To cluster similar data points together','To reduce the dimensionality of a dataset','B','Understanding the Purpose of Linear Regression');
INSERT INTO question VALUES(3,1,' In a simple linear regression model, what does the coefficient of the independent variable represent?',1,'The correlation between two variables','The rate of change of the dependent variable per unit change in the independent variable','The mean value of the dependent variable','The total sum of squared differences','B','Interpretation of Regression Coefficient');
INSERT INTO question VALUES(4,1,'What assumption does Linear Regression make about the relationship between independent and dependent variables?',1,'It is nonlinear','It is logarithmic','It is polynomial',' It is linear','D','Assumption About Relationship in Linear Regression');
INSERT INTO question VALUES(5,1,'What is the role of the cost function in Linear Regression?',1,'To calculate the difference between actual and predicted values','To increase the variance of data','To generate new independent variables','To eliminate multicollinearity','A','Role of Cost Function in Linear Regression');
INSERT INTO question VALUES(6,2,'What is Flask in Python?',3,'A machine learning framework','A lightweight web framework','A database management system','A programming language','B','Understanding Flask');
INSERT INTO question VALUES(7,2,'How does Flask differ from Django?',3,'Flask is a microframework, while Django is a full-stack framework','Flask does not support routing, while Django does','Flask requires JavaScript for backend operations','Flask does not allow template rendering','A','Flask vs Django');
INSERT INTO question VALUES(8,2,'How do you define a route in Flask?',3,'route.add(''/home'')','app.route(''/home'')','router.set(''/home'')','url.map(''/home'')','B',' Flask Routing');
INSERT INTO question VALUES(9,2,'Which template engine is used in Flask for rendering HTML pages?',3,'EJS','Jinja2','Handlebars','Mako','B','Flask Template Engine');
INSERT INTO question VALUES(10,2,'Which command is used to run a Flask application?',3,'flask run','python manage.py runserver','start_flask_app','run flask_app.py','A','Running a Flask App');
CREATE TABLE IF NOT EXISTS "user" (
	id INTEGER NOT NULL, 
	username VARCHAR NOT NULL, 
	email VARCHAR NOT NULL, 
	password VARCHAR NOT NULL, 
	full_name VARCHAR NOT NULL, 
	qualification VARCHAR NOT NULL, 
	dob DATE NOT NULL, 
	role VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (username), 
	UNIQUE (email)
);
INSERT INTO user VALUES(1,'Admin123','admin@user.com','1234','Admin','Master','1990-01-01','admin');
INSERT INTO user VALUES(2,'Aditya','aditya@iitm.com','1234','Aditya Gole','B.Tech','2002-02-25','user');
INSERT INTO user VALUES(3,'Mrunal','mrunal@iitm.com','1234','Mrunal Joshi','B.Tech','2001-10-31','user');
INSERT INTO user VALUES(4,'Adam','adam@iitm.com','1234','Adam L','M.Tech','1996-06-26','user');
CREATE TABLE IF NOT EXISTS "quiz" (
	id INTEGER NOT NULL, 
	chapter_id INTEGER NOT NULL, 
	date_of_quiz DATE NOT NULL, 
	time_duration VARCHAR(5) NOT NULL, 
	remarks TEXT, num_questions INTEGER DEFAULT 0, 
	PRIMARY KEY (id), 
	FOREIGN KEY(chapter_id) REFERENCES chapter (id)
);
INSERT INTO quiz VALUES(1,1,'2025-03-25','01:00','Linear Regression 1',0);
INSERT INTO quiz VALUES(2,3,'2025-03-26','01:00','A test on Flask and its applications.',0);
INSERT INTO quiz VALUES(3,3,'2025-03-26','01:30','Basic flask questions',0);
COMMIT;
