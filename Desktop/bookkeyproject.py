import csv
from sklearn.model_selection import train_test_split
from collections import Counter
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import numpy as np


aexist=0
bexist =0
while aexist==0 or bexist ==0:
    aexist=0
    bexist=0
    a=str(input("빌릴 책을 입력해주세요:"))  #읽을 책
    b=str(input("아이디를 입력해주세요:"))  #읽을 사람

    f = open("projecttest.csv" ,'r')
    r=csv.reader(f)
    for line in r:
        if line[0]==a:
            aexist=1
        if line[8]==b:
            bexist=1
            
    f.close()
    if aexist==0 :
        print("등록되지 않은 책입니다")
    
    if bexist ==0:
        print("등록되지 않은 아이디입니다")




userbook=list()#부가기호
ubook=list()#유저가 진짜 읽은 책



addsign=list()

sign=0 #읽을 책 부가기호 

time=0 #반납기간


data=list()


useraddday=0
usercount=0


recbook=list()
recday=list()

maxbook=100000
maxbookname=''






f = open("projecttest.csv" ,'r')
r=csv.reader(f)
for line in r:
    if line[0]==a:
        sign=line[5]
f.close()



f = open("projecttest.csv" ,'r')
r=csv.reader(f)
for line in r :
    if line[5] == sign:
        addsign.append(line[8])
f.close()

count={}
for i in addsign:
    try:
        count[i] += 1
    except:
        count[i]=1




overlap=0





f = open("projecttest.csv" ,'r')
r=csv.reader(f)
for line in r:
    if line[8]==b and overlap==0:
        data.append(line[1])
        data.append(line[2])
        overlap=1
    if line[8]==b:
        sign=line[5]
f.close()
try: 
    data.append(count[b])
except:  data.append(0)


nooverdue = 1

loop=0
while nooverdue == 1:
    loop=loop+1
    if loop>100:
        break
    trainset=list()
    testset=list()
    overlap=0
    overlap1=0
    time=time+1

    
    f = open("projecttest.csv" ,'r')
    r=csv.reader(f)



    for line in r:
        if a == line[0]:
            if  int(line[4]) > time :
                line[3] = 1
                overlap1=1
                
            else:
                line[3] = 0
                overlap=1
            tem=list()
            tem1=list()
            tem.append(line[1])
            tem.append(line[2])
            try: 
                tem.append(count[line[8]])
            except:
                tem.append(0)
            
            tem.append(line[3])
            tem1.append(line[1])
            tem1.append(line[2])
            try: 
                tem1.append(count[line[8]])
            except:
                tem1.append(0)
            trainset.append(tem)
            testset.append(tem1)
    f.close()



    
    if overlap ==0 or overlap1==0:
        continue
    f = open('ptrain.csv','w',encoding='cp949',newline='')
    w = csv.writer(f)
    cot=['sex','grade','as','overdue']
    w.writerow(cot)
    for i in range(len(trainset)):
        w.writerow(trainset[i])
    f.close()
    
    ptrain = pd.read_csv("ptrain.csv")

    features = ptrain[['sex', 'grade','as']]

    survival = ptrain['overdue']

    ptrain_features, ptest_features, ptrain_labels, ptest_labels = train_test_split(features, survival)

    scaler = StandardScaler()

    ptrain_features = scaler.fit_transform(ptrain_features)
    ptest_features = scaler.transform(ptest_features)
    try:
        
        model = LogisticRegression()
        model.fit(ptrain_features, ptrain_labels)
        


    except ValueError :
        continue
    ME = np.array(data)
    sample_ptrain = np.array([ME])
    sample_ptrain = scaler.transform(sample_ptrain)

    nooverdue=int(model.predict(sample_ptrain))



if loop>100 :
    print("데이터가 부족하여 예측이 불가능합니다")

else:
    print("이 사람의 적정 반납 기간은",time,"일 입니다")
    #print(model.score(ptrain_features, ptrain_labels))
    #print(model.predict(sample_ptrain))
    #print(model.predict_proba(sample_ptrain))
    #print(time)



chu=int(input("좋아하실 책을 추천해 드릴까요?\n1.수락\n2.거절\n"))

if chu==1:
    
    
    f = open("projecttest.csv" ,'r')
    r=csv.reader(f)
    for line in r:
        if line[8]==b :
            userbook.append(line[5])
            ubook.append(line[0])
    f.close()

    first=list()
    second=list()


    for i in range(len(userbook)):
        first.append(int(userbook[i])//10000)
        second.append(int(userbook[i])//10-int(userbook[i])//1000*100)
    f.close()

    count={}
    for i in first:
        try:
            count[i] += 1
        except:
            count[i]=1

    first1=0
    for i in range(len(first)):
        if first1 < count[first[i]]:
            first1=first[i]


    count={}
    for i in second:
        try:
            count[i] += 1
        except:
            count[i]=1

    second1=0
    for i in range(len(second)):
        if second1 < count[second[i]]:
            second1=second[i]



    overlap=0

    f = open("projecttest.csv" ,'r')
    r=csv.reader(f)
    for line in r:
            overlap=0
            if first1==int(line[5])//10000 and second1==int(line[5])//10-int(line[5])//1000*100:
               for i in range(len(ubook)):
                    if line[0]==ubook[i]:
                       overlap=1
                    if overlap==0:
                        recbook.append(line[0])
                        recday.append(line[4])
    

    recommend=Counter(recbook)
    recommendbook=recommend.most_common()

        
    f.close()

    f=open("projecttest.csv",'r',encoding='cp949',newline='')
    r=csv.reader(f)



    for line in r :
        if line[8]==b :
            if first1==int(line[5])//10000 and second1==int(line[5])//10-int(line[5])//1000*100:
                useraddday=useraddday+(int(line[4]))
                usercount=usercount+1
    userdaymean=useraddday/usercount

    for i in range(len(recday)) :
        if int(recday[i])>=userdaymean:
            if int(recday[i])-userdaymean<maxbook:
                maxbook=int(recday[i])-userdaymean
                maxbookname=recbook[i]
        if int(recday[i])<userdaymean:
            if userdaymean-int(recday[i])<maxbook:
                maxbook=userdaymean-int(recday[i])
                maxbookname=recbook[i]
    print("추천하는 책은 1.",recommendbook[0][0]," 2.",recommendbook[1][0]," 3.",maxbookname)         
       
    

    f.close()   
print("이용해주셔서 감사합니다")            
