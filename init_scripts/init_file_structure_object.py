import pickle
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

def main():
    file_structure_dict={}
    file_structure_dict["index"]=[]
    UID_map={}
    my_info_obj=structure_data(file_structure_dict,UID_map)
    choice=input("This will create new EMPTY structure object while discarding old one leaving your blog potentially non workable, continue?[y/n]")
    if(choice.lower()=='y'):
        with open("file_structure.obj","wb") as file:
            pickle.dump(my_info_obj,file,protocol=pickle.HIGHEST_PROTOCOL)
            print("New Empty file structure object initialized")
    else:
        exit()


if __name__ == '__main__':
    main()
