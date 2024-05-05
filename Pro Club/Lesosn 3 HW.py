import sys



# הערות: הסתבכתי בsys argv, אני אשאל לגבי זה בשיעור הבא.

def Frequency(file_name,n):

    # בניית המילון:
    with open(file_name,'r') as file:
        dict={}
        word_list=file.read().split(' ')
    for i in word_list:
        count=0
        for k in word_list:
            if i==k:
                count+=1

        if i not in dict.keys():
            dict[i]=count

     #מיון תדירות
    sorted_dict=sorted(dict.items(), key=lambda x:x[1],reverse=True)

    for i in range(0,n):
        print(sorted_dict[i][0], "Freq:",sorted_dict[i][1])






Frequency('test.txt',5)