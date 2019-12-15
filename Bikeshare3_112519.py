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
    print('Hello! Let\'s explore some US bikeshare data!')


    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Which city would you like to review, type:  chicago, new york or washington").title()
    while city not in ['Chicago', 'New York', 'Washington']:
        city = input("Try Again...which city would you like to review, type:  chicago, new york or washington").title()
    # get user input for month (all, january, february, ... , june)
    month = input("What months would you like to analyze: all, january, february, march, april, may, or june").title()
    while month not in ['All', 'January', 'February','March','April','May','June']:
        month = input("Try Again...What months would you like to analyze: all, january, february, march, april, may, or june").title()
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("What day would you like to analyze:  all, monday, tuesday, wednesday, thursday, friday, saturday, or sunday").title()
    while day not in ['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
        day = input("Try again....What day would you like to analyze:  all, monday, tuesday, wednesday, thursday, friday, saturday, or sunday").title()

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
    if city == "New York":
        city_file = 'new_york_city'
    elif city == "Chicago":
        city_file = 'chicago'
    elif city == "Washington":
        city_file = 'washington'
    df = pd.read_csv("{}.csv".format(city_file))

    # converting Start and End time to datetime and create new columns for month and day of week
    # strftime('%A') yields the day of the week
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].apply(lambda x: x.month)
    df['day_of_week'] = df['Start Time'].apply(lambda x: x.strftime('%A'))

    if month != 'All':
        months = ['January','February','March','April','May','June']
        month = months.index(month) + 1

        df = df.loc[df['month'] == month,:]

    if day != 'All':
        df = df.loc[df['day_of_week'] == day,:]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print("The most common month is: {}".format(str(df['month'].mode().values[0])))

    # TO DO: display the most common day of week
    print("The most common day of the week is: {}".format(str(df['day_of_week'].mode().values[0])))

    # TO DO: display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    print("The most common start hour: {}".format(str(df['start_hour'].mode().values[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("The most common start station is: {}".format(df['Start Station'].mode().values[0]))

    # TO DO: display most commonly used end station
    print("The most common end station is: {}".format(df['End Station'].mode().values[0]))

    # TO DO: display most frequent combination of start station and end station trip
    df['multi_leg'] = df['Start Station']+ ' ' + df['End Station']
    print("The most common start and end station combination is: {}".format(df['multi_leg'].mode().values[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    df['duration'] = df['End Time'] - df['Start Time']
    print("The total travel time is: {}".format(str(df['duration'].sum())))

    # TO DO: display mean travel time
    print("The mean travel time is: {}".format(str(df['duration'].mean())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print(df['User Type'].value_counts())

    # TO DO: Display counts of gender
    if city != 'Washington':
        print(df['Gender'].value_counts())


    # TO DO: Display earliest, most recent, and most common year of birth
        print("The earliest birth year is: {}".format(str(int(df['Birth Year'].min()))))
        print("The latest birth year is: {}".format(str(int(df['Birth Year'].max()))))
        print("The most common birth year is: {}".format(str(int(df['Birth Year'].mode().values[0]))))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_lines(df):
    """Displays five lines of data based on user input."""
    input_lines = input("Do you want to see the raw data?: yes or no ")
    if input_lines == "yes":
        start_line = 0
        end_line = 5
        while end_line <= df.shape[0]-1:
            print(df.iloc[start_line:end_line,:])
            start_line += 5
            end_line +=5
            input_lines_two = input("Do you want another five lines of data?: yes or no ")
            if input_lines_two == 'no':
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_lines(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
