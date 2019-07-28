# -*- coding: utf8 -*-
import ibm_db
import json


# trial = "INSERT INTO Vehicle VALUES(2,2,1,2,2,2,2,1.1,2.1,2,0)"
# ibm_db.exec_immediate(conn, trial)

# delegate work to a specific driver
def delegateDriverWork(driverId, food=0, water=0, clothes=0, medicine=0):
    conn = ibm_db.connect(
        "DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;PORT=50001;PROTOCOL=TCPIP;UID=tpj29337;PWD=8kzn@v6p7wlb4r75;Security=SSL;",
        "", "")
    try:
        sql_modify_Vehicle = "UPDATE Vehicle " \
                             "SET ifVacant=%s, food=%s, water=%s, clothes=%s, medicine=%s" \
                             " WHERE Driver=%s" %(0, food, water, clothes, medicine, driverId)
        ibm_db.exec_immediate(conn, sql_modify_Vehicle)
        ibm_db.close(conn)
        return True
    except:
        ibm_db.close(conn)
        return False



# find the nearest vacant driver
def findNearestDriver(Longtitude, Latitude):              #Return DriverId, -1: means None
    conn = ibm_db.connect(
        "DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;PORT=50001;PROTOCOL=TCPIP;UID=tpj29337;PWD=8kzn@v6p7wlb4r75;Security=SSL;",
        "", "")
    try:
        sql_find = "SELECT Driver from Vehicle WHERE ifVacant=%s AND vehicleKind=%s ORDER BY " \
                       "(POWER(Longtitude - %f,2) + POWER(Latitude - %f,2)) ASC LIMIT 1" \
                       %(1, 0, Longtitude, Latitude)
        res = ibm_db.exec_immediate(conn, sql_find)
        ibm_db.close(conn)
        return ibm_db.fetch_both(res)["DRIVER"]
    except:
        ibm_db.close(conn)
        return -1


def findNearestDrone(Longtitude, Latitude):              # Drone
    conn = ibm_db.connect(
        "DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;PORT=50001;PROTOCOL=TCPIP;UID=tpj29337;PWD=8kzn@v6p7wlb4r75;Security=SSL;",
        "", "")
    try:
        sql_find = "SELECT Driver from Vehicle WHERE ifVacant=%s AND vehicleKind=%s ORDER BY " \
                       "(POWER(Longtitude - %f,2) + POWER(Latitude - %f,2)) ASC LIMIT 1" \
                       %(1, 1, Longtitude, Latitude)
        res = ibm_db.exec_immediate(conn, sql_find)
        ibm_db.close(conn)
        return ibm_db.fetch_both(res)["DRIVER"]
    except:
        ibm_db.close(conn)
        return -1



# find the injury people among
def injuryAmong(Longtitude, Latitude, Range=0.05):    # key:[value1, value2, ...]
    conn = ibm_db.connect(
        "DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;PORT=50001;PROTOCOL=TCPIP;UID=tpj29337;PWD=8kzn@v6p7wlb4r75;Security=SSL;",
        "", "")
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
        ibm_db.close(conn)
        return dict
    except:
        ibm_db.close(conn)
        return -1


# report damage of the road or the building
def reportDamage(Longtitude, Latitude, ifBuilding=False):
    print (Longtitude, Latitude)
    conn = ibm_db.connect(
        "DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;PORT=50001;PROTOCOL=TCPIP;UID=tpj29337;PWD=8kzn@v6p7wlb4r75;Security=SSL;",
        "", "")
    try:
        sql_modify_Damage = "INSERT INTO Damage VALUES(%s, %s, %s)"% (Longtitude, Latitude, ifBuilding)
        ibm_db.exec_immediate(conn, sql_modify_Damage)
        ibm_db.close(conn)
        return True
    except:
        ibm_db.close(conn)
        return False


# report one's injury and needings
def reportInjury(Longtitude, Latitude, Water=0, Food=0, Clothes=0, Description=''):    # key:[value1, value2, ...]
    conn = ibm_db.connect(
        "DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;PORT=50001;PROTOCOL=TCPIP;UID=tpj29337;PWD=8kzn@v6p7wlb4r75;Security=SSL;",
        "", "")
    try:
        sql_modify_Damage = "INSERT INTO Injury VALUES(%s, %s, %s, %s, %s, %s, '"\
                            % (Longtitude, Latitude, Water, Food, Clothes, 1) +  Description  + "')"
        ibm_db.exec_immediate(conn, sql_modify_Damage)
        ibm_db.close(conn)
        return True
    except:
        ibm_db.close(conn)
        return False


# make a driver vacant
def makeVacant(driverId):
    conn = ibm_db.connect(
        "DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;PORT=50001;PROTOCOL=TCPIP;UID=tpj29337;PWD=8kzn@v6p7wlb4r75;Security=SSL;",
        "", "")
    try:
        sql_modify_Vehicle = "UPDATE Vehicle " \
                             "SET ifVacant=%s " \
                             "WHERE Driver=%s" % (1, driverId)
        ibm_db.exec_immediate(conn, sql_modify_Vehicle)
        ibm_db.close(conn)
        return True
    except:
        ibm_db.close(conn)
        return False



def releaseDrone(droneId, food, water, clothes, medicine, rescueeId):
    conn = ibm_db.connect(
        "DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;PORT=50001;PROTOCOL=TCPIP;UID=tpj29337;PWD=8kzn@v6p7wlb4r75;Security=SSL;",
        "", "")
    try:
        sql_modify_Vehicle = "UPDATE Vehicle " \
                             "SET ifVacant=%s, food=%s, water=%s, clothes=%s, medicine=%s" \
                             " WHERE Driver=%s" %(0, food, water, clothes, medicine, droneId)
        ibm_db.exec_immediate(conn, sql_modify_Vehicle)

        sql_modify_Injury = "UPDATE Injury " \
                             "SET Valid=%s" \
                             " WHERE id=%s" % (0, rescueeId())
        ibm_db.exec_immediate(conn, sql_modify_Injury)
        ibm_db.close(conn)
        return True
    except:
        ibm_db.close(conn)
        return False



def updateResource(stationId, food, water, clothes, medicine):
    conn = ibm_db.connect(
        "DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;PORT=50001;PROTOCOL=TCPIP;UID=tpj29337;PWD=8kzn@v6p7wlb4r75;Security=SSL;",
        "", "")
    try:
        sql_modify_Station = "UPDATE Station " \
                             "SET food=%s, water=%s, clothes=%s, medicine=%s" \
                             " WHERE Driver=%s" %(food, water, clothes, medicine, stationId)
        ibm_db.exec_immediate(conn, sql_modify_Station)
        dict = {}
        if food == 0:
            dict['food'] = 0
        if water == 0:
            dict['water'] = 0
        if clothes == 0:
            dict['clothes'] = 0
        if medicine == 0:
            dict['medicine'] = 0
        ibm_db.close(conn)
        return dict
    except:
        ibm_db.close(conn)
        return False

if __name__ == "__main__":
    conn = ibm_db.connect(
        "DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net;PORT=50001;PROTOCOL=TCPIP;UID=tpj29337;PWD=8kzn@v6p7wlb4r75;Security=SSL;",
        "", "")

# s = "SELECT * FROM Vehicle"
# print(ibm_db.fetch_both(ibm_db.exec_immediate(conn, s)))




