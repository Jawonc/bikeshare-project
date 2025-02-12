from colorama import Fore, Style, init
import pandas as pd
import time
from tabulate import tabulate  # For tabular display of raw data

# Initialize colorama for colored output
init(autoreset=True)

# Data files mapping
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day to filter by, or "all" to apply no day filter
    """
    print(Fore.YELLOW + "Let’s explore some US bikeshare data!" + Style.RESET_ALL)

    # Get city input
    while True:
        city = input(Fore.CYAN + "Enter city (Chicago, New York City, Washington): " + Style.RESET_ALL).strip().lower()
        if city in CITY_DATA:
            break
        print(Fore.RED + "Invalid input. Please choose from ['chicago', 'new york city', 'washington']." + Style.RESET_ALL)

    # Get month input
    while True:
        month = input(Fore.CYAN + "Enter month (January, February, ..., June) or 'all': " + Style.RESET_ALL).strip().title()
        if month in ['January', 'February', 'March', 'April', 'May', 'June', 'All']:
            break
        print(Fore.RED + "Invalid input. Enter a valid month or 'all'." + Style.RESET_ALL)

    # Get day input
    while True:
        day = input(Fore.CYAN + "Enter day of week (Monday, Tuesday, ..., Sunday) or 'all': " + Style.RESET_ALL).strip().title()
        if day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']:
            break
        print(Fore.RED + "Invalid input. Enter a valid day or 'all'." + Style.RESET_ALL)

    print(Fore.GREEN + f"\nFilters applied: City = {city.title()}, Month = {month}, Day = {day}" + Style.RESET_ALL)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    """
    # Load city data
    df = pd.read_csv(CITY_DATA[city])

    # Convert Start Time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month
    if month != 'All':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month_index = months.index(month) + 1
        df = df[df['month'] == month_index]

    # Filter by day
    if day != 'All':
        df = df[df['day_of_week'] == day]

    return df

def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    """
    print(Fore.LIGHTYELLOW_EX + "\nCalculating The Most Frequent Times of Travel..." + Style.RESET_ALL)
    start_time = time.time()

    # Display the most common month
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    most_common_month = months[df['month'].mode()[0] - 1]
    print(Fore.CYAN + f"Most Common Month: {most_common_month}" + Style.RESET_ALL)

    # Display the most common day
    most_common_day = df['day_of_week'].mode()[0]
    print(Fore.CYAN + f"Most Common Day: {most_common_day}" + Style.RESET_ALL)

    # Display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print(Fore.CYAN + f"Most Common Start Hour: {most_common_hour}" + Style.RESET_ALL)

    print(Fore.LIGHTCYAN_EX + f"\nThis took {time.time() - start_time:.2f} seconds." + Style.RESET_ALL)
    print("-" * 50)

def station_stats(df):
    """
    Displays statistics on the most popular stations and trips.
    """
    print(Fore.LIGHTYELLOW_EX + "\nCalculating The Most Popular Stations and Trips..." + Style.RESET_ALL)
    start_time = time.time()

    # Display most common start station
    most_common_start_station = df['Start Station'].mode()[0]
    print(Fore.CYAN + f"Most Common Start Station: {most_common_start_station}" + Style.RESET_ALL)

    # Display most common end station
    most_common_end_station = df['End Station'].mode()[0]
    print(Fore.CYAN + f"Most Common End Station: {most_common_end_station}" + Style.RESET_ALL)

    # Display most common trip
    df['Start_to_End'] = df['Start Station'] + " to " + df['End Station']
    most_common_trip = df['Start_to_End'].mode()[0]
    print(Fore.CYAN + f"Most Common Trip: {most_common_trip}" + Style.RESET_ALL)

    print(Fore.LIGHTCYAN_EX + f"\nThis took {time.time() - start_time:.2f} seconds." + Style.RESET_ALL)
    print("-" * 50)

def trip_duration_stats(df):
    """
    Displays statistics on total and average trip duration.
    """
    print(Fore.LIGHTYELLOW_EX + "\nCalculating Trip Duration..." + Style.RESET_ALL)
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    print(Fore.CYAN + f"Total Travel Time: {total_travel_time} seconds" + Style.RESET_ALL)

    average_travel_time = df['Trip Duration'].mean()
    print(Fore.CYAN + f"Average Travel Time: {average_travel_time:.2f} seconds" + Style.RESET_ALL)

    print(Fore.LIGHTCYAN_EX + f"\nThis took {time.time() - start_time:.2f} seconds." + Style.RESET_ALL)
    print("-" * 50)

def user_stats(df):
    """
    Displays statistics on bikeshare users.
    """
    print(Fore.LIGHTYELLOW_EX + "\nCalculating User Stats..." + Style.RESET_ALL)
    start_time = time.time()

    # Display counts of user types
    print(Fore.CYAN + "\nCounts of User Types:" + Style.RESET_ALL)
    print(df['User Type'].value_counts())

    # Display counts of gender
    try:
        print(Fore.CYAN + "\nCounts of Gender:" + Style.RESET_ALL)
        print(df['Gender'].value_counts())
    except KeyError:
        print(Fore.RED + "Gender data is not available." + Style.RESET_ALL)

    # Display birth year stats
    try:
        print(Fore.CYAN + "\nBirth Year Stats:" + Style.RESET_ALL)
        print(f"Earliest Year: {int(df['Birth Year'].min())}")
        print(f"Most Recent Year: {int(df['Birth Year'].max())}")
        print(f"Most Common Year: {int(df['Birth Year'].mode()[0])}")
    except KeyError:
        print(Fore.RED + "Birth Year data is not available." + Style.RESET_ALL)

    print(Fore.LIGHTCYAN_EX + f"\nThis took {time.time() - start_time:.2f} seconds." + Style.RESET_ALL)
    print("-" * 50)

def display_table(df):
    """
    Displays raw data in a tabular format, 5 rows at a time.
    """
    start_row = 0
    while True:
        show_data = input(Fore.CYAN + "\nWould you like to see 5 rows of raw data? Enter yes or no: " + Style.RESET_ALL).strip().lower()
        if show_data == 'yes':
            print(tabulate(df.iloc[start_row:star
