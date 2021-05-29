from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
from time import sleep
from sys import exit

#hospital_key = generate_keypair()
#public_key = hospital_key.public_key
#private_key = hospital_key.private_key

bdb_root_url = 'localhost:9984'  # Use YOUR BigchainDB Root URL here

bdb = BigchainDB(bdb_root_url)

def create_vaccination(public_key, private_key, prim_number, amka, name, age, gender, address, country, city, brand, status, doses, symptoms, first_date,second_dose_date, hospital):
    hospital_asset = {
        'data': {
            'vaccine': 'vaccine',
            'prim_number': prim_number,
            'amka': amka,
            'name': name,
            'age': age,
            'gender': gender,
            'country': country,
            'city': city,
            'address': address,
            },
        }

    hospital_metadata = {
        'vaccine_brand': brand,
        'status': status,
        'completed_doses': doses,
        'symptoms': symptoms,
        'first_dose_date': first_date,
        'second_dose_date': second_dose_date,
        'hospital': hospital
        }

    prepared_creation_tx = bdb.transactions.prepare(
        operation='CREATE',
        signers=public_key,
        asset=hospital_asset,
        metadata=hospital_metadata
    )

    fulfilled_creation_tx = bdb.transactions.fulfill(
        prepared_creation_tx,
        private_keys=private_key,
    )

    sent_creation_tx = bdb.transactions.send_commit(fulfilled_creation_tx)

    txid = fulfilled_creation_tx['id']
    print("THE TXID IS: ", txid)
    return txid


#create_vaccination(public_key, private_key, '1', '01109700300', 'JK', '25', 'male', 'grimold place', 'UK', 'London', 'Moderna', 'pending', '1', 'none', '5/6', 'St Mungos')
#create_vaccination(public_key, private_key, '2', '06055400800', 'Sherlock Holmes', '30', 'male', 'baker street', 'UK', 'London', 'Pfizer', 'pending', '1', 'none', '6/6', 'random')
#create_vaccination(public_key, private_key, '3', '13039000900', 'Lia', '40', 'female', 'unknown', 'Germany', 'Berlin', 'Pfeizer', 'pending', '1', 'fever', '10/6', 'random')


# print('*********************************************')
# query1 = bdb.metadata.get(search='completed')
# print(query1)
# print('*********************************************')
# query2 = bdb.metadata.get(search='1')
# print(query2)
# print('*********************************************')
# query3 = bdb.assets.get(search='JK')
# print(query3)
# print('*********************************************')
# query4 = bdb.assets.get(search='male')
# print(query4)
# print(len(query4))

# #print(query1[0]['id'])

# ######################################################################################################
# ######################################################################################################


def update_vaccination_bigchain(public_key, private_key, amka, **kwargs):
    print('IN UPDATE VACCINATION BIGCHAIN\n')
    txid = bdb.assets.get(search = amka)
    txid = txid[0]['id']

    fulfilled = bdb.transactions.get(asset_id=txid)
    last = len(fulfilled) - 1

    # t = bdb.transactions.get(asset_id=id)
    # print('######## 2 ##################')
    # print(t)

    update_asset = {
        'id': txid
    }

    update_metadata = {}
    for key, value in kwargs.items():
        if (kwargs.get('vaccine_brand') != None):
            update_metadata['vaccine_brand'] = kwargs['vaccine_brand']
        
        if (kwargs.get('status') != None):
            update_metadata['status'] = kwargs['status']

        if (kwargs.get('completed_doses') != None):
            update_metadata['completed_doses'] = kwargs['completed_doses']

        if (kwargs.get('symptoms') != None):
            update_metadata['symptoms'] = kwargs['symptoms']

        if (kwargs.get('first_date') != None):
            update_metadata['first_date'] = kwargs['first_date']

        if (kwargs.get('second_date') != None):
            update_metadata['second_date'] = kwargs['second_date']

        if (kwargs.get('hospital') != None):
             update_metadata['hospital'] = kwargs['hospital']


    output_index = 0
    output = fulfilled[last]['outputs'][output_index]

    update_input = {
        'fulfillment': output['condition']['details'],
        'fulfills': {
            'output_index': output_index,
            'transaction_id': fulfilled[last]['id']
        },
        'owners_before': output['public_keys']
    }

    prepared_update_tx = bdb.transactions.prepare(
        operation='TRANSFER',
        asset=update_asset,
        metadata=update_metadata,
        inputs=update_input,
        recipients=public_key,
    )

    fulfilled_update_tx = bdb.transactions.fulfill(
        prepared_update_tx,
        private_keys=private_key,
    )

    sent_update_tx = bdb.transactions.send_commit(fulfilled_update_tx)

    return



#update_vaccination(public_key, private_key, '06055400800',  vaccine_brand = None, status = None, completed_doses = None, symptoms = 'fever', second_date = None, hospital = None)

#update_vaccination(public_key, private_key, '13039000900', vaccine_brand = None, status = 'completed', completed_doses = '2', symptoms = 'none', second_date = '26/6', hospital = None)

# print('### 1 ###')
# q1 = bdb.metadata.get(search = 'cancelled')
# print(q1)

# print('### 2 ###')
#q2 = bdb.assets.get(search = '06055400800')
#print(q2)

#update_vaccination(public_key, private_key, '06055400800',  vaccine_brand = None, status = 'completed', completed_doses = '2', symptoms = 'tired', second_date = '30/6', hospital = None)
