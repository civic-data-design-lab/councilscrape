'''
with open('2020_nodes.txt', 'r') as reader:
    f = open("2020_nodes1.txt", "w")
    first_line=reader.readline()
    second_line=reader.readline()
    f.write(first_line)
    f.write(second_line)
    diff_ids=reader.readline()
    separated_articles=diff_ids.split(", {")
    for article in separated_articles:
        written="{"+article+",\n"
        f.write(written)
    third_line=reader.readline()
    bracket_line=reader.readline()
    f.write(third_line)
    f.write(bracket_line)


my_dict="{'my_id':'hello','yeet':'yah'}"
my_dict=eval(my_dict)
print(my_dict.keys())
'''

with open('2020_nodes.txt', 'r') as reader:
    my_dict=reader.read()
    my_dict=eval(my_dict)
    my_set=set()
    links={"links":[]}
    f = open("2020_nodes2.txt", "w")
    for entry in my_dict['nodes']:
        counter=0
        if entry["id"] not in my_set:
            f.write(str(entry)+",\n")
            my_set.add(entry["id"])
        else: 
            new_entry={}
            new_entry["id"]=entry["id"]+str(counter)
            new_entry["topic"]=entry["topic"]
            f.write(str(new_entry)+",\n")
            link={}
            link["source"]=entry["id"]
            link["target"]=new_entry["id"]
            link["value"]=1
            links["links"].append(link)
            counter+=1
    f.write("],\n")
    for link in links["links"]:
        f.write(str(link)+",\n")
