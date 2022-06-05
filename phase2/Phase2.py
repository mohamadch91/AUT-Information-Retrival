#!/usr/bin/env python
# coding: utf-8

# # phase 2
# 

# ## importing librarie
# 

# In[1]:


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

# In[2]:


file=open("IR_data_news_12k.json")
data=json.load(file)


# ## create empty arrays to store contents
# 

# In[3]:


data_content=[]
data_url=[]
data_title=[]


# ## store content in arrays 

# In[4]:


for i in range(len(data)):
    index=str(i)
    data_content.append(data[""+index]["content"])
    data_url.append(data[""+index]["url"])
    data_title.append(data[""+index]["title"])


# In[5]:


#comment after complete
# data_content=data_content[:10]


# ## define new array for tokenize

# In[6]:


data_tokens=[]


# # preproccesing start

# ## normalize contents
# tokenize and stemmer and lematize

# In[7]:


normalizer = Normalizer()
stemmer = Stemmer()
stop_words=set(stopwords_list())
stop_words.add('\u200cو')
stop_words.add('\u200cو')
stop_words.add('و\u200c')
lemmatizer = Lemmatizer()


# ## define punctuations

# In[8]:


punctuations=string.punctuation 
temp_list=set()
for i in punctuations:
    temp_list.add(i)
temp_list.add('،')
temp_list.add('.')
temp_list.add(':')
punctuations=temp_list.copy()


# ### loop over te content and preprocess

# In[9]:


for j in range (len(data_content)):
    data_content[j]=normalizer.normalize(data_content[j])
    new_contents=word_tokenize(data_content[j])
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
            


# In[ ]:





# ## define function for find Tf

# In[10]:


def find_tf(content,word):
    count=0
    for i in content:
        if(word==i):
            count+=1
      
    return math.log(count)+1


# ### indexing words 
# making words indexing in contents

# #### empty set for tokens index

# In[11]:


final_token=dict()


# ## find Tf for each word and document

# In[12]:


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
                last_item=last_content[len(last_content)-1].split("_")[0]+"_"+str(temp_count)+"_"
                new_string+=last_item
                final_token[data_tokens[i][j]]=new_string
            else: 
                final_token[data_tokens[i][j]]+="|"+"c"+str(i)+":"+str(find_tf(data_tokens[i],data_tokens[i][j]))+"_1_"
        else:
            final_token[data_tokens[i][j]]="|"+"c"+str(i)+":"+str(find_tf(data_tokens[i],data_tokens[i][j]))+"_1_"
            


# In[ ]:





# ##  calculating IDF

# ##### function for calulating IDF

# In[13]:


def idf(string):
    temp_str=len(string.split("|"))-1
    return math.log(len(data_tokens)/temp_str)
        


# In[14]:


for i in final_token:
    final_token[i]+="@"+str(idf(final_token[i]))+"@"


# In[ ]:





# ### make champion list

# In[15]:


temp_token=dict()
for i in final_token:
    string=final_token[i].split("|")[1:]
    idf=final_token[i].split("@")[1]
    new_arr=[]
    if(len(string)>=5):
        for j in range(5):
            maximum=-1
            maxstr=""
            for k in string:
                tf=float(k.split(":")[1].split("_")[0])
                if(maximum<=tf):
                    maximum=tf
                    maxstr=k
            new_arr.append(maxstr)
            string.remove(maxstr)
        ans=""
        for j in new_arr:
            ans+="|"+j
        ans+="@"+idf+"@"    
        temp_token[i]=ans
        
    else:
        temp_token[i]=final_token[i]
            
    


# In[ ]:





# In[16]:


final_token=temp_token


# In[ ]:





# ## make vector for each doc

# In[ ]:





# In[17]:


doc_vector=[]


# In[18]:


for i in range(len(data_tokens)):
    vector=[]
    sum_tf_idf=0
    for j in range(len(data_tokens[i])):
        term=data_tokens[i][j]
        term_data=final_token[term]
        
        tf_idf=-1
#         print(term_data.split("@")[len(term_data.split("@"))-2]
        idf=float(term_data.split("@")[len(term_data.split("@"))-2])
        term_data=term_data.split("|")[1:]
        for k in term_data:
            doc_no=int(k.split(":")[0].split("c")[1])
            if(i==doc_no):
#                 print(k.split(":")[1].split("_"))
                tf=float(k.split(":")[1].split("_")[0])
                tf_idf=tf*idf
        sum_tf_idf+=(tf_idf*tf_idf)
#         print(term)
#         print(tf_idf)
        vector.append(term+":"+str(tf_idf))  
    sum_tf_idf=math.sqrt(sum_tf_idf)   
    for j in range(len(vector)):
        word=vector[j].split(":")[0]
#         print(vector[j].split(":"))
        if(len(vector[j].split(":"))>2):
                tf_idf=float(vector[j].split(":")[2])
        else:        
            tf_idf=float(vector[j].split(":")[1])
        tf_idf/=sum_tf_idf
        vector[j]=word+":"+str(tf_idf)
        
    doc_vector.append(vector)         


# ### nomalize

# In[ ]:





# # User input Query
# get input from user to proccess query

# In[28]:


query=input("please enter your input : ")


# ##### process input

# In[29]:


query=query.split(" ")


# In[30]:


query_vector=dict()
tf_sum=0


# In[31]:


for i in query:
    tf=find_tf(query,i)
    idf=0
    if(i in final_token):
        temp=final_token[i]  
        idf=float(temp.split("@")[1])
    tf_idf=tf*idf    
    tf_sum+=(tf_idf*tf_idf)
    query_vector[i]=tf_idf
math.sqrt(tf_sum)
if(tf_sum!=0):
    for k in query_vector:
        query_vector[k]/=tf_sum
    


# In[32]:


query_vector


# In[33]:


docs_ans=[]
docs_ans_no=[]
for j in range(len(data_tokens)):
        ans=0
        doc_no=-1
        for i in query_vector:
            if i in data_tokens[j]:
                counter=1
                for k in range(len(doc_vector[j])):
                    word=doc_vector[j][k].split(":")
                    if(i==word[0]):
                        if(counter==1):
#                             print(word)
#                             print(query_vector[i])
#                             print(word[1])
                            ans+=query_vector[i]*float(word[1])
                            doc_no=j
                            counter-=1
        if(ans!=0):
            docs_ans.append(ans)
            docs_ans_no.append(doc_no)


# In[34]:


# docs_ans


# In[35]:


# docs_ans_no


# # show answers 

# In[36]:


final_answer=[]
if(len(docs_ans)==0):
    print("no answer found for your query")  
else:
    if(len(docs_ans)>=5):
        for i in range(5):
            maximum=-10
            max_id=0
            for k in range(len(docs_ans)):
                if(docs_ans[k]>maximum):
                    maximum=docs_ans[k]
                    max_id=docs_ans_no[k]       
            final_answer.append(max_id)
            docs_ans.remove(maximum)
            docs_ans_no.remove(max_id)
    else:
         for i in range(len(docs_ans)):
            maximum=0
            max_id=0
            for k in range(len(docs_ans)):
                if(docs_ans[k]>maximum):
                    maximum=docs_ans[k]
                    max_id=docs_ans_no[k]
            final_answer.append(max_id)
            docs_ans.remove(maximum)
            docs_ans_no.remove(max_id)
    count=0    
    for k in final_answer:
        docid=int(k)
        print("answer "+str(count+1)+": ")
        print("title: "+data_title[docid])
        print("url: "+data_url[docid])
        print(docid)
        print(data_content[docid])
        count+=1


# In[ ]:


# final_answer


# In[ ]:




