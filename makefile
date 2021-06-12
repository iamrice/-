db_sync.exe : main.cpp DB_sync.h DB_operator.h DB_data_structure.h binlog_parser.h
	g++ -std=c++11 main.cpp DB_sync.h DB_operator.h DB_data_structure.h binlog_parser.h -o db_sync.exe

clean:
	rm db_sync.exe

debug:
	g++ -std=c++11 main.cpp DB_sync.h DB_operator.h DB_data_structure.h binlog_parser.h -o db_sync.exe
	db_sync.exe

run:
	db_sync.exe