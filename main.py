from fastapi import FastAPI
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair

app = FastAPI()

@app.get("/getkeypair")
def root():
    alice= generate_keypair()
    return alice

@app.post("/todo")
def create_todo():
    bdb_root_url = 'http://localhost:9984'  # Use YOUR BigchainDB Root URL here
    alice, bob = generate_keypair(), generate_keypair()
    bdb = BigchainDB(bdb_root_url)

    bicycle_asset = {
        'data': {
            'bees': 'knees123',
        },
    }

    bicycle_asset_metadata = {
        'bees': 'knees123'
    }

    prepared_creation_tx = bdb.transactions.prepare(
        operation='CREATE',
        signers=alice.public_key,
        asset=bicycle_asset,
        metadata=bicycle_asset_metadata
    )

    print(prepared_creation_tx)

    fulfilled_creation_tx = bdb.transactions.fulfill(
        prepared_creation_tx,
        private_keys=alice.private_key
    )

    print('.................................................................')
    print(fulfilled_creation_tx)

    sent_creation_tx = bdb.transactions.send_commit(fulfilled_creation_tx)
    return sent_creation_tx


