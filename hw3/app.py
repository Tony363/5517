
# Import FastAPI
from fastapi import FastAPI
from pydantic import BaseModel

# Create an app instance
app = FastAPI()

class Year(BaseModel):
    year: int

@app.post("/is_leap_year/")
def is_leap_year(year: Year):
    """Endpoint to determine if a given year is a leap year."""
    y = year.year
    return {"year": y, "is_leap_year": (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)}
