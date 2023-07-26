import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse

from utility.constants import Constants
from utility.data_models import Insert
from utility.logger import get_logger

data = pd.read_csv(Constants.DATA_PATH.value)


LOGGER = get_logger("Main Module.")

app = FastAPI(debug=True)


@app.get("/get_all_id")
def get_all_id():
    global data
    my_list = list(data.car_ID)

    response = {"All_IDS": my_list}

    print(data.tail())

    return JSONResponse(content=response, status_code=200)


@app.post("/insert_car_entry")
def insert_data(msg: dict):
    Insert(**msg)
    global data
    new_dict = {key: [value] for key, value in msg.items()}
    new_entry = pd.DataFrame.from_dict(new_dict)
    print(new_entry)
    data = pd.concat([data, new_entry], axis=0, ignore_index=True)
    print(data.tail())

    response = {"Message": "New Entry Data validated and inserted succesfully!"}

    return JSONResponse(content=response, status_code=200)


@app.delete("/remove_entry/{car_ID}")
def remove_entry(car_ID: int):
    global data

    index = data.index[data["car_ID"] == car_ID]

    if index.empty:
        response = {"Message": f"Car ID - {car_ID} not found."}
        return JSONResponse(content=response, status_code=401)
    else:
        print(data.iloc[index])
        data.drop([index.values[0]], inplace=True)
        print(data.tail())

        response = {"Message": f"Entry with Car ID - {car_ID} has been deleted."}

        return JSONResponse(content=response, status_code=200)


@app.put("/update_entry/{car_ID}")
def update_entry(car_ID: int, msg: dict):
    global data

    index = data.index[data["car_ID"] == car_ID]

    if index.empty:
        response = {"Message": f"Car ID - {car_ID} not found."}
        return JSONResponse(content=response, status_code=401)

    print(data.columns)
    for key in msg:
        if key not in data.columns:
            response = {"Message": f"'{key}' not a valid column. Invalid input."}
            return JSONResponse(content=response, status_code=400)

    print(f"Row before update: \n{data.iloc[index]}")

    for key, value in msg.items():
        data.loc[index, key] = value

    print(f"Row after update: \n{data.iloc[index]}")

    response = {
        "Message": f"Entry with ID {car_ID} has been succesfully update with the data given."
    }

    return JSONResponse(content=response, status_code=200)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info", reload=True)
