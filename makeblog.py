from bs4 import BeautifulSoup
import time,re,sys,os
import pickle
import uuid #To generate unique IDs for posts
import arrow #for date generation, i found this easier than using datetime inbuilt in python

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

id_global=uuid.uuid4()
blog_raw_post_file=sys.argv[1]
title_found=0
content_found=0
tag_found=0
title_flag=0
content_flag=0
tag_flag=0
title=""
tag=""
url=""
content=[]
# init_count=0

def add_to_structure(tag):
    global id_global
    global title
    title=title.strip().replace('\n','')
    new_post_data=post(title,id_global)
    #Load the current file structure object of type <structure_data>
    with open("file_structure.obj","rb") as file:
        structure_obj=pickle.load(file)
    #Add new post in the index
    structure_obj.structure["index"].append(new_post_data)
    structure_obj.UID_map[id_global]={}
    structure_obj.UID_map[id_global]["Date"]=arrow.now().format('YYYY-MM-DD')
    structure_obj.UID_map[id_global]["Title"]=title
    structure_obj.UID_map[id_global]["Tags"]=[]
    #Add new post in all the tag named files
    for each_tag in tag.split(','):
        each_tag=each_tag.strip().lower()
        structure_obj.UID_map[id_global]["Tags"].append(each_tag)
        try:
            structure_obj.structure[each_tag].append(new_post_data)
        except KeyError:
            structure_obj.structure[each_tag]=[new_post_data] #Square btacckets to make it a list
    with open("file_structure.obj","wb") as file:
        pickle.dump(structure_obj,file,protocol=pickle.HIGHEST_PROTOCOL)
        print("File Structure Updated succefully.")

def toggle(a):
    if a==1:
        return 0
    else:
        return 1

def init_read_file_data():
    global title_found
    global content_found
    global tag_found
    global title_flag
    global content_flag
    global tag_flag
    global title
    global tag
    global content
    with open(blog_raw_post_file,encoding="utf-8") as post:
        for line in post:
            if "##Title" in line:
                title_found=toggle(title_found)
                title_flag=title_flag+1
                continue
            if(title_found):
                title=line
            if "##Tags" in line:
                tag_found=toggle(tag_found)
                tag_flag=tag_flag+1
                continue
            if(tag_found):
                tag=line
            if "##Content" in line:
                content_found=toggle(content_found)
                content_flag=content_flag+1
                continue
            if(content_found):
                content.append(line)
    if(content_flag!=2):
        ch1=input("Content data not found, want to continue? [Y/N]")
        if(ch1.lower()=="n"):
            sys.exit()
    if(title_flag!=2):
        title="untitled"
        ch1=input("Title not found, want to continue? [Y/N]")
        if(ch1.lower()=="n"):
            sys.exit()

def init_new_file(tag_name):
    os.makedirs("./categories/"+tag_name)
    with open("categories/"+tag_name+"/1.html","w+") as new_file:
        with open("init_html_file.obj", "rb") as kek:
            soup=pickle.load(kek)
        new_file.write(str(soup))
        # x=input("test")

