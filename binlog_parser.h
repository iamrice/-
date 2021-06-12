
/*
	Dependency:
		1. DB_change.h
		2. dll 相关库
	Todo:
		1. 将 binlog2sql 打包为 dll 动态链接库，便于在 C++ 中调用（这一步不是代码实现）
		2. 调用 binlog2sql，需要了解关于动态链接库的调用方法
		3. 观察 binlog2sql 中数据的输出方式，将其转为 DB_change 中定义的数据结构
	Test:
		1. 做完前两步，测试 dll 的输出是否正常
		2. 做完第三步，在 MySQL 上测试 INSERT, DELETE, UPDATE 语句，并观察经过 parser 后输出是否一致
*/

#ifndef BINLOG_PARSER_H
#define BINLOG_PARSER_H
#include <vector>
#include "DB_data_structure.h"

class binlog_parser
{
public:
	binlog_parser();
	/*
		TODO:
			初始化源端数据库
		Args:
			源端的服务器、端口、用户名、密码、数据库
		Return:

	*/
	~binlog_parser();

	std::vector<db_change*> check_source_db();
	/*
		TODO:
			检查源端数据库是否有变动
		Args:

		Return:
			零个、一个或多个 db_change
	*/
};

#endif