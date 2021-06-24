from binlog2sql import Binlog2sql
from pymysqlreplication.row_event import (
    WriteRowsEvent,
    UpdateRowsEvent,
    DeleteRowsEvent,
)

def get_binlog_parser(host='localhost',port=3306,user='root',password='root',database=[],table=[]):
	'''
		TODO:
			1. 查找最新的一个 binlog 文件
			2. 根据 binlog 文件名，以及其他参数，创建 binlog 解析器对象
		Args:
			1. 服务器名称、服务器端口、用户名、密码、数据库名、数据表
		Return:
			1. parser
	'''
	args = {'host':host, 'user':user, 'password':password, 'port':port, 
	'start_file':'mysql-bin.000001', 'start_pos':4, 'end_file':'', 'end_pos':0, 
	'start_time':'', 'stop_time':'', 'stop_never':False, 'help':False, 
	'databases':database, 'tables':table, 'only_dml':False, 
	'sql_type':['INSERT', 'UPDATE', 'DELETE'], 
	'no_pk':False, 'flashback':False, 'back_interval':1.0}

	conn_setting = {'host': args['host'], 'port': args['port'], 'user': args['user'], 'passwd': args['password'], 'charset': 'utf8'}

	binlog2sql = Binlog2sql(connection_settings=conn_setting, start_file=args['start_file'], start_pos=args['start_pos'],
	                    end_file=args['end_file'], end_pos=args['end_pos'], start_time=args['start_time'],
	                    stop_time=args['stop_time'], only_schemas=args['databases'], only_tables=args['tables'],
	                    no_pk=args['no_pk'], flashback=args['flashback'], stop_never=args['stop_never'],
	                    back_interval=args['back_interval'], only_dml=args['only_dml'], sql_type=args['sql_type'])
	return binlog2sql;

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
	return 1

def parse_binlog(parser, start_pos, end_pos):
	'''
		TODO:
			1. 使用 parser 获取数据库更新的内容
			注：binlog 解析器只能解析出命令，并不能解析出整个表项，所以需要对那个项目进行改造。
			改造方法是，在 binlog2sql_util.py 文件117行的 if 条件下，读取 row 的内容
			对于 insert 操作，读取 row.values
			对于 update 操作，读取 row.before_values 和 row.after_values
			对于 delete 操作，读取 row.values
			
		Args:
			1. 解析器，起始解析位置，终止解析位置
		Return:
			一个数组，数组的成员是 modify_unit
			modify_unit定义为 {'modify_type': INSERT/DELETE/UPDATE, 'content': [...#该表项的所有内容]}
	'''
	modify_units = []
	events = parser.process_binlog()
	for binlog_event,row in events:
		if isinstance(binlog_event, WriteRowsEvent):
			modify_units.append({'modify_type':'INSERT','after_values':row['values']})
		if isinstance(binlog_event, DeleteRowsEvent):
			modify_units.append({'modify_type':'DELETE','before_values':row['values']})
		if isinstance(binlog_event, UpdateRowsEvent):
			modify_units.append({'modify_type':'UPDATE','before_values':row['before_values'],'after_values':row['after_values']})

	return modify_units


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
	update_items = []
	update_content = {}

	if modify_unit['modify_type']=='DELETE' or modify_unit['modify_type']=='UPDATE':
		search_query = 'select ' + target_db.primary_key + ' from ' + target_db.table
		first_item = True
		for source_key,target_key in rule['search_keys'].items():
			if first_item==True:
				search_query += ' where '
				first_item = False
			else:
				search_query += ' and '
			search_query += target_key + ' = ' + modify_unit['before_values'][source_key]
		update_items = target_db.select(search_query)

	if modify_unit['modify_type']=='INSERT' or modify_unit['modify_type']=='UPDATE':
		for source_key,target_key in rule['update_keys'].items():
			update_content[target_key] = modify_unit['after_values'][source_key]
 
	if modify_unit['modify_type']!='UPDATE' and rule['update_only']==True:
		return 0
	else:
		return {'type':modify_unit['modify_type'],'update_items':update_items,'update_content':update_content}

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

	updateItem = []
	updateContent = []

	if update_unit['type'] == 'UPDATE':
		updateItems = update_unit['update_items']
		updateContent = update_unit['update_content']
		for i in updateItems:
			for j in updateContent:
				cond = updateContent[j]
				target_db.pgsUpdate(j,(cond,i))

	elif update_unit['type'] == 'INSERT':
		updateItem = update_unit['update_items']
		paramsTemp = []
		for i in updateItem:
			paramsTemp.append(updateItem[i])
		params = tuple(paramsTemp)
		target_db.pgsInsert(params)

	elif update_unit['type'] == 'DELETE':
		updateContent = update_unit['update_content']
		for i in updateContent:
			target_db.pgsDelete(i)


def Exit(source_db):
	'''
		TODO:
			通过 flush log 命令刷新 binlog，使得下一次访问时 binlog 是一个全新的日志文件。
		Args:
			none
		Return:
			none
	'''
	pass


class mysql_operator:
	'''
		TODO:
			实现两个函数
			1. 构造函数：创建数据库连接
			2. flush binlog
	'''
	pass

import time
from postgresql_operator import postgresql_operator

def main():
	# 初始化解析器、操作器
	parser = get_binlog_parser('localhost',3306,'root','root',['db01'],['course','teacher'])
	target_db = postgresql_operator(password='Aa15816601051')
	source_db = mysql_operator()
	# 初始化同步规则(在1.0 版本只考虑一个规则，后续视情况拓展)
	# e.g. {'search_keys':[{'course':'myCourse'}],update_keys:[{'time':'course_time'}]} 每一个键值对的键代表源端的key，值代表目标端的key
	sync_rule = [{
				'sourse_table':'course',
				'target_table':'senior_course',
				'update_only':False,
				'search_keys':{'id':'course_id'},
				'update_keys':{'name':'course_name','start_time':'course_start_time','end_time':'course_end_time','teacher_id':'teacher_id'}
				},{				
				'sourse_table':'teacher',
				'target_table':'senior_course',
				'update_only':True,
				'search_keys':{'id':'teacher_id'},
				'update_keys':{'name':'teacher_name','introduction':'teacher_introduction','photo':'teacher_photo'}				
				}]

	
	# 初始化读取位置
	start_pos = 0
	end_pos = 0
	# 初始化同步间隔(ms)
	sync_interval = 600

	# 定时版本：定时同步
	print("\n")
	print("WELCOME TO THE DATABASE SYNCHRONIZATION TOOL!")
	print("You can enter 'help' to get the usage of all the commands.\n")
	while(True):
		com = input("DB Sync tool@SCUT:")
		if com == "help":
			print("Commands:")
			print("help   ---   show help menu ")
			print("run    ---   run the synchronization ") 
			print("exit   ---   exit the tool ")

		elif com == "run":
			check_value = check_binlog_update(parser, end_pos)
			if(check_value > 0):
				# 解析更新内容
				start_pos = end_pos
				end_pos = check_value
				modify_units = parse_binlog(parser, start_pos, end_pos)
				# print('modify_units',modify_units)
				# 过滤,同步
				for unit in modify_units:
					for rule in sync_rule:
						update_unit = filter_sync_content(rule,unit,target_db)
						if update_unit!=0:
							print('update_unit',update_unit)
							sync_to_target_db(update_unit,target_db)

			# 等待下一次查询
			# time.sleep(sync_interval)
		else:
			break;
		Exit(source_db)


if __name__ == '__main__':
	main()
