from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
from fastapi.responses import JSONResponse
import os

class CreateTransaction(BaseModel):
    seed: str
    asset: Dict[str, Dict[str, str]]
    metaData: Dict[str, str]

app = FastAPI()

bdb_root_url = 'http://bigchaindb-bigchaindb-1:9984'
bdb = BigchainDB(bdb_root_url)

@app.get("/get_seed")
def get_seed():
    seed = os.urandom(32)
    data = {"result": "success", "data": {"seed": seed.hex()}}
    return JSONResponse(content=data)

@app.post("/create_transaction")
def create_transaction(data: CreateTransaction):
    seed = bytes.fromhex(data.seed)
    transaction_key_pair = generate_keypair(seed)

    prepared_creation_tx = bdb.transactions.prepare(
        operation='CREATE',
        signers=transaction_key_pair.public_key,
        asset=data.asset,
        metadata=data.metaData
    )
    fulfilled_creation_tx = bdb.transactions.fulfill(
        prepared_creation_tx,
        private_keys=transaction_key_pair.private_key
    )

    sent_creation_tx = bdb.transactions.send_commit(fulfilled_creation_tx)
    return sent_creation_tx

@app.get("/get_transaction/{id}")
def get_transaction(id: str):
    return bdb.transactions.get(asset_id= id)