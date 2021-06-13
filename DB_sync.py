
def get_binlog_parser(host='localhost',port='3306',user='root',password='root',database,table):
	'''
		TODO:
			1. 查找最新的一个 binlog 文件
			2. 根据 binlog 文件名，以及其他参数，创建 binlog 解析器对象
		Args:
			1. 服务器名称、服务器端口、用户名、密码、数据库名、数据表
		Return:
			1. parser
	'''
	pass

def check_binlog_update(parser, end_pos):
	'''
		TODO:
			1. 检查 binlog 文件大小是否大于 end_pos
		Args:
			1. parser: binlog 解析器
			2. end_pos
		Return:
			1. 如果文件相比上一次有所变动，则返回当前文件大小
			2. 如果没有变动，则返回 0
	'''
	pass

def parse_binlog(parser, start_pos, end_pos):
	'''
		TODO:
			1. 使用 parser 获取数据库更新的内容
		Args:
			1. 解析器，起始解析位置，终止解析位置
		Return:
			一个数组，数组的成员是 modify_unit
			modify_unit定义为 {'modify_type': INSERT/DELETE/UPDATE, 'content': [...#该表项的所有内容]}
	'''
	pass

def filter_sync_content(rule, modify_unit, target_db):
	'''
		TODO:
			1. 根据源端修改的表项，以及 rule 中的 search_title, 找到目标端中需要修改的表项的主键
			2. 根据源端修改的表项，以及 rule 中的 update_title, 过滤出需要修改的内容
		Args:
			1. rule
			2. modify_unit 
			3. target_db
		Return:
			1. 一个字典：{type:'', update_items:[],update_content:{}}，字典中的两个成员分别对应 TODO 中的两部分
			e.g.{type:'update',update_items:['001','008'],update_content:{'course':'math','time':'monday'}} 注：course和time应当是目标端的属性名，不是源端的。
			e.g.{type:'insert',update_items:[],update_content:{'course':'math','time':'monday'}}
			e.g.{type:'delete',update_items:['001','008'],update_content:{}}
	'''
	pass

def sync_to_target_db(update_unit, target_db):
	'''
		TODO:
			1. 将内容更新至目标端
		Args:
			1. update_unit
			2. target_db
		Return:
			none
	'''
	pass

def exit():
	'''
		TODO:
			通过 flush log 命令刷新 binlog，使得下一次访问时 binlog 是一个全新的日志文件。
		Args:
			none
		Return:
			none
	'''
	pass

class postgresql_operator:
	'''
		TODO:
			实现五个函数
			1. 构造函数：创建数据库连接
			2. insert
			3. select
			4. delete
			5. update
	'''
	pass

class mysql_operator:
	'''
		TODO:
			实现五个函数
			1. 构造函数：创建数据库连接
			2. insert
			3. select
			4. delete
			5. update
	'''
	pass

def main():
	# 初始化解析器、操作器
	parser = get_binlog_parser()
	target_db = postgresql_operator()
	source_db = mysql_operator()
	# 初始化同步规则(在1.0 版本只考虑一个规则，后续视情况拓展)
	sync_rule = {'search_keys'=[],'update_keys'=[]} # e.g. {'search_keys':[{'course':'myCourse'}],update_keys:[{'time':'course_time'}]} 每一个键值对的键代表源端的key，值代表目标端的key
	# 初始化读取位置
	start_pos = 0
	end_pos = 0
	# 初始化同步间隔(ms)
	sync_interval = 60000

	# 开始
	while(True){
		# 检查更新
		check_value = check_binlog_update(parser, end_pos)
		if(check_value == 0):
			break
		# 解析更新内容
		start_pos = end_pos;
		end_pos = check_value;
		modify_units = parse_binlog(parser, start_pos, end_pos)
		# 过滤,同步
		for unit in modify_units:
			update_unit = filter_sync_content(sync_rule,unit,target_db)
			sync_to_target_db(update_unit,target_db)
		# 等待下一次查询
		sleep(sync_interval)
	}
	

if __name__ == '__main__':
	main()