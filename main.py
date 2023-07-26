import pandas as pd
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from utility.constants import Constants
from utility.data_models import Insert
from utility.logger import get_logger

data = pd.read_csv(Constants.DATA_PATH.value)


LOGGER = get_logger("Main Module.")

app = FastAPI(debug=True)


@app.get("/get_all_id")
def get_all_id() -> dict:
    """
    This endpoint is just to check how many entries are there in the dataset and,
    what are the IDs.
    """
    global data
    my_list = list(data.car_ID)

    response = {"All_IDS": my_list}

    return JSONResponse(content=response, status_code=200)


@app.post("/insert_car_entry")
def insert_data(msg: dict) -> dict:
    """
    This post endpoint is used to insert data.
    First the JSON body is validated and then the dataset is updated.
    """
    Insert(**msg)
    global data
    new_dict = {key: [value] for key, value in msg.items()}
    new_entry = pd.DataFrame.from_dict(new_dict)

    data = pd.concat([data, new_entry], axis=0, ignore_index=True)

    response = {"Message": "New Entry Data validated and inserted succesfully!"}

    return JSONResponse(content=response, status_code=200)


@app.delete("/remove_entry/{car_ID}")
def remove_entry(car_ID: int) -> dict:
    """
    This delete endpoint can be used to delete an entry from the dataset using the Car ID.
    It also checks for invalid ID passed.
    """
    global data

    index = data.index[data["car_ID"] == car_ID]

    if index.empty:
        response = {"Message": f"Car ID - {car_ID} not found."}
        return JSONResponse(content=response, status_code=401)
    else:
        data.drop([index.values[0]], inplace=True)

        response = {"Message": f"Entry with Car ID - {car_ID} has been deleted."}

        return JSONResponse(content=response, status_code=200)


@app.put("/update_entry/{car_ID}")
def update_entry(car_ID: int, msg: dict) -> dict:
    """
    This put endpoint can be used for updating an existing entry using the Car ID.
    It checks whether the JSON body passed is valid or not.
    It also checks for invalid ID passed.
    """
    global data

    index = data.index[data["car_ID"] == car_ID]

    if index.empty:
        response = {"Message": f"Car ID - {car_ID} not found."}
        return JSONResponse(content=response, status_code=401)

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
