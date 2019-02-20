# file=open("data_n_R\\N50_R4_4","r")
# array_jobs = []
# for i in  file :
#     line=i.split("\t")
#     # print(line)
#     array_jobs.append(line)
# print(array_jobs)
import time
import datetime
num=1.1

from datetime import datetime, date
print(date.today())
print(datetime.now())


dt=datetime.now()
dt_str="{0:%m}{0:%d}-{0:%I:%M%p}".format(dt)
print(dt_str)
