import json
import random
import copy
import os




CoNLL_Target={"support":[],
        "target_label": [
        "LOC",
        "PER",
        "ORG",
        "MISC"
    ]}
movie1_Target={"support":[],
        "target_label": [
                "Actor",
                "Plot",
                "Opinion",
                "Award",
                "Year",
                "Genre",
                "Origin",
                "Director",
                "Soundtrack",
                "Relationship",
                "Character_Name",
                "Quote",
    ]}
movie2_Target={"support":[],
        "target_label": [
                "ACTOR",
                "YEAR",
                "TITLE",
                "GENRE",
                "DIRECTOR",
                "SONG",
                "PLOT",
                "REVIEW",
                "CHARACTER",
                "RATING",
                "RATINGS_AVERAGE",
                "TRAILER",
    ]}
rest_Target={"support":[],
        "target_label": [
                "Rating",
                "Amenity",
                "Location",
                "Restaurant_Name",
                "Price",
                "Hours",
                "Dish",
                "Cuisine",
    ]}
re3d_Target={"support":[],
        "target_label": [
                "Organisation",
                "Temporal",
                "Nationality",
                "Location",
                "Person",
                "DocumentReference",
                "Money",
                "Quantity",
                "MilitaryPlatform",
                "Weapon",
    ]}
WNUT17_Target={"support":[],
        "target_label": [
        "location",
        "creative_work",
        "person",
        "product",
        "group",
        "corporation",
    ]}

def changeTosupport(dataset_name,num,inputfile,outputfile):
    dataset = []
    Targets=[]

    if dataset_name=="CoNLL":
        chooseTarget=CoNLL_Target
    elif dataset_name=="mit-movie1":
        chooseTarget=movie1_Target
    elif dataset_name=="mit-movie2":
        chooseTarget=movie2_Target
    elif dataset_name=="mit-rest":
        chooseTarget=rest_Target
    elif dataset_name=="re3d":
        chooseTarget=re3d_Target
    elif dataset_name=="WNUT17":
        chooseTarget=WNUT17_Target
    Target=copy.deepcopy(chooseTarget)
    with open(inputfile) as f:
        for line in f:
            line = json.loads(line)
            dataset.append(line)
        random.shuffle(dataset)
        for data in dataset:
            Target["support"].append(data)
        Targets.append(Target)
        
    with open(outputfile,"a") as f:
        for data in Targets:
            f.write(json.dumps(data)+"\n")
    print(dataset_name+"...... finish!")


def replace_entities_with_tokens(original_item, entity_type, replacement_entities):
    
    item=original_item.copy()
    result=item.copy()
    entities=item["entity"].copy()
    num=0
    order=0
    for entity in entities:
        if entity["type"]==entity_type:
            num=num+1
    replace_index=set()
    while len(replace_index)<num:            
        replace_index.add(random.randint(0,len(replacement_entities[entity_type])-1))
    replace_index=list(replace_index)
    for i in range(len(entities)):
        entity=result["entity"][i]
        if entity["type"]==entity_type:
            start,end=entity["offset"]
            index=replace_index[order]
            order=order+1

            replace_en=replacement_entities[entity_type][index].copy()
            replace_en_len=replace_en["offset"][1]-replace_en["offset"][0]
            need_add=replace_en_len-(end-start)

            new_tokens=" ".join(result["tokens"][:start])
            new_tokens+=" "+replace_en["text"]+" "
            new_tokens+=" ".join(result["tokens"][end:])
            result['tokens']=new_tokens.split()
            replace_en["offset"]=[start,end+need_add]
            result["entity"][i]=replace_en
            
            for j in range(i+1,len(entities)):
                result["entity"][j]["offset"]=[result["entity"][j]["offset"][0]+need_add,result["entity"][j]["offset"][1]+need_add]
    return result



