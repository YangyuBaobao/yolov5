import os
from PIL import Image
import xml.etree.ElementTree as ET

def getImageInfo(Path_img):
    img = Image.open(Path_img)
    width=img.size[0]
    height=img.size[1]

    return width,height

def Create_head(img_path,width,height):
    img_name = os.path.split(img_path)[1][:-4]
    with open(img_path,"w",encoding='UTF-8') as f:
        f.write('<annotation>\n')
        f.write('   <folder>Annotations</folder>\n')
        f.write('   <filename>'+img_name+'.jpg</filename>\n')
        f.write('   <path>F:\DateSet\VOCdevkit\VOC2007\Annotations\example.JPG</path>\n')
        f.write('   <source>\n')
        f.write('       <database>Unknown</database>\n')
        f.write('   </source>\n')
        f.write('   <size>\n')
        f.write('       <width>'+str(width)+'</width>\n')
        f.write('       <height>'+str(height)+'</height>\n')
        f.write('       <depth>3</depth>\n')
        f.write('    </size>\n')
        f.write('    <segmented>0</segmented>\n')
        f.close()

def Add_object(img_path,label,x1,y1,x2,y2):
    with open(img_path,"a",encoding='UTF-8') as f:
        f.write('       <object>\n')
        f.write('       <name>'+label+'</name>\n')
        f.write('       <pose>Unspecified</pose>\n')
        f.write('       <truncated>0</truncated>\n')
        f.write('       <difficult>0</difficult>\n')
        f.write('       <bndbox>\n')
        f.write('           <xmin>'+str(x1)+'</xmin>\n')
        f.write('           <ymin>'+str(y1)+'</ymin>\n')
        f.write('           <xmax>'+str(x2)+'</xmax>\n')
        f.write('           <ymax>'+str(y2)+'</ymax>\n')
        f.write('       </bndbox>\n')
        f.write('       </object>\n')
        f.close()

def Add_end(img_path):
    with open(img_path,"a",encoding='UTF-8') as f:
        f.write('</annotation>')
        f.close()


path=r'VOCdevkit/VOC2007/Annotations'
list_file=os.listdir(path)

new_xml='new_xml'
if not os.path.exists(new_xml):
    os.mkdir(new_xml)

for item in list_file:

    src_full_path=os.path.join(path,item)
    dst_full_path=os.path.join(new_xml,item)

    img_name = item[:-4]+'.jpg'
    img_path=os.path.join('VOCdevkit/VOC2007/JPEGImages',img_name)
    width,height=getImageInfo(img_path)

    Create_head(dst_full_path,width,height)

    tree = ET.parse(src_full_path)
    root = tree.getroot()
    outputs = root.find('outputs')
    object = root.find('object')
    item = root.find('item')

    for it in root.iter('item'): #每一个标注对象
        name=it.find('name').text

        bndbox=it.find('bndbox')
        xmin = bndbox.find('xmin').text
        ymin = bndbox.find('ymin').text
        xmax = bndbox.find('xmax').text
        ymax = bndbox.find('ymax').text

        Add_object(dst_full_path, name, xmin, ymin, xmax, ymax)

        print(name,xmin,ymin,xmax,ymax)
    print('*'*100)
    Add_end(dst_full_path)

    # w = int(size.find('width').text)
    # h = int(size.find('height').text)
    #
    # with open(src_full_path, "r") as f:
    #     data = f.readlines()
    # f.close()
    #
    #
    # for line in data:
    #     if(origin_label in line):
    #         line=line.replace(origin_label,des_label)
    #
    #     with open(full_path, "a") as f:
    #         f.write(line)
    # f.close()


