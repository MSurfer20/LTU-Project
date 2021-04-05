import stanza

def get_dependencies(doc, n):
    """Get dependencies in the format of a list of
    (token, deprel, dependent_token) pairs- 
    for all 'n' sentences in doc"""

    def getdeps(i):
        deps = []
        for head, rel, dep in doc.sentences[i].dependencies:
            deps.append((head.id, head.text, rel, dep.text, dep.id, head.feats, dep.feats))
        return deps

    return [getdeps(i) for i in range(n)]


def get_pos_tags(doc, n):
    """Get POS-tagged tokens in the format of a list of 
    (token, POStag) pairs for all sentences in doc.
    Returns upos (Universal part-of-speech) tag only, not 
    xpos (treebank-specific part of speech)"""

    def getpos(i):
        tokens = []
        for token in doc.sentences[i].words:
            tokens.append((token.id, token.text, token.upos))
        return tokens

    return [getpos(i) for i in range(n)]

def check_subject_object(dependency, pos_tag):
    global sov
    global svo
    global vos
    global vso
    global osv
    global ovs
    global subject_object
    global object_subject  
    verb_indexes={}
    print("---------------------------------")
    for lemma in dependency:
        if lemma[2]=='root':
            verb_indexes[lemma[4]]=[-1, -1, "", "", lemma[1], "", "", "", -1] # subj index, object index, subj lemma, obj lemma, verb lemma, subj feats, verb feats, obj feats
    # for lemma in pos_tag:
    #     if lemma[0]=="is" or lemma[1]=="is" or lemma[2]=="is":
    #         print(lemma,"LOLLLLLLLLLLLLLLLLLLLLLL")
    #         SystemExit()
    #     if lemma[2]=='VERB':
    #         verb_indexes[lemma[0]]=[-1, -1, "", "", lemma[1], "", "", "", -1] # subj index, object index, subj lemma, obj lemma, verb lemma, subj feats, verb feats, obj feats
    for lemma in dependency:
        if 'nsubj' in lemma[2] or 'csubj' in lemma[2]:
            if not (lemma[0] in verb_indexes):
                continue
            verb_indexes[lemma[0]][0]=lemma[4]
            # print(dir(lemma[4]))
            verb_indexes[lemma[0]][2]=lemma[3]
            verb_indexes[lemma[0]][5]=lemma[6]
            verb_indexes[lemma[0]][6]=lemma[5]
            
        if 'obj' in lemma[2]:
            if not (lemma[0] in verb_indexes):
                continue
            verb_indexes[lemma[0]][1]=lemma[4]
            verb_indexes[lemma[0]][3]=lemma[3]
            verb_indexes[lemma[0]][7]=lemma[6]
            # verb_indexes[lemma[0]][6]=lemma[5]
        if 'ccomp' in lemma[2]:
            if not (lemma[0] in verb_indexes):
                continue
            verb_indexes[lemma[0]][1]=lemma[4]
            verb_indexes[lemma[0]][3]=lemma[3]
            verb_indexes[lemma[0]][7]=lemma[6]

        if 'xcomp' in lemma[2]:
            if not (lemma[0] in verb_indexes):
                continue
            verb_indexes[lemma[0]][1]=lemma[4]
            verb_indexes[lemma[0]][3]=lemma[3]
            verb_indexes[lemma[0]][7]=lemma[6]

        # if 'advcl' in lemma[2]:
        #     if not (lemma[0] in verb_indexes):
        #         continue
        #     if verb_indexes[lemma[0]][1]!=-1:
        #         continue
        #     verb_indexes[lemma[0]][1]=lemma[4]
    sentence=""
    v_count=1
    s_count=0
    o_count=0
    for index, lemma in enumerate(pos_tag):
        for v in verb_indexes:
            if v==index+1:
                verb_indexes[v][8]=v_count
                v_count+=1
    for index, lemma in enumerate(pos_tag):
        flag=0
        for v in verb_indexes:
            if v==index+1:
                sentence+=str(lemma[1])+f"(VERB{verb_indexes[v][8]})"+" "
                v_count+=1
                flag=1
                # print(sentence+"1")
            elif verb_indexes[v][0]==index+1:
                sentence+=str(lemma[1])+f"(SUBJECT{verb_indexes[v][8]})"+" "
                flag=1
                s_count+=1
                # print(sentence+"2")

            elif verb_indexes[v][1]==index+1:
                sentence+=str(lemma[1])+f"(OBJECT{verb_indexes[v][8]})"+" "
                flag=1
                o_count+=1
                # print(sentence+"3")
        if flag==0:
            sentence+=lemma[1]+" "
        # else:
        #     v_count+=1
    print(sentence)
    for index, lemma in enumerate(pos_tag):
        flag=0
        for v in verb_indexes:
            if v==index+1:
                # sentence+=str(lemma[1])+f"(VERB{verb_indexes[v][8]})"+" "
                if verb_indexes[v][6] is None:
                    a=f"(VERB{verb_indexes[v][8]})"+" - "
                else:    
                    a=f"(VERB{verb_indexes[v][8]})"+" - "+verb_indexes[v][6]
                print(a)
                # print(sentence+"1")
            elif verb_indexes[v][0]==index+1:
                if verb_indexes[v][5] is None:
                    a=f"(SUBJECT{verb_indexes[v][8]})"+" - "
                else:    
                    a=f"(SUBJECT{verb_indexes[v][8]})"+" - "+verb_indexes[v][5]
                print(a)

            elif verb_indexes[v][1]==index+1:
                if verb_indexes[v][7] is None:
                    a=f"(OBJECT{verb_indexes[v][8]})"+" - "
                else:    
                    a=f"(OBJECT{verb_indexes[v][8]})"+" - "+verb_indexes[v][7]
                print(a)
        if flag==0:
            sentence+=lemma[1]+" "

    for key in verb_indexes:
        if verb_indexes[key][0]==-1 or verb_indexes[key][1]==-1:
            continue
        subj_index=verb_indexes[key][0]
        obj_index=verb_indexes[key][1]
        verb_index=key
        if subj_index<obj_index and subj_index<verb_index:
            if obj_index<verb_index:
                file1 = open("english_sov.txt", "a")  # append mode 
                file1.write(sent+verb_indexes[key][2]+ " "+ verb_indexes[key][3]+" "+verb_indexes[key][4] +"\n") 
                file1.close() 
                sov+=1
                print("SOV")
            else:
                file1 = open("english_svo.txt", "a")  # append mode 
                file1.write(sent+verb_indexes[key][2]+ " "+ verb_indexes[key][3]+" "+verb_indexes[key][4] +"\n") 
                file1.close() 
                svo+=1
                print("SVO")
        elif verb_index<subj_index and verb_index<obj_index:
            if obj_index<subj_index:
                file1 = open("english_vos.txt", "a")  # append mode 
                file1.write(sent+verb_indexes[key][2]+ " "+ verb_indexes[key][3]+" "+verb_indexes[key][4] +"\n") 
                file1.close() 
                vos+=1
                print("VOS")
            else:
                file1 = open("english_vso.txt", "a")  # append mode 
                file1.write(sent+verb_indexes[key][2]+ " "+ verb_indexes[key][3]+" "+verb_indexes[key][4] +"\n") 
                file1.close() 
                vso+=1
                print("VSO")
        else:
            if subj_index<verb_index:
                file1 = open("english_osv.txt", "a")  # append mode 
                file1.write(sent+verb_indexes[key][2]+ " "+ verb_indexes[key][3]+" "+verb_indexes[key][4] +"\n") 
                file1.close() 
                osv+=1
                print("OSV")
            else:
                file1 = open("english_ovs.txt", "a")  # append mode 
                file1.write(sent+verb_indexes[key][2]+ " "+ verb_indexes[key][3]+" "+verb_indexes[key][4] +"\n") 
                file1.close() 
                ovs+=1
                print("OVS")
        if subj_index<obj_index:
            file1 = open("english_subj_obj.txt", "a")  # append mode 
            file1.write(sent+verb_indexes[key][2]+ " "+ verb_indexes[key][3]+"\n") 
            file1.close() 
            subject_object+=1
            print("SUBJECT OBJECT")
        else:
            file1 = open("english_obj_subj.txt", "a")  # append mode 
            file1.write(sent+verb_indexes[key][2]+ " "+ verb_indexes[key][3]+"\n") 
            file1.close() 
            object_subject+=1
            print("OBJECT SUBJECT")
    print("---------------------------------")
    

