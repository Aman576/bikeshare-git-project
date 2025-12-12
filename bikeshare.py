import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        city (str): name of the city to analyze
        month (str): name of the month to filter by, or "all" to apply no month filter
        day (str): name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")

    # asking the user for the city and repeating until a valid name is entered
    while True:
        city = input("Please choose a city (Chicago, New York City, Washington): ").strip().lower()
        if city in CITY_DATA:
            break
        print("That doesn't look right. Please try again.")

    # list of valid months (project uses only Jan to June)
    valid_months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input("Enter a month (Jan–Jun) or 'all': ").strip().lower()
        if month in valid_months:
            break
        print("Invalid month. Try again.")

    # asking for day of week
    valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                  'saturday', 'sunday', 'all']
    while True:
        day = input("Enter a day of the week or 'all': ").strip().lower()
        if day in valid_days:
            break
        print("Invalid day. Please enter a proper weekday name.")

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        city (str): name of the city
        month (str): name of the month to filter by, or "all"
        day (str): name of the day of week to filter by, or "all"

    Returns:
        df (DataFrame): Pandas DataFrame containing filtered city data
    """

    # reading the CSV file for the city chosen
    df = pd.read_csv(CITY_DATA[city])

    # converting the Start Time column so that we can extract month, day, hour later
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # adding extra columns that will help with filtering and statistics
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour

    # Apply month filter if user did not choose 'all'
    if month != 'all':
        month_index = ['january', 'february', 'march', 'april', 'may', 'june'].index(month) + 1
        df = df[df['month'] == month_index]

    # Apply day-of-week filter if user did not choose 'all'
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Shows the most common time values based on the filtered data."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # most common month (as a number)
    common_month = df['month'].mode()[0]
    print("Most common month:", common_month)

    # most common weekday
    common_day = df['day_of_week'].mode()[0]
    print("Most common day of week:", common_day.title())

    # most common hour of the day to start a trip
    common_hour = df['hour'].mode()[0]
    print("Most common start hour:", common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays the most commonly used stations and the most frequent trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # finding the station that appears most often as a start station
    start_station = df['Start Station'].mode()[0]
    print("Most common start station:", start_station)

    # finding the end station used most frequently
    end_station = df['End Station'].mode()[0]
    print("Most common end station:", end_station)

    # creating a combined trip to find the most popular route
    df['trip'] = df['Start Station'] + " -> " + df['End Station']
    common_trip = df['trip'].mode()[0]
    print("Most frequent trip:", common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # summing up the trip durations of all trips
    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time:", total_travel_time)

    # calculating the mean trip duration
    average_travel_time = df['Trip Duration'].mean()
    print("Average travel time:", average_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics about the users, including types and demographics."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # user types such as Subscriber or Customer
    print("User Types:\n", df['User Type'].value_counts(), "\n")

    # Gender column may not exist for Washington dataset
    if 'Gender' in df.columns:
        print("Gender breakdown:\n", df['Gender'].value_counts(), "\n")
    else:
        print("Gender information is not available for this dataset.\n")

    # Birth Year column likewise only exists for Chicago and NYC
    if 'Birth Year' in df.columns:
        print("Earliest birth year:", int(df['Birth Year'].min()))
        print("Most recent birth year:", int(df['Birth Year'].max()))
        print("Most common birth year:", int(df['Birth Year'].mode()[0]))
    else:
        print("Birth year data unavailable for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_separator():
    """Prints a clean separator line for improved readability."""
    print('-' * 60)


def main():
    """
    Main controller function for the Bikeshare program.
    Handles user input, loads filtered data,
    and calls all statistical analysis functions.
    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        display_separator()

        station_stats(df)
        display_separator()

        trip_duration_stats(df)
        display_separator()

        user_stats(df)
        display_separator()

        # ask if the user wants to see raw data 5 rows at a time
        index = 0
        while True:
            show_raw = input("Would you like to see 5 rows of raw data? (yes/no): ").strip().lower()
            if show_raw != 'yes':
                break
            print(df.iloc[index:index + 5])
            index += 5
            if index >= len(df):
                print("No more data to display.")
                break

        # restarting the entire program
        restart = input("\nWould you like to restart? (yes/no): ").strip().lower()
        if restart != 'yes':
            break


if __name__ == "__main__":
    main()
