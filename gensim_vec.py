
##....................convert glove to word2ve..........................
# from gensim.scripts.glove2word2vec import glove2word2vec
#
# glove_input_file = 'F:\\dl-data\\vector\\glove.twitter.27B.25d.txt'
# word2vec_output_file = 'F:\\dl-data\\vector\\glove.twitter.27B.25d.word2vec.txt'
# (count, dimensions) = glove2word2vec(glove_input_file, word2vec_output_file)
# print(count, '\n', dimensions)
##..............................................................

from typing import Dict
from gensim.models import KeyedVectors
import time
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import torch
import torch.nn.functional as F



words = ['man', 'woman', 'king', 'queen', 'uncle', 'aunt',
         'china', 'beijing', 'england', 'london', 'france', 'paris']
# 'delight', 'happy', 'joy', 'angry', 'grief', 'sad'

word2vec_file = 'F:\\dl-data\\vector\\glove\\glove.840B.300d.word2vec.txt' 
     # glove.840B.300d.word2vec.txt
     # glove.twitter.27B.25d.word2vec.txt

#把词向量映射到二维空间表示
def visualize_vec(matrix, save_path: str=None) -> None:
    """
    :param matrix: num_words * dimensions
    :param save_path: save final image to a dir.
    :return: None
    """
    if save_path is not None:
        if os.path.exists(save_path) == False:
            os.mkdir(save_path)

    cur_time = time.strftime("%Y%m%d_%H%M", time.localtime())
    if save_path is not None:
        cur_time = save_path + '/' + cur_time

    la = np.linalg
    U, s, Vh = la.svd(matrix, full_matrices=False)
    for i in range(matrix.shape[0]):   # word
        plt.text(U[i, 0], U[i, 1], words[i])

    coord = U[:, 0:2]
    plt.xlim((np.min(coord[:, 0]) - 0.1, np.max(coord[:, 0]) + 0.1))
    plt.ylim((np.min(coord[:, 1]) - 0.1, np.max(coord[:, 1]) + 0.1))

    # 保存
    savedir = cur_time + '.jpg'
    plt.savefig(savedir, dpi=1000, bbox_inches='tight')

    plt.show()

def word2vec_visual(words, word2vec_file, save_path: str=None) -> None:
    """
    :param words: a list of word.
    :param word2vec_file: word2vec format file, you can convert glove file to word2vec file.
    :param save_path: a dir to save image, if this directory is absent, the program automatically creates it.
    :return: None
    """
    # 加载模型
    glove_model = KeyedVectors.load_word2vec_format(word2vec_file, binary=False)
    matrix = []
    for word in words:
        matrix.append(glove_model[word])

    matrix = np.stack(matrix, 0)
    # print('shape:', matrix.shape)
    visualize_vec(matrix, save_path)


def save_vector(tokens, w2v_file):
    glove_model = KeyedVectors.load_word2vec_format(w2v_file, binary=False)
    for token in tokens:
        save_path = 'F:\\' + token + '.txt'
        with open(save_path, 'w') as f:
            vec = str(glove_model[token])
            f.write(vec[1:-1])


