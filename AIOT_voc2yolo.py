import shutil
import xml.etree.ElementTree as ET
import os
from PIL import Image
import random
from shutil import copyfile


#纠错版本： ---时间：2021.05.31 
    #<1>针对网图标注后获取不到宽度长度问题：运行第一遍会把有有问题的图片的标注的xml，重新生成好的xml文件，但是保存在照片路径下，需要手动去替换。
        # 替换后再次运行这个程序就把所有的文件都转换成yolo格式了。
    #<2>针对标注中数据标签difficult的处理。
    #<3>路径修改为相对路径，可跨机划分数据集。
    #<4>编码问题

#根据自己的数据标签修改
classes=['person']

def Write_Img_Info_2_Xml(ImgPath,Path_xml):
    img = Image.open(ImgPath)
    width=img.size[0]
    height=img.size[1]


    prcess_Label1='<width>'
    prcess_Label2='<height>'

    #读取原xml
    with open(Path_xml,"r",encoding='UTF-8') as f:    #设置文件对象
        info_Lines = f.readlines()    #可以是随便对文件的操作
        f.close()
    # os.remove(Path_xml)

    Nem_save_path=Path_xml.replace('Annotations','JPEGImages')
    with open(Nem_save_path,'w',encoding='UTF-8') as NewXml:

        for Line  in  info_Lines:
            if((prcess_Label1 not in Line)and(prcess_Label2 not in Line)):
                NewXml.writelines(Line)
            if('<width>' in Line):
                RPS1=Line.replace('>0<',('>'+str(width)+'<'))
                NewXml.writelines(RPS1)

            if ('<height>' in Line):
                RPS2=Line.replace('>0<', ('>' + str(height) + '<'))
                NewXml.writelines(RPS2)

        NewXml.close()

def clear_hidden_files(path):
    dir_list = os.listdir(path)
    for i in dir_list:
        abspath = os.path.join(os.path.abspath(path), i)
        if os.path.isfile(abspath):
            if i.startswith("._"):
                os.remove(abspath)
        else:
            clear_hidden_files(abspath)

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def mycopyfile(srcfile,dstpath):
    if not os.path.isfile(srcfile):
        print ("%s not exist!"%(srcfile))
    else:
        shutil.copy(srcfile, dstpath)
        print ("copy %s -> %s"%(srcfile, dstpath ))

def convert_annotation(image_id):
    in_file = open('VOCdevkit/VOC2007/Annotations/%s.xml' %image_id,encoding='UTF-8')
    out_file = open('VOCdevkit/VOC2007/YOLOLabels/%s.txt' %image_id, 'w',encoding='UTF-8')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        if obj.find('difficult'):
            difficult = int(obj.find('difficult').text)
        else:
            difficult = 0
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        if(w==0 or h==0):
            Write_Img_Info_2_Xml(('VOCdevkit/VOC2007/JPEGImages/%s.jpg' %image_id),('VOCdevkit/VOC2007/Annotations/%s.xml' %image_id))
            # bb = convert((w, h), b)
            # out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
            # mycopyfile(('VOCdevkit/VOC2007/JPEGImages/%s.jpg' %image_id),('F:/ReMark/%s.jpg' %image_id))
            # mycopyfile(('VOCdevkit/VOC2007/Annotations/%s.xml' %image_id),('F:/ReMark/%s.xml' %image_id))
        else:
            bb = convert((w,h), b)
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
    in_file.close()
    out_file.close()

# wd = os.getcwd()
wd=''
data_base_dir = os.path.join(wd, "VOCdevkit/")
# data_base_dir = os.path.join("VOCdevkit/")
if not os.path.isdir(data_base_dir):
    os.mkdir(data_base_dir)
work_sapce_dir = os.path.join(data_base_dir, "VOC2007/")
if not os.path.isdir(work_sapce_dir):
    os.mkdir(work_sapce_dir)
annotation_dir = os.path.join(work_sapce_dir, "Annotations/")
if not os.path.isdir(annotation_dir):
        os.mkdir(annotation_dir)
clear_hidden_files(annotation_dir)
image_dir = os.path.join(work_sapce_dir, "JPEGImages/")
if not os.path.isdir(image_dir):
        os.mkdir(image_dir)
