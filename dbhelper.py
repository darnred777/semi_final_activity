from mysql.connector import connect

db=connect(
    host='127.0.0.1',
    user='root',
    password='',
    database='sfdb'
)

def query(sql: str)->list:
    cursor: object = db.cursor(dictionary = True)
    cursor.execute(sql)
    rows: list = cursor.fetchall()
    return rows

def getallrecord(table: str)->list:
    sql: str = f"SELECT * FROM `(table)` "
    return query(sql)

def getrecord(table: str, **kwargs)->dict:
    keys: list = list(kwargs.keys())
    values: list = list(kwargs.values())
    sql: str = f"SELECT * FROM `{table}` WHERE `{keys[0]}` = '{values[0]}'"
    rows: list = query(sql)
    return rows

def deleterecord(table: str,**kwargs)->dict:
    keys: list = list(kwargs.keys())
    values: list = list(kwargs.values())
    sql: str = f"DELETE FROM `{table}` WHERE `{keys[0]}` = '{values[0]}'"
    okey: bool = None
    cursor: object = db.cursor()
    cursor.execute(sql)
    rc: int = cursor.rowcount
    db.commit()
    cursor.close()
    return rc

def addrecord(table: str, **kwargs)->int:
    keys: list = list(kwargs.keys())
    values: list = list(kwargs.values())
    # INSERT INTO `student`(`idno`,`lastname`,`......`) VALUES('5000','durano',......)
    flds: str = "`,`".join(keys)
    data: str = "','".join(values)
    sql: str = f"INSERT INTO `{table}`(`{flds}`) VALUES ('{data}')"
    #print(sql)
    cursor: object = db.cursor()
    cursor.execute(sql)
    rc: int = cursor.rowcount
    db.commit()
    cursor.close()
    return rc

def updaterecord(table: str, **kwargs)->int:
    keys: list = list(kwargs.keys())
    values: list = list(kwargs.values())
    # UPDATE `student` SET `lastname`='durano', `firstname`='dennis' WHERE `idno`='9000'
    flds: list = []
    for i in range(1, len(keys)):
        flds.append("`"+keys[i]+"`='"+values[i]+"'")
    fld: str = ",".join(flds)
    sql: str = f"UPDATE `{table}` SET {fld} WHERE `{keys[0]}`='{values[0]}'"
    cursor: object = db.cursor()
    cursor.execute(sql)
    rc: int = cursor.rowcount
    db.commit()
    cursor.close()
    return rc

def userlogin(table: str, **kwargs)->int:
    keys: list = list(kwargs.keys())
    values: list = list(kwargs.values())
    row: dict = {}
    sql: str = f"SELECT * FROM `{table}` WHERE `{keys[0]}`='{values[0]}' AND `{keys[1]}`='{values[1]}'"
    cursor: object = db.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    okey: bool = False
    if row !=None: 
        okey = True
    cursor.close()
    return okey



#testing the delete record module
#rows_affected: int = userlogin('users',username='hello',password='world')
#rows_affected: int = updaterecord('student',idno='454533',lastname='lokololo',firstname='wewewewe',course='BSIT',level='4')
#rows_affected: int = addrecord('student',idno='454533',lastname='ERT',firstname='ERT',course='ERT',level='ERT')
#rows_affected: int = addrecord('users',username='admin',password='user')
#ok: bool = deleterecord('student',idno='11111')
#print(rows_affected)
