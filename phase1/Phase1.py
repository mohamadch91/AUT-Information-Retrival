#!/usr/bin/env python
# coding: utf-8

# # Information retrival project phase 1

# ## Import libraries

# In[228]:


from hazm import *
from __future__ import unicode_literals
# from parsivar import *
import json
import string
from hazm import stopwords_list
from copy import copy
from matplotlib import pyplot as plt

import math


# ## Reading Json file

# In[229]:


file=open("IR_data_news_12k.json")
data=json.load(file)


# ## create empty arrays to store contents

# In[230]:


data_content=[]
data_url=[]
data_title=[]


# ## store content in arrays 

# In[231]:


for i in range(len(data)):
    index=str(i)
    data_content.append(data[""+index]["content"])
    data_url.append(data[""+index]["url"])
    data_title.append(data[""+index]["title"])


# In[232]:


#comment after complete
# data_content=data_content[:500]


# ## define new array for tokenize

# In[233]:


data_tokens=[]


# # preproccesing start

# ## normalize contents
# tokenize and stemmer and lematize

# In[234]:


normalizer = Normalizer()
stemmer = Stemmer()
stop_words=set(stopwords_list())
stop_words.add('\u200cو')
stop_words.add('\u200cو')
stop_words.add('و\u200c')
lemmatizer = Lemmatizer()


# ## define punctuations

# In[235]:


punctuations=string.punctuation 
temp_list=set()
for i in punctuations:
    temp_list.add(i)
temp_list.add('،')
temp_list.add('.')
temp_list.add(':')
punctuations=temp_list.copy()


# ### loop over te content and preprocess

# ## counting for reports

# In[236]:


word_count=0
tokens_num=[]


# In[237]:


for j in range (len(data_content)):
    data_content[j]=normalizer.normalize(data_content[j])
    new_contents=word_tokenize(data_content[j])
    tokens_num.append(math.log(len(new_contents)))
    word_count+=len(new_contents)
    temp_contents=copy(new_contents)
    for k in range(len(temp_contents)):
        if(temp_contents[k] in stop_words):
            new_contents.remove(temp_contents[k])    
        if(temp_contents[k] in punctuations):
            new_contents.remove(temp_contents[k])
    for k in range(len(new_contents)):
        new_contents[k]=lemmatizer.lemmatize(new_contents[k])
#         new_contents[k]=stemmer.stem(new_contents[k])

    data_tokens.append(new_contents)            
            
            


# ### indexing words 
# making words indexing in contents

# empty set for tokens index

# In[239]:


final_token=dict()


# ## iterate over content and tokens 
# find tokens index in each content and <br>
# find tokens count in each content<br>
# calculate tokens number in contents 

# In[240]:


for i in range(len(data_tokens)):
    for j in range(len(data_tokens[i])):
        if(data_tokens[i][j] in final_token):
            temp_string=final_token[data_tokens[i][j]]
            last_content=temp_string.split("|")
            no=int(last_content[len(last_content)-1].split(":")[0].split("c")[1])
            if(no==i):
                count=last_content[len(last_content)-1].split(":")
                temp_count=int(count[len(count)-1].split("_")[1])
                temp_count+=1
                new_string=""
                for s in range(len(last_content)-1):
                    new_string+=last_content[s]+"|"
#                 print(last_content[len(last_content)-1])
                last_item=last_content[len(last_content)-1].split("_")[0]+","+str(j)+"_"+str(temp_count)+"_"
                new_string+=last_item
                final_token[data_tokens[i][j]]=new_string
            else: 
                final_token[data_tokens[i][j]]+="|"+"c"+str(i)+":"+str(j)+"_1_"
        else:
            final_token[data_tokens[i][j]]="|"+"c"+str(i)+":"+str(j)+"_1_"
            
            


# ## counting tokens for report

# In[241]:


len(final_token)


# # User input Query
# get input from user to proccess query
# 

# In[296]:


query=input("please enter your input : ")


# ##### procces input

# ###### define list for searched wirds

# In[297]:


selected_words=[]


# #### define string for handle double quete (" ")
# <br>
# define boolean for handle !

# In[298]:


query.split(" ")
temp_string=""
forbidden=False
query_tokens=set()
forbiddens=set()


# In[299]:


for word in query.split(" "):
    if(word==''):
        continue
    if(word[0]=='"'):
        temp_string+=word[1:]+" "
        continue
    if(temp_string!=""):
        if(word[len(word)-1]=='"'):
            temp_string+=word[:len(word)-1]
            query_tokens.add(temp_string)
            temp_string=""
        else:
            temp_string+=word+" "
        continue
    if(word=="!"):
        forbidden=True
        continue
    if(forbidden):
        forbiddens.add(word)
        forbidden=False
        continue
    query_tokens.add(word)    


# ### finding query terms in tokens
# search in dic <br>
# and get token indexes

# In[300]:


query_dic=[]
forbidden_dic=[]


# In[301]:


for word in query_tokens:
        if(len(word.split(" "))==1):
            if(word in final_token and word not in stop_words):
                query_dic.append(final_token[word])
        else:
            qute=[]
            words=word.split(" ")
            for x in words:
                if(x in final_token and x not in stop_words):
                    qute.append(final_token[x])      
            query_dic.append(qute)  
