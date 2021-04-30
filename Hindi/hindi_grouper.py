file=open("./hindi_annotated.txt", "r")
data=file.read()
sent=data.split("---------------------------------")
# print(sent)
for each_sent in sent:
    dic={}
    lines=each_sent.split("\n")
    for each_line in lines:
        if each_line=='':
            continue
        if each_line[0]=="(":
                # print(each_line)
                inf=each_line.split("-")
                li=inf[1]
                ls=li.split("|")
                for ele in ls:
                        if "Case" in ele:
                                val=ele.split("=")
                                if val[1] in dic:
                                    dic[val[1]].append(inf[0][:-1])
                                else:
                                    dic[val[1]]=[inf[0][:-1]]
    print(dic)