def replace_CONLL_entities_with_file(inputfile,outputfile,support_id):
    replacement_entities = {
                'ORG':[],
                'PER':[],
                'LOC':[],
                'MISC':[],
            }
    dataset = []
    with open(inputfile) as f:
        for line in f:
            line = json.loads(line)
            dataset.append(line)
    print(len(dataset))
    data=dataset[support_id]
    datainfo=data["support"]
    for i in range(len(datainfo)):
        entity_deal=datainfo[i]["entity"]
        for en in entity_deal:
            start,end=en["offset"]
            en_len=end-start-1

            if en["type"]=="LOC":
                replacement_entities["LOC"].append(en)
            elif en["type"]=='ORG':
                replacement_entities["ORG"].append(en)
            elif en["type"]=='PER':
                replacement_entities["PER"].append(en)
            else:
                replacement_entities["MISC"].append(en)
    print("LOC")
    print(len(replacement_entities["LOC"]))
    print("ORG")
    print(len(replacement_entities["ORG"]))
    print("PER")
    print(len(replacement_entities["PER"]))
    print("MISC")
    print(len(replacement_entities["MISC"]))
    
    replaced_items=[]
    replaced_item=[]
    data=dataset[support_id]
    datainfo=data["support"]
    for item in datainfo:
        replaced_item = replace_entities_with_tokens(item, "LOC", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "ORG", replacement_entities) 
        replaced_item = replace_entities_with_tokens(replaced_item, "PER", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "MISC", replacement_entities)
        replaced_items.append(replaced_item)

    print(len(replaced_items))
    with open(outputfile,"a") as f:
        for item in replaced_items:
            f.write(json.dumps(item)+"\n")


def replace_WNUT17_entities_with_file(inputfile,outputfile,support_id):
    replacement_entities = {
                "location":[],
                "creative_work":[],
                "person":[],
                "product":[],
                "group":[],
                "corporation":[],
            }

    dataset = []
    with open(inputfile) as f:
        for line in f:
            line = json.loads(line)
            dataset.append(line)
    print(len(dataset))
    data=dataset[support_id]
    datainfo=data["support"]
    for i in range(len(datainfo)):
        entity_deal=datainfo[i]["entity"]
        for en in entity_deal:
            start,end=en["offset"]
            en_len=end-start-1

            if en["type"]=="location":
                replacement_entities["location"].append(en)
            elif en["type"]=='creative_work':
                replacement_entities["creative_work"].append(en)
            elif en["type"]=='person':
                replacement_entities["person"].append(en)
            elif en["type"]=='product':
                replacement_entities["product"].append(en)
            elif en["type"]=='group':
                replacement_entities["group"].append(en)
            else:
                replacement_entities["corporation"].append(en)
    print("location")
    print(len(replacement_entities["location"]))
    print("creative_work")
    print(len(replacement_entities["creative_work"]))
    print("person")
    print(len(replacement_entities["person"]))
    print("product")
    print(len(replacement_entities["product"]))
    print("group")
    print(len(replacement_entities["group"]))
    print("corporation")
    print(len(replacement_entities["corporation"]))

    replaced_items=[]    
    replaced_item=[]
    data=dataset[support_id]
    datainfo=data["support"]
    for item in datainfo:
        replaced_item = replace_entities_with_tokens(item, "location", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "creative_work", replacement_entities) 
        replaced_item = replace_entities_with_tokens(replaced_item, "person", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "product", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "group", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "corporation", replacement_entities)
        replaced_items.append(replaced_item)

    print(len(replaced_items))
    with open(outputfile,"a") as f:
        for item in replaced_items:
            f.write(json.dumps(item)+"\n")

