file=open("./telugu_annotated.txt", "r")
data=file.read()
sent=data.split("---------------------------------")
# print(sent)
for each_sent in sent:
    print("------------------------------")
    if each_sent=="":
        continue
    print(each_sent)
    dic={}
    subj_case=""
    obj_case=""
    verb_case=""
    subj_gender=""
    obj_gender=""
    verb_gender=""
    subj_person=""
    obj_person=""
    verb_person=""
    subj_number=""
    obj_number=""
    verb_number=""
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
                                if "SUBJE" in inf[0]:
                                    subj_case=val[1]
                                elif "OBJEC" in inf[0]:
                                    obj_case=val[1]
                                elif "VER" in inf[0]:
                                    verb_case=val[1]
                        if "Gender" in ele:
                                val=ele.split("=")
                                if "SUBJE" in inf[0]:
                                    subj_gender=val[1]
                                elif "OBJEC" in inf[0]:
                                    obj_gender=val[1]
                                elif "VER" in inf[0]:
                                    verb_gender=val[1]
                        if "Number" in ele:
                                val=ele.split("=")
                                if "SUBJE" in inf[0]:
                                    subj_number=val[1]
                                elif "OBJEC" in inf[0]:
                                    obj_number=val[1]
                                elif "VER" in inf[0]:
                                    verb_number=val[1]
                        if "Person" in ele:
                                val=ele.split("=")
                                if "SUBJE" in inf[0]:
                                    subj_person=val[1]
                                elif "OBJEC" in inf[0]:
                                    obj_person=val[1]
                                elif "VER" in inf[0]:
                                    verb_person=val[1]
    if subj_case==obj_case and obj_case==verb_case and subj_case!="":
        print("SUBJECT-VERB-OBJECT CASE AGREE")
    else:
        if subj_case==obj_case and subj_case!="":
            print("SUBJECT-OBJECT CASE AGREE")
        elif subj_case==verb_case and subj_case!="":
            print("SUBJECT-VERB CASE AGREE")
        elif obj_case==verb_case and obj_case!="":
            print("OBJECT-VERB CASE AGREE")

    if subj_number==obj_number and obj_number==verb_number and subj_number!="":
        print("SUBJECT-VERB-OBJECT NUMBER AGREE")
    else:
        if subj_number==obj_number and subj_number!="":
            print("SUBJECT-OBJECT NUMBER AGREE")
        elif subj_number==verb_number and subj_number!="":
            print("SUBJECT-VERB NUMBER AGREE")
        elif obj_number==verb_number and obj_number!="":
            print("OBJECT-VERB NUMBER AGREE")

    if subj_gender==obj_gender and obj_gender==verb_number and subj_gender!="":
        print("SUBJECT-VERB-OBJECT GENDER AGREE")
    else:
        if subj_gender==obj_gender and subj_gender!="":
            print("SUBJECT-OBJECT GENDER AGREE")
        elif subj_gender==verb_gender and subj_gender!="":
            print("SUBJECT-VERB GENDER AGREE")
        elif obj_gender==verb_gender and obj_gender!="":
            print("OBJECT-VERB GENDER AGREE")
    if subj_person==obj_person and obj_person==verb_person and subj_person!="":
        print("SUBJECT-VERB-OBJECT PERSON AGREE")
    else:
        if subj_person==obj_person and subj_person!="":
            print("SUBJECT-OBJECT PERSON AGREE")
        elif subj_person==verb_person and subj_person!="":
            print("SUBJECT-VERB PERSON AGREE")
        elif obj_person==verb_person and obj_person!="":
            print("OBJECT-VERB PERSON AGREE")
    
                                # if val[1] in dic:
                                #     dic[val[1]].append(inf[0][:-1])
                                # else:
                                #     dic[val[1]]=[inf[0][:-1]]