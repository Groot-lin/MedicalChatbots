## 一.项目简介

本项目是一个基于Neo4j图数据库的医疗知识图谱智能问答机器人

在[刘焕勇老师](https://liuhuanyong.github.io)的项目做的重构与增强

问答分为两个模块

基于知识图谱的问答和基于关键词的问答

基于知识图谱主要分为以下模块

* build_medicalgraph.py: 构建neo4j数据库
* question_analysis.py : 问题语义分析
* get_cql.py : 根据问题获取对应cql语句
* get_answer.py : 查询数据库并结合生成答案



## 二.项目启动

1. 环境要求,neo4j数据库,python3,pycharm
2. 打开build_medicalgraph.py文件

修改信息包括neo4j数据库的ip地址,端口号,用户名和密码

运行最下面的main函数(数据量较大,可能会运行几十分钟)

3. 打开main.py文件

修改main函数中的端口号

4. 打开static下的index.html文件并打开右上角浏览器即可使用





如遇到问题请联系QQ:2201716544

备注github
