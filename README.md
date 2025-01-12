# WebScrapingWithPostgreSQL
WebScrapingWithPostgreSQL is a web scraper with data processing functionality and PostgreSQL database integration. This script is designed to extract targeted information from a training website containing a catalog of books. It automatically collects data, including:

+ Book title
+ Price
+ Availability (in stock or not)
+ Genre
Once collected, the data is sorted, validated, and stored in a PostgreSQL database for further use or analysis.

**Key Features**
1. Extracting genres from the website's main page:
   + Retrieves a list of available book categories.
2. Generating links to genre-specific pages:
   + Creates URLs for navigating to pages containing books of each genre.
3. Collecting data from each genre page:
   + Extracts details about books, such as title, price, availability, and genre.
4. Validating and storing data in the database:
   + Ensures the correctness of the collected data before saving it into PostgreSQL.

**Technologies**

**Python**: The primary programming language used.

**BeautifulSoup**: For parsing HTML and extracting data.

**PostgreSQL**: To store structured data.

**Requests**: For sending HTTP requests and retrieving website data.

