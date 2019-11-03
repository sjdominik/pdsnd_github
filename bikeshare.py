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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        try:
            city = input('For which city would you like to see data? Chicago, New York City or Washington?\n').strip().lower()
            if city in ['chicago', 'new york city', 'washington']:
                break
            else:
               print('There is no data about the city "{}". Please enter one of the three cities listed above.'.format(city))
        except KeyboardInterrupt:
            print('\nNo input taken. Please enter one of the three cities listed above.')



    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input('For which month would you like to see data? Enter the full month name.\n').strip().lower()
            if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
                break
            else:
                print('Please enter the name of the month or \'All\' if you don\'t want to filter by month. Don\'t use abreviations.')
        except KeyboardInterrupt:
            print('\nNo input taken. Please enter the name of the month or \'All\' if you don\'t want to filter by month. Don\'t use abreviations.')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input('For which day would you like to see data? Enter the full day name.\n').strip().lower()
            if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
                break
            else:
                print('Please enter the name of the day or \'All\' if you don\'t want to filter by day. Don\'t use abreviations')
        except:
            print('\nNo input taken. Please enter the name of the day or \'All\' if you don\'t want to filter by day. Don\'t use abreviations')

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
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df["hour"] = df["Start Time"].dt.hour
    df['End Time'] = pd.to_datetime(df['End Time'])
    df["hour"] = df["End Time"].dt.hour

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    month_index = int(df['Start Time'].dt.month.mode())
    popular_month = months[month_index - 1]
    print('The most popular month is {}'.format(popular_month))

    # TO DO: display the most common day of week
    popular_weekday = df["day_of_week"].mode()[0]
    print('The most popular day of week is {}'.format(popular_weekday))

    # TO DO: display the most common start hour
    popular_start_hour = df["hour"].mode()[0]
    print("The most common start hour is {}".format(popular_start_hour))

    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df["Start Station"].mode()[0]
    print('The most popular start station is {}'.format(popular_start_station))
    # TO DO: display most commonly used end station
    popular_end_station = df["End Station"].mode()[0]
    print('The most popular end station is {}'.format(popular_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    popular_combination = df.groupby(["Start Station", "End Station"]).size().idxmax()
    print('The most popular combination is {}'.format(' - '.join(popular_combination)))

    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['Trip Duration'] = df['End Time'] - df['Start Time']
    # TO DO: display total travel time
    total_trip_duration = df['Trip Duration'].dt.total_seconds().sum()
    print('The total trip duration is {} seconds'.format(total_trip_duration))

    # TO DO: display mean travel time
    mean_trip_duration = df['Trip Duration'].dt.total_seconds().mean()
    print('The mean trip duration is {} seconds'.format(mean_trip_duration))

    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    type_count = df['User Type'].value_counts()
    print('Here is the number of subscribers and customers:\n{}'.format(type_count))

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print('\nThe gender count is:\n{}'.format(gender_count))
    else:
        print("No gender data to display.")

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_yob = df['Birth Year'].min()
        print('The earliest year of birth is:\n{}'.format(int(earliest_yob)))
        most_recent_yob = df['Birth Year'].max()
        print('The most recent year of birth is:\n{}'.format(int(most_recent_yob)))
        most_common_yob = df['Birth Year'].mode()
        print('The most common year of birth is:\n{}'.format(int(most_common_yob)))
    else:
        print('No birth year data to display.')

    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        see_raw_data = input('Would you like to see 5 rows of raw data? Please enter yes or no.').lower()
        if see_raw_data == 'yes':
            counter = 0
            while True:
                print(df.iloc[counter:counter+5])
                counter += 5
                see_raw_data = input('Would you like to see 5 more rows? Please enter yes or no: ').lower()
                if see_raw_data != 'yes':
                    break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
