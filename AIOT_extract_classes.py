import os
import os.path as osp
import shutil
from glob import glob
from tqdm import tqdm
import xml.etree.ElementTree as ET


def get_classes(srcpath, savepath, classes=None):
    """获取含有我们选定类别的标注图片和标签文件，原数据集不产生任何影响

    Args:
        srcpath (str): VOC数据集路径，在JPEGImages和Annotations上一级
        savepath (str): 保存获取数据的位置
        classes (list, optional): _description_. Defaults to None.用来指定我们要提取的分类

    Raises:
        Exception: _description_
    """

    lbs = glob(osp.join(srcpath, "Annotations", '*.xml'))
    if classes is not None:
        if osp.exists(savepath):
            shutil.rmtree(savepath)  # 因为不影响原始文件，所以可以直接删除
        os.makedirs(savepath, exist_ok=False)
        savepath_img = osp.join(savepath, "JPEGImages")
        savepath_xml = osp.join(savepath, "Annotations")
        os.makedirs(savepath_img)
        os.makedirs(savepath_xml)
        for lb in tqdm(lbs):
            tree = ET.parse(lb)
            root = tree.getroot()
            objs = root.findall("object")
            num = 0
            for obj in objs:
                if obj.find("name").text not in classes:
                    root.remove(obj)  # 删除标注文件中所有不需要的标注框
                else:
                    num += 1
            if num > 0:  # 删除完不需的框后任有剩余的框
                name = osp.splitext(osp.split(lb)[-1])[0]
                tree.write(osp.join(savepath_xml, name + '.xml'))
                img = osp.join(srcpath, "JPEGImages", name + '.jpg')
                shutil.copy(img, savepath_img)

        print("Done")
    else:
        print("需要定义合理的classes")

get_classes(srcpath="VOCdevkit/VOC2007",savepath='nianchong',classes=['nianchong'])
