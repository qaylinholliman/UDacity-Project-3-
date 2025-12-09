import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

#provide syntax for multiple cities, if not all##

def load_data(city=None, month=None, day=None):
    """load x with input and return a dataframe considering filter"""
    while True:
        try:
            city = input("Enter a city (Chicago, New York City, Washington): ").lower()
        except(KeyError, ValueError):
            print("invalid input")
        if city not in CITY_DATA:
            print("City not found.")
            return None
        else:
            break

    filename = CITY_DATA[city]
    df = pd.read_csv(filename)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name().str.lower()
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()

    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

    while month not in months:
        month = input("Enter a month (January - June) (or 'all'): ").lower()
        if month not in months:
            print("Invalid input. Please try again.")

    if month != 'all':
        df = df[df['month'] == month]

    while day not in days:
        day = input("Enter a day of the week or 'all': ").lower()
        if day not in days:
            print("Invalid input. Please try again.")

        if day != 'all':
            df = df[df['day_of_week'] == day]

    index = 0
    while True:
        raw_data = input('\nWould you like to see the first five lines of raw data? Enter yes or no.\n')
        if raw_data.lower() != 'yes':
            break
        else:
            print(df.iloc[index:index + 5])
            index += 5
        if index >= len(df):
            print("end of dataset.")
    return df, city

#you can define time_stats a little better#
def time_stats(df):
    """present time of travel considering new columns created"""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['hour'] = df['Start Time'].dt.hour

    popular_hour = df['hour'].mode()[0]
    popular_dow = df['day_of_week'].mode()[0]
    pop_month = df['month'].mode()[0]

    print("Popular Hour:", popular_hour)
    print("Day of the week:", popular_dow)
    print("popular month:", pop_month)

    print("\nThis took %s seconds." % (time.time() - start_time))
    return df


def station_stats(df):
    """Print stations most frequent and combos of stations"""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    popular_start_station = df['Start Station'].mode()[0]
    popular_end_station = df['End Station'].mode()[0]
    combo_stations = (popular_start_station, popular_end_station)[0]

    print("Popular start station is:", popular_start_station, "Popular end station is:", popular_end_station,
          "Best combo:", combo_stations)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)
    return df


def trip_duration_stats(df):
    """State trip duration in seconds, including the averages"""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    trip_total = df['Trip Duration'].sum()
    trip_mean = df['Trip Duration'].mean()

    print("Trip Total in seconds:", trip_total)
    print("Trip Average in seconds:", trip_mean)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)
    return df


def user_stats(df, city):
    """Provide general user statistics including birth and gender"""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    user = pd.Series(data=df["User Type"])
    user_types = user.value_counts()
    print("user type:", user_types)
    if city in ['new york city', 'chicago']:
        gender = pd.Series(data=df["Gender"])
        birth = df["Birth Year"]
        g = gender.value_counts()
        print("user type:", user_types, "\ngender:", g)
        print("First:", birth.iloc[1], "\nLatest:", birth.iloc[-1], "\nMost common:", birth.mode()[0])
    else:
        print("nothing to output")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)
    return df


def main():
    """run all functions listed below and ask (via input) to restart the process"""
    while True:
        df, city = load_data()
        time_stats(df)

        station_stats(df)

        trip_duration_stats(df)

        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

#this is the bookmark to make changes to code#
