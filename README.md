# DB Sync tool

#### 介绍
这是一个简易的数据库同步工具，通过解析 binlog 实习增量同步，支持 MySQL 和 PostGreSQL。

#### 开发目标
1. 以 MySQL 为源端，以 PostGreSQL 为目标端，做单向同步。
2. 主要应用与读写分离的主从数据库场景

#### 测试场景

| 源端: 平台课程信息 | 源端：教师      | 目标端：高三年级课程查询 |
| ------------------ | --------------- | ------------------------ |
| id(primary key)    | id(primary key) | course_id(primary key)   |
| grade              | name            | course_time              |
| time               | photo           | course_name              |
| name               | introduction    | teacher_photo            |
| teacher_id         | private_data    | teacher_name             |
|                    |                 | teacher_id               |
|                    |                 | teacher_intro            |



#### 感谢

[binlog2sql]: https://github.com/danfengcao/binlog2sql

