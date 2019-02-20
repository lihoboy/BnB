import copy
import time
import math
is_init=0
Lower_Bound_Jseq = []
def main():



    for i in range (10,101,10):

        print("Num_Jobs",i)

        BB(i)


        print("----------------------------")



def BB(Jobs_toDo):

    #Lower_Bound=100000000

    '''------------------- read xlsx file-------------------'''
    # file_name = "Test data (B_B).xlsx"
    file_name = "H&P_data18"
    # "Marc_data1.xlsx
    # Test data (B_B)
    array_jobs = read_xlsx(file_name + ".xlsx")

    '''-----------------Global Variable--------------------'''
    bb_tree=[] #tree list
    Jobs_list=[]
    Upper_BoundG=100000000
    Count_Node=0
    Count_Leaves=0
    Lower_BoundG=0
    Jseq_Justfor_init=[]
    global Lower_Bound_Jseq
    global is_init
    Lower_Bound_Jseq=[]
    is_init=0
    for i in range(0,len(array_jobs)):
        Jobs_init=Jobs(array_jobs[i][0],array_jobs[i][1],array_jobs[i][2],array_jobs[i][3])
        Jobs_list.append(Jobs_init)

    # array_jobs 0.job  1.release date d_j  2.processing length p_j  3.weight w_j
    '''--------------------init first layer-------------------'''
    # print("first")
    for i in range(0,Jobs_toDo):
        Jseq_Justfor_init.append(array_jobs[i][0])#full Jseq

    #print(Jseq_Justfor_init)
    #self,Job_index, Cmax_soFar,Cost_soFar, Jseq,Count_choosed_Jobs

    node_first = node(i, 0, 0, list(Jseq_Justfor_init), -1)
    # print("LB")
    Lower_BoundG=Lower_Bound(array_jobs,Jobs_list, node_first)
    # print("LB out")
    print("Lower_BoundG",Lower_BoundG)
    is_init = 1
    # print("len Lower_Bound_Jseq",len(Lower_Bound_Jseq))
    #print("Lower_Bound_Jseq",len(Lower_Bound_Jseq))
    '''--NEW UPPER BOUND------'''

    # print("new bound")
    Count_Upperbound=0
    Count_Upperbound_Cmax=0
    Job_list_renew(array_jobs, Jobs_list)
    #Job_id,release_date, processing_length,weight
    # for i in range(0, len(Lower_Bound_Jseq)):
    #     print("Lower_Bound_Jseq[i]. processing_length",Lower_Bound_Jseq[i]. processing_length)
    # for i in range(0, len(Lower_Bound_Jseq)):
    #     print(Lower_Bound_Jseq[i].Job_id)
    for i in range(0,len(Lower_Bound_Jseq)):
        if Count_Upperbound_Cmax>Lower_Bound_Jseq[i].release_date:
            Count_Upperbound_Cmax+=Jobs_list[Lower_Bound_Jseq[i]. Job_id-1].processing_length
        else:
            Count_Upperbound_Cmax=Lower_Bound_Jseq[i].release_date+Jobs_list[Lower_Bound_Jseq[i]. Job_id-1].processing_length
        Count_Upperbound+=Count_Upperbound_Cmax*Jobs_list[Lower_Bound_Jseq[i]. Job_id-1].weight
        # print("uppper",Count_Upperbound_Cmax," ",Jobs_list[Lower_Bound_Jseq[i]. Job_id-1].weight)
    # print("Lower_Bound_Jseq",Lower_Bound_Jseq)
    Upper_BoundG=Count_Upperbound
    # Upper_BoundG=9999999

    print("init Upper_BoundG",Upper_BoundG)
    '''--NEW UPPER BOUND------'''
    set_for_init = set([])
    for i in range(0,Jobs_toDo):
        #def __init__(self, Job_index, Cmax_soFar, Cost_soFar, Jseq, Count_choosed_Jobs):
        Job_list_renew(array_jobs,Jobs_list)
        cmax=Count_Cmax_soFar(array_jobs,0,0,i)
        node_init=node(i,cmax,0,copy.copy(Jseq_Justfor_init),-1)

        Swap_plusone(array_jobs, node_init)  # for Jseq
        # print(Jobs_list[1].weight)
        node_init.Cost_soFar+=cmax*Jobs_list[node_init.Jseq[0]-1].weight
        # print(node_init.Cost_soFar," ",cmax*Jobs_list[node_init.Jseq[0]-1].weight," ",Jobs_list[node_init.Jseq[i]-1].weight)
        node_init.Lower_Bound=node_init.Cost_soFar + Lower_Bound(array_jobs,Jobs_list, node_init)
        # print("Job",node_init.Jseq[i]," ",node_init.Cost_soFar," ",Lower_Bound(array_jobs,Jobs_list, node_init))
        # '''dominance branch'''
        # for d in range(Jobs_toDo + 1):
        #     node_init.Branch_dominance.append(set_for_init)
        # # print(node_init.Branch_dominance)
        # '''dominance branch'''
        bb_tree.append(node_init)
        Count_Node+=1

    '''------------------ init heap(first layer)----------------------'''
    tStart = time.time()
    min_heap_buildheap(array_jobs,bb_tree)
    # for i in range (0,len(bb_tree)-1):
    #     print(min_heap_getmin(array_jobs,bb_tree).Lower_Bound,end=' ')
    '''--------------------dominance------------------------------'''
    #Job_id,release_date, processing_length,weight
    Job_list_renew(array_jobs, Jobs_list)
    dominance_Cmax=0
    # for i in range(0,len(Jobs_list)):
    #     for j in range(0,len(Jobs_list)):
    #         if i!=j and Jobs_list[i].release_date<Jobs_list[j].release_date :
    #             if Jobs_list[i].processing_length<Jobs_list[j].processing_length:
    #                 Jobs_list[i].dominance.append(Jobs_list[j].Job_id)
    # for i in range(0, len(Jobs_list)):
    #     print(i,end=" ")
    #     print(Jobs_list[i].release_date,end=" ")
    #     print(Jobs_list[i].processing_length,end=" ")
    #     print(Jobs_list[i].dominance)

    # '''Domi_SPT'''
    # r_K=Jobs_list[0].release_date
    # r_K_1 = Jobs_list[1].release_date
    # if r_K_1>r_K:
    #     r_k,r_K_1=r_K_1,r_K
    # for min in range (2,Jobs_toDo):
    #     if r_K<Jobs_list[min].release_date:
    #         temp_r_k=r_K
    #         r_K=Jobs_list[min].release_date
    #         r_K_1=temp_r_k
    # # r_K = Jobs_list[Jobs_toDo - 1].release_date
    # # r_K_1 = Jobs_list[Jobs_toDo - 2].release_date
    # r_K_counter = 0
    # # print(r_K," ",r_K_1)
    # '''Domi_SPT'''
    '''---------------start BB------------------------'''
    best_node=bb_tree[0]
    print("start")
    while(len(bb_tree)!=1):
        # print("ll")
        dominance_flag = 0
        Current_node=bb_tree.pop(1)
        # '''Domi_SPT'''
        # if Current_node.Cmax_soFar >= r_K and Current_node.Count_choosed_Jobs < Jobs_toDo - 1:
        #
        #     list_SPT = []
        #     for get_SPT_jobs in range(Current_node.Count_choosed_Jobs + 1, Jobs_toDo):
        #         list_SPT.append(copy.copy(Jobs_list[Current_node.Jseq[get_SPT_jobs] - 1]))
        #     list_SPT = sorted(list_SPT, key=lambda c: c.processing_length)
        #     # print("SPT ",len(list_SPT)," jobs")
        #     for set_SPT_seq in range(len(list_SPT)):
        #         Current_node.Jseq[Current_node.Count_choosed_Jobs + 1 + set_SPT_seq] = list_SPT[set_SPT_seq].Job_id
        #         Current_node.Cmax_soFar += list_SPT[set_SPT_seq].processing_length
        #         Current_node.Cost_soFar += Current_node.Cmax_soFar
        #     Current_node.Count_choosed_Jobs = Jobs_toDo - 1
        # '''Domi_SPT'''

        if Current_node.Lower_Bound>Upper_BoundG:
            # print(Current_node.Lower_Bound," ",Upper_BoundG)
            # print("error")
            continue
        # for i in range(0, Current_node.Count_choosed_Jobs):
        #     for j in range (0,len(Jobs_list[Current_node.Job_index].dominance)):
        #         if Current_node.Jseq[i]==Jobs_list[Current_node.Job_index].dominance[j]:
        #             dominance_flag = 1
        #             break
        #     if dominance_flag==1:
        #         break
        # if dominance_flag==1:
        #     continue
        if Current_node.Count_choosed_Jobs>=Jobs_toDo-1:
            Count_Leaves+=1

            if Current_node.Cost_soFar<=Upper_BoundG:
                Upper_BoundG=Current_node.Cost_soFar
                print("Upper_BoundG Update = ",Upper_BoundG)

        # may should gan mo
                best_node=Current_node
                continue
        else:
            # '''Dominance(x,y)'''
            # S_x = Current_node.Cmax_soFar - Jobs_list[
            #     Current_node.Jseq[Current_node.Count_choosed_Jobs] - 1].processing_length
            # '''Dominance(x,y)'''
            for i in range(Current_node.Count_choosed_Jobs+1, Jobs_toDo):
                #Job_index, Cmax_soFar,Cost_soFar, Jseq,Count_choosed_Jobs
                # Job_list_renew(array_jobs, Jobs_list)
                # '''Dominance(x,y)'''
                #
                # # if S_x<0:
                # # print(S_x)
                # if S_x>=Jobs_list[Current_node.Jseq[i]-1].release_date and Jobs_list[Current_node.Jseq[i]-1].processing_length<Jobs_list[Current_node.Jseq[Current_node.Count_choosed_Jobs]-1].processing_length:
                #     # print("S_x",S_x,"r_y",Jobs_list[Current_node.Jseq[i]-1].release_date)
                #     continue
                # '''Dominance(x,y)'''
                # '''Domi_r_K'''
                # Domi_r_k_flag = 0
                # if r_K_1 <= Current_node.Cmax_soFar < r_K and Current_node.Cmax_soFar + Jobs_list[
                #     Current_node.Jseq[i] - 1].processing_length >= r_K and Jobs_list[
                #     Current_node.Jseq[i] - 1].release_date < r_K:
                #     for larger_than_r_k in range(Current_node.Count_choosed_Jobs + 1, Jobs_toDo):
                #         if i != larger_than_r_k and Jobs_list[
                #             Current_node.Jseq[larger_than_r_k] - 1].processing_length <= Jobs_list[
                #             Current_node.Jseq[i] - 1].processing_length and Current_node.Cmax_soFar + Jobs_list[
                #             Current_node.Jseq[larger_than_r_k] - 1].processing_length >= r_K:
                #             if Current_node.Jseq[larger_than_r_k] > Current_node.Jseq[i]:
                #                 Domi_r_k_flag = 1
                #                 break
                #
                # if Domi_r_k_flag == 1:
                #     r_K_counter += 1
                #     # print("r_K")
                #     continue
                # '''Domi_r_K'''
                '''dominance'''
                # is_dominanted = 0
                # for domi in range(Current_node.Count_choosed_Jobs + 1, len(Current_node.Jseq)):
                #     if domi != i:
                #         if Current_node.Jseq[domi] in Current_node.Branch_dominance[Current_node.Jseq[i]]:
                #             is_dominanted = 1
                #             break
                # if is_dominanted:
                #     # print("ban",node_init.Count_choosed_Jobs, node_init.Jseq,node_init.Cmax_soFar)
                #     continue

                '''dominance'''
                cmax = Count_Cmax_soFar(array_jobs, Current_node.Cmax_soFar, Current_node.Job_index, Current_node.Jseq[i]-1)
                node_init = node(Current_node.Jseq[i]-1, cmax, 0, copy.copy(Current_node.Jseq), Current_node.Count_choosed_Jobs)

                '''----------------------'''
                Swap_plusone(array_jobs, node_init)  # for Jseq
                # if node_init.Count_choosed_Jobs + 1 > len(node_init.Jseq) - 1:
                #     print("Swap_plusone: Out of index")
                # else:
                #     node_init.Count_choosed_Jobs += 1
                #     print("Count_choosed_Jobs123321321231",Current_node.Count_choosed_Jobs)
                #     for i in range(node_init.Count_choosed_Jobs, len(node_init.Jseq)):
                #         if array_jobs[node_init.Job_index][0] == node_init.Jseq[i]:
                #             temp_i = node_init.Jseq[i]
                #             temp_c = node_init.Jseq[node_init.Count_choosed_Jobs]
                #             node_init.Jseq.pop(i)
                #             node_init.Jseq.insert(i, temp_c)
                #             node_init.Jseq.pop(node_init.Count_choosed_Jobs)
                #             node_init.Jseq.insert(node_init.Count_choosed_Jobs, temp_i)
                '''-----------------------'''
                #print("Count_choosed_Jobs",Current_node.Count_choosed_Jobs)

                node_init.Cost_soFar = Current_node.Cost_soFar + cmax*Jobs_list[node_init.Job_index].weight
                node_init.Lower_Bound =node_init.Cost_soFar + Lower_Bound(array_jobs, Jobs_list, node_init)

                if node_init.Lower_Bound<=Upper_BoundG:
                    '''dominance'''
                    # # Job_list_renew(array_jobs, Jobs_list)
                    # node_init.Branch_dominance=copy.copy(Current_node.Branch_dominance)
                    # #,Job_index, Cmax_soFar,Cost_soFar, Jseq,Count_choosed_Jobs):
                    # already_Release=[]
                    # all_unscheduled=[]
                    # if node_init.Count_choosed_Jobs+1<Jobs_toDo:
                    #     # Job_list_renew(array_jobs, Jobs_list)
                    #     for job_unscheduled in range (node_init.Count_choosed_Jobs+1,len(node_init.Jseq)):
                    #         # print(job_unscheduled)
                    #         # print("Job",node_init.Jseq[job_unscheduled],"R_j= ",Jobs_list[node_init.Jseq[job_unscheduled]].release_date,"Cxax= ",node_init.Cmax_soFar)
                    #         all_unscheduled.append(copy.copy(Jobs_list[node_init.Jseq[job_unscheduled]-1]))
                    #         if Jobs_list[node_init.Jseq[job_unscheduled]-1].release_date<=node_init.Cmax_soFar:
                    #             # print("is released",node_init.Jseq[job_unscheduled])
                    #             already_Release.append(copy.copy(Jobs_list[node_init.Jseq[job_unscheduled]-1]))
                    #     # Job_list_renew(array_jobs, Jobs_list)
                    #     # already_Release = sorted(already_Release, key=lambda c: c.processing_length)
                    #     if len(already_Release)!=0:
                    #         sortest_p_x = copy.copy(already_Release[0])
                    #         for get_min in range(len(already_Release)):
                    #             if already_Release[get_min].processing_length<sortest_p_x.processing_length:
                    #                 sortest_p_x=copy.copy(already_Release[get_min])
                    #         # print("sortest_p_x",sortest_p_x)
                    #         all_unscheduled_less_than_x=copy.copy(all_unscheduled)
                    #         all_unscheduled_less_than_x=list(filter(lambda x: x.processing_length< sortest_p_x.processing_length, all_unscheduled_less_than_x))
                    #         num_less_than_x=len(all_unscheduled_less_than_x)
                    #         # print("num_less_than_x",num_less_than_x)
                    #         # if num_less_than_x>0:
                    #         #     for LT in range (num_less_than_x):
                    #         #         print("ID=",all_unscheduled_less_than_x[LT].Job_id,"p= ",all_unscheduled_less_than_x[LT].processing_length)
                    #         sum_pj_less_than_x=0
                    #         for sum_pj in range(len(all_unscheduled_less_than_x)):
                    #             sum_pj_less_than_x+=all_unscheduled_less_than_x[sum_pj].processing_length
                    #         Jobs_tobe_add=[]
                    #         # set_temp=set
                    #         # Job_list_renew(array_jobs, Jobs_list)
                    #         # print("already released")
                    #         # for al in range(len(already_Release)):
                    #         #
                    #         #     print("id",already_Release[al].Job_id,"p_time""",already_Release[al].processing_length ,end=" ")
                    #         # # print("")
                    #         # for al in range(len(all_unscheduled)):
                    #         #
                    #         #     print("id",all_unscheduled[al].Job_id,"p_time""",all_unscheduled[al].processing_length ,end=" ")
                    #         # print("")
                    #
                    #         for to_be_domi in range(len(already_Release)):
                    #             if to_be_domi!=0 and (1+num_less_than_x)*sortest_p_x.processing_length<=already_Release[to_be_domi].processing_length+sum_pj_less_than_x:
                    #
                    #
                    #                     # print(to_be_domi,"=",domi)
                    #                 Jobs_tobe_add.append(sortest_p_x.Job_id)
                    #             # print("Jobs_tobe_add",Jobs_tobe_add)
                    #             set_temp=set(Jobs_tobe_add)
                    #             # print("sv",set_temp)
                    #             # print(Jobs_tobe_add)
                    #             # print(node_init.Branch_dominance)
                    #             node_init.Branch_dominance[already_Release[to_be_domi].Job_id]=node_init.Branch_dominance[already_Release[to_be_domi].Job_id]|set_temp
                    #             # print(already_Release[to_be_domi].Job_id," ",node_init.Branch_dominance)
                    #             Jobs_tobe_add=[]
                    #     #     set_temp=set([])
                    #     # already_Release=[]
                    #     # Job_list_renew(array_jobs, Jobs_list)
                    #         # print(type(node_init.Branch_dominance[already_Release[to_be_domi]]))
                    #         # temp_domi=node_init.Branch_dominance[already_Release[to_be_domi]]
                    #         # node_init.Branch_dominance[already_Release[to_be_domi]]=set
                    #         #
                    #         # node_init.Branch_dominance[already_Release[to_be_domi]]=node_init.Branch_dominance[already_Release[to_be_domi].Job_id]|set_temp
                    # # for test_Joblist in range(len(Jobs_list)):
                    # #     print(test_Joblist," ",Jobs_list[test_Joblist].processing_length)
                    # #
                    # # print("choosed",node_init.Count_choosed_Jobs)
                    # # print(node_init.Jseq)
                    # # print("Cmax",node_init.Cmax_soFar)
                    # # for BD in range(len(node_init.Branch_dominance)):
                    # #     print(BD,node_init.Branch_dominance[BD])
                    #
                    # # print("]")

                    '''dominance'''
                    bb_tree.insert(1,node_init)
                    Count_Node+=1
                    need_build=1
                    min_heap_Heapify(array_jobs, bb_tree, 1)
                    # print("<3")
        # if need_build==1:
        #     min_heap_buildheap(array_jobs, bb_tree)
        #     need_build=0

        min_heap_Heapify(array_jobs, bb_tree, 1)


    '''--------------------------'''
    tEnd = time.time()





    t_count = tEnd - tStart
    file = open(file_name+"_1.txt", "a")
    file.write("%s\t" % Jobs_toDo)
    file.write("%s\t" % Upper_BoundG)
    file.write("%s\t" % Lower_BoundG)
    file.write("%s\t" % Count_Node)
    file.write("%s\t" % Count_Leaves)
    file.write("%s\t" % t_count)
    for i in range(0,len(best_node.Jseq)):
        file.write("%s"%best_node.Jseq[i])
        if i!=len(best_node.Jseq)-1:
            file.write("->" )
    file.write("\n")


    file.close()
    print("Upper_BoundG = ",Upper_BoundG)
    print("Lower_BoundG = ",Lower_BoundG)
    print("Count_Node = ",Count_Node)
    print("Count_Leaves = ",Count_Leaves)
    print("Sol = ",best_node.Cost_soFar)
    print(best_node.Jseq)
    print("Time cost = ", t_count)


