from urllib.request import urlopen
from bs4 import BeautifulSoup
import re,os

''' ============================================================获取item的页数=============================================='''
def getPages(url):
    html = urlopen(url)
    bsObj = BeautifulSoup(html, "lxml")

    page = list()
    for link in bsObj.find("div", {"id": "pages"}).findAll("a",href=re.compile(
            "http\:\/\/www\.meitulu\.com\/item.*\.html")):
        page.append(link.get_text())
    lastPage = page[-2]
    return lastPage

''' ============================================================保存图片=============================================='''
def SavePictures(imageUrl, imageName):

    web = urlopen(imageUrl)
    jpg = web.read()

    DstDir = "C:\\Pictures\\"   #保存所有图片在一个文件夹
    if not os.path.exists(DstDir):
        os.makedirs(DstDir)

    name = imageName + '.jpg'

    File = open(DstDir + name, "wb")
    File.write(jpg)
    File.close()


'''============================================================获取页面中图片的URL和名称=============================================='''
def GetItemPictures(url):
    html = urlopen(url)
    bsObj = BeautifulSoup(html, "lxml")
    title = bsObj.findAll({"h1"})
    print(title)
    print("Saving Pictures...")

    images = bsObj.find("div", {"class": "content"}).findAll("img", {
        "src": re.compile("http\:\/\/pic\.yiipic\.com\/uploadfile\/.*\.jpg")})

    for image in images:
        alt = image["alt"]
        alt = alt.replace('/', '_')
        alt = alt.replace('\\', '_')
        alt = alt.replace(':', '_')
        alt = alt.replace('*', '_')
        alt = alt.replace('<', '_')
        alt = alt.replace('>', '_')
        alt = alt.replace('|', '_')
        alt = alt.replace('、', '_')
        imageName = alt[:-5] + alt[-4:-1]


        imageUrl = image["src"]

        SavePictures(imageUrl, imageName)        #调用保存函数
    item = url[-9:-5]

    lastPage = int(getPages(url))


    for i in range(2, lastPage + 1):
        next = "http://www.meitulu.com/item/"+item+"_" + str(i) + ".html"


        html = urlopen(next)
        bsObj = BeautifulSoup(html, "lxml")
        images = bsObj.find("div", {"class": "content"}).findAll("img", {
            "src": re.compile("http\:\/\/pic\.yiipic\.com\/uploadfile\/.*\.jpg")})

        for image in images:
            alt = image["alt"]
            alt = alt.replace('/','_')
            alt = alt.replace('\\', '_')
            alt = alt.replace(':', '_')
            alt = alt.replace('*', '_')
            alt = alt.replace('<', '_')
            alt = alt.replace('>', '_')
            alt = alt.replace('|', '_')
            alt = alt.replace('、', '_')
            imageName = alt[:-5] + alt[-4:-1]

            imageUrl = image["src"]

            SavePictures(imageUrl, imageName)
        if i==(lastPage):
            print("---------------------end----------------")

''' ===================================================获取所有Item地址============================================='''
def GetItems(url):
    items = set()
    html = urlopen(url)
    bsObj = BeautifulSoup(html, "lxml")
    for link in bsObj.find("div",{"class":"boxs"}).findAll("a",href=re.compile("http\:\/\/www\.meitulu\.com\/item.*\.html")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in items:
                newItem = link.attrs['href']
                items.add(newItem)
                print(newItem)

                GetItemPictures(newItem)

GetItems("http://www.meitulu.com/t/linlin-ailin/")             #获取全部套图


#GetItemPictures("http://www.meitulu.com/item/8744.html")      #获取一套图




