"""
CS051P Final Project

    Author: Unity Tambellini-Smith

    Date: 12/10/2021

    Various analyses of airbnb data
"""
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

def price_satisfaction(filename):
    """
    Price_satisfaction extracts pairs of price-satisfaction data from an airbnb data file
    :param filename: str: name of airbnb data file
    :return: list: list of lists of data points in [price (float), satisfaction (float)] format
    """
    with open(filename, "r", encoding="utf-8") as file_in:

        # skip header
        header = file_in.readline().split(",")

        # get data set length
        dataset_length = len(header)

        # find indexes
        for i in range(dataset_length):
            if header[i] == "price":
                price_index = i
            if header[i] == "overall_satisfaction":
                satisfaction_index = i
            if header[i] == "reviews":
                review_index = i

        # initialize list
        datapoints = []

        # make data iterable
        for line in file_in:
            data = line.split(",")

            # remove incomplete lines and unreviewed properties
            if len(data) == dataset_length and int(data[review_index]) > 0:

                # extract price and satisfaction data
                price = float(data[price_index])
                satisfaction = float(data[satisfaction_index])

                # format data
                datapoint = [price, satisfaction]
                datapoints = datapoints + [datapoint]

    return datapoints


def correlation(l):
    """
    correlation(l) finds the correlation coefficient and pvalue for ordered pairs of price, satisfaction data
    :param l: list: list of lists of data points in [price (float), satisfaction (float)] format
    :return: tuple: in (correlation between price + satisfaction, pvalue) format
    """
    # create 2 ordered lists of price and satisfaction data
    price = []
    rating = []
    for elem in l:
        price_point = elem[0]
        satisfaction_point = elem[1]
        price = price + [price_point]
        rating = rating + [satisfaction_point]

    # find correlation
    result = spearmanr(price, rating)
    correlation = result.correlation
    pvalue = result.pvalue

    # format data
    data = (correlation, pvalue)

    return data

def host_listings(filename):
    """
    host_listings creates a dictionary mapping a particular host with all of their listings
    :param filename: str: name of airbnb data file
    :return: dictionary: in {host_id: [listing1, listing2], ...} format
    """
    with open(filename, "r", encoding="utf-8") as file_in:

        # skip header
        header = file_in.readline().split(",")

        # get data set length
        dataset_length = len(header)

        # find indexes for host and room IDs
        host_index = 0
        room_index = 0
        for i in range(dataset_length):
            if header[i] == "host_id":
                host_index = i
            if header[i] == "room_id":
                room_index = i

        # initialize dictionary
        host_dict = {}

        # make data iterable
        for line in file_in:
            data = line.split(",")

            # remove incomplete datasets
            if len(data) == dataset_length:

                # extract host and room data
                host_id = int(data[host_index])
                room_id = int(data[room_index])

                # enter data into dictionary: if host already in dictionary
                if host_id in host_dict.keys():
                    host_dict[host_id] = host_dict[host_id] + [room_id]

                # if host not in dictionary - add
                else:
                    host_dict[host_id] = [room_id]

    return host_dict

def num_listings(d):
    """
    num_listings counts how many hosts have how many listings
    :param d: disctionary: in {host_id: [listing1, listing2], ...} format
    :return: list: list where value for num_list[i] is how many hosts have i listings
    """

    # make a list of how many listings each host has
    num_list = []
    for key in d.keys():
        number = len(d[key])
        num_list = num_list + [number]

    # Find largest integer in list
    largest_integer = 0
    for key in d.keys():
        if len(d[key]) > largest_integer:
            largest_integer = len(d[key])

    # initialize final list
    final_num_list = []
    for i in range(largest_integer + 1):
        final_num_list = final_num_list + [0]

    # count number of listings of each size
    for number in num_list:
        final_num_list[number] = final_num_list[number] + 1

    return final_num_list

