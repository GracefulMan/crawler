import pymysql
from IpProxyPool.config import DATABASE

# this file creates mysql connection class.
class MySqlQuery:
    def __init__(self):
        self.__db = pymysql.connect(
                host=DATABASE['host'],
                port=DATABASE['port'],
                user=DATABASE['username'],
                password=DATABASE['password'],
                database=DATABASE['database']
            )
        self.data =''
        self.__sql=self.__db.cursor()
    def sql(self,query,value=0):
        try:
            if value!=0:
                self.__sql.execute(query,value)
            else:
                self.__sql.execute(query)
            self.__db.commit()
            return True
        except :
            print('ERROR in MysqlLib FOR SQL: %s,%s'%(query,value))
            self.__db.rollback()
            return False
    def query(self,sql,value=0):
        try:
            if value!=0:
                self.__sql.execute(sql,value)
            else:
                self.__sql.execute(sql)
            self.__db.commit()
            return self.__sql.fetchall()
        except :
            print('ERROR in MYSQLlib FOR SQL: %s\n'%sql)
            return ()
    def __del__(self):
        self.__sql.close()
        self.__db.close()





