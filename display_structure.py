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
        print("\n#### Post_ID_Map ####\n")
        for x in self.UID_map:
            print(str(x)+":\n\tTitle:"+str(self.UID_map[x]["Title"])+"\n\tDate:"+str(self.UID_map[x]["Date"])+"\n\tTags:"+str(self.UID_map[x]["Tags"]))

id_global=uuid.uuid4()

if __name__ == "__main__":
    with open("file_structure.obj","rb") as handle:
        a=pickle.load(handle)
    a.display()