for k in forbiddens:
    if(k in final_token):
        forbidden_dic.append(final_token[k])


# #### searching docs

# In[302]:


docs_point={}
for address in query_dic:
        if(type(address) is list):
            intersection=[]
            flag=False
            for x in address:
                if(len(intersection)==0):
                    intersection.append(x)
                else:
                    intersection_dic={}
                    x_dic={}
                    answer={}
                    inter_doc=intersection[0].split("|")
                    inter_doc=inter_doc[1:]
                    
                    for j in inter_doc:
                        docno=j.split(":")[0]
                        indexes=j.split(":")[1]
                        intersection_dic[docno]=indexes
                    x_doc=x.split("|")
                    x_doc=x_doc[1:]
                    for j in x_doc:
                        x_docno=j.split(":")[0]
                        x_index=j.split(":")[1]
                        x_dic[x_docno]=x_index
                    for key in intersection_dic.keys():
                        if(key in x_dic):
                            inter_index=intersection_dic[key].split("_")[0].split(",")
                            x_index=x_dic[key].split("_")[0].split(",")
                            for s in inter_index:
                                for m in x_index:
                                    index_no_inter=int(s)
                                    index_no_x=int(m)
                                    dif=index_no_x-index_no_inter
                                    if(dif==1):
                                        if(key in answer):
                                            ans_index=answer[key]
                                            ans_count=int(ans_index.split("_")[1])
                                            ans_indexes=ans_index.split("_")[0]
                                            ans_indexes+=","+str(m)
                                            ans_count+=1
                                            temp_ans=ans_indexes+"_"+str(ans_count)+"_"
                                            answer[key]=temp_ans
                                        else:
                                            answer[key]=str(m)+"_1_"
                    temp_s=""     
#                     print(answer)
                    for key in answer.keys():
                        temp_s+="|"+key+":"+answer[key]
                    answer.clear()
                    flag=True
                    intersection.clear()
                    intersection.append(temp_s)   
            if(flag):        
                docs=intersection[0].split("|")
                for x in docs:
                    if(x!=''):
                        docid=x.split(":")[0].split("c")[1]
                        count=x.split(":")[1].split("_")
                        count=int(count[len(count)-2])
                        if(docid in docs_point):
                            docs_point[docid]+=count*100
                        else:
                             docs_point[docid]=count*100
            


# In[303]:


for address in query_dic:
        if(type(address) is not list):
            docs=address.split("|")
            for x in docs:
                if(x!=''):
                    docid=x.split(":")[0].split("c")[1]
                    count=x.split(":")[1].split("_")
                    count=int(count[len(count)-2])
                    if(docid in docs_point):
                        docs_point[docid]+=count
                    else:
                         docs_point[docid]=count


# ### check ! for remove from answers

# In[304]:


for address in forbidden_dic:
    doc_id=address.split("|")
    for x in doc_id:
        if(x!=''):
            docid=x.split(":")[0].split("c")[1]
            if(docid in docs_point):
                docs_point.pop(docid)


# ### print answers

# In[305]:


# data_content=[]
# data_url=[]
# data_title=[]
final_answer=[]
if(len(docs_point)==0):
    print("no answer found for your query")  
else:
    if(len(docs_point)>=5):
        for i in range(5):
            maximum=0
            max_id=""
            for docid in docs_point.keys():
                if(docs_point[docid]>maximum):
                    maximum=docs_point[docid]
                    max_id=docid
            final_answer.append(max_id)
            docs_point.pop(max_id)
    else:
         for i in range(len(docs_point)):
            maximum=0
            max_id=""
            for docid in docs_point.keys():
                if(docs_point[docid]>maximum):
                    maximum=docs_point[docid]
                    max_id=docid
            final_answer.append(max_id)
            docs_point.pop(max_id)
    count=0    
    for k in final_answer:
        docid=int(k)
        print("answer "+str(count+1)+": ")
        print("title: "+data_title[docid])
        print("url: "+data_url[docid])
        print(docid)
        print(data_content[docid])
        count+=1
        


# #### calculate terms number in contents for report

# In[306]:


tokens_count={}
for j in final_token.keys():
    count=0
    string=final_token[j]
    for x in string.split("|")[1:]:
        num=int(x.split("_")[1])
        count+=num
    tokens_count[j]=count
z=list(range(1,len(tokens_count)+1))    


# In[ ]:


max_array=[]

for j in range(len(tokens_count)):
    maximum=0
    selected=""
    for x in tokens_count.keys():
        if(tokens_count[x]>maximum):
            maximum=tokens_count[x]
            selected=x        
    max_array.append(maximum)
    tokens_count.pop(selected)


# In[ ]:


for l in range(len(z)):
    z[l]=math.log(z[l])   
for k in range(len(max_array)):
    max_array[k]=math.log(max_array[k])
  
plt.plot(z,max_array)
plt.show()


# ## counting tokens of each content for report 

# In[173]:



zz=list(range(1,len(tokens_num)+1))    


# In[174]:


for l in range(len(zz)):
    zz[l]=math.log(zz[l])
for k in range(1,len(tokens_num)):
    tokens_num[k]+=tokens_num[k-1]
for k in range(len(tokens_num)):
    tokens_num[k]=math.log((tokens_num[k]))
    
plt.plot(zz,tokens_num)
plt.show()

