#Importing libraries which we need
from requests import Session
from bs4 import BeautifulSoup as bs
import os
import threading

#Defining category class
class Category:
    def __init__(self, text, href):
        self.text = text
        self.href = href

#Defining global variables
link = "https://www.freeimages.com"
categories = []
imageSources = []
successCategory = False

#Function of saving image to specific path and file
def saveImage(imageCount, imageSources, selectedCategory, s):
    if not os.path.exists("outputs/" + selectedCategory):
        os.mkdir("outputs/" + selectedCategory)
    for index in range(int(imageCount)):
        os.path.exists("outputs/" + selectedCategory + "/" + str(index) + ".jpg")
        response = s.get(imageSources[index])
        file = open("outputs/" + selectedCategory + "/" + str(index) + ".jpg", "wb")
        file.write(response.content)
        file.close()


with Session() as s:

    #Entering the categories page and getting all categories
    siteCategories = s.get(link + "/image")
    soupCategories = bs(siteCategories.text, "html.parser")
    result = soupCategories.find_all(
        "a",
        {
            "class": "flex flex hover:bg-secondary hover:text-white px-4 py-1.5 rounded-full mr-5 my-1"
        },
        text=True,
        href=True,
    )

    #Defining categories to category objects as text and href
    for item in result:
        categoryText = item.text.rstrip("\n").strip()
        categoryHref = item["href"]
        categories.append(Category(categoryText, categoryHref))
    for item in categories:
        print(item.text)

    #Getting category name from user
    while successCategory == False:
        selectedCategory = input("Please choose a category: \n")
        for item in categories:
            if selectedCategory in item.text:
                print("Your choose is: " + selectedCategory)
                selectedHref = item.href
                successCategory = True
        if successCategory == False:
            print("Hatalı kategori: " + selectedCategory)

    #Entering the category page which selected by the user and getting all image sources
    siteCategory = s.get(link + selectedHref)
    soupCategory = bs(siteCategory.text, "html.parser")
    result = soupCategory.find_all(
        "img",
        {"class": "grid-image h-full w-full object-cover"},
        src=True,
    )
    for item in result:
        imageSources.append(item["src"].replace("small", "large"))

    #Getting num of image from user
    imageCount = input("Please enter number of image: \n")

    #Checking entered number is higher than image source list's length
    if int(imageCount) >= len(imageSources):
        imageCount = len(imageSources)

    #Getting num of threads from user
    numThreads = input("Please enter thread number: \n")

    #Defining threads and run them
    threads = []
    for i in range(int(numThreads)):
        t = threading.Thread(
            target=saveImage, args=(imageCount, imageSources, selectedCategory, s)
        )
        t.start()
        threads.append(t)
    
    #Waiting all threads to finish.
    for t in threads:
        t.join()
