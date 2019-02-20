import copy
import time
def main():

    for i in range (5,50):
        print("Num_Jobs",i)
        tStart = time.time()
        BB(i)
        tEnd = time.time()
        print ("Time cost = ",tEnd-tStart)
        print("----------------------------")


def BB(Jobs_toDo):

    #Lower_Bound=100000000

    '''------------------- read xlsx file-------------------'''
    file_name = "Test data (B&B).xlsx"
    array_jobs =read_xlsx(file_name)
    Jseq_Justfor_init = []

    '''-----------------Global Variable--------------------'''
    bb_tree=[] #tree list
    Jobs_list=[]
    Upper_BoundG=100000000
    Count_Node=0
    Count_Leaves=0
    Lower_BoundG=0
    for i in range(0,len(array_jobs)):
        Jobs_init=Jobs(array_jobs[i][0],array_jobs[i][1],array_jobs[i][2],array_jobs[i][3])
        Jobs_list.append(Jobs_init)

    # array_jobs 0.job  1.release date d_j  2.processing length p_j  3.weight w_j
    '''--------------------init first layer-------------------'''

    for i in range(0,Jobs_toDo):
        Jseq_Justfor_init.append(array_jobs[i][0])#full Jseq

    #print(Jseq_Justfor_init)
    #self,Job_index, Cmax_soFar,Cost_soFar, Jseq,Count_choosed_Jobs

    node_first = node(i, 0, 0, list(Jseq_Justfor_init), -1)
    Lower_BoundG=Lower_Bound(array_jobs,Jobs_list, node_first)
    #print("Lower_BoundG",Lower_BoundG)
    for i in range(0,Jobs_toDo):
        #def __init__(self, Job_index, Cmax_soFar, Cost_soFar, Jseq, Count_choosed_Jobs):
        cmax=Count_Cmax_soFar(array_jobs,0,0,i)
        node_init=node(i,cmax,0,copy.copy(Jseq_Justfor_init),-1)

        Swap_plusone(array_jobs, node_init)  # for Jseq
        #print(node_init.Jseq)
        node_init.Cost_soFar+=cmax
        node_init.Lower_Bound=node_init.Cost_soFar + Lower_Bound(array_jobs,Jobs_list, node_init)
        bb_tree.append(node_init)
        Count_Node+=1

    '''------------------ init heap(first layer)----------------------'''

    min_heap_buildheap(array_jobs,bb_tree)
    # for i in range (0,len(bb_tree)-1):
    #     print(min_heap_getmin(array_jobs,bb_tree).Lower_Bound,end=' ')
    '''---------------start BB------------------------'''
    best_node=bb_tree[0]
    while(len(bb_tree)!=1):
        Current_node=bb_tree.pop(1)
        if Current_node.Count_choosed_Jobs>=Jobs_toDo-1:
            Count_Leaves+=1
            if Current_node.Cost_soFar<Upper_BoundG:
                Upper_BoundG=Current_node.Cost_soFar
                # print("Upper_BoundG Update = ",Upper_BoundG)

                best_node=Current_node
                continue
        else:
            for i in range(Current_node.Count_choosed_Jobs+1, Jobs_toDo):
                #Job_index, Cmax_soFar,Cost_soFar, Jseq,Count_choosed_Jobs
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

                node_init.Cost_soFar = Current_node.Cost_soFar + cmax
                node_init.Lower_Bound =node_init.Cost_soFar + Lower_Bound(array_jobs, Jobs_list, node_init)

                if node_init.Lower_Bound<Upper_BoundG:
                    # print("--------------")
                    # print("Cost_soFar",Current_node.Cost_soFar)
                    # print("Cmax_soFar", Current_node.Cmax_soFar)
                    # print("Count_choosed_Jobs",Current_node.Count_choosed_Jobs)
                    # print("Current_node.Jseq", Current_node.Jseq)
                    # print("--------------")
                    bb_tree.append(node_init)
                    Count_Node+=1
        min_heap_buildheap(array_jobs, bb_tree)
    '''--------------------------'''
    print("Upper_BoundG = ",Upper_BoundG)
    print("Lower_BoundG = ",Lower_BoundG)
    print("Count_Node = ",Count_Node)
    print("Count_Leaves = ",Count_Leaves)
    print("Sol = ",best_node.Cost_soFar)
    print(best_node.Jseq)


'''----------class define-------------'''
class Jobs:
    def __init__(self, Job_id,release_date, processing_length,weight):
        self.Job_id=Job_id
        self.release_date=release_date
        self.processing_length=processing_length
        self.weight=weight
class node:

    def __init__(self,Job_index, Cmax_soFar,Cost_soFar, Jseq,Count_choosed_Jobs):
        self.Job_index=Job_index
        self.Cmax_soFar=Cmax_soFar
        self.Cost_soFar = Cost_soFar
        self.Jseq = Jseq
        self.isOver=0
        self.Count_choosed_Jobs=Count_choosed_Jobs
        self.Lower_Bound=0
'''----------class define(end)-------------'''

'''-----------heap------------------------'''
def min_heap_Heapify(array_jobs,bb_list,i):
    l=2*i
    r=2*i+1
    size=len(bb_list)-1
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
        array_jobs.append(content[i])

    return array_jobs
def Lower_Bound(array_jobs,Jobs_list,node):
    Job_list_renew(array_jobs,Jobs_list)
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

        list_Proccesing=sorted(list_Proccesing,key= lambda c: c.processing_length)
        list_not_released=sorted(list_not_released,key= lambda c: c.release_date)
        #print("current_time",current_time)

        while len(list_not_released)!=0 or  len(list_Proccesing)!=0:

            if len(list_Proccesing) != 0 and list_Proccesing[0].processing_length <= 0:
                sum_Cj_counter += current_time
                list_Proccesing.pop(0)
            if (len(list_not_released) != 0 and list_not_released[0].release_date <= current_time):
                Scan_insert(list_Proccesing, list_not_released)
                if (len(list_not_released) != 0 and list_not_released[0].release_date <= current_time):
                    Scan_insert(list_Proccesing, list_not_released)

            if len(list_Proccesing) > 0:
                list_Proccesing[0].processing_length -= 1
            current_time += 1








    #print("lower_bound = ",sum_Cj_counter)
    return sum_Cj_counter
def Scan_insert( list_Proccesing, list_not_released):
    #print("list_Proccesing",len(list_Proccesing))
    if(len(list_Proccesing)<=0):
        list_Proccesing.append(list_not_released.pop(0))
    else:
        for i in range(0,len(list_Proccesing)):
            #print(i)
            if list_not_released[0].processing_length >list_Proccesing[i].processing_length:
                if i == len(list_Proccesing) - 1:
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
