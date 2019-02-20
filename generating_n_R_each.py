import  random


def main(num_of_job,R,i):





    filename="N"+str(n)+"_R"+str(R)+"_"+str(i)
    filename="data_n_R\\"+filename
    print(filename)
    file = open(filename, "a")


    for i in range (1,num_of_job+1):
        job=i
        p_j=random.randrange(1,101)


        temp=50.5*i*R
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
    R=[1.25,1.5,1.75,2,3]
    for n in range (10,51,10):
        for r in range(len(R)):
            for i in range (5):
                main(n,R[r],i)

