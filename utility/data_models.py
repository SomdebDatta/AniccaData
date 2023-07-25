from pydantic import BaseModel, StrictFloat, StrictInt, StrictStr


class Insert(BaseModel):
    car_ID: StrictInt
    symboling: StrictInt
    CarName: StrictStr
    fueltype: StrictStr
    aspiration: StrictStr
    doornumber: StrictStr
    carbody: StrictStr
    drivewheel: StrictStr
    enginelocation: StrictStr
    wheelbase: StrictFloat
    carlength: StrictFloat
    carwidth: StrictFloat
    carheight: StrictFloat
    curbweight: StrictInt
    enginetype: StrictStr
    cylindernumber: StrictStr
    enginesize: StrictInt
    fuelsystem: StrictStr
    boreratio: StrictFloat
    stroke: StrictFloat
    compressionratio: StrictFloat
    horsepower: StrictInt
    peakrpm: StrictInt
    citympg: StrictInt
    highwaympg: StrictInt
    price: StrictInt