'''----------class define-------------'''
class Jobs:
    def __init__(self, Job_id,release_date, processing_length,weight):
        self.Job_id=Job_id
        self.release_date=release_date
        self.processing_length=processing_length
        self.weight=weight
        self.dominance=[]
        self.w_j_p_j=weight/processing_length
class node:

    def __init__(self,Job_index, Cmax_soFar,Cost_soFar, Jseq,Count_choosed_Jobs):
        self.Job_index=Job_index
        self.Cmax_soFar=Cmax_soFar
        self.Cost_soFar = Cost_soFar
        self.Jseq = Jseq
        self.isOver=0
        self.Count_choosed_Jobs=Count_choosed_Jobs
        self.Lower_Bound=0
        self.Branch_dominance = []
'''----------class define(end)-------------'''

'''-----------heap------------------------'''
def min_heap_Heapify(array_jobs,bb_list,i):
    size = len(bb_list) - 1
    if size==1:
        return
    l=2*i
    r=2*i+1

    #print(array_jobs)
    #print("heapfy",i)

    if l<=size and bb_list[l].Lower_Bound<bb_list[i].Lower_Bound:
        min_index=l
    else :
        min_index=i
    if r<=size and bb_list[r].Lower_Bound<bb_list[min_index].Lower_Bound:
        #print("array_jobs[bb_list[r].Job_index][2]",array_jobs[bb_list[r].Job_index][2])
        min_index=r
    if min_index!=i:
        min_heap_swap(bb_list,i,min_index)
        min_heap_Heapify(array_jobs,bb_list,min_index)

