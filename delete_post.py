from bs4 import BeautifulSoup
import time,re,sys,os
import pickle
import uuid
import shutil

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

def save_file(file_name,soup):
    with open(file_name,"w+",encoding="utf-8") as new_html_file:
        new_html_file.write(str(soup))

def delete_from_here(file_name):
    with open(file_name,encoding="utf-8") as file:
        txt = file.read()
        soup = BeautifulSoup(txt,"html.parser")
        post = soup.find(id=id_to_del)
        if(post):
            print("Deleting from ",file_name)
            soup.find(id=id_to_del).decompose()
            save_file(file_name,soup)
        else:
            print("Not found in ",file_name)

def remove_empty_tags_and_update_structure(file_structure,list_of_tags,id_to_del):
    empty_tags=[]
    #Deleting from index, index is not appended to list_of_tags to prevent deletion of whole blog
    for each_post in file_structure.structure['index']:
        if(each_post.id==id_to_del):
            file_structure.structure['index'].remove(each_post)
    #Delete from map
    del file_structure.UID_map[id_to_del]
    #Delete from file structure
    for tag in list_of_tags:
        for each_post in file_structure.structure[tag]:
            if(each_post.id==id_to_del):
                file_structure.structure[tag].remove(each_post)
    #Remove empty tags and save it in empty_tags list to return later
    for tag in list_of_tags:
        if not file_structure.structure[tag]:
            print(tag+"/1.html file got empty and is now being deleted")
            try:
                shutil.rmtree("categories/"+tag)
            except OSError as e:
                print ("Error: %s - %s." % (e.filename, e.strerror))
            empty_tags.append(tag)
    #Removing empty tag entries from file structure
    for each_empty_tag in empty_tags:
        del file_structure.structure[each_empty_tag]

    #Write new file structure on disc
    with open("file_structure.obj","wb") as file:
        pickle.dump(file_structure,file,protocol=pickle.HIGHEST_PROTOCOL)
        print("File system structure updated")
    return empty_tags

def update_index_side_panel_tags(empty_tags):
    with open("index.html",encoding="utf-8") as index:
        txt = index.read()
        soup = BeautifulSoup(txt,"html.parser")
        tag_list=soup.find("ul",{"class":"categories"})
        current_tags=tag_list.find_all("li")
        tags_on_web=[]
        temp=0
        for each_current_tag in current_tags:
            temp_tagname=each_current_tag.find("a").string.strip().replace('\n','')
            if temp_tagname in empty_tags:
                temp=1
                each_current_tag.decompose()
        if(temp):
            with open("index.html","w+",encoding="utf-8") as new_html_file:
                new_html_file.write(str(soup))
                print(str(empty_tags)+" got empty and index.html got Updated again.")

def validate_id(id_to_del_string):
    try:
        id_to_del=uuid.UUID(id_to_del_string)
    except ValueError:
        print("Not a valid ID format.")
        exit()
    with open("file_structure.obj","rb") as handle:
        file_structure=pickle.load(handle)
    try:
        title=file_structure.UID_map[id_to_del]["Title"]
    except KeyError:
        print("No post matching to this ID exists")
        exit()
    return uuid.UUID(id_to_del_string)

if __name__ == "__main__":
    #Get ID from command line argument
    id_to_del_string=sys.argv[1]
    #Validate ID
    id_to_del=validate_id(id_to_del_string)
    with open("file_structure.obj","rb") as handle:
        file_structure=pickle.load(handle)
    title=file_structure.UID_map[id_to_del]["Title"]
    choice=input("Delete the post: \""+title+"\"? [y/n] ")
    if(choice.lower()=="n"):
        exit()
    delete_from_here("index.html")
    l=file_structure.UID_map[id_to_del]["Tags"]
    for each_tag in l:
        each_tag=each_tag.strip()
        delete_from_here("categories/"+each_tag+"/1.html")
    empty_tags=remove_empty_tags_and_update_structure(file_structure,l,id_to_del)
    update_index_side_panel_tags(empty_tags)
