#ifndef BINLOG_PARSER_H
#define BINLOG_PARSER_H

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
#endif