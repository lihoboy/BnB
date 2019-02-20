import  random


def main(n,R,i):
    num_of_job=100
    each_class=num_of_job/10
    each_remain=[]
    for i in range (10):
        each_remain.append(10)
    # R=[0.2,0.4,0.6,0.8,1.0,1.25,1.5,1.75,2,3]
    # print(each_remain)
    filename="n"+str(n)+"_R"+str(R)+"_"+str(i)
    print(filename)
    file = open("n=", "a")
    for i in range (1,num_of_job+1):
        job=i
        p_j=random.randrange(1,101)
        choose_class=0
        while(1):
            choose_class=random.randrange(10)
            if each_remain[choose_class]>0:
                each_remain[choose_class]-=1
                break
        temp=50.5*i*R[choose_class]
        # temp = 50.5 * i * 3
        r_j=random.randrange(0,int(temp))
        w_j=random.randrange(1,10)
        # print(p_j)
        if i ==1:
            r_j=0
        file.write("%s\t" %i )
        file.write("%s\t" %r_j)
        file.write("%s\t" %p_j)
        file.write("%s\t" % w_j)
        file.write("\n")
        # print(each_remain)
    file.close()
    # print(each_remain)
if __name__ == "__main__":
    R=[1,2,4,6,8]
    for n in range (10,51,10):
        for r in range(len(R)):
            for i in range (5):
                main(n,R[r],i)

