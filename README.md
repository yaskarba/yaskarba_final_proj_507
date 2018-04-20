
1. Data sources used:
	- Scraped 192 sites of each dog breed from the American Kennel Club website.
	- http://www.akc.org/dog-breeds/
	- From this page, I scraped the individual breed pages ex. http://www.akc.org/dog-breeds/affenpinscher/
	- no client secrets or anything needed, just used beautiful soup to do the scraping
	- there's no secrets.py

2. Get started:
	- To get started, open the "final_proj_yk.py" file
	- UNCOMMENT LINES 189-192 to build the database from scratch
	- Getting started with plotly : https://plot.ly/python/getting-started/
		- You will need to set up a plotly account in order to access the site tools

3. Structure of the code:
	- Lines 13-43 are the caching setup

	- Lines 45 - 119 --> scraping & caching of the dogs
		- this is a function that returns a list of lists
		- its a big list, it contains a list item for each breed

	- 122 - 162:
		- This is my database function, it makes my database with my column headings

	- Lines 165 - 173
		- populating the database (specifically the dogs table)

	- Lines 175-185
		- populating the "Groups" table

	- Lines 188-192
		- Here is where I call my functions so that it scrapes/populates the databases

	- Lines 196 - 197
		- Time calculator to see how long it takes to scrape and populate the database
		- I was curious so I included it!

	- Lines 201-217
		- This is the CLASS -> Dog_Info
		- I use it to make neat displays of the dog information for the interactive command component

	- Lines 220-366
		- Functions made to calculate the average (height, weight, life expectancy)
		- Functions made to plot average (height, weight, life expectancy)

	- Lines 374-387
		- Function that creates a table displaying the dog breeds & their classification into a group

	- Lines 389-442
		- Function that creates a bar graph that compares 2 types of dog breeds

	- Lines 447 - 497s
		- Interactive function designed for user interaction

4. User guide:
	- Very simple! Follow the menu options and enter them exactly as you see them written
	- REMEMBER: you must input the EXACT name of the breed in order for the "dog breed info" command to work
		- If you want to know which breeds are available just input "dogs" and a list of options will be given to you
	- If you want to compare breeds, simply enter "compare" and then enter the 2 breeds you'd like to compare
	- Enter:
	 	- avg life (for average life expectancy based on group)
		- avg height (for average height based on group)
		- avg weight (for average weight based on group)
		- help to show the instructions
	- Simply type "exit" whenever you wish to exit the program
