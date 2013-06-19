Gaea
====

Online Judge System powered by Tornado

###06.19 icefish
------
1>套用原前台模板

2>简单实现admin添加题目功能
	2.1 题目id自动增长(id 字段为 '_id')
	2.2 为了实现2.1功能添加 ids collection

###06.18 icefish
------
1>连接数据库到mongoDB
	1.1 数据库为本地数据库 Gaea
	
2>采用pymongo

3>因为mongoDB是Nosql，所以为了统一以后的说法，这里解释一下名词 :)
	MongoDB 的文档(document),相当于关系数据库中的一行记录
	多个文档组成一个集合(collection),相当于关系数据库的表
	多个集合(collection),逻辑上组织在一起,就是数据库(database)