def check_genitives(dependency, pos_tag, sent):
    global genitive_noun
    global noun_genitive
    poss_dictionary=["from", 'of']
    for lemma in dependency:
        if 'nmod:poss' in lemma[2] and (pos_tag[lemma[0]-1][2]=='NOUN' or pos_tag[lemma[0]-1][2]=='PRON' or pos_tag[lemma[0]-1][2]=='PROPN'):
            # print("---------------")
            # print(lemma)
            # print(dependency)
            # print("-----------------")
            if lemma[0]<lemma[4]:
                file1 = open("english_noun_genitive.txt", "a")  # append mode 
                file1.write(sent+str(lemma)+"\n") 
                file1.close() 
                noun_genitive+=1
            else:
                # print(sent)
                # print(lemma)
                file1 = open("english_genitive_noun.txt", "a")  # append mode 
                file1.write(sent+str(lemma)+"\n") 
                file1.close() 
                genitive_noun+=1
            continue
        if ('nmod' in lemma[2] and (pos_tag[lemma[0]-1][2]=='NOUN' or pos_tag[lemma[0]-1][2]=='PRON' or pos_tag[lemma[0]-1][2]=='PROPN')):
            # print("---------------")
            # print(lemma)
            # print(dependency)
            # print("-----------------")
            for lemma1 in dependency:
                if lemma1[0]==lemma[4] and lemma1[3] in poss_dictionary:
                    if lemma[0]<lemma[4]:
                        file1 = open("english_noun_genitive.txt", "a")  # append mode 
                        file1.write(sent+str(lemma)+"\n") 
                        file1.close() 
                        noun_genitive+=1
                    else:
                        # print(sent)
                        # print(lemma)
                        genitive_noun+=1
                        file1 = open("english_genitive_noun.txt", "a")  # append mode 
                        file1.write(sent+str(lemma)+"\n") 
                        file1.close() 

