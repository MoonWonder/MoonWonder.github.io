import json
import os
import frontmatter


dict = {}
dict["refrence"] = {}
dict["alias"] = {}


def read_to_config(str):
    article = open(str, encoding='UTF-8').read()
    j = 0
    # print(str)
    while article.find("@import \"", j) != -1:
        s = ""
        j = article.find("@import \"",j)
        while article[j] != "\"":
            j = j + 1
        j = j + 1
        while article[j] != "\"":
            s = s + article[j]
            j = j + 1
        # print(str)
        # print(s)
        if dict["refrence"].get(str, [111]) == [111]:
            dict["refrence"][str] = [s]
        else:
            dict["refrence"][str].append(s)


def get_alias(str):
    post = frontmatter.load(str)
    if post.get("alias", [111]) != [111]:
        dict["alias"][str] = post["alias"]


for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        path = os.path.join(root, name)
        x = os.path.splitext(path)
        # print(x[1])
        if x[1] == ".md":
            get_alias(path)
        # print(os.path.join(root, name))

for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        path = os.path.join(root, name)
        x = os.path.splitext(path)
        # print(x[1])
        if x[1] == ".md":
            read_to_config(path)
        # print(os.path.join(ss, name))
        # print(os.path.join(root, name))
# print(dict)
for key in dict["refrence"]:
    dict["refrence"][key]=list(set(dict["refrence"][key]));
str = json.dumps(dict, sort_keys=True, indent=4, separators=(',', ': '))
f = open("./config.json", "w")
f.write(str)
f.close()
