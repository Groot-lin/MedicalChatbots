# -*- coding: utf-8 -*-
import os


'''
回答一下模板问题
'''
class KeyWordTemplate:
    def __init__(self):

        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])

        self.keywords_path = os.path.join(cur_dir, 'dict/template_issues.txt')
        self.answers_path = os.path.join(cur_dir,'dict/template_answers.txt')

        # 例:self.keywords = ['生病了','不想活','做噩梦']
        self.keywords = [i.strip() for i in open(self.keywords_path,encoding="gbk") if i.strip()]
        self.answers  = [i.strip() for i in open(self.answers_path,encoding="gbk") if i.strip()]


        # 构造关键词字典
        self.template_dict = {key: value for key, value in zip(self.keywords, self.answers)}
        print("关键词机器人准备完成......")


    def getTempalte(self,question):
        for keyword in self.keywords:
            if keyword in question:
                return self.template_dict[keyword]



