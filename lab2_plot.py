import csv
import matplotlib.pyplot as plt
times = []
intervals = []
def file_reader(file_name):
    with open(file_name, encoding='utf-8') as r_file:
        dump = csv.reader(r_file, delimiter=",")
        count = 0
        for row in dump:
            if count != 0:
                times.append(row[1])
            count += 1
          
file_reader('5.csv')

for i in range(len(times)):
    if i != len(times) - 1:
        intervals.append(float(times[i + 1]) - float(times[i]))
      
distributed_intervals = []
counts = []

temp = 0
while temp < 4:
    distributed_intervals.append(temp)
    counts.append(0)
    temp += 0.1
  
for i in range(len(intervals)):
    for j in range(len(distributed_intervals) - 1):
        if distributed_intervals[j] < intervals[i] and intervals[i] < distributed_intervals[j + 1]:
            counts[j] += 1
            break
          
fig, ax = plt.subplots()
ax.bar(distributed_intervals, counts, width=0.3)
plt.show()
