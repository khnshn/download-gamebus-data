import requests
import json
import sys
import pandas as pd
import time

ENDPOINT = "https://api-new.gamebus.eu/v2"


def main(users_csv_path, game_descriptor, authcode):
    token_url = ENDPOINT + "/oauth/token"
    player_id_url = ENDPOINT + "/users/current"
    activities_url = ENDPOINT + "/players/{}/activities?sort=-date&limit=500&page={}"

    df = pd.read_csv(users_csv_path, header=None)
    users = df.to_numpy()
    for index, user in enumerate(users):

        username = user[0]
        password = user[1]

        payload = "grant_type=password&username={}&password={}".format(
            username, password
        )
        headers = {
            "Authorization": "Basic {}".format(authcode),
            "Content-Type": "application/x-www-form-urlencoded",
        }

        response = requests.request("POST", token_url, headers=headers, data=payload)

        token = json.loads(response.text)["access_token"]

        print("token fetched successfully")

        headers = {"Authorization": "Bearer {}".format(token)}

        response = requests.request("GET", player_id_url, headers=headers, data=payload)

        player_id = json.loads(response.text)["player"]["id"]

        for page in range(100):
            if game_descriptor == "selfreport":
                data_url = (activities_url + "&excludedGds=").format(player_id, page)
            else:
                data_url = (activities_url + "&gds={}").format(
                    player_id, page, game_descriptor
                )
            payload = {}
            headers = {"Authorization": "Bearer {}".format(token)}

            if game_descriptor not in [
                "notification(detail)",
                "tizen(detail)",
                "selfreport",
            ]:
                print("gamedescriptor is not supported")
                return

            response = requests.request("GET", data_url, headers=headers, data=payload)

            # uncomment the following to save the raw json
            # with open(str(index) + "_" + game_descriptor + ".json", "w") as j:
            #     j.write(response.text)

            print("data of {} is fetched successfully page {}".format(index + 1, page))
            time.sleep(0.5)  # required to ensure the server is responsive

            data = json.loads(response.text)
            if data:
                with open(
                    str(index + 1) + "_" + game_descriptor + "_" + str(page) + ".csv",
                    "w",
                ) as c:
                    c.write("id,session_id,timestamp,name,value\n")
                    if (
                        game_descriptor == "selfreport"
                        or game_descriptor == "tizen(detail)"
                    ):
                        for jobj in data:
                            c.write(
                                str(index + 1)
                                + ","
                                + str(jobj["id"])
                                + ","
                                + str(jobj["date"])
                                + ","
                                + jobj["gameDescriptor"]["translationKey"]
                                + ","
                                + str(jobj["propertyInstances"][0]["value"])
                                + "\n"
                            )
                    elif game_descriptor == "notification(detail)":
                        for jobj in data:
                            c.write(
                                str(index + 1)
                                + ","
                                + str(jobj["id"])
                                + ","
                                + str(jobj["propertyInstances"][1]["value"])
                                + ","
                                + jobj["gameDescriptor"]["translationKey"]
                                + ","
                                + str(jobj["propertyInstances"][0]["value"])
                                + "\n"
                            )
                    else:
                        print("gamedescriptor is not supported")
                    print(
                        "data of {} is saved successfully page {}".format(
                            index + 1, page
                        )
                    )
            else:
                print("no more data for {}".format(index + 1))
                break


if __name__ == "__main__":
    if len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("invalid number of command line parameters. 3 parameters are required")
