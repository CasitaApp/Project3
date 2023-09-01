# Project3
## Remix smart contract 
import streamlit as st
from datetime import datetime
from web3 import Web3
from pathlib import Path
import os
import json
from dotenv import load_dotenv
    
load_dotenv("env.txt")

owner_address = os.getenv("OWNER_ADDRESS")
private_key = os.getenv("PRIVATE_KEY")
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

def load_contract():

    with open(Path('./voting_abi.json')) as f:
        voting_abi = json.load(f)

    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    contract = w3.eth.contract(address=contract_address, abi=voting_abi)
    return contract

contract = load_contract()

st.title("Employee of the Month Voting System")

end_date = datetime(2023, 9, 28)
current_date = datetime.now()
voting_period_ended = current_date > end_date

if not voting_period_ended:
    time_left = end_date - current_date
    st.subheader(f"Time Left to Vote: {time_left.days} days, {time_left.seconds // 3600} hours, {time_left.seconds % 3600 // 60} minutes")
else:
    st.subheader("Voting period has not ended yet! ")

user_address = st.text_input("Enter your Ethereum address:")
voters_registry = []

hasVoted = False

if st.button("Register to Vote"):
    try:
        user_address = Web3.toChecksumAddress(user_address)
        # Verificar si el usuario ya está registrado
        if user_address in voters_registry:
            hasVoted = True
            st.write("You are already registered!")
        else:
            # Llamar a la función registerVoter del contrato inteligente
            tx_hash = contract.functions.registerVoter().transact({'from': user_address})
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            st.success("Great! Now you are registered and able to cast your vote")
            
        
            voters_registry.append(user_address)
            
    except Exception as e:
        st.error(f"Error during registration: {str(e)}")

candidate_names = ["Ken", "Elon", "Satoshi", "Nakamoto"]
selected_candidate = None  

vote_counts = {candidate: 0 for candidate in candidate_names}
selected_candidate = st.selectbox("Select a candidate:", candidate_names)
candidateIndex = candidate_names.index(selected_candidate)
voted_message = ""

if st.button("Vote", key="vote_button"):
    if selected_candidate is not None:
        try:
         
            if user_address not in votos_emitidos:
                st.write(f'candidateIndex:{candidateIndex}')
                tx_hash = contract.functions.vote(candidateIndex).transact({'from': user_address})
                tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
                # Actualizar la lista de votos emitidos
                votos_emitidos.append(user_address)
                voted_message = "Thank you for voting"
            else:
                voted_message = "You have already voted!"
        except ContractLogicError as e:
            voted_message = f"Error: {str(e)}"
    else:
        voted_message = "Please select a candidate before voting."

if st.button("Show Results"):
    st.subheader("Results")
    try:
        for candidateIndex in range(len(candidate_names)):
            number_of_votes = contract.functions.getCandidateVoteCount(candidateIndex).call()
            st.write(f'{candidate_names[candidateIndex]}: {number_of_votes} votes')
    except ValueError as e:
        error_message = str(e)
        st.error(f"Error: {error_message}. Please ensure the candidate index is valid.")


# Ganache

![image](https://github.com/CasitaApp/Project3/assets/39076992/0a4956ad-c00a-455a-bf62-1bb29466aa8e)