def replace_mitmovie1_entities_with_file(inputfile,outputfile,support_id):
    replacement_entities = {
                "Actor":[],
                "Plot":[],
                "Opinion":[],
                "Award":[],
                "Year":[],
                "Genre":[],
                "Origin":[],
                "Director":[],
                "Soundtrack":[],
                "Relationship":[],
                "Character_Name":[],
                "Quote":[],
            }

    dataset = []
    with open(inputfile) as f:
        for line in f:
            line = json.loads(line)
            dataset.append(line)
    print(len(dataset))
    data=dataset[support_id]
    datainfo=data["support"]
    for i in range(len(datainfo)):
        entity_deal=datainfo[i]["entity"]
        for en in entity_deal:
            start,end=en["offset"]
            en_len=end-start-1

            if en["type"]=="Actor":
                replacement_entities["Actor"].append(en)
            elif en["type"]=='Plot':
                replacement_entities["Plot"].append(en)
            elif en["type"]=='Opinion':
                replacement_entities["Opinion"].append(en)
            elif en["type"]=='Award':
                replacement_entities["Award"].append(en)
            elif en["type"]=='Year':
                replacement_entities["Year"].append(en)
            elif en["type"]=='Genre':
                replacement_entities["Genre"].append(en)
            elif en["type"]=="Origin":
                replacement_entities["Origin"].append(en)
            elif en["type"]=='Director':
                replacement_entities["Director"].append(en)
            elif en["type"]=='Soundtrack':
                replacement_entities["Soundtrack"].append(en)
            elif en["type"]=='Relationship':
                replacement_entities["Relationship"].append(en)
            elif en["type"]=='Character_Name':
                replacement_entities["Character_Name"].append(en)
            else:
                replacement_entities["Quote"].append(en)
    print("Actor")
    print(len(replacement_entities["Actor"]))
    print("Plot")
    print(len(replacement_entities["Plot"]))
    print("Opinion")
    print(len(replacement_entities["Opinion"]))
    print("Award")
    print(len(replacement_entities["Award"]))
    print("Year")
    print(len(replacement_entities["Year"]))
    print("Genre")
    print(len(replacement_entities["Genre"]))
    print("Origin")
    print(len(replacement_entities["Origin"]))
    print("Director")
    print(len(replacement_entities["Director"]))
    print("Soundtrack")
    print(len(replacement_entities["Soundtrack"]))
    print("Relationship")
    print(len(replacement_entities["Relationship"]))
    print("Character_Name")
    print(len(replacement_entities["Character_Name"]))
    print("Quote")
    print(len(replacement_entities["Quote"]))

    replaced_items=[]
    replaced_item=[]
    data=dataset[support_id]
    datainfo=data["support"]
    for item in datainfo:
        replaced_item = replace_entities_with_tokens(item, "Actor", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "Plot", replacement_entities) 
        replaced_item = replace_entities_with_tokens(replaced_item, "Opinion", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "Award", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "Year", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "Genre", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "Origin", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "Director", replacement_entities) 
        replaced_item = replace_entities_with_tokens(replaced_item, "Soundtrack", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "Relationship", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "Character_Name", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "Quote", replacement_entities)
        replaced_items.append(replaced_item)

    print(len(replaced_items))
    with open(outputfile,"a") as f:
        for item in replaced_items:
            f.write(json.dumps(item)+"\n")


