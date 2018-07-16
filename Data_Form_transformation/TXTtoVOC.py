#! /usr/bin/python
# -*- coding:UTF-8 -*-
import os
import sys
import glob
from PIL import Image


def Convert(Images, Annotations_TXT, VOC_Annotations):
    # VEDAI 图像存储位置
    src_img_dir = Images
    # VEDAI 图像的 ground truth 的 txt 文件存放位置
    src_txt_dir = Annotations_TXT
    src_xml_dir = VOC_Annotations

    img_Lists = glob.glob(src_img_dir + '/*.jpg')
    img_basenames = []  # e.g. 100.jpg
    for item in img_Lists:
        img_basenames.append(os.path.basename(item))

    img_names = []  # e.g. 100
    for item in img_basenames:
        temp1, temp2 = os.path.splitext(item)
        img_names.append(temp1)

    for img in img_names:
        im = Image.open((src_img_dir + '/' + img + '.jpg'))
        width, height = im.size

        # open the crospronding txt file
        gt = open(src_txt_dir + '/' + img + '.txt').read().splitlines()
        #gt = open(src_txt_dir + '/gt_' + img + '.txt').read().splitlines()

        # write in xml file
        #os.mknod(src_xml_dir + '/' + img + '.xml')
        xml_file = open((src_xml_dir + '/' + img + '.xml'), 'w')
        xml_file.write('<annotation>\n')
        xml_file.write('    <folder>VOC2007</folder>\n')
        xml_file.write('    <filename>' + str(img) + '.jpg' + '</filename>\n')
        xml_file.write('    <size>\n')
        xml_file.write('        <width>' + str(width) + '</width>\n')
        xml_file.write('        <height>' + str(height) + '</height>\n')
        xml_file.write('        <depth>3</depth>\n')
        xml_file.write('    </size>\n')

        # write the region of image on xml file
        for img_each_label in gt:
            # 这里如果txt里面是以逗号‘，’隔开的，那么就改为spt = img_each_label.split(',')。
            spt = img_each_label.split(' ')
            wid = float(spt[3]) * width
            hei = float(spt[4]) * height
            cen_x = float(spt[1]) * width
            cen_y = float(spt[2]) * height
            x1 = round(cen_x - wid / 2)
            x2 = round(cen_x + wid / 2)
            y1 = round(cen_y - hei / 2)
            y2 = round(cen_y + wid / 2)
            xml_file.write('    <object>\n')
            xml_file.write('        <name>' + str(spt[0]) + '</name>\n')
            xml_file.write('        <pose>Unspecified</pose>\n')
            xml_file.write('        <truncated>0</truncated>\n')
            xml_file.write('        <difficult>0</difficult>\n')
            xml_file.write('        <bndbox>\n')
            xml_file.write('            <xmin>' + str(x1) + '</xmin>\n')
            xml_file.write('            <ymin>' + str(y1) + '</ymin>\n')
            xml_file.write('            <xmax>' + str(x2) + '</xmax>\n')
            xml_file.write('            <ymax>' + str(y2) + '</ymax>\n')
            xml_file.write('        </bndbox>\n')
            xml_file.write('    </object>\n')

        xml_file.write('</annotation>')


Convert('./TXT_dataset/val/Images',
        './TXT_dataset/val/Annotations', './VOC_dataset/val/Annotations')
