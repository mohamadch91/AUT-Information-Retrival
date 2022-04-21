from hazm import *
from parsivar import *
import json
# reading file
file=open("IR_data_news_12k.json")
data=json.load(file)
data_content=[]
data_url=[]
data_title=[]
data_category=[]