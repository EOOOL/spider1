import matplotlib.pyplot as plt
from pyecharts import Bar

with open('上海-2016.csv', 'r') as csv_file:
    lines = csv_file.readlines()
    lines.pop(0)
    data_list = []
    for line in lines:
        line = line.rstrip()
        line = line.split(',')
        data = int(line[2])
        data_list.append(data)

#matplotlib可视化
def mpl_draw():
    plt.plot(data_list)
    plt.ylabel('2016-2017  PM2.5')
    plt.savefig('result.png')

#pyecharts可视化
def p_draw():
    v1 = [i for i in range(len(data_list))]
    bar = Bar("PM2.5数值")
    bar.add('上海市',v1,data_list)
    bar.render()

if __name__=="__main__":
    mpl_draw()
    p_draw()