def edit_html(file_name,new_page_title):
    # global init_count
    global id_global
    global url
    with open(file_name,encoding="utf-8") as index:
        txt = index.read()
        soup = BeautifulSoup(txt,"html.parser")
        post_section=soup.find_all("div", {"class":"short_post"})
        new_post=soup.new_tag("div")
        new_post['class']="short_post"
        new_post['id']=id_global
        new_title = soup.new_tag("h2")
        new_url=soup.new_tag("a",href="")
        new_url.string=title.strip()
        new_title.append(new_url)
        new_post.append(new_title)
        new_content=soup.new_tag("p")
        line_break=soup.new_tag("hr")

        code_flag=0
        image_flag=0

        for every_line_of_content in content:
            if(every_line_of_content.strip()=="##Code"):
                code_flag=toggle(code_flag)
                continue
            if(every_line_of_content.strip()=="##Image"):
                image_flag=toggle(image_flag)
                continue
            if(image_flag):
                image_tag=soup.new_tag('img',src=every_line_of_content)
                image_wrapper=soup.new_tag('div')
                image_wrapper["class"]="image_size_fix"
                image_wrapper.append(image_tag)
                new_content.append(image_wrapper)
                continue
            if(code_flag):
                code_wrapper=soup.new_tag("span")
                code_wrapper["class"]="a_code"
                code_gist=soup.new_tag("script",src=every_line_of_content)
                code_wrapper.append(code_gist)
                new_content.append(code_wrapper)
                continue
            new_paragraph=soup.new_tag("p")
            new_paragraph.string=every_line_of_content
            new_content.append(new_paragraph)



        # new_content.string=content[0] #modify this later to have all the content
        tags=soup.new_tag("p")
        tags.string="Tags: "
        date=arrow.now().format('YYYY-MM-DD')
        date_object=soup.new_tag("p")
        date_object['class']="date"
        date_span=soup.new_tag("span")
        date_span['class']="glyphicon glyphicon-calendar"

        date_object.append(date_span)
        date_object.append(date)

        # #Getting the list of tags currently on the website sidepanel
        tag_list=soup.find("ul",{"class":"categories"})
        # current_tags=tag_list.find_all("li")
        # tags_on_web=[]
        # for every_current_tag in current_tags:
        #     link_list=every_current_tag.find("a")
        #     temp_tagname=link_list.string
        #     temp_tagname=temp_tagname.rstrip()
        #     tags_on_web.append(temp_tagname)

        for each_tag in tag.split(','):
            each_tag=each_tag.strip()
            #Adding to sidepanel and creating new directory and file for it (not adding the redundant tags)
            if(file_name=="index.html"):
                current_tag_files=os.listdir("./categories")
            else:
                current_tag_files=os.listdir("../")
            if(each_tag.lower() not in current_tag_files):
                if(file_name!="index.html"):
                    #If file name is index then relative path to others different from all others
                    url="../"+each_tag.lower()+"/1.html"
                else:
                    url="categories/"+each_tag.lower()+"/1.html"

                new_c_link=soup.new_tag("a",href=url)
                new_c_link.string=each_tag.lower()
                new_c_li=soup.new_tag("li")
                new_c_li.append(new_c_link)
                tag_list.append(new_c_li)
                soup.find("div", { "class" : "c_list" }).clear()
                soup.find("div", { "class" : "c_list" }).append(tag_list)
                current_tag_files=os.listdir("./categories")
                if(each_tag.lower() not in current_tag_files):
                    print(each_tag.lower()+" got initialized")
                    init_new_file(each_tag.lower())
                try:
                    os.makedirs("./categories/"+each_tag.lower())
                except FileExistsError as e:
                    a=False
                    # nothing


                # if(init_count!=len(tag.split(','))):
                #     print(each_tag.lower()+" got initialized")
                #     init_new_file(each_tag.lower())
                #     init_count=init_count+1



            if(file_name!="index.html"):
                #If file name is index then relative path to others different from all others
                lower_url="../"+each_tag.lower()+"/1.html"
            else:
                lower_url="categories/"+each_tag.lower()+"/1.html"
            #Adding to main blog post (all tags need to be added here)
            new_underpost_tag_label=soup.new_tag("span")
            new_underpost_tag_label['class']="label label-default tag"
            new_underpost_tag_link=soup.new_tag("a",href=lower_url)
            new_underpost_tag_link.string=each_tag.lower()
            new_underpost_tag_label.append(new_underpost_tag_link)
            if(each_tag.lower()!=""):
                tags.append(new_underpost_tag_label)

        new_post.append(new_content)
        new_post.append(date_object)
        new_post.append(tags)
        new_post.append(line_break)
        post_section.insert(0,new_post)
        soup.find("h3",{"class":"page_title"}).string=new_page_title
        soup.find("div", { "class" : "latest_posts" }).clear()
        for every_post in post_section:
                soup.find("div", { "class" : "latest_posts" }).append(every_post)
        soup=soup.prettify(formatter=None)
        with open(file_name,"w+",encoding="utf-8") as new_html_file:
            new_html_file.write(str(soup))

if __name__ == "__main__":
    init_read_file_data()
    l=os.listdir("categories/")
    add_to_structure(tag)
    edit_html("index.html","Latest posts")
    for each_tag in tag.split(','):
        each_tag=each_tag.strip()
        print("writing file: "+each_tag)
        edit_html("categories/"+each_tag.lower()+"/1.html","Category: "+each_tag.lower())
    print("New file with ID: %s has been created" %(id_global))
