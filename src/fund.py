from edgar import *
import os
from edgar import find
from dotenv import load_dotenv
def doit():
    load_dotenv()
    name = os.getenv("NAME")
    email = os.getenv("EMAIL")
    set_identity(email)

    fund = find("VFIAX")  # Vanguard 500 Index Fund
    print(fund.__repr__())
    
    
    return fund