def check_prep_post(dependency, pos_tag, sent):
    global preposition
    global postposition
    for lemma in dependency:
        if lemma[2]=='case' and (pos_tag[lemma[0]-1][2]=='NOUN' or pos_tag[lemma[0]-1][2]=='PRON' or pos_tag[lemma[0]-1][2]=='PROPN') and pos_tag[lemma[4]-1][2]=='ADP':
            # print("---------------")
            # print(lemma)
            # print(dependency)
            # print("-----------------")
            if lemma[0]>lemma[4]:
                # print("PREPPP", lem
                # akshilesh(subjma)
                preposition+=1
                file1 = open("english_prep.txt", "a")  # append mode 
                file1.write(sent+str(lemma)+"\n") 
                file1.close() 
            else:
                # print("POSTTT", lemma)
                # print(sent)
                # print(lemma)
                file1 = open("english_post.txt", "a")  # append mode 
                file1.write(sent+str(lemma)+"\n") 
                file1.close() 
                postposition+=1

def check_adjective(dependency, pos_tag, sent):
    global noun_adjective
    global adjective_noun
    for lemma in dependency:
        if lemma[2]=='amod' and (pos_tag[lemma[0]-1][2]=='NOUN' or pos_tag[lemma[0]-1][2]=='PRON' or pos_tag[lemma[0]-1][2]=='PROPN'):
            # print("---------------")
            # print("-----------------")
            if lemma[0]>lemma[4]:
                # print((sent.strip()))
                # print(lemma)
                file1 = open("english_adj_noun.txt", "a")  # append mode 
                file1.write(sent+str(lemma)+"\n") 
                file1.close() 
                adjective_noun+=1
            else:
                file1 = open("english_noun_adj.txt", "a")  # append mode 
                file1.write(sent+str(lemma)+"\n") 
                file1.close() 
                noun_adjective+=1

