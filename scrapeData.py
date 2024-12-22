import requests
from bs4 import BeautifulSoup
from database_connection import cursor

#Получение чистого текста, без тегов html, в который они обернуты. BS возвращает текст с тегами, в которые они обернуты
def clean_results(list):
    cleaned_list = []
    for listItem in list:
        cleaned_list.append(listItem.text)
    return cleaned_list

#Используем landing page сайта, чтобы получить список жанров, которые есть на сайте, для формирование ссылок на страницу каждого жанра
landingPageLink = "https://books.toscrape.com/index.html"

landingPageHtml = requests.get(landingPageLink).text
soup = BeautifulSoup(landingPageHtml,'lxml')

categories = soup.select('ul.nav-list li ul li a')

formattedCategories =[]

for genre in categories:
    formattedCategories.append(genre.text.strip())


for index, genre in enumerate(formattedCategories, start= 2):
    genre_link = "https://books.toscrape.com/catalogue/category/books/"
    if " " in genre:
        splitted_genre = "-".join(genre.lower().split())
        genre_link = genre_link + splitted_genre + f"_{index}" + "/index.html"
        genrePageHtml = requests.get(genre_link).text
        soup = BeautifulSoup(genrePageHtml,'lxml')

        
    else:
        genre_link = genre_link + genre.lower() + f'_{index}' + "/index.html"
        genrePageHtml = requests.get(genre_link).text
        soup = BeautifulSoup(genrePageHtml,'lxml')

        





#=============================Старый код (не актуальный)============================================

targettedData = []
amountOfPages = 50
amountOfCategories = 51 




for i in range(amountOfPages + 1):
    link = "https://books.toscrape.com/catalogue/page-" + str(i) + ".html"
    htmlPage = requests.get(link).text

    soup = BeautifulSoup(htmlPage,"lxml")

    price = soup.find_all('p', class_= "price_color")
    availability = soup.find_all('p',class_ = "instock availability")

    name = soup.select('h3 a')



    for itemPrice, itemAvailability,title in zip(price,availability,name):
        bufferList = []
        bufferList.append(float(itemPrice.text.lstrip("Â£")))
        bufferList.append(itemAvailability.text.strip())
        bufferList.append(title.text)
        targettedData.append(bufferList)

print(targettedData)
print("-------------------------------------------------------")
print(f"amount of scrapped elements: {len(targettedData)}")


# print("------Categories--------")


categories = soup.select('ul.nav-list li ul li a')

cleaned_categories = []

for genre in categories:
    cleaned_categories.append(genre.text.strip())

# print(cleaned_categories)

# print("---------sorted by categories-------------")

links = []


for index, genre in enumerate(cleaned_categories, start= 2):
    genre_link = "https://books.toscrape.com/catalogue/category/books/"
    if " " in genre:
        splitted_genre = "-".join(genre.lower().split())
        genre_link = genre_link + splitted_genre + f"_{index}" + "/index.html"
        links.append(genre_link)
    else:
        genre_link = genre_link + genre.lower() + f'_{index}' + "/index.html"
        links.append(genre_link)

# print(links)

booksCollections = {}

for link_ in links:
    htmlPage = requests.get(link_).text
    soup = BeautifulSoup(htmlPage,"lxml")
    genreTitle = soup.select("div.page-header h1")
    listOfTitles = clean_results(soup.select("h3 a"))
    booksCollections[genreTitle[0].text] = listOfTitles
    # print(booksCollections)
















   


