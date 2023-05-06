# coding=gbk
from chat_robot import ChatRobot
from keyword_template import KeyWordTemplate
from flask import Flask
from flask_cors import CORS
from flask import request
import json


app = Flask(__name__)
CORS(app)# ���ÿ���
ans = 'С��û���������������\n�������������ϵפ̨ҽ����'

keyword = KeyWordTemplate()
handler = ChatRobot()

@app.route('/question', methods=['POST'])
def controller():
    # ���json��ʽ���ַ���
    data = request.get_data()
    # ���json��ʽ
    json_data = json.loads(data.decode("utf-8"))
    # ��ȡ����
    question = json_data.get('question')

    print('\n')
    print(question)
    return robot(question)
# ��ȡ��
def robot(question):
    answer = handler.chat_main(question)
    if ans == answer:
        answer = keyword.getTempalte(question)
    if answer == None:
        answer = ans
    # ���ɴ��ֵ�
    ans_dict = dict()
    ans_dict['answer'] = answer

    # ��ȡjson��ʽ
    ans_json = json.dumps(ans_dict)
    print(answer)
    print('\n')
    return ans_json



# main��������
if __name__ == '__main__':
    app.run(host='localhost',port=5000,debug=True)




