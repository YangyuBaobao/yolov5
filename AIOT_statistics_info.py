import os

from matplotlib import pyplot as plt


def getLabel(s):
    s = s[s.find('name')+len('name'):] # 截取第一个name后面的内容（假设都存在如果有name的话）
    s = s[s.find('>') + 1:s.find('<')] # 截取括号中的内容（假设左右括号成对出现，不嵌套）
    return(s)

def Plo2class(Dir,title):
    New_Dir=Dir.copy()
    Null_List=[]

    for k in New_Dir:
        if(New_Dir[k]==0):
            Null_List.append(k)
    for i in range(len(Null_List)):
        New_Dir.pop(Null_List[i])

    labels = []
    data = []

    for k in New_Dir:
        labels.append(k)
        data.append(New_Dir[k])

    # 绘图。
    fig, ax = plt.subplots()
    b = ax.barh(range(len(labels)), data, color='#6699CC')

    # 为横向水平的柱图右侧添加数据标签。
    for rect in b:
        w = rect.get_width()
        ax.text(w, rect.get_y() + rect.get_height() / 2, '%d' %
                int(w), ha='left', va='center')

    # 设置Y轴纵坐标上的刻度线标签。
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels)

    # 不要X横坐标上的label标签。
    plt.xticks(())

    plt.title('水平横向的柱状图', loc='center', fontsize='25',
              fontweight='bold', color='red')

    plt.title(title)
    # plt.savefig('Statistics.jpg')
    plt.show()
    plt.close()

path='VOCdevkit/VOC2007/Annotations'
list_file=os.listdir(path)

Number_sum=0
dic_classes=dict()

for item in list_file:
    full_path=os.path.join(path,item)

    with open(full_path, "r", encoding='utf-8') as f:
        data = f.readlines()#读取每个xml里面的内容
    f.close()

    for line in data:
        if('<name>'in line)and('/name'in line):
            label=getLabel(line)
            Number_sum += 1

            if  label in dic_classes.keys():
                dic_classes[label]+=1
            else:
                dic_classes[label]=0

print('标注对象总个数：'+str(Number_sum))

list_classes=list(dic_classes.keys())
list_number=list()

for key in list_classes:
    list_number.append(dic_classes[key])

print(list_classes) # x
Plo2class(dic_classes,'Number of each category')

# print(list_number) # Y











