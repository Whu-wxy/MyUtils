def punctuation_mend(string):
    import unicodedata
    import os

    table = {ord(f):ord(t) for f,t in zip(
        u'，。！？【】（）％＃＠＆１２３４５６７８９０“”‘’',
        u',.!?[]()%#@&1234567890""''')}
    if os.path.isfile(string):
        with open(string, 'w+', encoding='utf-8') as f:
            res = unicodedata.normalize('NFKC', f.read())
            res = res.translate(table)
            f.write(res)
    else:
        res = unicodedata.normalize('NFKC', string)
        res = res.translate(table)
        return res

print(punctuation_mend('【】（）％＃＠＆“”'))