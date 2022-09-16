from collections import defaultdict 
str = input("input a string:") 
str = str.lower() 
chars = defaultdict(int) 
for char in str: 
   chars[char]+=1 
new chars = sorted(chars,items(),key=lambda d:d[1],reverse=Ture) 
print(new_chars)