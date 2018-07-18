import os
import glob
import numpy as np
import shutil
from prettytable import PrettyTable
from PIL import Image
from sklearn.cluster import KMeans


class data_analysis(object):
    def __init__(self, classes, image_size=(1080, 1920), label_map='label_map.txt', ann_path='./'):
        ''''' 
        :param xml: 所有Pascal VOC的xml文件路径组成的列表 
        :param ann_path: ann_path 
        :param classes_path: classes_path 
        '''
        self.image_size = image_size
        self.class_num = classes
        self.image_nums = np.zeros(
            classes, int)  # image_num of each categories
        self.ann_path = ann_path
        self.bbox_nums = np.zeros(classes, int)  # bbox_num of each categories
        self.bbox_width_averaged = np.zeros(
            classes, float)  # bbox_size of each categories
        self.bbox_height_averaged = np.zeros(
            classes, float)  # bbox_size of each categories
        self.multiclass_num = 0
        self.classes_name = []
        self.image_categories = {}
        self.multi_class_image = np.zeros(classes, int)
        f = open(label_map)
        for line in f.readlines():
            lab = line.rstrip().split(' ')
            self.classes_name.append(lab[1])
            self.image_categories[int(lab[0])] = []
        self.init_Analysis()
        self.show_distribution()
        # src_ann_dir = 'Annotations_TXT'
        # img_Lists = glob.glob(src_ann_dir + '/*.txt')
        # for item in img_Lists:
        #     # print(item)
        #     f = open(item, 'r')
        #     for line in f.readlines():

    def init_Analysis(self):
        ann_lists = glob.glob(self.ann_path + './Annotations/*.txt')
        bbox_width = np.zeros(self.class_num, float)
        bbox_height = np.zeros(self.class_num, float)
        for item in ann_lists:
            f = open(item, 'r')
            cat = set()
            for line in f.readlines():
                # print(line)
                data = line.rstrip().split(' ')
                category = int(data[0])
                cat.add(category)
                self.bbox_nums[category] += 1
                bbox_width[category] += float(data[3])
                bbox_height[category] += float(data[4])
            for it in cat:
                self.image_categories[it].append(
                    self.ann_path + 'Images/' + item[14:-3] + 'jpg')
            if len(cat) > 1:
                self.multiclass_num += 1
                for it in cat:
                    self.multi_class_image[it] += 1
                    # if it == 3:
                    #     img = Image.open('Images/' + item[12:-3] + 'jpg')
                    #     img.show()
            for it in cat:
                self.image_nums[it] += 1

        for i in range(self.class_num):
            self.bbox_width_averaged[i] = bbox_width[i] * \
                self.image_size[1] / self.bbox_nums[i]
            self.bbox_height_averaged[i] = bbox_height[i] * \
                self.image_size[0] / self.bbox_nums[i]

    def show_distribution(self):
        table = PrettyTable(['Category'] + self.classes_name)
        table.align = 'l'
        str_class_num = [str(ite) for ite in self.image_nums]
        table.add_row(['#Images'] + str_class_num)
        str_bbox_num = [str(ite) for ite in self.bbox_nums]
        table.add_row(['#Bbox'] + str_bbox_num)
        str_bbox_width = [str(int(ite)) for ite in self.bbox_width_averaged]
        table.add_row(['#Aver_width'] + str_bbox_width)
        str_bbox_height = [str(int(ite)) for ite in self.bbox_height_averaged]
        table.add_row(['#Aver_height'] + str_bbox_height)
        str_multi_class = [str(ite) for ite in self.multi_class_image]
        table.add_row(['#multiclass'] + str_multi_class)
        print(str(table))
        print('Number of images which have multi-categories:',
              self.multiclass_num)

    def sepdata_categories(self, ratio, target_file='sampled'):
        os.mkdir(target_file)
        os.mkdir(target_file + '/Annotations')
        os.mkdir(target_file + '/Images')
        os.mkdir('rest')
        os.mkdir('rest' + '/Annotations')
        os.mkdir('rest' + '/Images')
        for i in range(self.class_num):
            total = len(self.image_categories[i])
            sampled = round(total * ratio)
            dataset = [i for i in range(total)]
            sed_train = (np.random.choice(
                np.arange(total), sampled, replace=False))
            sed_test = list(set(dataset) - set(sed_train))
            for target in sed_train:
                # print(self.image_categories[i][target])
                # break

                shutil.copy(
                    "Images" + self.image_categories[i][target][8:], target_file + '/Images' + self.image_categories[i][target][8:])
                shutil.copy('Annotations' + self.image_categories[i][target][8:-4] + '.txt',
                            target_file + '/Annotations' + self.image_categories[i][target][8:-4] + '.txt')

            for target in sed_test:
                # print('Annotations' + self.image_categories[i][target][6:-4]+'.txt')
                # break
                try:
                    shutil.copy(
                        "Images" + self.image_categories[i][target][8:], 'rest/Images' + self.image_categories[i][target][8:])
                    shutil.copy('Annotations' + self.image_categories[i][target][8:-4] + '.txt',
                                'rest/Annotations' + self.image_categories[i][target][8:-4] + '.txt')
                except:
                    continue
        print("Dataset has been separated with ratio %d according to categories" % ratio)


a = data_analysis(7)
# a.k_means_bbox()
