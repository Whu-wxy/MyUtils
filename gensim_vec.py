
##....................convert glove to word2ve..........................
# from gensim.scripts.glove2word2vec import glove2word2vec
#
# glove_input_file = 'F:\\dl-data\\vector\\glove.twitter.27B.25d.txt'
# word2vec_output_file = 'F:\\dl-data\\vector\\glove.twitter.27B.25d.word2vec.txt'
# (count, dimensions) = glove2word2vec(glove_input_file, word2vec_output_file)
# print(count, '\n', dimensions)
##..............................................................

from gensim.models import KeyedVectors
import time
import os
import numpy as np
import matplotlib.pyplot as plt

words = ['cat', 'dog', 'pig', 'fish', 'sheep',
         'basketball', 'football', 'tennis', 'badminton',
         'man', 'woman', 'king', 'queen', 'doctor',
         'wuhan', 'beijing', 'shandong']

word2vec_file = 'F:\\dl-data\\vector\\glove.twitter.27B.25d.word2vec.txt'

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


word2vec_visual(words, word2vec_file, 'F:\\zzzzzzz')


# print(cat_vec)
# 获得单词frog的最相似向量的词汇
# print(glove_model.most_similar('frog'))

# most_similar = glove_model.most_similar(positive=['woman', 'king'], negative=['man'])
# print("{}: {:.4f}".format(*most_similar[0]))
# # woman+king-man = queen
# # king-man = queen-woman
# # v(“国王”) – v(“王后”) ≈ v(“男”) – v(“女”)
#
# similarity = glove_model.similarity('woman', 'man')
# print(similarity)


