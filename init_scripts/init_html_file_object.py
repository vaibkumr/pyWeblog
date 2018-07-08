import pickle
from bs4 import BeautifulSoup
import time,re,sys,os

if __name__==__main__:
    with open("template.html") as index:
        txt = index.read()
        soup = BeautifulSoup(txt,"html5lib")
        with open("init_html_file.obj", "wb") as kek:
            pickle.dump(soup,kek)
        print("html object initialized!")