def check_adverb(dependency, pos_tag, sent):
    global verb_adverb
    global adverb_verb
    for lemma in dependency:
        if (lemma[2]=='advmod' or lemma[2]=="advcl") and (pos_tag[lemma[0]-1][2]=='VERB' or pos_tag[lemma[0]-1][2]=='AUX'):
            if lemma[0]>lemma[4]:
                adverb_verb+=1
                # print((sent.strip()))
                # print(lemma)
                file1 = open("english_adverb_verb.txt", "a")  # append mode 
                file1.write(sent+str(lemma)+"\n") 
                file1.close() 
            else:
                # print((sent.strip()))
                # print(lemma)
                file1 = open("english_verb_adverb.txt", "a")  # append mode 
                file1.write(sent+str(lemma)+"\n") 
                file1.close() 
                verb_adverb+=1

def check_aux(dependency, pos_tag):
    global verb_aux
    global aux_verb
    for lemma in dependency:
        if lemma[2]=='aux':
            # print("---------------")
            # print(lemma)
            # print(dependency)
            # print("-----------------")
            if lemma[0]>lemma[4]:
                file1 = open("english_aux_verb.txt", "a")  # append mode 
                file1.write(sent+str(lemma)+"\n") 
                file1.close() 
                aux_verb+=1
            else:
                # print((sent.strip()))
                # print(lemma)
                file1 = open("english_verb_aux.txt", "a")  # append mode 
                file1.write(sent+str(lemma)+"\n") 
                file1.close() 
                verb_aux+=1

def check_pos(pos_tag):
    for i in range(len(pos_tag)-1):
        if((pos_tag[i][2], pos_tag[i+1][2]) in pos_tag_dict):
            pos_tag_dict[(pos_tag[i][2], pos_tag[i+1][2])]+=1
        else:
            pos_tag_dict[(pos_tag[i][2], pos_tag[i+1][2])]=1
            

    

# ==== MAIN: English ====

data_file = open("./hindi_data.txt", "r")
nlp_en = stanza.Pipeline('hi') # This sets up a default neural pipeline in English
# doc = nlp_en("Barack Obama was born in Hawaii.  He was elected president in 2008.")
# this prints the dependencies in a human-readable format
# ==== MAIN: Hindi ====

# this sets up a default neural pipeline for Hindi

#check sov and svo counts
sov=0
svo=0
vos=0
vso=0
osv=0
ovs=0
subject_object=0
object_subject=0
genitive_noun=0
noun_genitive=0
preposition=0
postposition=0
noun_adjective=0
adjective_noun=0
verb_adverb=0
adverb_verb=0
aux_verb=0
verb_aux=0
pos_tag_dict={}
english_data_file=open("./hindi_data.txt", "r")
for i in range(702):
    sent=data_file.readline()
    docs = nlp_en(sent)
    dep=(get_dependencies(docs, 1))
    pos=(get_pos_tags(docs, 1))
    # print("---------------------")
    # print(sent)
    # print(dep)
    # print(pos)
    # print("-----------------------")
    check_subject_object(dep[0], pos[0])
    check_genitives(dep[0], pos[0], sent)
    check_prep_post(dep[0], pos[0], sent)
    check_adjective(dep[0], pos[0], sent)
    check_adverb(dep[0], pos[0], sent)
    check_aux(dep[0], pos[0])
    check_pos(pos[0])

pos_tag_dict={k: v for k, v in sorted(pos_tag_dict.items(), key=lambda item: item[1])}

print(pos_tag_dict)
