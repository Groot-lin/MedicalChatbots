from get_answer import Answer
from get_cql import GetCQL
from question_analysis import QuestionAnalysis

'''问答机器人主类'''
class ChatRobot:
    def __init__(self):
        self.analysis = QuestionAnalysis()
        self.getCQL = GetCQL()
        self.searcher = Answer()  # 调用问题搜索子函数
        print("知识图谱机器人准备完成......")


    def chat_main(self, question):
        answer = '小康没能理解您的问题呢\n换个问题或者联系驻台医生吧'#这是初始答案
        res_analysis = self.analysis.classify(question)#'question'是用户的输入内容，利用classify函数先对其进行分类

        if not res_analysis:
            return answer#没有找到对应分类内容，返回初始答案

        res_cql = self.getCQL.parser_main(res_analysis)#调用parser_main对内容进行解析
        final_answers = self.searcher.search_main(res_cql)#对内容搜索合适的答案

        if not final_answers:
            return answer#如果没有找到合适的最终答案，返回初始答案
        else:
            return '\n'.join(final_answers)#连接字符


