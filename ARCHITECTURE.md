 ## Drones API

Here you could take a closer approach to understand how the developer implement the study case and business rules.

### Models

Based on the **STUDY_CASE.md** we implement three model classes

- Drone
- Load
- Medication

**Drone** model has its attributes (serial, model, weight_limit, battery_capacity, state). *model* and *state* 
attributes are Enums, *battery_capacity* and *weight_limit* has range validations.

>*model* attribute could be implemented as another model class in case it has specific attributes. 

**Load** class is an interface that has common attributes (weight and drone instance). This assumption was made in case
that later other loads (different of Medication) could be assign to drones

**Medication** model implements **Load** and has their own attributes (name, code, image). The validations about name 
and code were made with regex.

### Views

Based on DRF was implemented main features

#### [POST] Register Drone (/register) 
loads array on register will be empty because once the drone is register it doesnt have any load

- **INPUT** 
```json
{
    "loads": [],
    "serial_number": "",
    "model": null,
    "weight_limit": null,
    "battery_capacity": null,
    "state": null
}
```

- **OUTPUT** 
```json
{
    "loads": [],
    "serial_number": "0005",
    "model": "Lightweight",
    "weight_limit": 500,
    "battery_capacity": 60,
    "state": "IDLE"
}
```

#### [GET] Check available drones (/available_drones)
Drones available are the ones has IDLE state and its battery level is over 25 %

- **INPUT** 
> Has no input, GET request 


- **OUTPUT** 
```json
[
    {
        "id": 3,
        "loads": [],
        "serial_number": "0003",
        "model": "Cruiserweight",
        "weight_limit": 400,
        "battery_capacity": 80,
        "state": "IDLE"
    },
    {
        "id": 5,
        "loads": [],
        "serial_number": "0005",
        "model": "Lightweight",
        "weight_limit": 500,
        "battery_capacity": 60,
        "state": "IDLE"
    }
]
```

#### [GET] Check drone battery level (/battery_level/<drone_pk>/)
Returns *battery level* for the given drone (*<drone_pk>*)  

- **INPUT** 
> Has no input, GET request 


- **OUTPUT** 
```json
{
    "battery_capacity": 20
}
```

#### [POST] Load drone with medications (/drone/<drone_pk>/load/)
Receive a list of medications ids and loads the drone, taking into account **requirements** described below

- **INPUT** 
```json
{
  "loads":[1,2,3]
}
```


- **OUTPUT** 

Successful response >  HTTP 202 Accepted

Error response > Error message, HTTP 406 Not Acceptable

#### [GET] Load drone with medications (/drone/<drone_pk>/loaded_medication/)

Returns a list of Medications loaded on the given drone (*<drone_pk>*)

- **INPUT** 
> Has no input, GET request 


- **OUTPUT** 
```json
[
    {
        "id": 1,
        "weight": 150,
        "name": "MED_1",
        "code": "101",
        "drone": 1
    },
    {
        "id": 2,
        "weight": 200,
        "name": "MED_2",
        "code": "102",
        "drone": 1
    }
]
```

### Requirements

*Prevent the drone from being loaded with more weight that it can carry;*

- To accomplish this requirement was implemented *can_be_loaded_weight(drone, medication_list)*. 
In case *get_load_total_weight(medication_list)* is greater than *drone_weight_limit*, 
*medication_list* would not be loaded.

*Prevent the drone from being in LOADING state if the battery level is **below 25%**;*

- To accomplish this requirement was implemented *can_be_loaded_battery_level(drone)*. 
In case *drone_battery_capacity* is under 25 %, would not be loaded.

*Introduce a periodic task to check drones battery levels and create history/audit event log 
for this.*

- To accomplish this requirement was implemented a cron job (*check_drone_battery_level*) to 
write on a log file, the battery capacity from every drone registered in a range of time.


### TODO

- Implement endpoints to manage Medications through API, now it is doing by admin panel

- Implement more test to verify each feature
