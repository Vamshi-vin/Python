from pathlib import Path
from typing import Dict

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="Bank Management System")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


class Account(BaseModel):
    account_number: int
    account_holder: str
    balance: float


accounts: Dict[str, Account] = {}


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )


@app.post("/accounts/")
def create_account(account: Account):
    if account.account_number in accounts:
        raise HTTPException(status_code=400, detail="Account already exists")
    if account.balance < 0:
        raise HTTPException(status_code=400, detail="Initial balance cannot be negative")

    accounts[account.account_number] = account
    return account


@app.get("/accounts/{account_number}")
def get_account(account_number: int):
    if account_number not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    return accounts[account_number]


@app.post("/accounts/{account_number}/deposit")
def deposit(account_number: int, amount: float):
    if account_number not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Deposit amount must be positive")

    accounts[account_number].balance += amount
    return accounts[account_number]


@app.post("/accounts/{account_number}/withdraw")
def withdraw(account_number: int, amount: float):
    if account_number not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Withdrawal amount must be positive")
    if accounts[account_number].balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    accounts[account_number].balance -= amount
    return accounts[account_number]


#http://127.0.0.1:8000/ for the app
#http://127.0.0.1:8000/docs for Swagger API docs
#uvicorn main:app --reload
