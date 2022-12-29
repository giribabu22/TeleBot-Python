li = [9,55,1,2,3,5,6,7]
li2 = li.copy()
li.sort(reverse=True)
print(li)
print(li2.index(6))
firs = li2.index(li[0])
li.pop(0)
sec  = li2.index(li[0])
li.pop(0)
thd  = li2.index(li[0])
li.pop(0)

print(firs,sec,thd)