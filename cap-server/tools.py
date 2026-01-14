from livekit.agents.llm import function_tool
import pandas as pd
from typing import List, Dict
from pathlib import Path
from enum import Enum

class EmployeeField(Enum):
    def __new__(cls, column_name: str, restricted: bool):
        obj = object.__new__(cls)
        obj._value_ = column_name
        obj.column = column_name
        obj.restricted = restricted
        return obj
    email = ("Email", False)
    phone = ("Phone", False)
    address = ("Address", True)
    role = ("Role", False)
    salary = ("Salary", False)
    def set_access(self, restricted: bool) -> None:
        self.restricted = restricted



empl_df = None

def load_employee_directory():
    global empl_df
    # Get the directory where this file is located
    _current_dir = Path(__file__).parent
    empl_df = pd.read_csv(_current_dir / "empl.csv")

@function_tool
async def get_employee_directory(employee_name: str, fields: List[EmployeeField]) -> List[Dict[str, str]]:
    """
    Find employees by name prefix in the company directory.
    Use ONLY when the user asks for employee lookup, info such as
    email, phone, role, address by name.
    Performs case-insensitive prefix matching on employee names.
    Returns a list of matching employee records or an empty list.
    """
    if empl_df is not None:
        result = []
        matches = empl_df[empl_df["Name"].str.lower().str.startswith(employee_name.lower())]
        for idx, match in matches.iterrows():
            employee_record = {}
            for field in fields:
                if field.restricted:
                    employee_record[field.column] = "********"
                else:
                    employee_record[field.column] = str(match[field.column])
            result.append(employee_record)
        return result
    else:
        return []