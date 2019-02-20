from gurobipy import *
def main():

    for i in range(5,51):
        print("-----------------------------------------------------")
        print("--------------Num of Jobs = ",i,"----------------------")
        print("-----------------------------------------------------")
        Start_GRB(i)
def Start_GRB(n):
    print("test")
    '''Dataset and Size'''
    path="Test data (B_B).csv"


    Job_list=[]
    # print(len(read_csv(path)))
    # read_csv(path)
    read_in=read_csv(path)
    for i in range(1,len(read_csv(path))):
        Job_init=Job(read_in[i][0],read_in[i][1],read_in[i][2],read_in[i][3])
        Job_list.append(Job_init)
    print(Job_list[1].Jid)
    call_gurobi(Job_list,n)



class Job():
    def __init__(self,Jid,r_j,p_j,w_j):
        self.Jid=int(Jid)
        self.r_j=int(r_j)
        self.p_j=int(p_j)
        self.w_j=w_j
def read_csv(path):
    file=open(path)
    list_out=[]
    for i in file:
        #print(i.split(","))
        list_out.append(i.split(","))
    #print(list_out[1])
    return list_out
def call_gurobi(Job_list,n):
    try:

        # Create a new model
        m = Model("1|r_j|sum_c_j")

        # Create variables
        M=9999
        x={}
        c={}
        for i in range(n):
            for j in range(n):
                if i!=j:
                    str1=str(i)+","+str(j)
                    x[i,j]=m.addVar(vtype=GRB.BINARY, name=str1)
        for i in range(n):
            str1 = "C_"+str(i)
            c[i]=m.addVar(vtype=GRB.INTEGER, name=str1)

        # Set objective function
        Obj=LinExpr()
        for i in range(n):
            #Job_list[i].w_j
            Obj.addTerms(Job_list[i].w_j,c[i])
        m.setObjective(Obj, GRB.MINIMIZE)

        # C1
        for i in range(n):
            for j in range(n):
                if i!=j:
                    m.addConstr(x[i,j]+x[j,i] == 1, "c0")


        # C2
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if i!=j and j!=k and k!=i:
                        m.addConstr(x[i, j] + x[j, k]+x[k,i] <= 2, "c0")

        #C3
        for i in range(n):
            for j in range(n):
                if i != j:
                    m.addConstr(c[j]-Job_list[j].p_j>=c[i]-M*(1-x[i,j]), "c1")
        #C4
        for j in range(n):

            m.addConstr(c[j]-Job_list[j].p_j>=Job_list[j].r_j, "c1")

        m.optimize()

        for v in m.getVars():
            print('%s %g' % (v.varName, v.x))

        print('Obj: %g' % m.objVal)

    except GurobiError as e:
        print('Error code ' + str(e.errno) + ": " + str(e))

    except AttributeError:
        print('Encountered an attribute error')
if __name__ == "__main__":
    # execute only if run as a script
    main()