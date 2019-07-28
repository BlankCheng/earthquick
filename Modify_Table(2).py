# -*- coding: utf8 -*-
import ibm_db
import json


conn = ibm_db.connect( "DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;PORT=50001;PROTOCOL=TCPIP;UID=tpj29337;PWD=8kzn@v6p7wlb4r75;Security=SSL;", "", "")

# trial = "INSERT INTO Vehicle VALUES(2,2,1,2,2,2,2,1.1,2.1,2,0)"
# ibm_db.exec_immediate(conn, trial)

# delegate work to a specific driver
def delegateWork(conn, driverId, food=0, water=0, clothes=0, medicine=0 ):
    try:
        sql_modify_Vehicle = "UPDATE Vehicle " \
                             "SET ifVacant=%s, food=%s, water=%s, clothes=%s, medicine=%s" \
                             " WHERE Driver=%s" %(0, food, water, clothes, medicine, driverId)
        ibm_db.exec_immediate(conn, sql_modify_Vehicle)
        return True
    except:
        return False


# find the nearest vacant driver
def findNearestDriver(conn, Longtitude, Latitude):              #Return DriverId, -1: means None
    try:
        sql_find = "SELECT Driver from Vehicle WHERE ifVacant=%s ORDER BY " \
                       "(POWER(Longtitude - %f,2) + POWER(Latitude - %f,2)) ASC LIMIT 1" \
                       %(1, Longtitude, Latitude)
        res = ibm_db.exec_immediate(conn, sql_find)
        return ibm_db.fetch_both(res)["DRIVER"]
    except:
        return -1


# find the injury people among
def injuryAmong(conn, Longtitude, Latitude, Range = 0.5):    # key:[value1, value2, ...]
    try:
        sql_find = "SELECT * from Injury WHERE " \
                       "(POWER(longtitude - %f,2) + POWER(Latitude - %f,2)) <= POWER(%f, 2) LIMIT 100" \
                       %(Longtitude, Latitude, Range)
        res = ibm_db.exec_immediate(conn, sql_find)
        dict = {}
        result = ibm_db.fetch_both(res)

        for key in result.keys():
            if type(key) != int:
                dict[key] = [result[key]]
        while result != False:
            for key in result.keys():
                if type(key) != int:
                    dict[key].append(result[key])
            result = ibm_db.fetch_both(res)
        return dict
    except:
        return -1


# report damage of the road or the building
def reportDamage(conn, Longtitude, Latitude, ifBuilding = False):
    try:
        sql_modify_Damage = "INSERT INTO Damage VALUES(%s, %s, %s)"% (Longtitude, Latitude, ifBuilding)
        ibm_db.exec_immediate(conn, sql_modify_Damage)
        return True
    except:
        return False


# report one's injury and needings
def reportInjury(conn, Longtitude, Latitude, Water=0, Food=0, Clothes=0, Description=''):    # key:[value1, value2, ...]
    try:
        sql_modify_Damage = "INSERT INTO Injury VALUES(%s, %s, %s, %s, %s, '"\
                            % (Longtitude, Latitude, Water, Food, Clothes) +  Description  + "')"
        ibm_db.exec_immediate(conn, sql_modify_Damage)
        return True
    except:
        return False


# make a driver vacant
def makeVacant(conn, driverId):
    try:
        sql_modify_Vehicle = "UPDATE Vehicle " \
                             "SET ifVacant=%s " \
                             "WHERE Driver=%s" % (1, driverId)
        ibm_db.exec_immediate(conn, sql_modify_Vehicle)
        return True
    except:
        return False




# s = "SELECT * FROM Vehicle"
# print(ibm_db.fetch_both(ibm_db.exec_immediate(conn, s)))




ibm_db.close(conn)
