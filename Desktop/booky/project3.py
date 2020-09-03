from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pandas as pd
import matplotlib.pyplot as plt
import csv
from datetime import datetime, timedelta

f = open("도서관대출자료편집.csv" ,'r')
r=csv.reader(f)

next(r)

a=str(input())  #예측할 사람 의 이름 입력받기
b=str(input())  #읽을 책의 이름 입력받기

a_book=list() #예측할 사람이 읽었던 책들
a_combook=list() #공통으로 읽을 책

comreadingtime=list() # 읽는데 걸리는 시간 저장
sereadingtime=list() # b를 읽는데 걸린 시간 

a_booknum= list() #예측할 사람이 읽었던 책들을   읽을 책을 읽었던 사람들이 읽은 횟수 
b_bookreader = list() # 읽을 책을 읽었던 사람들
b_combookreader = list() # 읽을 책을 읽었던 사람들중에 한번이라도 예측할 사람이 읽었던 책을 읽은 사람들 


overlap = 0  #중복되는지 확인하는 변수 0이면 중복 없음 1이면 중복 있음

for line in r :
    if a == line[1]:
        overlap = 0
        
        for i in range(len(a_book)):
                       if a_book[i] == line[3]:
                           overlap = 1 #반복을 찾는 프로그램 
                           
        if overlap==0:
            a_book.append(line[3])
    
    if b == line[3]:
        overlap = 0
        
        for i in range(len(b_bookreader)):
                       if b_bookreader[i] == line[1]:
                           overlap = 1 #반복을 찾는 프로그램
                           
        if overlap==0:
            b_bookreader.append(line[1])




for i in range(len(b_bookreader)):
    overlap = 0
    f = open("도서관대출자료편집.csv" ,'r')
    r=csv.reader(f)
    for line in r:
        if line[1]==b_bookreader[i]:
            for k in range(len(a_book)):
                if line[3]==a_book[k]:
                    
                    for j in range(len(b_combookreader)):
                        if b_combookreader[j]==line[1]:
                            overlap = 1
                    if overlap ==0:
                        b_combookreader.append(line[1])
                        
                    
                    
                    


            

for i in range(len(a_book)):
    num = 0
    overlap = 0
    overlaplist = list() # 중복되는지 확인 하는 리스트
    
    f = open("도서관대출자료편집.csv" ,'r')
    r=csv.reader(f)
    
    for line in r :
        if a_book[i] == line[3]:
            for j in range(len(b_combookreader)):
                if b_combookreader[j] == line[1]:
                    for k in range(len(overlaplist)):
                        if overlaplist[k] == b_combookreader[j]:
                            overlap=1
                    if overlap==0:        
                        overlaplist.append(b_combookreader[j])
                        num =num +1
                    
                    
    a_booknum.append(num)

for i in range(len(a_book)):
    a_combook.append(a_book[i])


for i in range(len(a_booknum)):

    if a_booknum[i]==0:
        
        a_combook.remove(a_book[i])
        

        
b_combookreader.insert(0,a)

for i in range(len(b_combookreader)):
    readingtime=list() #읽는 시간 잠시 저장해 두는 곳
    ttt = 0
    for j in range(len(a_combook)):
        overlap=0
        f = open("도서관대출자료편집.csv" ,'r')
        r=csv.reader(f)
        for line in r:
            if overlap ==0:
                if b_combookreader[i]==line[1]:
                    if a_combook[j]==line[3]:
                        time = line[6].split(".",3)
                        time1 = line[7].split(".",3)
        
                        t1 = datetime(int(time[0]), int(time[1]), int(time[2]), 0, 0, 0)
                        t2 = datetime(int(time1[0]), int(time1[1]), int(time1[2]), 0, 0, 0)
                        readingtime.append((t2-t1).days) #독자들 읽는데 걸린 시간
                        overlap=1
                        
        if overlap == 0: #읽지 않은 부분에 평균값넣는 알고리즘
            avertime=0
            ttt = 0
            f = open("도서관대출자료편집.csv" ,'r')
            r=csv.reader(f)
            for line in r:
                if line[3]==a_combook[j]:
                    ttt=ttt+1
                    time = line[6].split(".",3)
                    time1 = line[7].split(".",3)
        
                    t1 = datetime(int(time[0]), int(time[1]), int(time[2]), 0, 0, 0)
                    t2 = datetime(int(time1[0]), int(time1[1]), int(time1[2]), 0, 0, 0)
                    avertime=avertime+(t2-t1).days #독자들 읽는데 걸린 시간
            readingtime.append(avertime/ttt)        

            
    comreadingtime.append(readingtime)
    
b_combookreader.remove(a)
        
for i in range(len(b_combookreader)):
    overlap=0;
    f = open("도서관대출자료편집.csv" ,'r')
    r=csv.reader(f)
    for line in r :
        if overlap==0:
            if line[3]==b:
                if line[1]==b_combookreader[i]:
                    time = line[6].split(".",3)
                    time1 = line[7].split(".",3)
        
                    t1 = datetime(int(time[0]), int(time[1]), int(time[2]), 0, 0, 0)
                    t2 = datetime(int(time1[0]), int(time1[1]), int(time1[2]), 0, 0, 0)
                    sereadingtime.append((t2-t1).days) #독자들 읽는데 걸린 시간
                    overlap=1;
  
                    
    
        

f.close()

f1 = open('도서자료모음.csv','w',encoding='cp949',newline='')
w = csv.writer(f1)



line1 = list()
asdf = list()


line1.append('')
line1.append(b)


for i in range(len(a_combook)) :
    line1.append(a_combook[i])
w.writerow(line1)

for i in range(len(b_combookreader)) :
    asdf = list()
    asdf.append(b_combookreader[i])
    asdf.append(sereadingtime[i])
    for j in range(len(comreadingtime[i+1])) :
        asdf.append(comreadingtime[i+1][j])
    w.writerow(asdf)


f1.close()

result_book = [b]

df = pd.read_csv('도서자료모음.csv',encoding='cp949') 

x = df[a_combook]
y = df[result_book]
x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.5, test_size=0.5)

mlr = LinearRegression()
mlr.fit(x, y)

my_apartment = [comreadingtime[0]]
my_predict = mlr.predict(my_apartment)


print(my_predict)
        

