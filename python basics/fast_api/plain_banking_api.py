#create FastAPI backend application related to Bank management system, which has the following features:
#1. Create a new bank account with a unique account number, account holder's name, and initial balance.
#2. Retrieve account details using the account number.
#3. Deposit money into an account.
#4. Withdraw money from an account, ensuring that the balance does not go negative. 


#create a FastAPI application with the above features:
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict 

#initialize the FastAPI application
app = FastAPI() 

# Define the Account model using Pydantic
# The Account class inherits from BaseModel, which allows us to define the structure of the 
# account data and automatically handle validation and serialization.

class Account(BaseModel):
    account_number: str
    account_holder: str
    balance: float
accounts: Dict[str, Account] = {}

# Define the API endpoints for the bank management system
@app.post("/accounts/")
def create_account(account: Account):
    if account.account_number in accounts:
        raise HTTPException(status_code=400, detail="Account already exists")
    accounts[account.account_number] = account
    return account


@app.get("/accounts/{account_number}")
def get_account(account_number: str):
    if account_number not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    return accounts[account_number]


@app.post("/accounts/{account_number}/deposit")
def deposit(account_number: str, amount: float):
    if account_number not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    accounts[account_number].balance += amount
    return accounts[account_number]

@app.post("/accounts/{account_number}/withdraw")
def withdraw(account_number: str, amount: float):
    if account_number not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    if accounts[account_number].balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    accounts[account_number].balance -= amount
    return accounts[account_number]
# In this code, we define a FastAPI application with endpoints to create a new bank account,
#  retrieve account details, deposit money, and withdraw money. 
# We use a dictionary to store the accounts in memory, and we handle errors using HTTP exceptions. 
# To run this application, you would typically use a command like `uvicorn main:app --reload`, where `main` is the name of the Python file containing the code and `app` is the name of the FastAPI instance.

#initialize the FastAPI application and run it using uvicorn:
# To run the application, save the code in a file named `main.py` and use the following command in the terminal:
# uvicorn main:app --reload
# This command will start the FastAPI application and make it available at `http://127.0.1:8000`. You can then use tools like curl, Postman, or a web browser to interact with the API endpoints defined in the application.    
