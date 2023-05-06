# coding=gbk
from chat_robot import ChatRobot
from keyword_template import KeyWordTemplate
from flask import Flask
from flask_cors import CORS
from flask import request
import json


app = Flask(__name__)
CORS(app)# 设置跨域
ans = '小康没能理解您的问题呢\n换个问题或者联系驻台医生吧'

keyword = KeyWordTemplate()
handler = ChatRobot()

@app.route('/question', methods=['POST'])
def controller():
    # 获得json格式的字符串
    data = request.get_data()
    # 获得json格式
    json_data = json.loads(data.decode("utf-8"))
    # 获取问题
    question = json_data.get('question')

    print('\n')
    print(question)
    return robot(question)
# 获取答案
def robot(question):
    answer = handler.chat_main(question)
    if ans == answer:
        answer = keyword.getTempalte(question)
    if answer == None:
        answer = ans
    # 生成答案字典
    ans_dict = dict()
    ans_dict['answer'] = answer

    # 获取json格式
    ans_json = json.dumps(ans_dict)
    print(answer)
    print('\n')
    return ans_json



# main启动函数
if __name__ == '__main__':
    app.run(host='localhost',port=5000,debug=True)




