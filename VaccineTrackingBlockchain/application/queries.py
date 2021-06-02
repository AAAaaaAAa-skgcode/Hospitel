from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
from time import sleep
from sys import exit
import json
import requests

bdb_root_url = 'localhost:9984'  
bdb = BigchainDB(bdb_root_url)


def get_both(id):
    tr = bdb.transactions.get(asset_id=id)
    if (len(tr) != 0):
        usersc = tr[0]['asset']['data']
        usersc.update(tr[0]['metadata']) 
        if (len(tr) == 1):    
            usersc = usersc.copy()
        else: 
            for x in tr:
                if (x.get('metadata', {}).get('vaccine_brand') != None):
                    usersc['vaccine_brand'] = x['metadata']['vaccine_brand']
                if (x.get('metadata', {}).get('status') != None):
                    usersc['status'] = x['metadata']['status']
                if (x.get('metadata', {}).get('completed_doses') != None):
                    usersc['completed_doses'] = x['metadata']['completed_doses']
                if (x.get('metadata', {}).get('symptoms') != None):
#                     concat = usersc['symptoms']
#                     if (x['metadata']['symptoms'] not in concat):
#                         concat = concat + ', ' + x['metadata']['symptoms']
                    usersc['symptoms'] = x['metadata']['symptoms']
                if (x.get('metadata', {}).get('first_date') != None):
                    usersc['first_dose_date'] = x['metadata']['first_date']
                if (x.get('metadata', {}).get('second_date') != None):
                    usersc['second_dose_date'] = x['metadata']['second_date']
                if (x.get('metadata', {}).get('hospital') != None):
                    usersc['hospital'] = x['metadata']['hospital']
                
            usersc = usersc.copy()
                
    
    return usersc


def get_asset_data(user):
    idlist = [] 
    userlist = [] 
    for x in user:
        id = x['id']
        if (id not in idlist):
            idlist.append(id)
            usersc = get_both(id)
            userlist.append(usersc)

    userlist = json.dumps(userlist, indent=4)
    return userlist


def get_metadata(user):
    url = 'http://localhost:9984/api/v1/transactions/'
    idlist = []  
    userlist = [] 
    for x in user:
            users = x['id']
            url1 = url + users
            req = requests.get(url1)
            data = req.json()
            try:
                id = data['asset']['id']
            except KeyError:
                id = data['id']
            if (id not in idlist):
                idlist.append(id)
                usersc = get_both(id)
                userlist.append(usersc)

    return userlist



#########################################################################################


def search_amka(amka):
    user = bdb.assets.get(search = amka)
    userlist = get_asset_data(user)
    return userlist


def search_status(status):
    stat = bdb.metadata.get(search = status)
    # print(stat)
    userlist = get_metadata(stat)
    list1 = []
    for x in userlist:
        if (x['status'] == status):
            c = {}
            c.update(x)
            c = c.copy()
            list1.append(c)
    list1 = json.dumps(list1, indent=4)
    return list1
   

def search_hospital(hospital_name):
    hospitals = bdb.metadata.get(search = hospital_name)
    userlist = get_metadata(hospitals)
    list1 = []
    for x in userlist:
        if (x['hospital'] == hospital_name):
            c = {}
            c.update(x)
            c = c.copy()
            list1.append(c)
    list1 = json.dumps(list1, indent=4)
    return list1



def search_country(country):
    cntr = bdb.assets.get(search = country)
    userlist = get_asset_data(cntr)
    return userlist


def search_city(city):
    ct = bdb.assets.get(search = city)
    userlist = get_asset_data(ct)
    return userlist



def search_gender(gender):
    gndr = bdb.assets.get(search = gender)
    userlist = get_asset_data(gndr)
    return userlist



def search_brand(vaccine_brand):
    br = bdb.metadata.get(search = vaccine_brand)
    userlist = get_metadata(br)
    list1 = []
    for x in userlist:
        if (x['vaccine_brand'] == vaccine_brand):
            c = {}
            c.update(x)
            c = c.copy()
            list1.append(c)
    list1 = json.dumps(list1, indent=4)
    return list1



def search_all():
    all = bdb.assets.get(search = 'vaccine')
    userlist = get_asset_data(all)
    return userlist



# user = search_amka('01109700300')
# print(user)

# status = search_status('pending')
# print(status)

# hosp = search_hospital('random')
# print(hosp)

# c = search_country('UK')
# print(c)

# g = search_gender('female')
# print(g)

# b = search_brand('Pfeizer')
# print(b)

# ct = search_city('London')
# print(ct)

# all = search_all()
# print(all)
