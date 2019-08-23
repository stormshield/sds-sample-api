# SDS Sample Api

This project explains how to use SDMC external api to retrieve informations as csv file.
One subProject is created to describe one Api call, each api is defined [here](https://sds.stormshieldcs.eu/doc/api/).

- [prerequisites](#prerequisites)
- [How to export User?](#export-user)

## Prerequisites

- Install python 3.6.5
- Ask an access token to your SDMC administrator

## How to export User?
Sample is defined in sample-export-users folder.
### Configuration
You have to edit config.js and copy your access token on it.
```
{
    "token": "SDMC access token"
}
```
### Launch
Command to execute example is:
```
    python exportUser.py --config=config.json
```
At the end, a successfully message is logged and you can open the file ```UserData.csv``` which contains all users informations.

Default user informations are :
```
id;first_name;last_name;email;state;roles;devices_count;last_activity_date;register_date.
```

### Options
- You can change SMDC url by defining ```serverUrl``` in config.json
- You can filter user columns you want to retrieve by defining ```exposedData``` in config.json.
This atttribute is an array which is a subassembly of Default user informations.

 For example, if you want id and email you have to add :
 ```
 "exposedData": ["id", "email"]
  ```

## How to predefine users ?
Folder : sample-predefine-users

### Configuration
You have to edit config.js and copy your access token on it.
```
{
    "token": "SDMC access token"
}
```

### Input CSV file content
Your input CSV file should contains a first line with headers and then data.

```csv
email;
my-email@acme.com;
my-email2@acme.com;
```

### Launch
Command to execute example is:
```
    python predefine-users.py --config=config.json --input=input.csv
```