def replace_mitmovie2_entities_with_file(inputfile,outputfile,support_id):
    replacement_entities = {
                "ACTOR":[],
                "YEAR":[],
                "TITLE":[],
                "GENRE":[],
                "DIRECTOR":[],
                "SONG":[],
                "PLOT":[],
                "REVIEW":[],
                "CHARACTER":[],
                "RATING":[],
                "RATINGS_AVERAGE":[],
                "TRAILER":[],
            }

    dataset = []
    with open(inputfile) as f:
        for line in f:
            line = json.loads(line)
            dataset.append(line)
    print(len(dataset))
    data=dataset[support_id]
    datainfo=data["support"]
    for i in range(len(datainfo)):
        entity_deal=datainfo[i]["entity"]
        for en in entity_deal:
            start,end=en["offset"]
            en_len=end-start-1

            if en["type"]=="ACTOR":
                replacement_entities["ACTOR"].append(en)
            elif en["type"]=='YEAR':
                replacement_entities["YEAR"].append(en)
            elif en["type"]=='TITLE':
                replacement_entities["TITLE"].append(en)
            elif en["type"]=='GENRE':
                replacement_entities["GENRE"].append(en)
            elif en["type"]=='DIRECTOR':
                replacement_entities["DIRECTOR"].append(en)
            elif en["type"]=='SONG':
                replacement_entities["SONG"].append(en)
            elif en["type"]=="PLOT":
                replacement_entities["PLOT"].append(en)
            elif en["type"]=='REVIEW':
                replacement_entities["REVIEW"].append(en)
            elif en["type"]=='CHARACTER':
                replacement_entities["CHARACTER"].append(en)
            elif en["type"]=='RATING':
                replacement_entities["RATING"].append(en)
            elif en["type"]=='RATINGS_AVERAGE':
                replacement_entities["RATINGS_AVERAGE"].append(en)
            else:
                replacement_entities["TRAILER"].append(en)
    print("ACTOR")
    print(len(replacement_entities["ACTOR"]))
    print("YEAR")
    print(len(replacement_entities["YEAR"]))
    print("TITLE")
    print(len(replacement_entities["TITLE"]))
    print("GENRE")
    print(len(replacement_entities["GENRE"]))
    print("DIRECTOR")
    print(len(replacement_entities["DIRECTOR"]))
    print("SONG")
    print(len(replacement_entities["SONG"]))
    print("PLOT")
    print(len(replacement_entities["PLOT"]))
    print("REVIEW")
    print(len(replacement_entities["REVIEW"]))
    print("CHARACTER")
    print(len(replacement_entities["CHARACTER"]))
    print("RATING")
    print(len(replacement_entities["RATING"]))
    print("RATINGS_AVERAGE")
    print(len(replacement_entities["RATINGS_AVERAGE"]))
    print("TRAILER")
    print(len(replacement_entities["TRAILER"]))

    replaced_items=[]
    replaced_item=[]
    data=dataset[support_id]
    datainfo=data["support"]
    for item in datainfo:
        replaced_item = replace_entities_with_tokens(item, "ACTOR", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "YEAR", replacement_entities) 
        replaced_item = replace_entities_with_tokens(replaced_item, "TITLE", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "GENRE", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "DIRECTOR", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "SONG", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "PLOT", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "REVIEW", replacement_entities) 
        replaced_item = replace_entities_with_tokens(replaced_item, "CHARACTER", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "RATING", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "RATINGS_AVERAGE", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "TRAILER", replacement_entities)
        replaced_items.append(replaced_item)

    print(len(replaced_items))
    with open(outputfile,"a") as f:
        for item in replaced_items:
            f.write(json.dumps(item)+"\n")

def replace_mitrest_entities_with_file(inputfile,outputfile,support_id): 
    replacement_entities = {
                "Rating":[],
                "Amenity":[],
                "Location":[],
                "Restaurant_Name":[],
                "Price":[],
                "Hours":[],
                "Dish":[],
                "Cuisine":[],
            }

    dataset = []
    with open(inputfile) as f:
        for line in f:
            line = json.loads(line)
            dataset.append(line)
    print(len(dataset))
    data=dataset[support_id]
    datainfo=data["support"]
    for i in range(len(datainfo)):
        entity_deal=datainfo[i]["entity"]
        for en in entity_deal:
            start,end=en["offset"]
            en_len=end-start-1

            if en["type"]=="Rating":
                replacement_entities["Rating"].append(en)
            elif en["type"]=='Amenity':
                replacement_entities["Amenity"].append(en)
            elif en["type"]=='Location':
                replacement_entities["Location"].append(en)
            elif en["type"]=='Restaurant_Name':
                replacement_entities["Restaurant_Name"].append(en)
            elif en["type"]=='Price':
                replacement_entities["Price"].append(en)
            elif en["type"]=='Hours':
                replacement_entities["Hours"].append(en)
            elif en["type"]=="Dish":
                replacement_entities["Dish"].append(en)
            else:
                replacement_entities["Cuisine"].append(en)
    print("Rating")
    print(len(replacement_entities["Rating"]))
    print("Amenity")
    print(len(replacement_entities["Amenity"]))
    print("Location")
    print(len(replacement_entities["Location"]))
    print("Restaurant_Name")
    print(len(replacement_entities["Restaurant_Name"]))
    print("Price")
    print(len(replacement_entities["Price"]))
    print("Hours")
    print(len(replacement_entities["Hours"]))
    print("Dish")
    print(len(replacement_entities["Dish"]))
    print("Cuisine")
    print(len(replacement_entities["Cuisine"]))

    replaced_items=[]
    replaced_item=[]
    data=dataset[support_id]
    datainfo=data["support"]
    for item in datainfo:
        replaced_item = replace_entities_with_tokens(item, "Rating", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "Amenity", replacement_entities) 
        replaced_item = replace_entities_with_tokens(replaced_item, "Location", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "Restaurant_Name", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "Price", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "Hours", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "Dish", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "Cuisine", replacement_entities)
        replaced_items.append(replaced_item)

    print(len(replaced_items))
    with open(outputfile,"a") as f:
        for item in replaced_items:
            f.write(json.dumps(item)+"\n")

