import shutil
annotations = "./Annotations/"
images = "./JPEGImages/"
train = './train/'
val = './val/'
test = './test/'
annotations_train = './Annotations_train/'
annotations_val = './Annotations_val/'
annotations_test = './Annotations_test/'


def copyfile(lab, filename):
    # copy process from fetched filename
    if lab == 'train':
        shutil.copy(images + filename + '.jpg', train + filename + '.jpg')
        shutil.copy(annotations + filename + '.xml',
                    annotations_train + filename + '.xml')
    if lab == 'val':
        shutil.copy(images + filename + '.jpg', val + filename + '.jpg')
        shutil.copy(annotations + filename + '.xml',
                    annotations_val + filename + '.xml')
    if lab == 'test':
        shutil.copy(images + filename + '.jpg', test + filename + '.jpg')
        shutil.copy(annotations + filename + '.xml',
                    annotations_test + filename + '.xml')
    return


def catfile(lab, file):
    with open(file, 'r') as fp:
        for f in fp:
            f = f.rstrip()
            copyfile(lab, f)


catfile('train', './ImageSets/Main/train.txt')
catfile('test', './ImageSets/Main/test.txt')
catfile('val', './ImageSets/Main/val.txt')
