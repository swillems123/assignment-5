# Helper function to convert month abbreviation to month number
def month_str_to_num(month_str):
    months = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
        'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
    }
    return months.get(month_str, 0)

# Function to parse date strings formatted as 'Mon DD, YYYY'
def parse_date(date_str):
    """Parse a date string formatted as 'Mon DD, YYYY' and return a tuple (year, month, day)."""
    try:
        parts = date_str.split()
        month = month_str_to_num(parts[0])
        day = int(parts[1].strip(','))
        year = int(parts[2])
        return year, month, day
    except (IndexError, ValueError):
        return None

# Function to check if a year is a leap year
def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

# Function to calculate the number of days in a given month of a given year
def days_in_month(year, month):
    if month in {1, 3, 5, 7, 8, 10, 12}:
        return 31
    elif month in {4, 6, 9, 11}:
        return 30
    elif month == 2:
        return 29 if is_leap_year(year) else 28
    return 0

# Function to calculate the number of days since January 1, 1900
def days_since_1900(year, month, day):
    """Calculate the number of days since January 1, 1900."""
    days = 0
    for y in range(1900, year):
        days += 366 if is_leap_year(y) else 365
    for m in range(1, month):
        days += days_in_month(year, m)
    days += day - 1
    return days

# Function to find the longest running animes
def longest_running_animes(file_path):
    animes = []

    with open(file_path, 'r') as file:
        # Skip the header line
        header = file.readline().strip().split(',')

        for line in file:
            fields = []
            field = ''
            in_quotes = False

            for c in line:
                if c == ',' and not in_quotes:
                    fields.append(field.strip())
                    field = ''
                elif c == '"':
                    in_quotes = not in_quotes
                else:
                    field += c
            fields.append(field.strip())

            if len(fields) < 5:
                continue  # Skip if not enough columns

            name = fields[0]
            aired = fields[4].strip('"')  # Remove quotes if present

            # Check if the 'aired' field contains a date range
            if ' to ' in aired:
                start_str, end_str = aired.split(' to ')
                start_date = parse_date(start_str.strip())
                end_date = parse_date(end_str.strip())
                if start_date is None or end_date is None:
                    continue  # Skip if date parsing fails

                start_days = days_since_1900(*start_date)
                end_days = days_since_1900(*end_date)
                duration = end_days - start_days

                if duration < 0:
                    continue  # Skip if end date is before start date

                animes.append((duration, name))
            else:
                continue  # Skip if 'aired' does not contain a date range

    # Sort the animes by duration in descending order and get the top 10
    top_10_animes = sorted(animes, key=lambda x: x[0], reverse=True)[:10]

    # Return the names of the top 10 longest running animes
    return [anime[1] for anime in top_10_animes]

# Example usage
file_path = r"C:\Users\sethw\Downloads\new folder\toprankedanime.csv"
top_10_longest_running_animes = longest_running_animes(file_path)
print(top_10_longest_running_animes)