import requests
from bs4 import BeautifulSoup
from database_connection import cursor
from database_connection import conn


#Получение чистого текста, без тегов html, в который они обернуты. BS возвращает текст с тегами, в которые они обернуты
def clean_results(list):
    cleaned_list = []
    for listItem in list:
        cleaned_list.append(listItem.text)
    return cleaned_list
#Функция, которая преобразует значения In stock в булевое значение (мне не нравится название переменной)
def toBool(checkAvailability):
    if checkAvailability == "In stock":
        return True
    else:
        return False

def dataExtractionURL(genrePageLink):
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
        for itemPrice, itemAvailability,title1 in zip(price,availability,title):
            bufferTuple = (title1.text,float(itemPrice.text.lstrip("Â£")),toBool(itemAvailability.text.strip()),genre[0].text)
            bookInfo1.append(bufferTuple)
        return bookInfo1
        
def storeBooks(booksInfo1):
    queryToDB = """INSERT INTO scrapped_books(title,price,availability,genre)
                   VALUES(%s,%s,%s,%s);
                """
    try:
        cursor.executemany(queryToDB,booksInfo1)
        print("Data added successfully!")
    except Exception as e:
        print(f"Error during executemany: {e}")
        conn.rollback()
    else:
        conn.commit()
       
     


#Используем landing page сайта, чтобы получить список жанров, которые есть на сайте, для формирование ссылок на страницу каждого жанра
landingPageLink = "https://books.toscrape.com/index.html"

landingPageHtml = requests.get(landingPageLink).text
soup = BeautifulSoup(landingPageHtml,'lxml')

#Получим жанры книг, присутствующих на сайте, чтобы сформировать ссылки на страницы книг по жанрам
categories = soup.select('ul.nav-list li ul li a')

formattedCategories =[]

for genre in categories:
    formattedCategories.append(genre.text.strip())

#Формирование ссылок на страницы книг по жанрам, передача их в функцию для изъятия данных со страниц
for index, genre in enumerate(formattedCategories, start= 2):
    genre_link = "https://books.toscrape.com/catalogue/category/books/"
    if " " in genre:
        splitted_genre = "-".join(genre.lower().split())
        genre_link = genre_link + splitted_genre + f"_{index}" + "/index.html"
        bookInfo = dataExtractionURL(genre_link)
        storeBooks(bookInfo)

    else:
        genre_link = genre_link + genre.lower() + f'_{index}' + "/index.html"
        bookInfo = dataExtractionURL(genre_link)
        storeBooks(bookInfo)

        
#Мне не нравится, что используется одна и та же переменная bookinfo, данные по сути ни где не фиксируется в промежутке, не хорошо





















   


