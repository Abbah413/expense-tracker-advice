# BalanceBoost
---
## Overview:
Balance Boost is a user-friendly expense tracking tool that allows you to effortlessly 
track your spending by uploading your bank statements as .csv files. With the option 
to customize categories, you can easily view a breakdown of your expenses. Currently, 
the webapp supports statements from popular banks such as Ally Bank, Bank of America, 
Discover, Chase, and Wells Fargo. The tool was developed using Python/Flask for the 
back-end and HTML, JavaScript, and CSS for the front-end. While the core functionality 
is complete, future plans include adding features to view your expense breakdown by 
month and the option to filter your transaction, making it even easier to manage your 
finances.

## How To Use:
To get started with the website, simply create an account, then head to the upload 
page to upload your transactions. Once your file is uploaded, you'll be redirected 
to the summary page, where you can add or delete categories as needed. From there, 
you can navigate to the transaction page, where you can assign categories to your 
transactions. Note that many bank statements already have categories when uploaded, 
which you can either keep or change to better suit your needs. If you encounter any 
issues with your transaction page, you can delete your transactions. Currently, there 
is only an option to delete all categories, but additional features may be added 
in the future.

## Python Functions
---

### Init.py
- This file contains the application factory. It is the core of the app and connects all the flask blueprints together.

### Db.py
- This file has a function get_db() with is used throughout the project. It defines how 
to access the database. It also has close_db(), which closes the database after querying it.
The other functions just help to set up the schema of the database. 

### Auth.py
- This file contains all the login functionality. It manages logging in, registering,
and the users' session.

### Register_validation.py
- Contains the input validation for the register and login forms. It is called by the
register function in auth.py.

### Tracker.py
This file contains the flask blueprints for the main views of the website. There are four
functions in it. 
1. Index() which prints the users categories and their totals to the summary page. It first selects all the users categories from the db. Then it calls category_totals, a function in categories.py, which gets the transaction sums of the users categories. Then prints to the page.
2. Append_summary() this function adds new categories and budgets to the database and removes categories from the database. It receives the new data as JSON from JS functions. The JSON contains a dictionary with the key "action". This tells the function what to do with the data.
3. Import_csv() is the next function. It imports the user's CSV. Then saves it to the UPLOADS_FOLDER to be used in parse_csv.py.
4. transactions() For the GET method this function queries the db for the users transactions, then outputs them to the transaction table. For POST, this function also receives JSON data and checks the action. It can either update the category for a transaction or delete all the users transactions.

### Categories.py
This function has many of the functions for tracker.py
1. format_output() formats the file that is output by the CSV parser, then inputs the information into the current user's transaction list
2. Category_totals() receives categories as a list or a single category, then gets the associated transaction info.
3. Is_capital() checks if incoming JSON data is capitalized and capitalizes it if it is not.
4. Has_category() queries the db to see if the category exists for the current user.

### Parse_csv()
This file reads in CSV data, then parses it to figure out what bank it is from.
1. Import_file() reads in the CSV file, then sends it to the parser.
2. Export_csv() writes the data it receives from the parser to a temp file.
3. Parse() receives the CSV data, then it sends it to line_parsers.py. It first determines what bank the data belongs to. Then it uses that bank's line parser to format the data and output it as a list.
4. Has_header() determines if the first line of the data is a header. If it is a DictReader is used, if it is not a header a simple reader is used.

### Line_parsers.py
- This file contains the line parsers for each bank.

### Models.py
- This contains a class that defines the format for the transactions

## JavaScript Functions
---
This project uses a lot of JS functions to make calls to the back end so that the web pages are more dynamic and don't have to be reloaded while in use.
### Delete_transactions.js
- This file has a function with an event listener to listen for when the delete button on the transaction page is clicked. If it is, the delete button, it uses fetch() to send a request containing the "delete" action. If the transactions are successfully deleted, it clears the users' transaction table.

### Edit_types.js
- The first function listens for the edit checkbox to be toggled, then updates the read-only value of the categories column in the transaction table. The second function listens for the categories to be updated and dynamically updates them in the db.

### Edit_categories.js
- This file has the functions that add and remove rows from the table on the summary page. The first function adds a new row to the table when the add category button is clicked. The next 4 functions create all the HTML elements that go in the new row.
- The last 3 functions remove categories from the summary table. The first of those has an event listener to listen for when the remove button is clicked. The second sends a request to the back end to remove that category from the user's list of categories. The last one removes the row from the HTML table.

### Sort.js
- This file adds the sort functions for the transaction table. It also has a function for the clear button to clear the selected sort option.
- The first function listens for the clear button to be clicked. If it is the clear button it runs the sort be recent upload sort function which is the default sort option
- The second function listens for the sort selector to change. If it is changed, it gets the index of the selected option, then runs the corresponding sort function.
- The last four functions are the sort functions. They all work similarly, just adapted for their specific use case.

### Update_summary.js
- This file contains the functions that update the totals in the footer of the summary table. 
- The first two functions update the db when a new category is added or a categories budget is updated. 
- AppendTable() updates the table with the Sum of the transaction amounts with that category.
- The next function sums all the categories totals.
- The last function hides the income category from the summary table.

### Tooltips.js
- This file does not contain much. it initializes all the bootstrap tooltips.




