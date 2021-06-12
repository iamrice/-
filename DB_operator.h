
/*
	Dependency:
		1. DB_change.h
		2. PostGreSQL 相关库
	Todo:
		1. 根据 DB_change 的数据结构，实现对 PostGreSQL 的操作，包括 INSERT, DELETE, UPDATE，SELECT
	Test:
		1. 用 DB_change 中提供的样例测试。
*/

#ifndef DB_OPERATOR_H
#define DB_OPERATOR_H
#include <string.h>
#include "DB_data_structure.h"

class DB_operator
{
public:
	DB_operator(std::string,int,std::string,std::string,std::string);
	/*
		TODO:
			1. 与数据库建立连接
		Args:
			1. 服务器名称：string
			2. 端口：int
			3. 数据库名称：string
			4. 用户名：string
			5. 密码：string
		Return: None
	*/

	~DB_operator();
	
	bool Insert(db_to_write,primarykey);
	bool Delete(db_to_write,primarykey);
	bool Update(db_to_write,primarykey);
	bool Select(db_to_write,primarykey);
};
#endif