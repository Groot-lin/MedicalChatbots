coding: "utf-8"
import os
import json
from py2neo import Graph, Node

'''构建neo4j数据库'''
class MedicalGraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])  # 获取当前绝对路径的上层目录 linux中应用'/'split和join
        self.data_path = os.path.join(cur_dir, 'data/medical.json')  # 获取json文件路径
        print(self.data_path)
        self.g = Graph("http://0.0.0.0/:7474", auth=("neo4j", "neo4j"))# 修改信息

    '''读取文件'''

    def read_nodes(self):
        # 共6类节点，节点的设置与业务相关

        checks = []  # 检查
        departments = []  # 科室
        diseases = []  # 疾病
        drugs = []  # 药品
        foods = []  # 食物
        symptoms = []  # 症状

        # 这一项没有出现在节点中，在后面编程中用于创建疾病信息表
        disease_infos = []  # 疾病信息

        # 构建节点实体关系,共11类，medical2做出来的只有10类，因为数据量少
        rels_noteat = []  # 疾病－忌吃食物关系
        rels_doeat = []  # 疾病－宜吃食物关系
        rels_commondrug = []  # 疾病－药品关系
        rels_check = []  # 疾病－检查关系
        rels_symptom = []  # 疾病-症状关系
        rels_acompany = []  # 疾病-并发关系
        rels_category = []  # 疾病-科室的关系

        count = 0
        # 构造疾病字典
        for data in open(self.data_path):
            disease_dict = {}
            count += 1
            print(count)
            data_json = json.loads(data)  # 读取数据
            disease = data_json['name']
            disease_dict['name'] = disease
            diseases.append(disease)
            disease_dict['desc'] = ''
            disease_dict['prevent'] = ''
            disease_dict['cause'] = ''
            disease_dict['easy_get'] = ''
            disease_dict['cure_department'] = ''
            disease_dict['cure_way'] = ''
            disease_dict['cure_lasttime'] = ''
            disease_dict['symptom'] = ''
            disease_dict['cured_prob'] = ''

            # 查找一下词条是否在提取出来的文档段中，每一条文档段内容长度不一
            if 'symptom' in data_json:
                symptoms += data_json['symptom']  # +号用于组合列表
                for symptom in data_json['symptom']:  # 用for循环的原因：一个疾病可能对应好几个症状，手画图表示
                    rels_symptom.append([disease, symptom])  # 对于每个症状都建立一个疾病——症状的关系

            if 'acompany' in data_json:
                for acompany in data_json['acompany']:  # 同上，一个疾病可能伴随多个并发症
                    rels_acompany.append([disease, acompany])  # 建立一个疾病——伴随疾病的关系

            if 'desc' in data_json:
                disease_dict['desc'] = data_json['desc']  # 疾病描述，这里不是关系，而是定义的属性。根据业务要求把一个字段定义为关系或者节点的属性

            if 'prevent' in data_json:
                disease_dict['prevent'] = data_json['prevent']  # 疾病预防

            if 'cause' in data_json:
                disease_dict['cause'] = data_json['cause']  # 引起疾病的原因

            if 'get_prob' in data_json:
                disease_dict['get_prob'] = data_json['get_prob']  # 发病率

            if 'easy_get' in data_json:
                disease_dict['easy_get'] = data_json['easy_get']  # 易感人群

            if 'cure_department' in data_json:
                cure_department = data_json['cure_department']  # 治疗科室
                rels_category.append([disease, cure_department[0]])
                disease_dict['cure_department'] = cure_department
                departments += cure_department

            if 'cure_way' in data_json:
                disease_dict['cure_way'] = data_json['cure_way']  # 治疗途径

            if 'cure_lasttime' in data_json:
                disease_dict['cure_lasttime'] = data_json['cure_lasttime']  # 治疗时间

            if 'cured_prob' in data_json:
                disease_dict['cured_prob'] = data_json['cured_prob']  # 治愈概率

            if 'common_drug' in data_json:
                common_drug = data_json['common_drug']  # 常用药物
                for drug in common_drug:
                    rels_commondrug.append([disease, drug])  # 提取疾病——药物的关系
                drugs += common_drug

            if 'not_eat' in data_json:
                not_eat = data_json['not_eat']  # 不能吃的食物,忌口
                for _not in not_eat:
                    rels_noteat.append([disease, _not])  # 提取疾病——不能吃的食物的关系
                foods += not_eat

                do_eat = data_json['do_eat']  # 可以吃的食物
                for _do in do_eat:
                    rels_doeat.append([disease, _do])  # 提取疾病——能吃的食物的关系
                foods += do_eat

            if 'check' in data_json:
                check = data_json['check']  # 检查项，一个疾病对应多个检查
                for _check in check:
                    rels_check.append([disease, _check])  # 提取疾病——检查项的关系
                checks += check
            disease_infos.append(disease_dict)  # 添加疾病信息list

        # 共返回6类节点,七种关系
        return set(drugs), set(foods), set(checks), set(departments), set(symptoms), set(diseases), disease_infos, \
            rels_check, rels_noteat, rels_doeat, rels_commondrug, \
            rels_symptom, rels_acompany, rels_category

    '''建立节点'''

    def create_node(self, label, nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.g.create(node)
            count += 1
            print(count, len(nodes))
        return

    '''创建知识图谱中心疾病的节点,存放节点信息'''
    def create_diseases_nodes(self, disease_infos):
        count = 0
        for disease_dict in disease_infos:
            node = Node("Disease", name=disease_dict['name'], desc=disease_dict['desc'],
                        prevent=disease_dict['prevent'], cause=disease_dict['cause'],
                        easy_get=disease_dict['easy_get'], cure_lasttime=disease_dict['cure_lasttime'],
                        cure_department=disease_dict['cure_department']
                        , cure_way=disease_dict['cure_way'], cured_prob=disease_dict['cured_prob'])  # 各个疾病节点的属性
            self.g.create(node)
            count += 1
            print(count)
        return

    '''创建知识图谱实体节点类型,节点个数多，创建过程慢'''
    def create_graphnodes(self):
        Drugs, Foods, Checks, Departments, Symptoms, Diseases, disease_infos, rels_check, rels_noteat, rels_doeat, rels_commondrug, rels_symptom, rels_acompany, rels_category = self.read_nodes()
        self.create_diseases_nodes(disease_infos)  # 调用上面的疾病节点创建函数
        self.create_node('Drug', Drugs)  # 创建药物节点
        print(len(Drugs))
        self.create_node('Food', Foods)  # 创建食物节点
        print(len(Foods))
        self.create_node('Check', Checks)  # 创建检查节点
        print(len(Checks))
        self.create_node('Department', Departments)  # 创建科室节点
        print(len(Departments))
        self.create_node('Symptom', Symptoms)  # 创建症状节点
        return

    '''创建11种实体关系边'''
    def create_graphrels(self):
        Drugs, Foods, Checks, Departments, Symptoms, Diseases, disease_infos, rels_check, rels_noteat, rels_doeat, rels_commondrug, rels_symptom, rels_acompany, rels_category = self.read_nodes()
        self.create_relationship('Disease', 'Food', rels_noteat, 'no_eat', '忌吃')
        self.create_relationship('Disease', 'Food', rels_doeat, 'do_eat', '宜吃')
        self.create_relationship('Disease', 'Check', rels_check, 'need_check', '诊断检查')
        self.create_relationship('Disease', 'Symptom', rels_symptom, 'has_symptom', '症状')
        self.create_relationship('Disease', 'Disease', rels_acompany, 'acompany_with', '并发症')
        self.create_relationship('Disease', 'Department', rels_category, 'belongs_to', '所属科室')

    '''创建实体关联边'''
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):  # 起点节点，终点节点，边，关系类型，关系名字
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))  # 使用###作为不同关系之间分隔的标志
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')  # 选取前两个关系，因为两个节点之间一般最多两个关系
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)  # match语法，p，q分别为标签，rel_type关系类别，rel_name 关系名字
            try:
                self.g.run(query)  # 执行语句
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return

    '''导出数据'''
    def export_data(self):
        Drugs, Foods, Checks, Departments, Symptoms, Diseases, disease_infos, rels_check, rels_noteat, rels_doeat, rels_commondrug, rels_symptom, rels_acompany, rels_category = self.read_nodes()
        f_drug = open('drug.txt', 'w+')
        f_food = open('food.txt', 'w+')
        f_check = open('check.txt', 'w+')
        f_department = open('department.txt', 'w+')
        f_symptom = open('symptoms.txt', 'w+')
        f_disease = open('disease.txt', 'w+')

        f_drug.write('\n'.join(list(Drugs)))
        f_food.write('\n'.join(list(Foods)))
        f_check.write('\n'.join(list(Checks)))
        f_department.write('\n'.join(list(Departments)))
        f_symptom.write('\n'.join(list(Symptoms)))
        f_disease.write('\n'.join(list(Diseases)))

        f_drug.close()
        f_food.close()
        f_check.close()
        f_department.close()
        f_symptom.close()
        f_disease.close()

        return


if __name__ == '__main__':
    handler = MedicalGraph()  # 创建图数据库
    # handler.export_data()#输出数据，可以选择不执行
    handler.create_graphnodes()  # 创建节点
    handler.create_graphrels()  # 创建关系