def room_prices(filename_list, roomtype):
    """
    room_prices maps listings of a certain type with a ordered list of their price history
    :param filename_list: list: list of airbnb data filenames (str)
    :param roomtype: str: one of â€œEntire home/aptâ€, â€œPrivate roomâ€, â€œShared roomâ€
    :return: dictionary: in { room ID: [oldest price(float), ... newest price(float)] format
    """
    # create dictionary mapping dates(int) to filename(str)
    date_dictionary = {}
    for filename in filename_list:

        # isolate date
        unformatted_date_str = filename[-14: -4]

        # reformat date
        date_str = ""
        for character in unformatted_date_str:
            if character != "-":
                date_str = date_str + character
        date = int(date_str)

        # map filename to date
        date_dictionary[filename] = date

    # sort files by date
    start = 0
    sorted_files = []
    for key in date_dictionary.keys():
        number = date_dictionary[key]

        # add number to end if it is largest yet
        if number >= start:
            sorted_files = sorted_files + [key]
            start = number
            start_key = key

        # if file needs to be placed
        elif number < start:
            stop = 0

            # find where file needs to be inserted
            for i in range(len(sorted_files)):
                if number >= date_dictionary[sorted_files[i]]:
                    stop = i

            for i in range(stop + 1, len(sorted_files)):

                # move files over by one
                sorted_files[i] = sorted_files[i-1]

                # insert file
                sorted_files[stop + 1] = key

                # extend list by one
                sorted_files = sorted_files + [start_key]

                # update start
                start = number
                start_key = key

    # map ID to price
    dictionary = {}
    for filename in sorted_files:
        with open(filename, "r", encoding="utf-8") as file_in:

            # skip header
            header = file_in.readline().split(",")

            # get data set length
            dataset_length = len(header)

            # find indexes for host and room IDs
            for i in range(dataset_length):
                if header[i] == "room_type":
                    room_type_index = i
                if header[i] == "room_id":
                    room_index = i
                if header[i] == "price":
                    price_index = i

            for line in file_in:
                data = line.split(",")

                # remove incomplete data and filter by roomtype
                if len(data) == dataset_length and data[room_type_index] == roomtype:

                    # extract ID and price data
                    ID = int(data[room_index])
                    price = float(data[price_index])

                    # map ID to price: if ID in dictionary already
                    if ID in dictionary.keys():
                        dictionary[ID] = dictionary[ID] + [price]

                    # if ID not in dictionary - add
                    else:
                        dictionary[ID] = [price]
    return dictionary

def price_change(d):
    """
    price_change calculates the maximum percent change for the properties in the data set
    :param d: dictionary: in { room ID: [oldest price(float), ... newest price(float)] format
    :return: tuple: in (max % change (float), starting price of property (float), ending price of property(float)) format
    """

    # calculate percent change
    for key in d.keys():
        first = d[key][0]
        last = d[key][-1]
        percent_change = ((last - first) / first) * 100

        # map property to percent change
        d[key] = d[key] + [percent_change]

    # find highest percent change
    highest_change = 0
    for key in d.keys():
        if d[key][-1] > highest_change:
            highest_change = d[key][-1]

    # find property with highest change
    for key in d.keys():
        if d[key][-1] == highest_change:

            # find earliest and latest price data
            start = d[key][0]
            stop = d[key][-2]

    # format data
    price_data = (highest_change, start, stop)

    return price_data

def price_by_neighborhood(filename):
    """
    price_by_neighborhood maps a neighborhood with the average price of a home there
    :param filename: str: name of airbnb file
    :return: dictionary: in { neighborhood(str): avg price for "Entire home/apt" (float), ...}
    """
    with open(filename, "r", encoding="utf-8") as file_in:

        # skip header
        header = file_in.readline().split(",")

        # get data set length
        dataset_length = len(header)

        # find indexes for host and room IDs
        for i in range(dataset_length):
            if header[i] == "room_type":
                room_type_index = i
            if header[i] == "neighborhood":
                neighborhood_index = i
            if header[i] == "price":
                price_index = i

        # initialize dictionary
        d = {}

        # make data iterable
        for line in file_in:
            data = line.split(",")

            # remove incomplete datasets and filter to onlu Entire home/apt
            if len(data) == dataset_length and data[room_type_index] == "Entire home/apt":

                # extract neighborhood and price date
                neighborhood = data[neighborhood_index]
                price = data[price_index]

                # map neighborhood to price - if neighborhood in dictionary
                if neighborhood in d.keys():
                    d[neighborhood] = d[neighborhood] + [price]

                # if neighborhood not in dictionary - add
                else:
                    d[neighborhood] = [price]

        # calculate average for each key
        for key in d.keys():
            n = len(d[key])
            sum = 0
            for i in range(n):
                sum = sum + float(d[key][i])
            average = (sum / n)

            # map neighborhood to average
            d[key] = average

    return d

def plot_data():
    """
    plot_data makes a bar graph showing how many hosts have how many listings
    :return:
    """
    # make data:
    d = host_listings("tomslee_airbnb_amsterdam_0698_2016-12-15.csv")
    data = (num_listings(d))

    # find len for Y axis
    largest_integer = 0
    for elem in data:
        if elem > largest_integer:
            largest_integer = elem

    # set two ordered lists
    number_hosts = data
    number_rooms = []
    for i in range (len(data)):
        number_rooms = number_rooms + [i]

    x = number_rooms
    y = number_hosts

    # plot
    fig, ax = plt.subplots()

    ax.bar(x, y, width=1, edgecolor="white", linewidth=0.7)

    ax.set(xlim=(0, 10),
           ylim=(0, largest_integer))

    # Set labels
    plt.xlabel("# of listings")
    plt.ylabel("# of hosts")
    plt.title("# of listings per host")

    plt.show()

def main():
    plot_data()

if __name__ == '__main__':
    main()
