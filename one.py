#include<stdio.h>
data = input("输入各个科目成绩")
data ={}
while data:
    t=data.split()
    data[t[0]]=t[1]
    data = input()
ls=list(data.items())
ls.sort(key=lambda x:x[1],reverse=True)
s1,g1=ls[0]
s2,g2=ls[len(ls)-1]
a=0
for i in data.values():
    a=a+int(i)
a=a/len(ls)
print("最高分课程是{}{},最低分课程是{}{},平均分是{:.2f}",format(s1,g1,s2,g2,a))