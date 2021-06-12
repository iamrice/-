

#ifndef DB_DATA_STRUCTURE_H
#define DB_DATA_STRUCTURE_H
#include <string.h>

struct db_change
{

	/*
		1. 设计数据结构，能够清晰地表示数据库的变动，且便于使用
		2. 为这个数据结构写一个 to_string 函数，清晰地展示内容
	*/
	std::string to_string();
};


struct db_relationship
{
	/*
		存储数据库之间关系的数据结构，包含三部分：
			1. 两个表的表头
			2. 用来查询的关键字段
			3. 更新字段
	*/
};

struct db_to_write
{
	/*
		db_change 过滤后的内容，只包括更新字段
	*/
};

struct primary_key
{
	/*
		主键，用于标识目标端数据库需要修改的表项，考虑到主键的数据结构多种多样，且有可能是双主键啥的，所以用一个数据结构来定义
	*/
};

#endif