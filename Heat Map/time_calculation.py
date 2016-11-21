import csv
import numpy as np

data = np.loadtxt('dataPoints.csv', delimiter=',')
f=open('actualDataPoints.csv','wt')
writer=csv.writer(f)

c=data[:,0]
time=data[:,1]
print c[0]
k = time.shape[0]
x=time[0]
total_time=x
i=1
for j in range(1,k):
    if time[j]==x:
        total_time+=time[j]
    else:
        name = "Customer " + str(i)
        writer.writerow((name,i,c[0],total_time))
        i+=1
        x=time[j]
        total_time=x
name = "Customer " + str(i)
writer.writerow((name,i,c[0],total_time))
f.close()