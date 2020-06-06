import json
import itertools
import sys
hrlist_file = open("arhr.json","r",encoding='utf-8')
hr_list = json.load(hrlist_file)
tags_name = []
six_tags_name = []
name_to_level = {}


for i in hr_list:
    name_to_level[i['name']] = i['level']
    if i['hidden']:
        continue
    if i['level'] == 6:
        itags = []
        itags.append(i['type'])
        itags.append(i['sex'])
        for t in i['tags']:
            itags.append(t.replace("干员", "").replace("位", ""))
        six_tags_name.append((i['name'],itags,i['level']))
        continue
    itags = []
    itags.append(i['type'])
    itags.append(i['sex'])
    for t in i['tags']:
        itags.append(t.replace("干员","").replace("位",""))
    tags_name.append((i['name'],itags,i['level']))

def get_gy(tags):
    t_to_n = tags_name
    if '高级资深' in tags or '高级资深干员' in tags :
        t_to_n = six_tags_name
    new_tags = []
    gy_list = []
    for j in tags:
        s = j.replace("干员", "").replace("性", "").replace("位", "")
        new_tags.append(s)
    minlevel = 7
    for i in t_to_n:
        flag = True
        for j in new_tags:
            if j not in i[1]:
                flag = False
                break
        if flag :
            if i[2] >= 3:
                minlevel = min(i[2],minlevel)
            gy_list.append(i[0])
    if minlevel == 7:
        minlevel = 0
    return gy_list,minlevel

def get_gy_with_level(tags):
    if len(tags) > 5:
        return []
    youxiao = []
    for i in range(1,4):
        for tagcomb in itertools.combinations(tags,i):
            tags_ = list(tagcomb)
            gy,minlevel = get_gy(tags_)
            #if minlevel > 3:
            youxiao.append((tags_,gy,minlevel))
    return youxiao

