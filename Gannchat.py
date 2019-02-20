from GanntChart import *

print("Start drawing Gannt...")
"""儲存初始訂單之甘特圖"""
test = GanntChart()
test.init(1, 160, 5)  # 參數順序 NumberOfMachine,TotalLength,Scale
test.SetFontSize(12)
J=[["1",1,0,27],["2",1,27,10],["1",1,37,13],["3",1,50,19],["5",1,69,23],["4",1,92,7],["6",1,99,15],["4",1,114,42]]

for p in range(0, len(J)):  # job
    # test.AddJob(Job name, machine index, start time, processing time)
    test.AddJob(J[p][0],J[p][1],J[p][2],J[p][3])



test.SavetoFile("Gannt_SRPT")
print("Gannt drawing done.")