clear_hidden_files(image_dir)
yolo_labels_dir = os.path.join(work_sapce_dir, "YOLOLabels/")
if not os.path.isdir(yolo_labels_dir):
        os.mkdir(yolo_labels_dir)
clear_hidden_files(yolo_labels_dir)
yolov5_images_dir = os.path.join(data_base_dir, "images/")
if not os.path.isdir(yolov5_images_dir):
        os.mkdir(yolov5_images_dir)
clear_hidden_files(yolov5_images_dir)
yolov5_labels_dir = os.path.join(data_base_dir, "labels/")
if not os.path.isdir(yolov5_labels_dir):
        os.mkdir(yolov5_labels_dir)
clear_hidden_files(yolov5_labels_dir)
yolov5_images_train_dir = os.path.join(yolov5_images_dir, "train/")
if not os.path.isdir(yolov5_images_train_dir):
        os.mkdir(yolov5_images_train_dir)
clear_hidden_files(yolov5_images_train_dir)
yolov5_images_test_dir = os.path.join(yolov5_images_dir, "val/")
if not os.path.isdir(yolov5_images_test_dir):
        os.mkdir(yolov5_images_test_dir)
clear_hidden_files(yolov5_images_test_dir)
yolov5_labels_train_dir = os.path.join(yolov5_labels_dir, "train/")
if not os.path.isdir(yolov5_labels_train_dir):
        os.mkdir(yolov5_labels_train_dir)
clear_hidden_files(yolov5_labels_train_dir)
yolov5_labels_test_dir = os.path.join(yolov5_labels_dir, "val/")
if not os.path.isdir(yolov5_labels_test_dir):
        os.mkdir(yolov5_labels_test_dir)
clear_hidden_files(yolov5_labels_test_dir)

train_file = open(os.path.join(wd, "yolov5_train.txt"), 'w',encoding='UTF-8')
test_file = open(os.path.join(wd, "yolov5_val.txt"), 'w',encoding='UTF-8')
train_file.close()
test_file.close()
train_file = open(os.path.join(wd, "yolov5_train.txt"), 'a',encoding='UTF-8')
test_file = open(os.path.join(wd, "yolov5_val.txt"), 'a',encoding='UTF-8')
list_imgs = os.listdir(image_dir) # list image files
probo = random.randint(1, 100)
print("Probobility: %d" % probo)
for i in range(0,len(list_imgs)):
    path = os.path.join(image_dir,list_imgs[i])
    if os.path.isfile(path):
        image_path = image_dir + list_imgs[i]
        image_path=image_path.replace('\\','/')
        voc_path = list_imgs[i]
        print('#'*30)
        print(voc_path)
        (nameWithoutExtention, extention) = os.path.splitext(os.path.basename(image_path))
        (voc_nameWithoutExtention, voc_extention) = os.path.splitext(os.path.basename(voc_path))
        annotation_name = nameWithoutExtention + '.xml'
        annotation_path = os.path.join(annotation_dir, annotation_name)
        label_name = nameWithoutExtention + '.txt'
        label_path = os.path.join(yolo_labels_dir, label_name)
    probo = random.randint(1, 100)
    print("Probobility: %d" % probo)
    if(probo < 80): # train dataset
        if os.path.exists(annotation_path):
            train_file.write(image_path + '\n')
            convert_annotation(nameWithoutExtention) # convert label
            copyfile(image_path, yolov5_images_train_dir + voc_path)
            copyfile(label_path, yolov5_labels_train_dir + label_name)
    else: # test dataset
        if os.path.exists(annotation_path):
            test_file.write(image_path + '\n')
            convert_annotation(nameWithoutExtention) # convert label
            copyfile(image_path, yolov5_images_test_dir + voc_path)
            copyfile(label_path, yolov5_labels_test_dir + label_name)
    print('#'*30)
    print()
train_file.close()
test_file.close()

L_xml=os.listdir('VOCdevkit/VOC2007/Annotations')
L_img=os.listdir('VOCdevkit/VOC2007/JPEGImages')

if(len(L_xml)!=len(L_img)):
    print('标注文件有误，已在JPEGImages文件夹下重新生成xml文件，请替换后再次运行本程序。')
