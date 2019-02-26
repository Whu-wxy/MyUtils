import json
from tqdm import tqdm
import numpy as np
from typing import List
import spacy
from spacy.tokens import Token

def Count_SQuAD(file_path:str, use_spacy:bool=False):    
    #文章数量，文章片段数量，问答对数量，平均文章切分段落数， 平均文章长度，平均问题长度，平均回答长度
    dataset_count = {'article':0, 'paragraphs':0, 'qas':0, 'art_para_ave':0, 'para_ave':0, 'q_ave':0, 'a_ave':0}
    context_range = 1000
    question_range = 50
    answer_range = 50
    #统计数据
    context_word = [0 for _ in range(context_range)]
    question_word = [0 for _ in range(question_range)]
    answer_word = [0 for _ in range(answer_range)]
    answer_start = [0 for _ in range(context_range)]  #答案起始位置统计

    para_length = 0
    q_length = 0
    a_length = 0
    if use_spacy:
        nlp = spacy.load('en')

    with open(file_path, 'r') as dataset_file:
        dataset_json = json.load(dataset_file)
        dataset = dataset_json['data']
        dataset_count['article'] += len(dataset)
        for article in tqdm(dataset):
            paragraphs = article['paragraphs']
            dataset_count['paragraphs'] += len(paragraphs)
            for paragraph in paragraphs:
                context = paragraph['context']
                #统计 文章-词数
                index = len(context.split())
                if use_spacy:
                    index = len(remove_spaces(nlp(context)))
                para_length += index
                index = index if index<=(context_range-1) else context_range-1  #防止越界
                context_word[index] += 1

                qas = paragraph['qas']
                dataset_count['qas'] += len(qas)
                #统计 问题-词数
                for qa in qas:
                    question = qa['question']
                    index = len(question.split())
                    if use_spacy:
                        index = len(remove_spaces(nlp(question)))
                    q_length += index
                    index = index if index<=(question_range-1) else question_range-1
                    question_word[index] += 1
                     #统计 回答-词数
                    for answer in qa['answers']:
                        tokens = answer['text'].split()
                        a_l = len(tokens)
                        if use_spacy:
                            tokens = remove_spaces(nlp(answer['text']))
                            a_l = len(tokens)

                        a_length += a_l
                        a_l = a_l if a_l<=(answer_range-1) else answer_range-1
                        answer_word[a_l] += 1
                        #统计 回答的起始位置
                        #json中记录的answer_start是char的位置，要转为token的位置
                        span_start = answer['answer_start']
                        index = to_token_span(span_start, answer['text'])

                        index = index if index<=(context_range-1) else context_range-1
                        answer_start[index] += 1
 
        dataset_count['art_para_ave'] = dataset_count['paragraphs'] / dataset_count['article']
        dataset_count['para_ave'] = para_length / dataset_count['paragraphs']
        dataset_count['q_ave'] = q_length / dataset_count['qas']
        dataset_count['a_ave'] = a_length / (dataset_count['qas'] * 3)  #一个问题对应三个回答

        print(dataset_count)

        # draw_bar(context_word, context_range, '文章词数', '文章数量', '文章词数-文章数量统计')
        # draw_bar(question_word, question_range, '问题词数', '问题数量', '问题词数-问题数量统计')
        # draw_bar(answer_word, answer_range, '回答词数', '答案数量', '回答词数-答案数量统计')
        draw_bar(answer_start, context_range, '起始位置', '答案数量', '起始位置-答案数量统计')

        # save2file('context_word', context_word)
        # save2file('question_word', question_word)
        # save2file('answer_word', answer_word)
        save2file('answer_start', answer_start)


def draw_bar(y, x_count, x_text, y_text, title):
    import matplotlib.pyplot as plt

    plt.rcParams['font.family'] = ['sans-serif'] #加上这个，中文显示不会乱码
    plt.rcParams['font.sans-serif'] = ['SimHei']

    x = [x for x in range(x_count)]
    plt.bar(x, y, width=1)


    plt.xlabel(x_text)
    plt.ylabel(y_text)
    if x_count > 200:
        x_ticks1 = np.arange(0, x_count, 50)
        x_ticks2 = np.arange(x_count, x_count+100, 100)
        x_ticks3 = np.append(x_ticks1, x_ticks2)
        plt.xticks(x_ticks3, x_ticks3)
    else:
        x_ticks = np.arange(0, x_count+5, 5)
        plt.xticks(x_ticks)

    plt.title(title)
    plt.show()


def read_list_show(file_path):
    """
    读取保存数据的txt文件，条形图显示
    """
    with open(file_path, 'r') as f:
        data = f.read()
        data = eval(data)
        draw_bar(data, len(data), '', '', '')

def save2file(file_name, data):
    """
    保存List数据到txt文件
    """
    file_name = 'F:\\' + file_name + '.txt'
    with open(file_name, 'w') as f:
        f.write(str(data))


def to_token_span(char_start: int, passage_tokens: str) -> int:
    """
    json中保存的是字符级的位置，并且在答案首单词的前一个位置
    这里统计第一个字母到这个位置有多少个空格，作为单词位置的近似
    """
    start_index = 0
    for i in range(char_start):
        if i >= len(passage_tokens):
            break
        if passage_tokens[i].isspace():
            start_index += 1
    return start_index


def remove_spaces(tokens: List[spacy.tokens.Token]) -> List[spacy.tokens.Token]:
    """
    去除是空格的token
    """
    return [token for token in tokens if not token.is_space]



def paragraph_join(src_json, dst_text):
    with open(src_json, 'r', encoding='utf-8') as dataset_file:
        dataset_json = json.load(dataset_file)
        dataset = dataset_json['data']
        article = dataset[0]
        paragraphs = article['paragraphs']
        with open(dst_text, 'a', encoding='utf-8') as dst_file:
            for paragraph in tqdm(paragraphs):
                context = paragraph['context'] + '\n\n'
                dst_file.write(context)


# paragraph_join('F:\dl-data\datasets\SQuAD\\dev-v1.1.json', 'F:\\result.txt')

print('............................using spacy...............................')
print('........................dev-v1.1 preprocessing...........................')
Count_SQuAD('F:\dl-data\datasets\SQuAD\\dev-v1.1.json', use_spacy=True)
print('........................train-v1.1 preprocessing...........................')
Count_SQuAD('F:\dl-data\datasets\SQuAD\\train-v1.1.json', use_spacy=True)