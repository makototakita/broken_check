from web3 import Web3
import json

w3 = Web3(Web3.HTTPProvider('http://127.21.0.5:8545'))

# ノードに接続されているかどうかを確認
if w3.is_connected():
    print("Connected to Ethereum node")

    # 最新のブロック番号を取得
    latest_block = w3.eth.block_number
    print("Latest block number:", latest_block)
else:
    print("Failed to connect to Ethereum node")

    # Ethereumアドレスの残高を取得（実際のアドレスに置き換えてください）
account_0 = "0xdfe90111aA6021f47154a9a592B3016c48f5696d"
private_key = "0xd6ac6a0cc54ecea8425d597f69665ef4a860662390494a77d3897bdb826d846e"
balance_wei = w3.eth.get_balance(account_0)
balance_eth = w3.from_wei(balance_wei, 'ether')
print(f"アドレス {account_0} の残高: {balance_eth} ETH")

contract_address = "0x0b34d756b7d1655818c3a5Ef51F79e03A7ae9E80"

with open("build/contracts/HelloWorld.json") as file:
    contract_interface = json.load(file)

# print(contract)

bytecode = contract_interface['deployedBytecode']
abi = contract_interface['abi']

print(bytecode)
print(abi)

acct = w3.eth.account.from_key(private_key)


contract = w3.eth.contract(abi=abi, bytecode=bytecode)

# トランザクションの生成
tx = contract.constructor().build_transaction({
    'from': acct.address,
    'to'
    'nonce': w3.eth.get_transaction_count(acct.address),
    'gas': 1728712,
    'gasPrice': w3.to_wei('21', 'gwei')})

signed  = acct.sign_transaction(tx)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
#print(tx_hash.hex())

# トランザクションに署名
#signed_tx = w3.eth.account.sign_transaction(tx, private_key)

# トランザクションの送信
#tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)


greeter = w3.eth.contract(address=contract_address, abi=abi)
print(greeter.functions.add(1,2**256-2).call())

#print(greeter.functions.times2(100).call())


#print(greeter.functions.add(100,200).call())

