import json

file_json = 'result.json'
map_json = 'Name_map.json'

f = open(map_json)
dic = json.load(f)
f.close()


def format_trans(filename):
    with open(filename) as f:
        pop = json.load(f)
        out = open('result.txt', 'a')
        img_id = -1
        for item in pop:
            if img_id == item['image_id']:
                out.write(str(item['category_id']) + ' ' +
                          str(item['score']) + ' ' + str(item['bbox'])[1:-1] + '\n')
            else:
                img_id = item['image_id']
                out.close()
                out = open(
                    'result/' + str(dic[img_id - 1]['file_name'][:-4]) + '.txt', 'a')
                out.write(str(item['category_id']) + ' ' +
                          str(item['score']) + ' ' + str(item['bbox'])[1:-1] + '\n')
        out.close()


format_trans(file_json)