def get_vector_from_file(token1, token2):
    save1 = 'F:\\论文\\毕设\\词向量可视化\\words\\' + token1 + '.txt'
    save2 = 'F:\\论文\\毕设\\词向量可视化\\words\\' + token2 + '.txt'  
    t1 = []
    t2 = []
    with open(save1, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line.strip('\n')
            line = ' '.join(line.split())
            for number in line.split(' '):
                t1.append(float(number))
    with open(save2, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line.strip('\n')
            line = ' '.join(line.split())
            for number in line.split(' '):
                t2.append(float(number))   
    return t1, t2  

def get_vector_from_files(tokens):
    vecs = {}
    for token in tokens:
        vec = []
        save_path = 'F:\\论文\\毕设\\词向量可视化\\words\\' + token + '.txt'
        with open(save_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line.strip('\n')
                line = ' '.join(line.split())
                for number in line.split(' '):
                    vec.append(float(number))
        vecs[token] = vec
    return vecs
##########################

def cosine_similarity(cat, dog):
    sum = 0
    for c, d in zip(cat, dog):
        sum += c*d
    ##########################
    cat_sum = 0
    for c in cat:
        cat_sum += c ** 2
    cat_sum = cat_sum ** 0.5
    ##########################
    dog_sum = 0
    for d in dog:
        dog_sum += d ** 2
    dog_sum = dog_sum ** 0.5

    cos = sum / (cat_sum * dog_sum)
    return cos

#################################################
def draw_bar(value, interval, dim, x_text, y_text, title):
    import matplotlib.pyplot as plt

    plt.rcParams['font.family'] = ['sans-serif'] #加上这个，中文显示不会乱码
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus']=False   #负号不会乱码
    
    x = np.arange(0+interval/2, dim+interval/2, interval)
    plt.bar(x, value, width=interval*0.7)

    plt.xlabel(x_text)
    plt.ylabel(y_text)
    x_ticks = np.arange(0, dim+interval, interval)
    plt.xticks(x_ticks)

    plt.title(title)
    plt.show()

#################################################
count = 0
interval = 10
dimension = 300
similarity = []
# vec1, vec2 = get_vector_from_file('king', 'queen')
# print(cosine_similarity(vec1, vec2))
# ####维度对应
# while count+interval <= dimension:
#     value = cosine_similarity(vec1[count:count+interval], vec2[count:count+interval])
#     count += interval
#     similarity.append(value)
# draw_bar(similarity, interval, dimension, 'dimensions', 'cosine_similarity', 'Segmented feature cosine similarity')

####维度不对应
# while count+interval <= dimension:
#     value = cosine_similarity(vec1[80:80+interval], vec2[count:count+interval])
#     count += interval
#     similarity.append(value)
# draw_bar(similarity, interval, dimension, 'dimensions', 'cosine_similarity', 'Segmented feature cosine similarity')



def attention_visualize(predict_result: Dict,
                  serialization_dir: str=None,
                  show_img: bool=False,
                  show_colorbar: bool=True,
                  multiImg :bool=False,
                  count: int=0) -> None:
    """
    可视化显示模型中间层的“文章-问题”相似度矩阵
    """
    if serialization_dir is not None:
        if os.path.exists(serialization_dir) == False:
            os.mkdir(serialization_dir)

    cur_time = time.strftime("%Y%m%d_%H%M", time.localtime())
    if serialization_dir is not None:
        if multiImg:
            cur_time = serialization_dir + '/' + cur_time + '('+ str(count) +')'
        else:
            cur_time = serialization_dir + '/' + cur_time

    attention = np.array(predict_result['passage_question_attention'])
    if attention.shape[0] > attention.shape[1]:
        attention = attention.transpose()

    col = np.array(predict_result['passage_tokens'])
    ind = np.array(predict_result['question_tokens'])
    df = pd.DataFrame(attention, columns=col, index=ind)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(df, interpolation='nearest', cmap='hot_r')
    if show_colorbar==True:
        fig.colorbar(cax)
    tick_spacing = 1
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    ax.set_xticklabels([''] + list(df.columns), rotation=90, fontsize=10)
    ax.set_yticklabels([''] + list(df.index), fontsize=10)

    #保存
    savedir = cur_time+'_attention.jpg'
    plt.savefig(savedir, dpi=800)
    if show_img:
        plt.show()


words = ['cat', 'beijing', 'man', 'woman', 'china', 'dog', 'king', 'queen']
# save_vector(words, word2vec_file)
def show_matrix(words, usepart:bool, part2part:bool, interval:int):
    vecs_dict = get_vector_from_files(words)
    atten_dict = {}
    atten_dict['passage_tokens'] = words
    atten_dict['question_tokens'] = words
    
    matrix = []
    if usepart:
        count = 0
        while count + interval <= 300:
            matrix = []
            for p_vec in vecs_dict.values():
                sim = []
                top = count + interval
                if part2part:
                    sim = [cosine_similarity(p_vec[count:top], q_vec[count:top]) for q_vec in vecs_dict.values()]
                else:
                    # mask = [0.1] * 300
                    # mask[count:top] = [1 for _ in range(interval)]
                    sim = [cosine_similarity(p_vec[count:top]*(300//interval), q_vec) for q_vec in vecs_dict.values()]
                matrix.append(sim)
                atten_dict['passage_question_attention'] = matrix
            count += interval
            attention_visualize(atten_dict, 'F:\\论文\\毕设\\词向量可视化\\', False, multiImg=True,count=count)
    else:
        for p_vec in vecs_dict.values():
                sim = [cosine_similarity(p_vec, q_vec) for q_vec in vecs_dict.values()]
                matrix.append(sim)
                atten_dict['passage_question_attention'] = matrix
                attention_visualize(atten_dict, 'F:\\论文\\毕设\\词向量可视化\\', True)

cat = []
beijing = []
cat, beijing  = get_vector_from_file('cat', 'beijing')
print(cosine_similarity(cat, beijing))
    

# show_matrix(words)
#show_matrix(words, True, True, 30)
# show_matrix(words, True, False, 30)


# word2vec_visual(words, word2vec_file, 'F:\\word2vec')

# print(cat_vec)
# 获得单词frog的最相似向量的词汇
# print(glove_model.most_similar('frog'))

# most_similar = glove_model.most_similar(positive=['woman', 'king'], negative=['man'])
# print("{}: {:.4f}".format(*most_similar[0]))
# # woman+king-man = queen
# # king-man = queen-woman
# # v(“国王”) – v(“王后”) ≈ v(“男”) – v(“女”)
#


# cat&dog = 0.8016855055594707
# king&queen = 0.7252610335547771