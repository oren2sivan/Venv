import math

#האם מספר ראשוני או לא 
def Is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3,int(math.sqrt(n))+1,2):
        if n % i == 0:
            return False
    return True




def Reversed(word):
    list1=list(word)
    list2=[]
    count=0
    for i in range(-1,-1-len(list1),-1):
        list2.insert(count,list1[i])
        count+=1
    return(''.join(list2))
#Reversed('hello World!')



def IsPhil(word):
    list1 = list(word)
    size = len(list1)
    flist = []
    slist = []
    for i in range(0,size // 2):  
        flist.append(list1[i])
    if size%2==1:
        for i in range(size // 2+1, size): 
            slist.append(list1[i])
    else:
        for i in range(size // 2, size): 
            slist.append(list1[i])
    word1=''.join(flist)
    word2=Reversed(''.join(slist))
    if (word1==word2):
        return True
    else:
        return False    

IsPhil('abccba')
 
def Longest(sen):
    list1=sen.split(' ')
    max=list1[0]
    
    for i in list1:
        if int(len(i))>int(len(max)):
            max=i

    return(max)
    

print(Longest('my name is oren and im writing this code on a friday night:)'))
