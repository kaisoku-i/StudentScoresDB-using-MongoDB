import pymongo
import json

client=pymongo.MongoClient("mongodb://localhost:27017")

db=client.Students
records=db.Examscores

file=[line.rstrip() for line in open('task2\\students.txt','r+',newline='')]

for item in file:
    data=json.loads(item)
    records.insert_one(data)
    
#student name who scored maximum scores in all (exam, quiz and homework)
agg_max=records.aggregate(
    [{
      "$group":
        {
        "_id":"$name",
         "Totalscore":{"$max":{"$sum":["$scores.score"]}}}},  
         {"$sort":{"Totalscore":-1}},
         {"$limit":1} 
    ])
for i in agg_max:print(i)
      
#students who scored below average in the exam and pass mark is 40%
escore =[]
for x in records.find({},{"_id":0, "scores":1}):
  escore.append(x["scores"][0]["score"])
eavg = sum(escore)/len(escore)

b_avg=records.find({q:{'$gt':40,'$lt':eavg}})

for i in b_avg:print(i)

#students who scored below pass mark and assigned them as fail, and above pass mark as pass in all the categories
s_list=list(records.find())

for i in range(200):
  count=0
  for j in range(len(s_list[i]['scores'])):
    if 40<=s_list[i]['scores'][j]['score']<=100:
      s_list[i]['scores'][j].update({'remark':'pass'})
      records.update_one({'_id':i},{'$set':{'scores':s_list[i]['scores']}})
      count+=1
    else:
      s_list[i]['scores'][j].update({'remark':'fail'})
      records.update_one({'_id':i},{'$set':{'scores':s_list[i]['scores']}})
    if count==3:records.update_one({'_id':i},{'$set':{'remark':'pass'}})
    else:records.update_one({'_id':i},{'$set':{'remark':'fail'}})

#total and average of the exam, quiz and homework and store them in a separate collection.
total=records.aggregate([{'$unwind':'$scores'},{'$group':{'_id':'$scores.type',
                            'Totalsum':{'$sum':'$scores.score'},
                            'TotalAverage':{'$avg':'$scores.score'}}},
                            {'$sort':{'Totalsum':1}},
                            {'$out':{'db':'Students','coll':'Totalvalues'}}])

tot_val=db.Totalvalues
avg_all=list(tot_val.find({}))

#new collection which consists of students who scored below average and above 40% in all the categories
for i in range(200):
    count=0
    for j in range(len(s_list[i]['scores'])):
        if (s_list[i]['scores'][j]['type']==avg_all[j]['_id']) and (40<=s_list[i]['scores'][j]['score']<=48):
            count+=1
        else:
            pass
        if count==3:print(s_list[i])
#None students scored below average and above 40% in all the categories      

#new collection which consists of students who scored below the fail mark in all the categories
records.aggregate([{'$match':{'$and':[{'scores.0.remark':'fail'},{'scores.1.remark':'fail'},{'scores.2.remark':'fail'}]}},
                    {'$out':{'db':'Students','coll':'FailedList'}}])   

#new collection which consists of students who scored above pass mark in all the categories
records.aggregate([{'$match':{'remark':'pass'}},
                    {'$out':{'db':'Students','coll':'PassList'}}
                    ]) 
