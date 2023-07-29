import os



path=r'VOCdevkit/VOC2007/Annotations2'
list_file=os.listdir(path)

origin_label='Mediurm_Ripeness'
des_label='Medium_Ripeness'

    #遍历每一个文件
for item in list_file:
    full_path=os.path.join(path,item)

    with open(full_path, "r") as f:
        data = f.readlines()#读取每个xml里面的内容
    f.close()

    with open(full_path, "w") as f:
        f.write('')

    for line in data:
        if(origin_label in line):
            line=line.replace(origin_label,des_label)

        with open(full_path, "a") as f:
            f.write(line)
    f.close()



