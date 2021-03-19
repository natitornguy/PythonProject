from library.mongoDB import connectDB
import hashlib
import pymongo
from bson.objectid import ObjectId

def checkLogin(id, password):
    db = connectDB()
    password = hashlib.md5(password.encode()).hexdigest()
    result = db.users.count_documents({'$and': [{'username': id}, {'password': password}]})
    if result == 1:
        return True
    return False


def changePassword(username, password):
    db = connectDB()
    password = hashlib.md5(password.encode()).hexdigest()
    where = {'username': username}
    setTo = {'$set': {'password': password, 'needChange': 0}}
    db.users.update_one(where, setTo)
    return True


def promoteToAdmin(username):
    db = connectDB()
    where = {'username': username}
    setTo = {'$set': {'isAdmin': 1}}
    db.users.update_one(where, setTo)
    return True


def checkAdmin(id):
    db = connectDB()
    result = db.users.find({'username': id})
    for i in result:
        if i['isAdmin'] == 1:
            return True
    return False


def setNeedChange(username):
    db = connectDB()
    password = hashlib.md5("P@ssw0rd".encode()).hexdigest()
    where = {'username': username}
    setTo = {'$set': {'password': password, 'needChange': 1}}
    db.users.update_one(where, setTo)
    return True


def checkIfNeedChange(username):
    db = connectDB()
    where = {'$and': [{'username': username}, {'needChange': 1}]}
    cursor = db.users.count_documents(where)
    if cursor == 1:
        return True
    return False


def insetUser(info):
    password = hashlib.md5(info['password'].encode()).hexdigest()
    db = connectDB()
    s = "ghktr"
    s.lower()
    finddub = db.users.count_documents({'username': info['username'].lower()})
    if finddub > 0:
        return False
    else:
        db.users.insert_one(
            {'username': info['username'], 'password': password, 'name': info['name'], 'lastname': info['lastname'],
             'email': info['email'], 'phone': info['phone'], 'isAdmin': info['isAdmin'], 'needChange': 0})
        return True


def getUserCount():
    db = connectDB()
    where = {'isAdmin': 0}
    total = db.users.count_documents(where)
    return total


def getAllGeneralUser():
    data = []
    db = connectDB()
    where = {'isAdmin': 0}
    cursor = db.users.find(where)
    for i in cursor:
        user = {'username': i['username'], 'name': i['name'], 'lastname': i['lastname'], 'email': i['email'],
                'phone': i['phone']}
        data.append(user)
    return data


def deleteUser(username):
    db = connectDB()
    where = {'username': username}
    cursor = db.users.delete_one(where)
    return True


def updateUser(data):
    db = connectDB()
    where = {'username': data[0]}
    setTo = {'$set': {'name': data[1], 'lastname': data[2], 'phone': data[3], 'email': data[4]}}
    db.users.update_one(where, setTo)
    return True


def createTask(data):
    db = connectDB()
    try:
        db.alltasks.insert_one(
            {'topic': data['topic'], 'detail': data['detail'], 'status': data['status'], 'owner': data['owner'],
             'createdate': data['createdate'], 'deadline': data['deadline']}
        )
        return True
    except:
        return False

def updateTask(_id,data):
    id = ObjectId(_id)
    try:
        db = connectDB()
        where = {'_id': id}
        setTo = {'$set': {'topic': data['topic'], 'detail': data['detail'], 'status': data['status'], 'owner': data['owner'],
             'createdate': data['createdate'], 'deadline': data['deadline']}}
        db.alltasks.update_one(where, setTo)
        return True
    except:
        return False

def getAllTasks():
    tasks = []
    db = connectDB()
    where = {}
    cursor = db.alltasks.find(where)
    for i in cursor:
        task = {'_id': i['_id'], 'topic': i['topic'], 'detail': i['detail'], 'status': i['status'], 'owner': i['owner'],
                'createdate': i['createdate'], 'deadline': i['deadline']}
        tasks.append(task)
    return tasks

def deleteTask(_id):
    id = ObjectId(_id)
    db = connectDB()
    where = {'_id' : id}
    try:
        db.alltasks.delete_one(where)
        return True
    except:
        return False