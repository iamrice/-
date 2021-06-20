import psycopg2

class postgresql_operator:

    def __init__(self):
        self.conn = psycopg2.connect(database="postgres", user="postgres", password="123", host="127.0.0.1", port="5432")
        #test
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
    	sql = "INSERT INTO student (id, address) VALUES (%s, %s)"#senior_course、参数、 (%d,%d,%s,%%Y-%%m-%%d,%%Y-%%m-%%d,%%Y-%%m-%%d,%s,%s,%s)
    	try:
            cursor.execute(sql,params)
        except psycopg2.Error as e:
            print(e)

    def pgsSelect(self):
    	"""
    	读取目标表中所有数据
    	"""
    	cursor = self.conn.cursor()
    	sql = """SELECT * from student """
    	try:
            cursor.execute(sql)
            data = cursor.fetchall()
            print(data)
            #return data
        except psycopg2.Error as e:
            print(e)
        

    def pgsSelectCond(self,params):#参数末尾需加上",",例如id=2的话，params=(2,)
        """
        按primary key 查询
        """
        cursor = self.conn.cursor()
        sql = """SELECT * from student where id = %s"""#senior_course course_id
        try:
            cursor.execute(sql,params)
            data = cursor.fetchall()
            print(data)
            #return data
        except psycopg2.Error as e:
            print(e)

    def pgsUpdate(self,cond):
        cursor = self.conn.cursor()
        #str = "address"
        sql = """update student set """ + cond + """= %s where id = %s  """
        try:
            cursor.execute(sql)
            print("Updated successfully")
        except psycopg2.Error as e:
            print(e)

    def pgsDelete(self,params):#params需写成（2，）加一个逗号这种形式
        """
        按primary key删除相关所有行数据
        """
        cursor = self.conn.cursor()
        #str = "address"
        sql = """delete from student where id = %s"""
        try:
            cursor.execute(sql,params)
            print("Deleted successfully")
        except psycopg2.Error as e:
            print(e)
        
    def getRowCount(self):
        """
        获取表中元素行数
        """
        cursor = self.conn.cursor()
        sql ="""select * from student"""
        cursor.execute(sql)
        count = cursor.rowcount
        print(count)
        #return count

    def __del__(self):
        """
        关闭数据库访问
        """
        self.conn.commit()
        self.conn.close()






#test
po = postgresql_operator()
#po.postgresCreate()
#po.pgInsert((2,'b'))

po.pgsSelect()
po.pgsInsert((3,'c'))
po.pgsSelect()
	