# Running the project
	The webpage can be run by launching run.py through python from the root directory of the project.
	Before running, the database may need to be setup along with installing any additional requirements for python.

# Python Requirements
	This project requires some additional libraries that can be installed using pip.
	
	The following commands should install all that is neccessary if any of these are missing.

		pip install cryptography
		pip install python-dotenv
		pip install python-jose
		pip install Flask-Cors

	All of the requirements are listed in requirements.txt
		Note that some of these requirements may already be met.

# Database Requirements
	The database must be setup before running the website. The provided database in DBFiles is sufficent however,
	a new database can be created using the following commands from the root directory of the project.
		
		sqlite3 DBFiles/coffeeShop.db < DBFiles/create_db_coffeeshop.sql
		sqlite3 DBFiles/coffeeShop.db < DBFiles/addTestData.sql

	This creates the neccessary tables and populates the Item table with different drinks that can be ordered.

# Other Requirements
	The project uses Auth0 for logging in and out so the file .env should be left unmodified.