def min_heap_swap(list,i,j):
    temp_i=list[i]
    temp_j=list[j]
    list.pop(i)
    list.insert(i,temp_j)
    list.pop(j)
    list.insert(j, temp_i)
def min_heap_buildheap(array_jobs,heap_list):
    #print(len(heap_list))
    if  len(heap_list)==0 or heap_list[0].Job_index!=-1 :
        node_for_heap_init=node(-1,0,0,0,0)
        heap_list.insert(0,node_for_heap_init)
    list_len=len(heap_list)
    list_len=int(list_len)
    #print("build")
    for i in range(int(list_len/2),0,-1):
        #print("heap at ",i)
        min_heap_Heapify(array_jobs,heap_list,i)
def min_heap_getmin(array_jobs,heap_list):
    temp=heap_list[1]
    heap_list.pop(1)
    min_heap_buildheap(array_jobs,heap_list)
    return temp
'''-----------heap(end)-------------------'''

'''----------functions defind------------------------------'''
def Job_list_renew(array_jobs,Jobs_list):
    for i in range(0,len(array_jobs)):
        Jobs_list[i].Job_id=array_jobs[i][0]
        Jobs_list[i].release_date = array_jobs[i][1]
        Jobs_list[i].processing_length = array_jobs[i][2]
        Jobs_list[i].weight = array_jobs[i][3]

