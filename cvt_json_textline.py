# 2019/7/30 wxy

# 把json文件转为txt格式
# [[[[]]]] #类别数,图片数,最大边界框数,两点式坐标值+置信度
############2,    233,   100,       [x1,y1,x2,y2,confidence]
# convert result, each line: x1,y1,x2,y2,confidence

# Ground truth, each line: 38, 43, 920, 215, "Tiredness"

import os
import json

# only_pos：只保留坐标值？
# float2int：坐标是否转为整形
# skip_invalid_data:是否跳过不合适的坐标值？（Xmax<Xmin，Ymax<Ymin）
def json2txt(json_path, save_path, gt_path, score_threshold:int=1, only_pos:bool=True, float2int:bool=True, skip_invalid_data:bool=True):
    if not os.path.exists(json_path):
        print('json_path not exist!')
        return  
    if not os.path.exists(gt_path):
        print('gt_path not exist!')
        return      
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    image_name_id = []
    gt_data = json.load(open(gt_path))
    image_name_id = gt_data['images']

    all_data = json.load(open(json_path))
    all_data = all_data[1:]
    cls_count = len(all_data)
    for cls_num in range(cls_count):  #第一个是background
        class_save_dir = os.path.join(save_path, 'class_' + str(cls_num+1))
        os.mkdir(class_save_dir)

        class_images = all_data[cls_num]
        for i, img in enumerate(class_images):
            if image_name_id[i]['id'] != i:
                continue
            gt_file_name = image_name_id[i]['file_name'] #ICDAR2013_Test_img_100.jpg
            gt_base_name = gt_file_name.split('.')[0]
            gt_idx = int(gt_base_name.split('_')[-1])

            file_name = 'res_img_' + str(gt_idx)
            with open(os.path.join(class_save_dir, file_name+'.txt'), 'w', encoding='utf8') as img_file:
                bbox_data = []
                for bbox_obj in img:
                    str_bbox = ''
                    if skip_invalid_data:
                        if bbox_obj[0] > bbox_obj[2] or bbox_obj[1] > bbox_obj[3] \
                           or bbox_obj[2] < 0 or bbox_obj[3] < 0:
                            print('INVALID###', file_name, '###', bbox_obj)
                            continue
                    if score_threshold > float(bbox_obj[4]):
                        continue
                    if only_pos:
                        if float2int:
                            str_bbox = ','.join('%s' % int(number) for number in bbox_obj[:-1]) + '\n'
                        else:
                            str_bbox = ','.join('%s' % number for number in bbox_obj[:-1]) + '\n'
                    else:
                        if float2int:
                            str_bbox = ','.join('%s' % int(number) for number in bbox_obj[:-1]) + "," + str(bbox_obj[-1]) + '\n'
                        else:
                            str_bbox = ','.join('%s' % number for number in bbox_obj) + '\n'
                    bbox_data.append(str_bbox)
                img_file.writelines(bbox_data)
    print('Finished!')


if __name__ == "__main__":
    os.chdir('E:\ICDAR\ICDAR2013\VOC2007')
    json2txt('results2.json', './cvt_results2.0.4', 'pascal_test2007.json', score_threshold=0.4, only_pos=True, float2int=True)