def replace_re3d_entities_with_file(inputfile,outputfile,support_id): 
    replacement_entities = {
                "Organisation":[],
                "Temporal":[],
                "Nationality":[],
                "Location":[],
                "Person":[],
                "DocumentReference":[],
                "Money":[],
                "Quantity":[],
                "MilitaryPlatform":[],
                "Weapon":[],
            }

    dataset = []
    with open(inputfile) as f:
        for line in f:
            line = json.loads(line)
            dataset.append(line)
    print(len(dataset))
    data=dataset[support_id]
    datainfo=data["support"]
    for i in range(len(datainfo)):
        entity_deal=datainfo[i]["entity"]
        for en in entity_deal:
            start,end=en["offset"]
            en_len=end-start-1

            if en["type"]=="Organisation":
                replacement_entities["Organisation"].append(en)
            elif en["type"]=='Temporal':
                replacement_entities["Temporal"].append(en)
            elif en["type"]=='Nationality':
                replacement_entities["Nationality"].append(en)
            elif en["type"]=='Location':
                replacement_entities["Location"].append(en)
            elif en["type"]=='Person':
                replacement_entities["Person"].append(en)
            elif en["type"]=='DocumentReference':
                replacement_entities["DocumentReference"].append(en)
            elif en["type"]=="Money":
                replacement_entities["Money"].append(en)
            elif en["type"]=='Quantity':
                replacement_entities["Quantity"].append(en)
            elif en["type"]=='MilitaryPlatform':
                replacement_entities["MilitaryPlatform"].append(en)
            else:
                replacement_entities["Weapon"].append(en)
    print("Organisation")
    print(len(replacement_entities["Organisation"]))
    print("Temporal")
    print(len(replacement_entities["Temporal"]))
    print("Nationality")
    print(len(replacement_entities["Nationality"]))
    print("Location")
    print(len(replacement_entities["Location"]))
    print("Person")
    print(len(replacement_entities["Person"]))
    print("DocumentReference")
    print(len(replacement_entities["DocumentReference"]))
    print("Money")
    print(len(replacement_entities["Money"]))
    print("Quantity")
    print(len(replacement_entities["Quantity"]))
    print("MilitaryPlatform")
    print(len(replacement_entities["MilitaryPlatform"]))
    print("Weapon")
    print(len(replacement_entities["Weapon"]))

    replaced_items=[]
    replaced_item=[]
    data=dataset[support_id]
    datainfo=data["support"]
    for item in datainfo:
        replaced_item = replace_entities_with_tokens(item, "Organisation", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "Temporal", replacement_entities) 
        replaced_item = replace_entities_with_tokens(replaced_item, "Nationality", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "Location", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "Person", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "DocumentReference", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "Money", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "Quantity", replacement_entities) 
        replaced_item = replace_entities_with_tokens(replaced_item, "MilitaryPlatform", replacement_entities)
        replaced_item = replace_entities_with_tokens(replaced_item, "Weapon", replacement_entities)
        replaced_items.append(replaced_item)      

    print(len(replaced_items))
    with open(outputfile,"a") as f:
        for item in replaced_items:
            f.write(json.dumps(item)+"\n")


