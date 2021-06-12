
/*
	Todo:
		1. 实现“实时同步”的监听功能，定时 binlog_parser 去检查源端数据库是否有变动
		2. 如果有变动，则将变动内容传给 DB_sync 进行同步
*/

#include "DB_data_structure.h"
#include "DB_operator.h"
#include "binlog_parser.h"

using namespace std;

int main(){
	
}