def Count_Cmax_soFar(array_jobs,father_Cmax,father_JobIndex,Job_index):
    if(father_Cmax>array_jobs[Job_index][1]):
        return father_Cmax+array_jobs[Job_index][2]
    else:
        return array_jobs[Job_index][1]+array_jobs[Job_index][2]
def read_xlsx(fn):
    from openpyxl import load_workbook
    filename = fn
    wb = load_workbook(filename=filename, data_only=True)
    sheets = wb.get_sheet_names()
    sheet0 = sheets[1]
    ws = wb.get_sheet_by_name(sheet0)
    # set variable
    rows = ws.rows
    columns = ws.columns

    content = []
    for row in rows:
        line = [col.value for col in row]
        content.append(line)


    array_jobs = []
    for i in range(1, len(content)):
        # print(content[i])
        array_jobs.append(content[i])
    # print(array_jobs)
    return array_jobs
def Lower_Bound(array_jobs,Jobs_list,node):
    #global Lower_Bound_Jseq
    global Lower_Bound_Jseq
    global is_init

    #print("processing_length", Jobs_list[0].processing_length)
    #print("Job_list_renew", len(Jobs_list))
    current_time=node.Cmax_soFar
    sum_Cj_counter=0
    #print("------LB------index",node.Job_index)
    if node.Count_choosed_Jobs+1==len(node.Jseq):
        a=1
        #print("here is LB ,all Jobs been choosed")
    else:
        list_Proccesing=[]
        list_not_released=[]

        for i in range(node.Count_choosed_Jobs+1,len(node.Jseq)):#index
            #print(i)
            if Jobs_list[node.Jseq[i]-1].release_date >current_time:
                list_not_released.append(Jobs_list[node.Jseq[i]-1])
            else:
                list_Proccesing.append(Jobs_list[node.Jseq[i] - 1])
        # print("current time= ",current_time)
        #print("non_r= ",len(list_not_released),"proing",len(list_Proccesing))

        list_Proccesing=sorted(list_Proccesing,key= lambda c: c.w_j_p_j,reverse=True)
        list_not_released=sorted(list_not_released,key= lambda c: c.release_date)
        #print("current_time",current_time)
        '''old_SRPT'''
        # while len(list_not_released) != 0 or len(list_Proccesing) != 0:
        #     if is_init == 0:
        #         if len(Lower_Bound_Jseq)==0 and len(list_Proccesing)!=0:
        #             Lower_Bound_Jseq.append(copy.copy(list_Proccesing[0]))
        #         elif len(list_Proccesing)!=0:
        #             for i in range (0,len(Lower_Bound_Jseq)):
        #                 if list_Proccesing[0].Job_id ==Lower_Bound_Jseq[i].Job_id :
        #                     break
        #                 elif i==len(Lower_Bound_Jseq)-1:
        #                     Lower_Bound_Jseq.append(copy.copy(list_Proccesing[0]))
        #     if (len(list_not_released) != 0 and list_not_released[0].release_date <= current_time):
        #         Scan_insert(list_Proccesing, list_not_released)
        #     if len(list_Proccesing) != 0 and list_Proccesing[0].processing_length <= 0:
        #         sum_Cj_counter += current_time
        #         #Lower_Bound_Jseq.append(list_Proccesing.pop(0))
        #
        #
        #         list_Proccesing.pop(0)
        #     if len(list_Proccesing) > 0:
        #         list_Proccesing[0].processing_length -= 1
        #
        #     current_time += 1
        '''old_SRPT'''
        time_can_do=0
        while len(list_not_released) != 0 or len(list_Proccesing) != 0:
            # print("0")
            # list_Proccesing = sorted(list_Proccesing, key=lambda c: c.w_j_p_j)
            # print("len(list_Proccesing)", len(list_Proccesing))
            # print("list_not_released)", len(list_not_released))
            # print(current_time)
            if is_init == 0:
                if len(Lower_Bound_Jseq)==0 and len(list_Proccesing)!=0:
                        Lower_Bound_Jseq.append(copy.copy(list_Proccesing[0]))
                elif len(list_Proccesing)!=0:
                    for i in range (0,len(Lower_Bound_Jseq)):
                        if list_Proccesing[0].Job_id ==Lower_Bound_Jseq[i].Job_id :
                            break
                        elif i==len(Lower_Bound_Jseq)-1:
                            Lower_Bound_Jseq.append(copy.copy(list_Proccesing[0]))

            x_start_time=current_time

            if len(list_Proccesing) == 0 and len(list_not_released) != 0:
                '''no j can procces so release'''
                current_time = list_not_released[0].release_date
                list_Proccesing.append(list_not_released.pop(0))
                # print("case1.1 len_p=0 len_r!=0", current_time)
                continue
            if len(list_not_released) == 0 and len(list_Proccesing) != 0:
                '''Case1 all Released'''
                # print("Case1 all Released")
                current_time+=list_Proccesing[0].processing_length
                sum_Cj_counter+=current_time*(list_Proccesing[0].processing_length*list_Proccesing[0].w_j_p_j)
                # print(current_time*(list_Proccesing[0].processing_length*list_Proccesing[0].w_j_p_j))
                # if is_init==0:
                #     Lower_Bound_Jseq.append(copy.copy(list_Proccesing[0]))
                list_Proccesing.pop(0)
                # print("Case1 current_time= ",current_time)
                continue

            elif len(list_Proccesing) !=0:
                # print("Case2 current_time= ", current_time)


                if list_Proccesing[0].processing_length+current_time<list_not_released[0].release_date:
                    '''can done complete'''
                    # print("case2 can done complete")
                    # print(list_Proccesing[0].Job_id,list_Proccesing[1].Job_id)
                    current_time+=list_Proccesing[0].processing_length
                    sum_Cj_counter += current_time*(list_Proccesing[0].processing_length*list_Proccesing[0].w_j_p_j)
                    # print("current_time",current_time,current_time*(list_Proccesing[0].processing_length*list_Proccesing[0].w_j_p_j))
                    # if is_init == 0:
                    #     Lower_Bound_Jseq.append(copy.copy(list_Proccesing[0]))
                    list_Proccesing.pop(0)
                    continue

                else :
                    # '''New_LB'''
                    # if list_Proccesing[0].processing_length-(list_not_released[0].release_date - current_time)>list_not_released[0].processing_length :
                    #     x_delay=list_Proccesing[0].processing_length-(list_not_released[0].release_date - current_time)
                    #     y_delay=(list_not_released[0].release_date - current_time)+list_not_released[0].processing_length
                    #     min_delay=min(x_delay,y_delay)
                    #     TLB=min_delay-list_not_released[0].processing_length
                    #     sum_Cj_counter+=TLB
                    # '''New_LB'''
                    if list_Proccesing[0].w_j_p_j < list_not_released[0].w_j_p_j:
                        # print("case3 preemption",end='')
                        '''New_LB'''
                        # if math.pow(list_Proccesing[0].processing_length-(list_not_released[0].release_date - current_time),2)*list_Proccesing[0].w_j_p_j>math.pow(list_not_released[0].processing_length,2)*list_not_released[0].w_j_p_j :
                        #     x_delay=list_Proccesing[0].processing_length-(list_not_released[0].release_date - current_time)
                        #     x_delay=math.pow(x_delay,2)*list_Proccesing[0].w_j_p_j
                        #     y_delay=(list_not_released[0].release_date - current_time)+list_not_released[0].processing_length
                        #     y_delay = math.pow(y_delay, 2) * list_not_released[0].w_j_p_j
                        #     min_delay=min(x_delay,y_delay)
                        #     TLB=min_delay-math.pow(list_not_released[0].processing_length,2)*list_not_released[0].w_j_p_j
                        #     # print(TLB)
                        #     sum_Cj_counter+=TLB
                        '''New_LB'''
                        p_done_before_preemp=list_not_released[0].release_date - current_time
                        list_Proccesing[0].processing_length -= p_done_before_preemp
                        current_time = list_not_released[0].release_date
                        sum_Cj_counter += current_time*(p_done_before_preemp *list_Proccesing[0].w_j_p_j)
                        # print("",current_time," ",p_done_before_preemp *list_Proccesing[0].w_j_p_j)
                        # print(current_time*(p_done_before_preemp *list_Proccesing[0].w_j_p_j))


                        Scan_insert(list_Proccesing, list_not_released)
                        continue
                    else:
                        # print("case4 can release but can't preemption",current_time)
                        # while list_Proccesing[0].w_j_p_j > list_not_released[0].w_j_p_j :
                        # p_done_before_preemp = list_not_released[0].release_date - current_time
                        # list_Proccesing[0].processing_length -= p_done_before_preemp
                        # current_time = list_not_released[0].release_date
                        # sum_Cj_counter += current_time * (p_done_before_preemp * list_Proccesing[0].w_j_p_j)
                        # print("", current_time, " ", p_done_before_preemp * list_Proccesing[0].w_j_p_j)
                        # print(current_time * (p_done_before_preemp * list_Proccesing[0].w_j_p_j))
                        # for ii in range (len(list_Proccesing)):
                        #     print(list_Proccesing[ii].w_j_p_j)
                        # print("----------------------")
                        Scan_insert(list_Proccesing, list_not_released)
                        # for ii in range (len(list_Proccesing)):
                        #     print(list_Proccesing[ii].w_j_p_j)
                        # list_Proccesing = sorted(list_Proccesing, key=lambda c: c.w_j_p_j)
                        continue





    #
    # for i in range(len(Lower_Bound_Jseq)):
    #     print(Lower_Bound_Jseq[i].Job_id)
    # print("len(Lower_Bound_Jseq)",len(Lower_Bound_Jseq))
    # print("lower_bound = ",sum_Cj_counter)
    Job_list_renew(array_jobs, Jobs_list)
    return sum_Cj_counter
