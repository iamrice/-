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
| grade              | name            | course_start_time        |
| name               | introduction    | course_end_time          |
| start_time         | photo           | course_name              |
| end_time           | private_data    | teacher_photo            |
| teacher_id         |                 | teacher_name             |
|                    |                 | teacher_id               |
|                    |                 | teacher_intro            |

#### Usage

##### 导入源数据库（mysql） demo

```
mysql -h 服务器地址 -u 用户名 -p 密码
create database 数据库名;
use 数据库名;
source xxx\demo_mysql.sql; # xxx 替换为项目路径
```

##### 导入目标数据库(postgresql) demo

```
psql -U 用户名 数据库名< xxx\demo_psql.sql # xxx 替换为项目路径
```



#### 感谢

1. <a herf="https://github.com/danfengcao/binlog2sql">binlog2sql</a>
2. kettle