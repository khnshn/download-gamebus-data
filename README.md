# Download (ESM-specific) GameBus Data
The script allows study owners to download the data gathered during their experiment

Before first run, install python and then run `pip install -r requirements.txt`.

## Format of the command
`python get_data.py <<USERS_CSV_FILE_PATH>> <<DATA_KEYWORD>> <<AUTH_CODE>>`

### Supported commands:

`python get_data.py ./test.csv notification(detail) secret_auth_code`

`python get_data.py ./test.csv selfreport secret_auth_code`

`python get_data.py ./test.csv selfreport secret_auth_code`

## Structure of the csv file
The csv file should include the email and password of the participants where column 0 is the email and column 1 is the password. Please note that the csv must not have a header row.

## Auth code
To get the auth code contact the GameBus representative.

**Note** that for csv conversion of selfreport, it is assumed that each activity holds a propertyInstance array with length of 1.

**Note** that for csv conversion of notification(detail), it is assumed that each activity holds a propertyInstance array with length of 2.