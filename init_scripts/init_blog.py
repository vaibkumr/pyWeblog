import pickle
import sys
from bs4 import BeautifulSoup
class post:
    def __init__(self,title,id):
        self.id=id
        self.title=title
    def display(self):
        print("\tID: "+str(self.id)+"\n\tTitle: "+self.title)

class structure_data:
    def __init__(self,dict_structure,UID_map_dict):
        self.structure=dict_structure
        self.UID_map=UID_map_dict
    def display(self):
        for x in self.structure.keys():
            print(str(x)+":")
            for y in self.structure[x]:
                y.display()
        print("#### Post_ID_Map ####\n")
        for x in self.UID_map:
            print(str(x)+":\n\tTitle:"+str(self.UID_map[x]["Title"])+"\n\tDate:"+str(self.UID_map[x]["Date"])+"\n\tTags:"+str(self.UID_map[x]["Tags"]))

def file_structure_init():
    file_structure_dict={}
    file_structure_dict["index"]=[]
    UID_map={}
    my_info_obj=structure_data(file_structure_dict,UID_map)
    # choice=input("This will create new EMPTY structure object while discarding old one leaving your blog potentially non workable, continue?[y/n]")
    with open("file_structure.obj","wb") as file:
        pickle.dump(my_info_obj,file,protocol=pickle.HIGHEST_PROTOCOL)


def edit_title(soup,cname):
        title_header=soup.find("title")
        title_header.string=cname
        footer=soup.find("span",{"class":"footer_name"})
        footer.string=cname
        name=soup.find("a",{"class":"blog_heading"})
        name.string=cname
        return soup

def edit_about(soup,about_text):
    about=soup.find("div",{"class":"about"})
    new_p=soup.new_tag("p")
    new_p.string=about_text
    about.clear()
    about.append(new_p)
    return soup

def edit_image(soup,url):
    image=soup.find("img",{"class":"avatar"})
    image['src']=url
    return soup

def edit_template1(cname,url,about):
    with open("template_index.html",encoding="utf-8") as index:
        txt = index.read()
        soup=BeautifulSoup(txt,"html.parser")
        soup=edit_title(soup,cname)
        soup=edit_about(soup,about)
        soup=edit_image(soup,url)

    with open("index.html","w+",encoding="utf-8") as new_html_file:
        new_html_file.write(str(soup))

def edit_template2(cname,url,about):
    with open("template.html",encoding="utf-8") as index:
        txt = index.read()
        soup=BeautifulSoup(txt,"html.parser")
        soup=edit_title(soup,cname)
        soup=edit_about(soup,about)
        soup=edit_image(soup,url)
    with open("init_html_file.obj", "wb") as kek:
        pickle.dump(soup,kek)



if __name__=="__main__":
    print("Initializing the blog..")
    name=input("Enter blog name (Main heading text): ")
    username=input("Enter the url of your display image: ")
    about=input("Enter a short text about the author: ")
    print("You can change any of other information/create a completely different HTML layout by editing \"template.html\" file as per your needs.")
    edit_template1(name,username,about)
    print("index.html created")
    edit_template2(name,username,about)
    print("init_html_file.obj created")
    file_structure_init()
    print("New Empty file structure object initialized")
    print("All Done")
