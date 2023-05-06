
'''获取用户像所需要查询得到CQL语句'''
class GetCQL:

    '''解析主函数'''
    def parser_main(self, res_analysis):
        args = res_analysis['args']
        entity_dict = self.build_entitydict(args)#调用上面的构造实体节点函数
        question_types = res_analysis['question_types']#需要question_classifier.py完成问题类型的识别
        cqls = []
        for question_type in question_types:
            cql_ = {}#注意与下面cql的区别,cql_集成多个信息,cql包含查询语句
            cql_['question_type'] = question_type
            cql = []
            if question_type == 'disease_symptom':
                cql = self.cql_transfer(question_type, entity_dict.get('disease'))#sql_transfer是下面定义的分开处理问题子函数

            elif question_type == 'symptom_disease':
                cql = self.cql_transfer(question_type, entity_dict.get('symptom'))

            elif question_type == 'disease_cause':
                cql = self.cql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_acompany':
                cql = self.cql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_not_food':
                cql = self.cql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_do_food':
                cql = self.cql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'food_not_disease':
                cql = self.cql_transfer(question_type, entity_dict.get('food'))

            elif question_type == 'food_do_disease':
                cql = self.cql_transfer(question_type, entity_dict.get('food'))

            elif question_type == 'disease_drug':
                sql = self.cql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'drug_disease':
                cql = self.cql_transfer(question_type, entity_dict.get('drug'))

            elif question_type == 'disease_check':
                cql = self.cql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'check_disease':
                cql = self.cql_transfer(question_type, entity_dict.get('check'))

            elif question_type == 'disease_prevent':
                cql = self.cql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_lasttime':
                cql = self.cql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_cureway':
                cql = self.cql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_cureprob':
                cql = self.cql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_easyget':
                cql = self.cql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_desc':
                cql = self.cql_transfer(question_type, entity_dict.get('disease'))

            if cql:
                cql_['cql'] = cql

                cqls.append(cql_)

        return cqls#返回cql查询语句，可以是多条，给图谱

    '''构建实体节点'''
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)
        return entity_dict


    '''针对不同的问题，分开进行处理'''
    def cql_transfer(self, question_type, entities):
        if not entities:
            return []

        # 查询语句
        cql = []
        # 查询疾病的原因，在debug的时候，运行到对应的elif（说明已经找到合适的关系）会自动停止该函数的执行
        if question_type == 'disease_cause':
            cql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cause".format(i) for i in entities]#调用match语句

        # 查询疾病的防御措施
        elif question_type == 'disease_prevent':
            cql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.prevent".format(i) for i in entities]

        # 查询疾病的持续时间
        elif question_type == 'disease_lasttime':
            cql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cure_lasttime".format(i) for i in entities]

        # 查询疾病的治愈概率
        elif question_type == 'disease_cureprob':
            cql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cured_prob".format(i) for i in entities]

        # 查询疾病的治疗方式
        elif question_type == 'disease_cureway':
            cql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cure_way".format(i) for i in entities]

        # 查询疾病的易发人群
        elif question_type == 'disease_easyget':
            cql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.easy_get".format(i) for i in entities]

        # 查询疾病的相关介绍
        elif question_type == 'disease_desc':
            cql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.desc".format(i) for i in entities]

        # 查询疾病有哪些症状
        elif question_type == 'disease_symptom':
            cql = ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 查询症状会导致哪些疾病
        elif question_type == 'symptom_disease':
            cql = ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 查询疾病的并发症
        elif question_type == 'disease_acompany':
            cql1 = ["MATCH (m:Disease)-[r:acompany_with]->(n:Disease) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            cql2 = ["MATCH (m:Disease)-[r:acompany_with]->(n:Disease) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            cql = cql1 + cql2
        # 查询疾病的忌口
        elif question_type == 'disease_not_food':
            cql = ["MATCH (m:Disease)-[r:no_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 查询疾病建议吃的东西
        elif question_type == 'disease_do_food':
            cql = ["MATCH (m:Disease)-[r:do_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 已知忌口查疾病
        elif question_type == 'food_not_disease':
            cql = ["MATCH (m:Disease)-[r:no_eat]->(n:Food) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 已知推荐查疾病
        elif question_type == 'food_do_disease':
            cql = ["MATCH (m:Disease)-[r:do_eat]->(n:Food) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 查询疾病常用药品－药品别名记得扩充
        elif question_type == 'disease_drug':
            cql = ["MATCH (m:Disease)-[r:common_drug]->(n:Drug) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 已知药品查询能够治疗的疾病
        elif question_type == 'drug_disease':
            cql = ["MATCH (m:Disease)-[r:common_drug]->(n:Drug) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 查询疾病应该进行的检查
        elif question_type == 'disease_check':
            cql = ["MATCH (m:Disease)-[r:need_check]->(n:Check) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 已知检查查询疾病
        elif question_type == 'check_disease':
            cql = ["MATCH (m:Disease)-[r:need_check]->(n:Check) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        return cql

