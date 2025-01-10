import requests
from bs4 import BeautifulSoup
from database_connection import cursor
from database_connection import conn



#converts "In stock" value to bool 
def isInStock(checkAvailability):
    return checkAvailability == "In stock"
     
#forms link to specific genre page
def formLinkToPage(index,genre):
    genre_link = "https://books.toscrape.com/catalogue/category/books/"
    if " " in genre:
        splitted_genre = "-".join(genre.lower().split())
        genre_link = genre_link + splitted_genre + f"_{index}" + "/index.html"
        return genre_link
    else:
        genre_link = genre_link + genre.lower() + f'_{index}' + "/index.html"
        return genre_link

#getting link to genre page, retriving data from page
def dataExtractionURL(genrePageLink):
    try:
        bookInfo1 = []
        genrePageHtml = requests.get(genrePageLink)
        if genrePageHtml.status_code !=200:
            print(f"failed to load page: {genrePageHtml.status_code}")
            return []
        else:
            soup = BeautifulSoup(genrePageHtml.text,'lxml')
            price = soup.find_all('p', class_= "price_color")
            availability = soup.find_all('p',class_ = "instock availability")
            title = soup.select('h3 a')
            genre = soup.select('.page-header h1')
            if not(price and availability and title and genre):
                print("Missign elements on the page")
                return []
            for itemPrice, itemAvailability,title1 in zip(price,availability,title):
                bufferTuple = (title1.text,
                               float(itemPrice.text.lstrip("Â£")),
                               isInStock(itemAvailability.text.strip()),
                               genre[0].text)
                bookInfo1.append(bufferTuple)
            return bookInfo1
    except Exception as e:
        print(f'Error extracting data from URL{e}')

#checking that data is valid
def validateBookData(book):
    title, price, availability, genre = book
    return (
        isinstance(title, str) and
        isinstance(price, float) and
        isinstance(availability, bool) and
        isinstance(genre, str)
    )  

#checking validation of values, then write it to database       
def storeBooks(bookData):
    validBooks = [book for book in bookData if validateBookData(book)]
    if not validBooks:
        print("No valid data to insert.")
        return

    queryToDB = """INSERT INTO scrapped_books(title,price,availability,genre)
                   VALUES(%s,%s,%s,%s);
                """
    try:
        cursor.executemany(queryToDB,validBooks)
        print("Data added successfully!")
    except Exception as e:
        print(f"Error during executemany: {e}")
        conn.rollback()
    else:
        conn.commit()

def main():
    #Using landing page to get genres which website has, in order to form links for each page with specific genre
    landingPageLink = "https://books.toscrape.com/index.html"

    landingPageHtml = requests.get(landingPageLink).text
    soup = BeautifulSoup(landingPageHtml,'lxml')

    categories = soup.select('ul.nav-list li ul li a')

    formattedCategories =[]

    for genre in categories:
        formattedCategories.append(genre.text.strip())

    #forming links for gere pages, getting targetted data from each page, store it to table in database 
    for index, genre in enumerate(formattedCategories, start= 2):
        genre_link = formLinkToPage(index,genre)
        bookInfo = dataExtractionURL(genre_link)
        if bookInfo:
            storeBooks(bookInfo)




if __name__ == "__main__":
    main()












   


