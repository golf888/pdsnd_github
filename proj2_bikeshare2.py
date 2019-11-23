import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('-'*40)
    print('\n')
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city_input = input("Would you like to see data for Chicago, New York City, or Washington? Please choose a city name: ")
        if city_input.lower() in ['chicago', 'new york city', 'washington']:
            city = city_input.lower()
            break
        else:
            print("Please choose a valid option for a city.")
            continue
    # get user input for month (all, january, february, ... , june)
    while True:
        month_input = input('Are you interested in a specific month or all months (enter "all" for all months)? ')
        if month_input.lower() in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            month = month_input.lower()
            break
        else:
            print("Please choose a valid option of all, January, February, March, April, May, or June. \n")
            continue


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day_input = input('Are you interested in a specific day of week or all days (enter "all" for all days)? ')
        if day_input.lower() in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            day = day_input
            break
        else:
            print('Please choose a valid option of all, Monday, Tuesday, Wednesday, Thursday or Friday. \n')
            continue

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # extract hour from Start Time to create new columns
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month is: ", df['month'].mode()[0])

    # display the most common day of week
    print("The most common day is: ", df['day_of_week'].mode()[0])

    # display the most common start hour
    print("The most common start hour is: ", df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used start station is: ", df['Start Station'].mode()[0])

    # display most commonly used end station
    print("The most commonly used end station is: ", df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    pair_counts = df.groupby(['Start Station', 'End Station']).size().reset_index(name = "Count")
    print("The most frequent combination of start station and end station trip is: \n", pair_counts[pair_counts["Count"] == pair_counts["Count"].max()])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total travel time is ', df['Trip Duration'].sum())

    # display mean travel time
    print('The mean travel time is ', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The counts of user types are: \n', df.dropna(axis = 0, subset = ['User Type'])['User Type'].value_counts().to_frame())
    print('\n')
    # Display counts of gender
    if 'Gender' in df.columns:
        print('The counts of gender are: \n', df.dropna(axis = 0, subset = ['Gender'])['Gender'].value_counts().to_frame())

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\n')
        print('The earliest rider year of birth is: ', int(df.dropna(axis = 0, subset = ['Birth Year'])['Birth Year'].min()))
        print('The most recent rider year of birth is: ', int(df.dropna(axis = 0, subset = ['Birth Year'])['Birth Year'].max()))
        print('The most common year of birth is: ', int(df.dropna(axis = 0, subset = ['Birth Year'])['Birth Year'].mode()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data_review(df):
    """Displays raw data 5 lines at a time based on the request."""
    print('\n')
    print('-'*40)

    # get user input for review the raw data 5 lines at a time
    read_raw = input("Would you like to see the raw data? Answer yes or no: ")
    if read_raw.lower() == 'yes':
        f_length = 0
        while f_length < len(df):
            if len(df) - f_length < 5:
                print(df[f_length:])
            else:
                print(df[f_length:f_length+5])
                read_more = input("Continue? Answer yes or no: ")
                if read_more.lower() == 'yes':
                    print('\n')
                    f_length += 5
                    continue
                else:
                    break
    return None

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data_review(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
