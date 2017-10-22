import matplotlib.pyplot as plt

with open('上海-2016.csv', 'r') as csv_file:
    lines = csv_file.readlines()
    lines.pop(0)
    data_list = []
    for line in lines:
        line = line.rstrip()
        line = line.split(',')
        data = int(line[2])
        data_list.append(data)

plt.plot(data_list)
plt.ylabel('PM2.5')
plt.savefig('result.png')
plt.show()