def Scan_insert( list_Proccesing, list_not_released):
    #print("list_Proccesing",len(list_Proccesing))
    if(len(list_Proccesing)==0):
        list_Proccesing.append(list_not_released.pop(0))
    else:
        for i in range(0,len(list_Proccesing)):
            #print(i)
            if list_not_released[0].w_j_p_j < list_Proccesing[i].w_j_p_j:
                if i==len(list_Proccesing)-1:
                    list_Proccesing.append(list_not_released.pop(0))
                    break
                continue
            else:
                list_Proccesing.insert(i,list_not_released.pop(0))
                break
def Swap_plusone( array_jobs,node):
    if node.Count_choosed_Jobs+1>len(node.Jseq)-1:
        return
    else:
        node.Count_choosed_Jobs+=1

        for i in range(node.Count_choosed_Jobs,len(node.Jseq)):
            #print("i at ",i)
            if array_jobs[node.Job_index][0]==node.Jseq[i]:
                #print("swap job ",node.Job_index,"job",i)
                temp_i = node.Jseq[i]
                temp_c = node.Jseq[node.Count_choosed_Jobs]
                node.Jseq.pop(i)
                node.Jseq.insert(i, temp_c)
                node.Jseq.pop(node.Count_choosed_Jobs)
                node.Jseq.insert(node.Count_choosed_Jobs, temp_i)
                break
'''----------functions defind(end)------------------------------'''
if __name__ == "__main__":
    main()
