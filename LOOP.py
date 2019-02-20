list={1,2,3,4,5}
list2=set([2,3,5,7,9])
a=set([555,666])

temp=a
list.add(100)
a=list|list2|a

print(a)
print(1 in a)
listt=[1,2,3,4,5,6]
# for i in range(len(listt)-1,-1,-1):
#     for j in range(i,-1,)
#     print(listt[i])