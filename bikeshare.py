import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

INPUT_DATA = {
    'input city': "Which city's data would you want to explore? \n\n "
        "1. Chicago \n "
        "2. New York \n "
        "3. Washington \n",
    'input month': "Which month's data would you want to explore? \n\n "
        "0. All Months \n"
        "1. January \n "
        "2. February \n "
        "3. March \n"
        "4. April \n"
        "5. May \n"
        "6. June \n",
    'input day': "Which day's data would you want to explore? \n\n"
        "0. All Days \n"
        "1. Monday \n"
        "2. Tuesday \n"
        "3. Wednesday \n"
        "4. Thursday \n"
        "5. Friday \n"
        "6. Saturday \n"
        "7. Sunday \n"
}

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

    cities = ['chicago', 'new york city', 'washington']

    city_no = get_valid_selected_item(
        INPUT_DATA['input city'],
        "Enter the city's no: ",
        ['1','2','3'],
        "Reply with either number 1, 2 or 3 to choose city\n"
    )

    city = cities[city_no - 1]
    print("Awesome, let's explore {}'s data \n\n".format(cities[city_no - 1].title()))

    # get user input for month (all, january, february, ... , june)

    month_no = get_valid_selected_item(
        INPUT_DATA['input month'],
        "Enter the month's no: ",
        ['0','1','2','3','4','5','6'],
        "Reply with the month number 0, 1, 2, 3, 4, 5 or 6 \n"
    )

    month = month_no
    print("You chose {} \n\n".format(months[month_no].title()))

    # get user input for day of week (all, monday, tuesday, ... sunday)

    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    
    day_no = get_valid_selected_item(
        INPUT_DATA['input day'],
        "Enter the day's no: ",
        ['0','1','2','3','4','5','6','7'],
        "Reply with the day number 0, 1, 2, 3, 4, 5, 6 or 7 \n"
    )

    day = days[day_no]
    print("You chose {}".format(days[day_no].title()))

    print('-'*40)
    return city, month, day

def get_valid_selected_item(info, prompt_message, options, options_message):
    """
    Computes the selected item from user input and validates it

    Args:
        (str) info - a message of what is expected by the user
        (str) promt_message - a message to prompt the user to input data
        (list) options - list to select from
        (str) options_message - validation message

    Returns:
        selected - The selected item from the provided list
    """

    print(info)
    selected = input(prompt_message)
    while selected not in options:
        selected = input(options_message)

    selected = int(selected)
    return selected


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
    
    df['Month'] = df['Start Time'].dt.month
    df['Day Of Week'] = df['Start Time'].dt.weekday_name
    
    if month != 0:
        df = df[df['Month'] == month]
        
    if day != 'all':
        df = df[df['Day Of Week'] == day.title()]
    
    return df

def most_common(value_count):
    """Returns the most common item in the value_count"""
    common_no = 0
    common = ''
    for i, value in value_count.items():
        if value > common_no:
            common_no = value
            common = i

    return common

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Most common month: ', months[int(df['Month'].mode())].title())

    # display the most common day of week
    days_of_week_count = df['Day Of Week'].value_counts()
    print('Most common day of the week: ', most_common(days_of_week_count))

    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    print('Most common start hour: ', int(df['Hour'].mode()))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station_count = df['Start Station'].value_counts()
    print('Most commonly used start station: ', most_common(start_station_count))
    
    # display most commonly used end station
    end_station_count = df['End Station'].value_counts()
    print('Most commonly used end station: ', most_common(end_station_count))
    
    # display most frequent combination of start station and end station trip
    df['Start End Combination'] = df['Start Station'] + ' - ' + df['End Station'] 
    combination_count = df['Start End Combination'].value_counts()
    print('Most frequent combination of start station and end station trip: ', most_common(combination_count))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time: ', df['Trip Duration'].sum())

    # display mean travel time
    print('Mean travel time: ', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types, '\n\n')

    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print(gender, '\n\n')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('Earliest year of birth: ', int(df['Birth Year'].min()))
        print('Most recent year of birth: ', int(df['Birth Year'].max()))
        print('Most common year of birth: ', int(df['Birth Year'].mode()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_raw_data(city):
    """Interactively displays raw data to the user."""

    explore = input('Do you want to see 5 lines of raw data? Enter yes or no.\n')
    while explore.lower() != 'yes' and explore.lower() != 'no':
        explore = input('Do you want to see 5 lines of raw data? Enter yes or no.\n')

    if explore.lower() == 'no':
        return

    df = pd.read_csv(CITY_DATA[city], sep=',', chunksize=5)

    for chunk in df:
        print(chunk)

        more = input('View 5 more lines? Enter yes or no.\n')
        while more.lower() != 'yes' and more.lower() != 'no':
            more = input('View 5 more lines? Enter yes or no.\n')
        
        if more.lower() == 'no':
            break



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_raw_data(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