def writeOriginal(inputfile,outputfile,support_id):
    dataset = []
    with open(inputfile) as f:
        for line in f:
            line = json.loads(line)
            dataset.append(line)
    data=dataset[support_id]
    datainfo=data["support"]
    with open(outputfile,"a") as f:
        for item in datainfo:  
            f.write(json.dumps(item)+"\n")






if __name__ == "__main__":  
    # dataset="CoNLL" 
    # dataset="mit-movie1"
    # dataset="mit-movie2"
    # dataset="mit-rest"
    dataset="re3d"
    # dataset="WNUT17"
    K_num=1 
    mutiNum=4  
    i=0  
    supportNum=10  
    inputfile="./data/"+dataset+"/"+str(K_num)+"shot.json"
   
    print("**************"+inputfile+"**************************")
    middlePath="./dataMiddle/"+dataset+"/"
    outputPath="./dataNew/"+dataset+"/"
    
    if not os.path.exists(middlePath):
        os.makedirs(middlePath)
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
    middlefile=middlePath+str(K_num)+"shot_needDeal.json"  
    outputfile=outputPath+str(K_num)+"shot.json"   
    
    open(middlefile,"w").close()
    open(outputfile,"w").close()
    if dataset=="CoNLL":
        num=4*K_num*mutiNum  
        for i in range(supportNum):
            open(middlefile,"w").close()  
            writeOriginal(inputfile,middlefile,i)  
            for j in range(mutiNum):
                replace_CONLL_entities_with_file(inputfile,middlefile,i)
            changeTosupport(dataset,num,middlefile,outputfile) 
    elif dataset=="mit-movie1":
        num=12*K_num*mutiNum 
        for i in range(supportNum):
            open(middlefile,"w").close()  
            writeOriginal(inputfile,middlefile,i)  
            for j in range(mutiNum):
                replace_mitmovie1_entities_with_file(inputfile,middlefile,i)
            changeTosupport(dataset,num,middlefile,outputfile) 
    elif dataset=="mit-movie2":
        num=12*K_num*mutiNum 
        for i in range(supportNum):
            open(middlefile,"w").close()  
            writeOriginal(inputfile,middlefile,i)  
            for j in range(mutiNum):
                replace_mitmovie2_entities_with_file(inputfile,middlefile,i)
            changeTosupport(dataset,num,middlefile,outputfile) 
    elif dataset=="mit-rest":
        num=8*K_num*mutiNum  
        for i in range(supportNum):
            open(middlefile,"w").close()  
            writeOriginal(inputfile,middlefile,i)  
            for j in range(mutiNum):
                replace_mitrest_entities_with_file(inputfile,middlefile,i)
            changeTosupport(dataset,num,middlefile,outputfile) 
    elif dataset=="re3d":   
        num=10*K_num*mutiNum 
        for i in range(supportNum):
            open(middlefile,"w").close() 
            writeOriginal(inputfile,middlefile,i)  
            for j in range(mutiNum):
                replace_re3d_entities_with_file(inputfile,middlefile,i)
            changeTosupport(dataset,num,middlefile,outputfile) 
    elif dataset=="WNUT17":
        num=6*K_num*mutiNum  
        for i in range(supportNum):
            open(middlefile,"w").close()  
            writeOriginal(inputfile,middlefile,i)  
            for j in range(mutiNum):
                replace_WNUT17_entities_with_file(inputfile,middlefile,i)
            changeTosupport(dataset,num,middlefile,outputfile) 
    with open(middlefile,"r") as f:
        i=0
        for line in f:
            i=i+1
    print("i",i)
    num=i//10
    print("num:",num)