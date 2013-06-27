Gaea
====

Online Judge System powered by Tornado

06.27 icefish
------
		1>实现测试数据上传<br />
			1.1 在新建题目时,自动在judger/DataFile 下建立对应id的数据文件夹<br />

		2>修改部分数据库模型<br />
		3>judger 实现判定 AC,WA,TLE,RE 结果<br />

### 06.26 icefish
------
1>实现判题judger模块
	judger 模块设计
	judger 模块完全独立于 tornado 部分，独立服务
	分为本地和网络两个部分
	其中网络部分是为了提供远程判题服务器和集群功能的支持
	本地 judger 服务器默认开启(也是必须)
	judger 识别本地服务，不进行额外的检查工作
	由 redis 提供的同步队列功能，judger 可以自动接受判题请求
	支持阻塞

2>judger 目前现有缺陷
	2.1 只实现本地模块
	2.2 由于暂时没有找到一种较好的内存检测方法，暂不支持内存判断
	2.3 不能保证判题机的安全(不能进行代码安全行检查)
	2.4

3>OJ现有问题
	3.1 admin 添加题目还不能添加数据

### 06.22 icefish
------
1>提交题目
	1.1 status数据库集合为 judge_queues
	1.2 提交代码文件名为集合'_id'，放在dissemination目录等待分发
	1.3 提交时记录题目信息、用户提交信息
	1.4 判题请求发送时将设计为异步模式
2>ranklist界面显示
	2.1 仅显示普通用户
3>部分代码和前台代码调整
4>部分数据库结构调整
	4.1 pull 后需要执行数据库语句 
		ids.remove()
		problems.remove()
		judge_queues.remove()

### 06.20 icefish
------
bug 修复

### 06.20 icefish
------
1>对原有部分代码风格调整
2>实现基本user
	2.1 user密码采用base64库基础加密
	2.2 user尚未完善
3>实现前台user响应
4>实现提交题目form

### 06.19 icefish
------
1>套用原前台模板
	1.1 实现主页显示(因为还没有设计user，所以暂不支持登陆)
	1.2 实现题目列表显示
	1.3 实现题目显示
	
2>简单实现admin添加题目功能
	2.1 题目id自动增长(id 字段为 '_id')
	2.2 为了实现2.1功能添加 ids collection

### 06.18 icefish
------
1>连接数据库到mongoDB
	1.1 数据库为本地数据库 Gaea
	
2>采用pymongo

3>因为mongoDB是Nosql，所以为了统一以后的说法，这里解释一下名词 :)
	MongoDB 的文档(document),相当于关系数据库中的一行记录
	多个文档组成一个集合(collection),相当于关系数据库的表
	多个集合(collection),逻辑上组织在一起,就是数据库(database)
