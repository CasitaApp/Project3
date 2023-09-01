import streamlit as st
from web3 import Web3
import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv(".env")

# Conectar a un nodo de Ethereum
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

# Dirección del propietario y clave privada (para transacciones)
owner_address = os.getenv("OWNER_ADDRESS")
private_key = os.getenv("PRIVATE_KEY")

# Función para cargar el contrato
def load_contract():
    with open(Path('./voting_abi.json')) as f:
        voting_abi = json.load(f)

    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
    contract = w3.eth.contract(address=contract_address, abi=voting_abi)
    return contract

# Cargar el contrato
contract = load_contract()

# Configurar la cuenta del propietario con derechos de registrar votantes y agregar candidatos
w3.eth.defaultAccount = owner_address

# Definir la interfaz de usuario de Streamlit
st.title('Sistema de Votación')
st.sidebar.title('Panel de Control')

# Aquí puedes agregar elementos de Streamlit como botones y formularios para interactuar con tu contrato

# Ejemplo de uso: Mostrar el número de candidatos
candidate_count = contract.functions.getCandidateCount().call()
st.write(f'Número de candidatos: {candidate_count}')

# Función para registrar un votante
def register_voter():
    tx_hash = contract.functions.registerVoter().transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return tx_receipt

# Función para agregar un candidato
def add_candidate(name):
    tx_hash = contract.functions.addCandidate(name).transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return tx_receipt

# Función para emitir un voto
def vote(candidate_index):
    tx_hash = contract.functions.vote(candidate_index).transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return tx_receipt

# Función para obtener el número de candidatos
def get_candidate_count():
    return contract.functions.getCandidateCount().call()

# Función para obtener información de un candidato por índice
def get_candidate_info(index):
    return contract.functions.getCandidate(index).call()

# Ejemplo de uso
if st.button("Registrar Votante"):
    register_voter()

if st.button("Agregar Candidatos"):
    add_candidate("Candidato A")
    add_candidate("Candidato B")

if st.button("Emitir Votos"):
    vote(0)
    vote(1)

# Obtener el número de candidatos y sus detalles
candidate_count = get_candidate_count()
for i in range(candidate_count):
    name, vote_count = get_candidate_info(i)
    st.write(f"Candidato: {name.decode('utf-8')}, Votos: {vote_count}")

# Función para contar votos por candidato
def count_votes():
    votes = contract.functions.countVotes().call()
    return votes

# Ejemplo de uso: Mostrar los votos por candidato
if st.button("Contar Votos"):
    candidate_votes = count_votes()
    candidate_count = get_candidate_count()
    for i in range(candidate_count):
        name, _ = get_candidate_info(i)
        candidate_name = name.decode('utf-8')
        vote_count = candidate_votes[i]
        st.write(f"Candidato: {candidate_name}, Votos: {vote_count}")
