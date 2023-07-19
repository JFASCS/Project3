#Imported Libraries

import time
import pandas as pd
import numpy as np
from datetime import timedelta

####################################


CITY_DATA = { 'chicago': r"C:\Users\FRIE354\OneDrive - Arvato Supply Chain Solutions\Desktop\Udacity\Python\Bikeshare_Data\DATA\chicago.csv",
              'new york city': r"C:\Users\FRIE354\OneDrive - Arvato Supply Chain Solutions\Desktop\Udacity\Python\Bikeshare_Data\DATA\new_york_city.csv",
              'washington': r"C:\Users\FRIE354\OneDrive - Arvato Supply Chain Solutions\Desktop\Udacity\Python\Bikeshare_Data\DATA\washington.csv" }
accepted_city_values = {'chicago','new york city', 'washington'}
accepted_month_values = {'1','2','3','4','5','6','7','8','9','10','11','12','all'}
accepted_day_values = {'1','2','3','4','5','6','7','all'}
accepted_filter_values = {'1', '2', '3', '4'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = str(input('Would you like to see data for Chicago, New York City, or Washington?\n')).lower()
        except ValueError:
            print("Sorry, I didn\'t understand you.")
            continue
        if city not in accepted_city_values:
            print("I don't have information to ", city, ". Possible inputs are Chicago, New York City or Washington.")
            continue
        else:
            break


    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            global choiceOfFilter
            choiceOfFilter = input('Please insert the number of your choice! \n Would you like to filter the data by \n [1] month \n [2] day \n [3] not at all \n [4] see raw data \n')
        except ValueError:
            print("Sorry, I didn\'t understand you.")
        if choiceOfFilter not in accepted_filter_values:
            print('\n Please type only the numbers 1, 2, 3 or 4.')
            continue
        else:
            break

    if choiceOfFilter == '1':
        while True:
            try:
                month = str(input('Please insert the number of the month (1-12) you wan\'t to investigate or all for all months. \n')).lower()
            except ValueError:
                print("Sorry, I didn\'t understand you.")
                continue
            if month not in accepted_month_values:
                print("I don't have information to ", month, ". Possible inputs:", sorted(accepted_month_values))
                continue
            else:
                day = 'all'
                break

    elif choiceOfFilter == '2':
    # get user input for day of week (all, monday, tuesday, ... sunday)

        while True:
            try:
                day = str(input('Please insert the number of the day (1-7) you wan\'t to investigate or all for all days. \n')).lower()
            except ValueError:
                print("Sorry, I didn\'t understand you.")
                continue
            if day not in accepted_day_values:
                print("I don't have information to ", day, ". Possible inputs:", sorted(accepted_day_values))
                continue
            else:
                month = 'all'
                break

    elif choiceOfFilter == '4':
        month = 'all'
        day = 'all'

    else:
        month = 'all'
        day = 'all'

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    

    if month != 'all':
        df = df[(df['Start Time'].dt.month == int(month))]

    if day != 'all':
        df = df[(df['Start Time'].dt.dayofweek == (int(day)-1))]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if 'Start Time' in df:
        df['YearMonth'] = df['Start Time'].dt.strftime('%m/%Y')
        countsYearMonth = df.groupby(['YearMonth']).size()
        print('The most common month is', countsYearMonth.idxmax())
   


    # display the most common day of week
    if 'Start Time' in df:
        df['Day'] = df['Start Time'].dt.strftime('%A')
        countsDay = df.groupby(['Day']).size()
        print('The most common day is', countsDay.idxmax())

    # display the most common start hour
    if 'Start Time' in df:
        df['Hour'] = df['Start Time'].dt.strftime('%H')
        countsHour = df.groupby(['Hour']).size()
        print('The most common hour is', countsHour.idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    if 'Start Station' in df:
        countsStartStation = df['Start Station'].value_counts().idxmax()
        print('The most common Start Station is ' + countsStartStation)

    # display most commonly used end station
    if 'End Station' in df:
        countsEndStation = df['End Station'].value_counts().idxmax()
        print('The most common End Station is ' + countsEndStation)

    # display most frequent combination of start station and end station trip
    if 'End Station' in df and 'Start Station' in df:
        df['StartEndStation'] = df['Start Station'] + ' to ' + df['End Station']
        countsStationCombination = df['StartEndStation'].value_counts().idxmax()
        print('The most common combination of start station and end station is ' + countsStationCombination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    if 'Trip Duration' in df:
        totalTravelTime = timedelta(seconds = int(df['Trip Duration'].sum()))
        print('The total travel time was ' + str(totalTravelTime))

    # display mean travel time
    if 'Trip Duration' in df:
        meanTravelTime = timedelta(seconds = int(df['Trip Duration'].mean()))
        print('The mean travel time was ' + str(meanTravelTime))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df:
        countsUserType = df['User Type'].value_counts()
        print((countsUserType))

    # Display counts of gender
    if 'Gender' in df:
        countsGender = df['Gender'].value_counts()
        print(countsGender)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print('The earliest year of birth is ' + str(df['Birth Year'].min()))
        print('The most recent birth year is ' + str(df['Birth Year'].max()))
        print('The most common year of birth is ' + str(df['Birth Year'].value_counts().idxmax()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    number_of_rows = 6
    while True:
        try:
            print(df.head(number_of_rows))
            morerows = str(input('Do you want to see more data? Please type yes or no.\n'))
        except ValueError:
            print("Sorry, I didn\'t understand you.")
            continue
        if morerows == 'yes':
            number_of_rows = number_of_rows + 5
            continue
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if len(df.index) == 0:
            print('No values. Lets try again')
        
        elif choiceOfFilter == '4':
            raw_data(df)
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
