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
    # display welcome message to the user
	print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('\nWould you like to see data for Chicago, New York City, or Washington?\nPlease enter your choice...\n\n')
        city = city.lower()
        if city in ['chicago','new york city','washington']:
            break
    # get input for filters
    while True:
        filter = input('\nWould you like to filter the data by month, day, both, or not at all?\nPlease enter your choice..."all" for "not at all"\n\n')
        filter = filter.lower()
        if filter in ['all','both','month','day']:
            break
    if filter == 'both':
        # get user input for month (all, january, february, ... , june)
        while True:
            month = input('\nWhich month - January, February, March, April, May, or June?\nPlease enter your choice...\n\n')
            month = month.lower()
            if month in ['january','february','march','april','may','june']:
                break
        # get user input for day of week (all, monday, tuesday, ... sunday)
        while True:
            day = input('\nWhich day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\nPlease enter your choice...\n\n')
            day = day.lower()
            if day in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']:
                break
    elif filter == 'month':
        day = 'all'
        # get user input for month (all, january, february, ... , june)
        while True:
            month = input('\nWhich month - January, February, March, April, May, or June?\nPlease enter your choice...\n\n')
            month = month.lower()
            if month in ['january','february','march','april','may','june']:
                break
    elif filter == 'day':
        month = 'all'
        # get user input for day of week (all, monday, tuesday, ... sunday)
        while True:
            day = input('\nWhich day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\nPlease enter your choice...\n\n')
            day = day.lower()
            if day in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']:
                break
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

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
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'November', 'December']
    common_month = df['month'].mode()[0]
    print('\nMost Common Month:', months[common_month-1])

    # display the most common day of week
    print('\n\nThe Most Common Day of week:', df['day_of_week'].mode()[0])

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print('\n\nThe Most Common Start Hour:', df['hour'].mode()[0])


    print("\n\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('\nThe Most Common Used Start Station:', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('\n\nThe Most Common Used End Station:', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    frequent_combination_start_end_station = df[['Start Station', 'End Station']].mode().loc[0]
    print("\n\nThe Most Frequent Combination of Start Station and End Station Trip: {}, {}".format(frequent_combination_start_end_station[0], frequent_combination_start_end_station[1]))

    print("\n\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('\nThe Total Travel Time:', df['Trip Duration'].sum())

    # display mean travel time
    print('\n\nThe Mean Travel Time:', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nThe Counts of user types:\n', user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        user_genders = df['Gender'].value_counts()
        print('\nThe Counts of user genders:\n', user_genders)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\nThe Earliest Year of Birth:\n', int(df['Birth Year'].min()))
        print('\nThe Most recent Year of Birth:\n', int(df['Birth Year'].max()))
        print('\nThe Common Year of Birth:\n', int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_rawdata(df):
    # display raw data
    size = 5
    index_length = len(df.index)
    for i in range(0, index_length, size):
        rawdata = input('\nWould you like to see 5 lines of the raw data?\nPlease enter your choice..."yes" or "no"\n\n')
        rawdata = rawdata.lower()
        if rawdata == 'yes':
            subdf = df.iloc[i:i + size]
            print(subdf, "\n")
        if rawdata.lower() == 'no':
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_rawdata(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
