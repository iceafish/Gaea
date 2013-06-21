Gaea
====

Online Judge System powered by Tornado

###06.20 icefish
------
1>对原有部分代码风格调整
2>实现基本user
	2.1 user密码采用base64库基础加密
	2.2 user尚未完善
3>实现前台user响应
4>实现提交题目form

###06.19 icefish
------
1>套用原前台模板
	1.1 实现主页显示(因为还没有设计user，所以暂不支持登陆)
	1.2 实现题目列表显示
	1.3 实现题目显示
	
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
