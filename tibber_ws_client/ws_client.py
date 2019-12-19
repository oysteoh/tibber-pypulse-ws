import requests
import pprint

headers = None


def name():
    query = """
    {
    viewer {
        name
    }
    }
    """
    result = execute(query)
    print(result["data"]["viewer"]["name"])


def homes():
    query = """
    {
    viewer {
        homes {
        address {
            address1
            address2
            address3
            postalCode
            city
            country
            latitude
            longitude
        }
        }
    }
    }
    """
    result = execute(query)
    pprint.pprint(result)


def current_energy_price():
    query = """
    {
    viewer {
        homes {
        currentSubscription{
            priceInfo{
            current{
                total
                energy
                tax
                startsAt
            }
            }
        }
        }
    }
    }
    """
    result = execute(query)
    pprint.pprint(result)


def consumption():
    query = """
    {
    viewer {
        homes {
        consumption(resolution: HOURLY, last: 100) {
            nodes {
            from
            to
            cost
            unitPrice
            unitPriceVAT
            consumption
            consumptionUnit
            }
        }
        }
    }
    }
    """
    result = execute(query)
    pprint.pprint(result)


def home_price_consumption():
    query = """
    {
    viewer {
        homes {
        timeZone
        address {
            address1
            postalCode
            city
        }
        owner {
            firstName
            lastName
            contactInfo {
            email
            mobile
            }
        }
        consumption(resolution: HOURLY, last: 10) {
            nodes {
            from
            to
            cost
            unitPrice
            unitPriceVAT
            consumption
            consumptionUnit
            }
        }
        currentSubscription {
            status
            priceInfo {
            current {
                total
                energy
                tax
                startsAt
            }
            }
        }
        }
    }
    }
    """
    result = execute(query)
    pprint.pprint(result)


def push_notification(message):
    query = """
    mutation {{
    sendPushNotification(input: {{title: "Notification through API", message: "{}", screenToOpen: CONSUMPTION}}) {{
        successful
        pushedToNumberOfDevices
    }}
    }}
    """.format(
        message
    )
    result = execute(query)
    pprint.pprint(result)


def execute(query):
    request = requests.post(
        "https://api.tibber.com/v1-beta/gql", json={"query": query}, headers=headers
    )
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception(
            "Query failed to run by returning code of {}. {}".format(
                request.status_code, query
            )
        )


if __name__ == "__main__":
    home_price_consumption()
