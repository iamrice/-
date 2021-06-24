import psycopg2

class postgresql_operator:

    def __init__(self,database="postgres", user="postgres", password="123", host="127.0.0.1", port="5432"):
        self.conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
        #test 用于测试连接成功 以下可删除
        cursor = self.conn.cursor()
        sql = "SELECT VERSION()"
        cursor.execute(sql)
        data = cursor.fetchone()
        print("database version : %s " % data)
    
    def pgsInsert(self,params):
        """
        向表中插入一行数据
        """
        cursor = self.conn.cursor()
        sql ="""INSERT INTO senior_course (course_id, teacher_id,course_name,course_start_time,course_end_time,teacher_name,teacher_photo,teacher_introduction) VALUES (%s, %s, %s, %s, %s, %s,%s, %s)"""
        try:
            cursor.execute(sql,params)
            self.conn.commit()
            print("Inserted successfully")
        except psycopg2.Error as e:
            print(e)

    def pgsSelect(self):
        """
        读取目标表中所有数据
        """
        cursor = self.conn.cursor()
        sql = """SELECT * from senior_course """
        try:
            cursor.execute(sql)
            data = cursor.fetchall()
            return data
        except psycopg2.Error as e:
            print(e)
        

    def pgsSelectCond(self,params):#参数末尾需加上",",例如id=2的话，params=(2,)
        """
        按primary key 查询
        """
        cursor = self.conn.cursor()
        sql = """SELECT * from senior_course where course_id = %s"""#senior_course course_id
        try:
            cursor.execute(sql,params)
            data = cursor.fetchall()
            return data
        except psycopg2.Error as e:
            print(e)

    def pgsUpdate(self,cond,params):
        cursor = self.conn.cursor()
        #str = "address"
        sql = """update senior_course set """ + cond + """= %s where course_id = %s  """
        try:
            cursor.execute(sql,params)
            print("Updated successfully")
            self.conn.commit()
        except psycopg2.Error as e:
            print(e)

    def pgsDelete(self,params):
        """
        按primary key删除相关所有行数据
        """
        cursor = self.conn.cursor()
        #str = "address"
        sql = """delete from senior_course where course_id = """ + params
        try:
            cursor.execute(sql)
            print("Deleted successfully")
            self.conn.commit()
        except psycopg2.Error as e:
            print(e)
        
    def getRowCount(self):
        """
        获取表中元素行数
        """
        cursor = self.conn.cursor()
        sql ="""select * from senior_course"""
        cursor.execute(sql)
        count = cursor.rowcount
        #print(count)
        return count

    def __del__(self):
        """
        关闭数据库访问
        """
        self.conn.close()

