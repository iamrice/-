
/*
	Dependency:
		1. DB_oprator.h
		2. DB_change.h
	Todo:
		1. 定义一个数据结构，用来表示异构数据库的对应关系
			1. 两个表的表头
			2. 用来查询的关键字段
			3. 更新字段
		2. 初始化函数
			1. 实例化第1点中的数据结构，两个数据库可能有多个对应关系，因此使用 vector 存比较好。
			2. (optional) 确认表结构，表间关系确认后，需检查
				1. 目标端是否有关键字段和更新字段，如果没有，使用 alter table 命令增加字段
				2. 目标段和源端所对应的字段类型是否一致（数据类型、最大长度）。 如果不一致，修改目标端字段类型
			3. (optional) 执行第一次同步，将源端已有的内容迁移过来
		2. 根据数据库变动和两个数据库的对应关系，解析出目标端数据库需要修改的内容，用 DB_change 结构表示
			1. 当源端数据库有变动时，根据“用来查询的关键字” 去匹配目标端的内容
			2. 根据源端的操作类型，分别做 insert，delete，update操作
		3. 调用 DB operator，将第三步的解析结果传入
*/

#ifndef DB_SYNC_H
#define DB_SYNC_H
#include "DB_oprator.h"
#include "DB_data_structure.h"
#include <vector>

class DB_sync
{
public:
	DB_sync();

	~DB_sync();

	bool addRule();
	/*
		TODO:
			增加两个数据库之间的关系，加入 relations 变量中。
		Args:
			参数很多，就是实例化一个 db_relationship 的所有内容，因为这部分是由用户输入，所以输入参数是零散的，所以这个函数中需要用 db_relationship 来规范化。
		Return:
			操作是否成功
	*/

	bool sync();

private:
	std::vector<db_relationship*> relations; // 存储数据库对应关系
	DB_oprator* target_db; // 目标数据库
	
	std::vector<primary_key*> search_items(db_change*);
	/*
		TODO:
			根据 db_change，以及 db_relationship 中用于查询的关键字段，来查询那些表项需要同步，因为考虑到目标端和源端不一定是一一对应的关系，所以用一个vector 来存储。
		Args:
			db_change: 源端的一个变化
		Return:
			primary_keys: 目标端匹配到的表项的主键的值
	*/

	db_to_write* parse_change(db_change*);
	/*
		TODO:
			根据 db_change，以及 db_relationship 中的更新字段，只过滤出需要修改的内容，减少数据传输，也让 db_operator 更好操作
		Args:
			db_change: 源端的一个变化
		Return:
			db_to_write： 需要修改的内容
	*/

	bool sync_item(db_to_write,primary_key*,int);
	/*
		TODO:
			调用 db_operator, 同步内容。注：search_item 中可能返回多个 primary_key，但此函数只处理一个，因此如果有多个匹配表项需要多次调用此函数
		Args:
			db_to_write： 需要修改的内容
			primary_keys: 目标端匹配到的表项的主键的值
			int：同步的类型，1 代表 insert，2 代表 delete，3 代表 update
		Return:
			bool：是否成功
	*/

};

#endif