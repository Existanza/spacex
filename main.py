# https://github.com/Existanza/

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import requests
from datetime import datetime
import numpy as np


def capsules():
    r = requests.get("https://api.spacexdata.com/v3/capsules")
    caps = r.json()
    for c in caps:
        print(c)


def launch_info():
    dates = []
    rocket_ids = []

    r = requests.get("https://api.spacexdata.com/v3/launches")
    launches = r.json()
    for l in launches:
        dates.append(datetime.utcfromtimestamp(l['launch_date_unix']))
        rocket_ids.append(l['rocket']['rocket_name'])

    years = mdates.YearLocator()
    months = mdates.MonthLocator()
    my_fmt = mdates.DateFormatter('%Y')

    fig, ax = plt.subplots()
    ax.scatter(dates, rocket_ids, s=0.2)

    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(my_fmt)
    ax.xaxis.set_minor_locator(months)

    fig.autofmt_xdate()
    plt.yticks(rotation=60)

    plt.savefig('a.png', dpi=300)


def customer_info():
    customers = {}

    r = requests.get("https://api.spacexdata.com/v3/payloads")
    pays = r.json()
    for p in pays:
        for c in p['customers']:
            if c not in customers:
                customers[c] = 1
            else:
                customers[c] += 1

    sorted_customers = sorted(customers.items(), key=lambda kv: kv[1], reverse=True)
    for el in sorted_customers:
        print(el[0] + ": " + str(el[1]))


def mass_correlation():
    dimensions = []
    masses = []

    r = requests.get("https://api.spacexdata.com/v3/rockets")
    rockets = r.json()
    for r in rockets:
        dimensions.append(r['height']['meters']*r['diameter']['meters']*np.pi)
        masses.append(r['mass']['kg'])

    poly_coeffs = np.polyfit(dimensions, masses, 1)
    poly = np.poly1d(poly_coeffs)

    fig, ax = plt.subplots()
    plt.title('Mass/volume correlation')
    plt.xlabel('Volume [m^3]')
    plt.ylabel('Mass [kg]')

    plt.plot(dimensions, poly(dimensions), 'r')
    plt.scatter(dimensions, masses)

    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.E'))

    plt.savefig('d.png', dpi=300)


# launch_info()  # A - done
# total_payload()  # B
# payload_difference()  # C
mass_correlation()  # D - done
# customer_info()  # E - done
