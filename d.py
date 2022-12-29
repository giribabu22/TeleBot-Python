str = 'prem'
str2 = 'mrep'
dic = {}
dic2 = {}
for i in range(len(str)):

    print(str2[i])
    if str2[i] not in dic2:
        dic2[str2[i]] = 1
    else:
        print('////',str2[i])
        dic2[str2[i]] += 1

    if str[i] not in dic:
        dic[str[i]] = 1
    else:
        dic[str[i]] += 1

print(dic,dic2)
for k in dic:
    if dic[k] != dic2[k]:
        print('Wrong')
        break

