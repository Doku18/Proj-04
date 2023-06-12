import pylab

def do_plot(x_vals, y_vals, year):
    pylab.xlabel('Income')
    pylab.ylabel('Cumulative Percent')
    pylab.title("Cumulative Percent for Income in " + str(year))
    pylab.plot(x_vals, y_vals)
    pylab.show()

def open_file(): #opens the file for the given year
    while True:
        year_str = input("\nEnter a year where 1990 <= year <= 2023: ")
        try:
            year = int(year_str)
            if 1990 <= year <= 2023:
                return year
            print("\nError: Invalid year. Please try again.")
        except ValueError:
            print("\nError: Invalid year. Please try again.")

def read_file(fp): #reads the text files for the given year
    data_lst = []
    for line in fp:
        columns = line.strip().split()  # Split line into columns
        if len(columns) >= 8 and all(column.replace('.', '', 1).isdigit() for column in columns):
            data_lst.append([float(column) for column in columns])
    return data_lst

def find_average(data_lst): #finds the average salary for the year provided from the data
    if not data_lst:
        return 0
    total_income = sum(data[6] for data in data_lst)
    return total_income / len(data_lst)

def find_median(data_lst): #finds the median from the year and data provided
    target_percent = 0.5
    sorted_data = sorted(data_lst, key=lambda x: x[5])  # Sort data by cumulative percentage

    for data in sorted_data:
        if data[5] >= target_percent:
            return data[7]

    return 0

def get_range(data_lst, percent):
    target_percent = percent / 100

    sorted_data = sorted(data_lst, key=lambda x: x[5])  # Sort data by cumulative percentage

    for data in sorted_data:
        if data[5] >= target_percent:
            salary_range = (data[0], data[2])
            cumulative_percent = data[5]
            average_income = data[7]
            return salary_range, cumulative_percent, average_income

    return None

def get_percent(data_lst, income):
    for data in data_lst:
        if data[0] <= income <= data[2]:
            income_range = (data[0], data[2])
            cumulative_percent = data[5]
            return income_range, cumulative_percent

    return None

def main():
    year = open_file()
    filename = "year{}.txt".format(year)
    
    try:
        with open(filename) as fp:
            data_lst = read_file(fp)
    except FileNotFoundError:
        print("\nError: File '{}' not found. Please try again.".format(filename))
        return

    avg = find_average(data_lst)
    median = find_median(data_lst)

    print("\n{:6s}{:15s}{:15s}".format("Year", "Mean", "Median"))
    print("{:<6d}${:<14,.2f}${:<14,.2f}".format(year, avg, median))

    response = input("\nDo you want to plot values (yes/no)? ")
    if response.lower() == 'yes':
        x_vals = [data[0] for data in data_lst[:40]]
        y_vals = [data[5] for data in data_lst[:40]]
        do_plot(x_vals, y_vals, year)

    while True:
        choice = input("\nEnter a choice to get (r)ange, (p)ercent, or nothing to stop: ")
        if not choice:
            break
        elif choice.lower() == 'r':
            percent_str = input("Enter a percentage (0-100): ")
            try:
                percent = float(percent_str)
                if 0 <= percent <= 100:
                    result = get_range(data_lst, percent)
                    if result is not None:
                        low, high = result[0]
                        print("Range for {:.2f}%: ${:,.2f} - ${:,.2f}".format(percent, low, high))
                    else:
                        print("Error: No data line found for the given percentage.")
                else:
                    print("Error: Invalid percentage. Please try again.")
            except ValueError:
                print("Error: Invalid percentage. Please try again.")
        elif choice.lower() == 'p':
            income_str = input("Enter an income: $")
            try:
                income = float(income_str)
                if income < 0:
                    print("Error: Income must be positive.")
                    continue
                result = get_percent(data_lst, income)
                if result is not None:
                    percent = result[1]
                    print("Percentage of incomes below ${:,.2f}: {:.2f}%".format(income, percent))
                else:
                    print("Error: No data line found for the given income.")
            except ValueError:
                print("Error: Invalid income. Please try again.")
        else:
            print("Error: Invalid selection.")

if __name__ == "__main__":
    main()