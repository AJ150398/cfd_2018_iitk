Microsoft code.fun.do hackathon 
 An Application to analyse sentiments of a newly released movie and predict if it can be a potential hit.


1. Softwares/Algorithms used
	PyCharm
	MongoDb
	ML/AI - scikit learn, nltk, SGD classifier, bag of words
	Flask
	
2. Folders
	C:\Users\ADITYA JAIN\Desktop\web app\final_code_fun_do
	C:\Program Files\MongoDB

3. Important Files
	src -> python package

		app.py -> main application file
		train.tsv -> obtained training data from https://www.kaggle.com/c/sentiment-analysis-on-movie-reviews/data
		Obtained testing data (reviews of the specified movie) from https://www.rottentomatoes.com

		testing.py -> for doing some tests on parts of code
	
		templates
			base.html -> layout of page (all our pages live inside this page)
			home.html-> home page
			login.html -> login page
			new_blog.html -> user's new blog page
			register.html -> new user registration page
			user_blogs.html -> user's already created blogs page

		models
			user.py -> contains user related functions
			blog.py -> contains user's blogs related functions

		database.py -> database class

	requirements.txt -> necessary packages to be installed
	ReadMe -> This file
	

4. Things to be shown in video
	
	x. INTRO

	a. Run app.py explaining it as the main application file
	b. Say that it takes about 20 seconds to run, so pausing video
	c. Click on the link
	d. Point at the text that shows we need to provide the correct endpoints i.e. login or register
		Login if you already have an account
		Register if you are a new user (Shows user_names's Movies - currently empty as it is a 'new' user)
	e. First show Register, then login (with wrong and then right credentials)
	f. To see the list of movies whose sentiments the user has already checked, go for blogs.
	g. For a new moview, go for blogs/new. After submit, show that it is highlighted in /blogs. Then go to /blogs/new for a new movie. 
	h. Examples - Harry Potter (+ve), 3 Idiots (+ve), foodfight (neutral), Warcraft (neutral), Humshakals (-ve), John Carter (-ve). Also, give an example
		of a movie with spelling mistake and/or no reviews yet.

5. Future Improvements Possible
	a. 'blogs/new' link should open after pressing 'submit' in 'blogs/new'
	b. Save the reviews of already searched movies (see 'blog'/'post' files in web_blog for help)

	


