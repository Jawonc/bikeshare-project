from colorama import Fore, Style, init
import pandas as pd
import time
from tabulate import tabulate

# Initialize colorama for colored output
init(autoreset=True)

# Data files
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

from colorama import Fore, Style, init
import pandas as pd
import time

# Initialize colorama
init(autoreset=True)

# Data files
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    """
    print(Fore.YELLOW + "Let’s explore some US bikeshare data!" + Style.RESET_ALL)

    while True:
        city = input(Fore.CYAN + "Enter city (Chicago, New York City, Washington): " + Style.RESET_ALL).strip().lower()
        if city in CITY_DATA:
            break
        else:
            print(Fore.RED + "Invalid input. Choose from ['chicago', 'new york city', 'washington']." + Style.RESET_ALL)

    while True:
        month = input(Fore.CYAN + "Enter month (January, February, ..., June) or 'all': " + Style.RESET_ALL).strip().title()
        if month in ['January', 'February', 'March', 'April', 'May', 'June', 'All']:
            break
        else:
            print(Fore.RED + "Invalid input. Enter a valid month or 'all'." + Style.RESET_ALL)

    while True:
        day = input(Fore.CYAN + "Enter day of week (Monday, Tuesday, ..., Sunday) or 'all': " + Style.RESET_ALL).strip().title()
        if day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']:
            break
        else:
            print(Fore.RED + "Invalid input. Enter a valid day or 'all'." + Style.RESET_ALL)

    print(Fore.GREEN + f"\nFilters applied: City = {city.title()}, Month = {month}, Day = {day}" + Style.RESET_ALL)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'All':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month_index = months.index(month) + 1
        df = df[df['month'] == month_index]

    if day != 'All':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    """
    print(Fore.LIGHTYELLOW_EX + "\nCalculating The Most Frequent Times of Travel..." + Style.RESET_ALL)
    start_time = time.time()

    months = ['January', 'February', 'March', 'April', 'May', 'June']
    most_common_month = months[df['month'].mode()[0] - 1]
    print(Fore.CYAN + f"Most Common Month: {most_common_month}" + Style.RESET_ALL)

    print(Fore.CYAN + f"Most Common Day of the Week: {df['day_of_week'].mode()[0]}" + Style.RESET_ALL)
    print(Fore.CYAN + f"Most Common Start Hour: {df['hour'].mode()[0]}" + Style.RESET_ALL)

    print(Fore.LIGHTCYAN_EX + f"\nThis took {time.time() - start_time:.2f} seconds." + Style.RESET_ALL)
    print("-" * 50)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trips.
    """
    print(Fore.LIGHTYELLOW_EX + "\nCalculating The Most Popular Stations and Trips..." + Style.RESET_ALL)
    start_time = time.time()

    print(Fore.CYAN + f"Most Common Start Station: {df['Start Station'].mode()[0]}" + Style.RESET_ALL)
    print(Fore.CYAN + f"Most Common End Station: {df['End Station'].mode()[0]}" + Style.RESET_ALL)
    df['Start_to_End'] = df['Start Station'] + " to " + df['End Station']
    print(Fore.CYAN + f"Most Common Trip: {df['Start_to_End'].mode()[0]}" + Style.RESET_ALL)

    print(Fore.LIGHTCYAN_EX + f"\nThis took {time.time() - start_time:.2f} seconds." + Style.RESET_ALL)
    print("-" * 50)


def trip_duration_stats(df):
    """
    Displays statistics on total and average trip duration.
    """
    print(Fore.LIGHTYELLOW_EX + "\nCalculating Trip Duration..." + Style.RESET_ALL)
    start_time = time.time()

    print(Fore.CYAN + f"Total Travel Time: {df['Trip Duration'].sum()} seconds" + Style.RESET_ALL)
    print(Fore.CYAN + f"Average Travel Time: {df['Trip Duration'].mean():.2f} seconds" + Style.RESET_ALL)

    print(Fore.LIGHTCYAN_EX + f"\nThis took {time.time() - start_time:.2f} seconds." + Style.RESET_ALL)
    print("-" * 50)


def user_stats(df):
    """
    Displays statistics on bikeshare users.
    """
    print(Fore.LIGHTYELLOW_EX + "\nCalculating User Stats..." + Style.RESET_ALL)
    start_time = time.time()

    try:
        print(Fore.CYAN + "\nCounts of User Types:" + Style.RESET_ALL)
        print(df['User Type'].value_counts())
    except KeyError:
        print(Fore.RED + "User Type data is not available." + Style.RESET_ALL)

    try:
        print(Fore.CYAN + "\nCounts of Gender:" + Style.RESET_ALL)
        print(df['Gender'].value_counts())
    except KeyError:
        print(Fore.RED + "Gender data is not available." + Style.RESET_ALL)

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
    start_row = 0
    while True:
        show_data = input(Fore.CYAN + "\nWould you like to see 5 rows of raw data? Enter yes or no: " + Style.RESET_ALL).strip().lower()
        if show_data == 'yes':
            print(tabulate(df.iloc[start_row:start_row+5], headers='keys', tablefmt='pretty'))
            start_row += 5
            if start_row >= len(df):
                print(Fore.YELLOW + "\nNo more rows to display." + Style.RESET_ALL)
                break
        elif show_data == 'no':
            break
        else:
            print(Fore.RED + "Invalid input. Enter 'yes' or 'no'." + Style.RESET_ALL)

def restart_prompt():
    while True:
        restart = input(Fore.CYAN + "\nWould you like to restart? Enter yes or no: " + Style.RESET_ALL).strip().lower()
        if restart in ['yes', 'no']:
            return restart
        else:
            print(Fore.RED + "Invalid input. Enter 'yes' or 'no'." + Style.RESET_ALL)

def main():
    print(Fore.LIGHTBLUE_EX + "=" * 60)
    print("             Ultimate Bikeshare Explorer.us!")
    print("=" * 60 + Style.RESET_ALL)
    print(Fore.YELLOW + "Analyze bikeshare trends, fun facts, and unique insights.\n" + Style.RESET_ALL)

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if df.empty:
            print(Fore.RED + "No data available for the selected filters. Please try again." + Style.RESET_ALL)
        else:
            display_table(df)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

        if restart_prompt() == 'no':
            print(Fore.LIGHTGREEN_EX + "Thank you for exploring Bikeshare Data! Have a great day!" + Style.RESET_ALL)
            break

if __name__ == "__main__":
    main()






