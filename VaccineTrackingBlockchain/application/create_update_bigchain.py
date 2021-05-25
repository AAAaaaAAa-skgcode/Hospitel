from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
from time import sleep
from sys import exit

hospital_key = generate_keypair()

bdb_root_url = 'localhost:9984'  # Use YOUR BigchainDB Root URL here

bdb = BigchainDB(bdb_root_url)

def create_vaccination(hospital_key, amka, name, age, gender, address, country, brand, status, doses, symptoms, first, hospital):
    hospital_asset = {
        'data': {
            'amka': amka,
            'name': name,
            'age': age,
            'gender': gender,
            'address': address,
            'country': country,
            },
        }

    hospital_metadata = {
        'vaccine_brand': brand,
        'status': status,
        'completed_doses': doses,
        'symptoms': symptoms,
        'first_dose_date': first,
        'hospital': hospital
        }

    prepared_creation_tx = bdb.transactions.prepare(
        operation='CREATE',
        signers=hospital_key.public_key,
        asset=hospital_asset,
        metadata=hospital_metadata
    )

    fulfilled_creation_tx = bdb.transactions.fulfill(
        prepared_creation_tx,
        private_keys=hospital_key.private_key,
    )

    sent_creation_tx = bdb.transactions.send_commit(fulfilled_creation_tx)

    txid = fulfilled_creation_tx['id']
    print("THE TXID IS: ", txid)


# create_vaccination(hospital_key, '0101199700300', 'JK', '25', 'male', 'grimold place', 'UK', 'Pfeizer', 'completed', '2', 'none', '5/6', 'St Mungos')
# create_vaccination(hospital_key, '0707197000800', 'Sherlock Holmes', '30', 'male', 'baker street', 'England', 'Pfeizer', 'pending', '1', 'fever', '6/6', 'random')


######################################################################################################


def update_vaccination(hospital_key, amka, brand, status, doses, symptoms, second):

    txid = bdb.assets.get(search= amka)
    txid = txid[0]['id']

    fulfilled = bdb.transactions.retrieve(txid)

    update_asset = {
        'id': txid
    }

    update_metadata = {
        'vaccine_brand': brand,
        'status': status,
        'completed_doses': doses,
        'symptoms': symptoms,
        'second_dose_date': second
    }  
    output_index = 0
    output = fulfilled['outputs'][output_index]

    update_input = {
        'fulfillment': output['condition']['details'],
        'fulfills': {
            'output_index': output_index,
            'transaction_id': fulfilled['id']
        },
        'owners_before': output['public_keys']
    }

    prepared_update_tx = bdb.transactions.prepare(
        operation='TRANSFER',
        asset=update_asset,
        metadata=update_metadata,
        inputs=update_input,
        recipients=hospital_key.public_key,
    )

    fulfilled_update_tx = bdb.transactions.fulfill(
        prepared_update_tx,
        private_keys=hospital_key.private_key,
    )

    sent_update_tx = bdb.transactions.send_commit(fulfilled_update_tx)



# update_vaccination(hospital_key, '0707197000800', 'Pfizer', 'completed', '2', 'none', '26/6')




