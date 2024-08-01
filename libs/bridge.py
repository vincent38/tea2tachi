from .data import Database
from .tachi import putScoresFile
from .tea import getDataFromTea

#
#   Management procedures
#

def setTables():
    # For reset purposes. Not to be launched on production context
    db_instance = Database()
    db_instance.setTables()
    db_instance.close()

#
#   Sync procedure
#

def executeBridge(user_id):
    db_instance = Database()
    user = db_instance.getUserData(user_id)
    if user is not None:
        data = getDataFromTea(user[1])
        reply = putScoresFile(data, user[2])
        if reply.json()['success'] is not True:
            status = 'Failed'
            print(reply.json())
        else:
            status = 'Received by Tachi'
        db_instance.insertLog(user_id, status)
    else:
        status = 'No API key found for this user. Please do /bind_account beforehand.'
    db_instance.close()
    return status

#
#   Account management procedures
#

def registerUser(user_id, tea_key, tachi_key):
    db_instance = Database()
    status = db_instance.registerBindings(user_id, tea_key, tachi_key)
    db_instance.close()
    return status

def editUser(user_id, tea_key, tachi_key):
    db_instance = Database()
    status = db_instance.editBindings(user_id, tea_key, tachi_key)
    db_instance.close()
    return status

def removeUser(user_id):
    db_instance = Database()
    status = db_instance.deleteBindings(user_id)
    db_instance.close()
    return status

#
#   Logging procedures
#

def logbook(user_id):
    db_instance = Database()
    logs = db_instance.getLogs(user_id)
    db_instance.close()
    return logs