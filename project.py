import logging
import csv
from datetime import date
from tabulate import tabulate
import matplotlib.pyplot as plt

# Create a logger object, format, and file handler
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('debug.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

logger.info(f'Program Start')


class Routine:
    """Represents a list of exercises input by user"""
    def __init__(self):
        self.exercises = []

    def __str__(self):
        return "self.exercises"

    def add_exercise(self, exercise):
        self.exercises.append(exercise)


class Exercise:
    """Represents an exercise input by user"""
    def __init__(self, person, r_date, routine_type, exercise_name, reps=0, weight=0, sets=0, total_weight=0):
        self.person = person
        self.r_date = r_date
        self.routine_type = routine_type
        self.exercise_name = exercise_name
        self.reps = reps
        self.weight = weight
        self.sets = sets
        self.total_weight = total_weight

    def __str__(self):
        return f"{self.exercise_name} {self.reps} {self.weight} {self.sets} {self.total_weight}"

    @property
    def person(self):
        return self._person

    @person.setter
    def person(self, person):
        self._person = person

    @property
    def r_date(self):
        return self._r_date

    @r_date.setter
    def r_date(self, r_date):
        self._r_date = r_date

    @property
    def routine_type(self):
        return self._routine_type

    @routine_type.setter
    def routine_type(self, routine_type):
        self._routine_type = routine_type

    @property
    def exercise_name(self):
        return self._exercise_name

    @exercise_name.setter
    def exercise_name(self, exercise_name):
        self._exercise_name = exercise_name

    @property
    def reps(self):
        return self._reps

    @reps.setter
    def reps(self, reps):
        if type(reps) is not int or reps < 0:
            raise ValueError("Reps not non-negative integer")
        self._reps = reps

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, weight):
        if type(weight) is not int or weight < 0:
            raise ValueError("Weight not non-negative integer")
        self._weight = weight

    @property
    def sets(self):
        return self._sets

    @sets.setter
    def sets(self, sets):
        if type(sets) is not int or sets < 0:
            raise ValueError("Sets not non-negative integer")
        self._sets = sets

    @property
    def total_weight(self):
        return self._total_weight

    @total_weight.setter
    def total_weight(self, total_weight):
        if type(total_weight) is not int or total_weight < 0:
            raise ValueError("Total_weight not non-negative integer")
        self._total_weight = total_weight


def main():
    """Start of Main Program"""
    user_interface()


def user_interface():
    """Command Line user interface"""
    print("--- Welcome to Mike's Workout Tracker Python Project ---\n")
    while True:
        show_main_menu()
        user_selection = input('Enter your choice: ')
        if user_selection == '1':
            print('Start new workout routine')
            routine = Routine()
            routine = create_routine(routine)
        elif user_selection == '2':
            print('Load workout from file')
            print()
            f = input('Enter filename to load: ')
            try:
                routine = read_routine_file(f)
            except FileNotFoundError as e:
                print(f"Error - File not found: {f}", e)
        elif user_selection == '3':
            print('Display workout')
            print()
            try:
                print_routine(routine)
            except UnboundLocalError as e:
                print("No routine loaded or entered - Chose option 1 or 2 first", e)

        elif user_selection == '4':
            print('Update routine')
            try:
                p = routine.exercises[0].person
                d = routine.exercises[0].r_date
                t = routine.exercises[0].routine_type
                routine = get_exercise_input(routine, p, d, t)
            except UnboundLocalError as e:
                print("No routine loaded or entered - Chose option 1 or 2 first", e)

        elif user_selection == '5':
            print('Display weight progress over time chart')
            print()
            n = input('Enter the name of the person: ').lower()
            e = input('Enter to name of the exercise to plot: ').lower()
            plot_data = get_plot_data(routine, n, e)
            print(plot_data)
            draw_chart(plot_data, n, e)

        elif user_selection == '6':
            print('Save workout to file')
            print()
            f = input('Enter filename to save: ')
            try:
                write_routine_file(routine, f)
            except UnboundLocalError as e:
                print("No routine loaded or entered - Chose option 1 or 2 first", e)
        elif user_selection == '7':
            print('Exiting...')
            break
        else:
            print("Invalid choice. Please try again.")


def show_main_menu():
    """Display the main menu"""
    print('\nMain Menu:')
    print('1. Start new workout routine')
    print('2. Load workout from file')
    print('3. Display workout routine on screen')
    print('4. Add to workout routine')
    print('5. Plot weight over time')
    print('6. Save workout routine to file')
    print('7. Exit')


def create_routine(r):
    """Get routine info from user"""
    print()
    person = input('Enter the name of the person: ').lower()
    my_date = date.today()
    routine_type = input('Enter the type of routine: ').lower()

    r = get_exercise_input(r, person, my_date, routine_type)
    return r


def get_exercise_input(r, p, d, t):
    """Get exercise data from user"""

    while True:
        selection = input("Press enter to add an exercise or 'e' to exit ")
        if selection == 'e':
            break
        else:
            exercise_name = input('Enter the name of the exercise: ').lower()
            reps = int(input('Enter the number of reps: '))
            weight = int(input('Enter the weight: '))
            sets = int(input('Enter number of sets: '))
            total_weight = calc_total(reps, weight, sets)
            ex = Exercise(p, d, t, exercise_name, reps, weight, sets, total_weight)
            r.add_exercise(ex)
    return r


def calc_total(r, w, s):
    """Calculates the total weight lifted"""
    return int(r*w*s)


def read_routine_file(filename):
    """Load data from file into Routine object"""

    with open(filename, mode='r', encoding='utf-8') as file:
        my_routine = None
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        my_routine = Routine()
        for row in reader:
            person, r_date, routine_type, exercise_name, reps, weight, sets, total_weight = row
            ex = Exercise(person, r_date, routine_type, exercise_name, int(reps), int(weight), int(sets), int(total_weight))
            my_routine.add_exercise(ex)
        logger.info(f'Portfolio file: {filename} read into memory.')
        return my_routine


def print_routine(r):
    """Print routine data in table format"""
    header_list = ['Name', 'Date', 'Routine', 'Exercise', 'Reps', 'Weight', 'Sets', 'Total Weight']
    table_data = []
    for exercise in r.exercises:
        table_data.append([exercise.person, exercise.r_date, exercise.routine_type, exercise.exercise_name, exercise.reps, exercise.weight, exercise.sets, exercise.total_weight])
    print(tabulate(table_data, header_list, tablefmt="orgtbl"))


def get_plot_data(r, n, e):
    """Get data to plot weight"""
    e_dates = []
    weights = []
    for exercise in r.exercises:
        if exercise.person == n and exercise.exercise_name == e:
            e_dates.append(exercise.r_date)
            weights.append(exercise.weight)
    return [e_dates, weights]


def draw_chart(d, n, e):
    """Draws a chart of weight lifted over time"""
    fig, ax = plt.subplots()
    ax.plot(d[0], d[1], linewidth=3)
    # Format chart
    ax.set_title(f"{n.title()}'s {e.title()} Weight Over Time", fontsize=14)
    ax.set_xlabel("Date", fontsize=14)
    ax.set_ylabel("Weight in Pounds", fontsize=14)
    ax.tick_params(labelsize=14)
    plt.show()


def write_routine_file(r, filename):
    """Create csv file of the routine and exercises"""

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Date', 'Routine', 'Exercise', 'Reps', 'Weight', 'Sets', 'Total Weight'])
        for exercise in r.exercises:
            writer.writerow([exercise.person, exercise.r_date, exercise.routine_type, exercise.exercise_name, exercise.reps, exercise.weight, exercise.sets, exercise.total_weight])
    logger.info(f'Workout file: {filename} written to drive.')


if __name__ == "__main__":
    main()

# class Jar:
#     def __init__(self, capacity=12, size=0):
#         self.capacity = capacity
#         self.size = size
#
#     def __str__(self):
#         return "🍪" * self.size
#
#     def deposit(self, n):
#         self.size += n
#         if self.size > self.capacity:
#             raise ValueError("Too many cookies for capacity")
#
#
#     def withdraw(self, n):
#         self.size -= n
#         if self.size < 0:
#             raise ValueError("Not enough cookies to withdraw")
#
#     @property
#     def capacity(self):
#         return self._capacity
#
#     @capacity.setter
#     def capacity(self, capacity):
#         if type(capacity) != int or capacity < 0:
#             raise ValueError("Capacity not non-negative integer")
#         self._capacity = capacity
#
#     @property
#     def size(self):
#         return self._size
#
#     @size.setter
#     def size(self, size):
#         self._size = size






# from datetime import datetime
#
# # Get the current date and time
# current_time = datetime.now()
#
# # Access individual components
# print("Year:", current_time.year)
# print("Month:", current_time.month)
# print("Day:", current_time.day)
# print("Hour:", current_time.hour)
# print("Minute:", current_time.minute)
# print("Second:", current_time.second)
#
#
#
# from datetime import datetime
# now = datetime.now()
# current_time = now.strftime("%H:%M:%S")
# print("Current Time =", current_time)
#
#
# from datetime import date
#
# current_date = date.today()
# print(current_date)  # Output: YYYY-MM-DD (e.g., 2024-08-02)


#
# from tabulate import tabulate
#
# # Example data
# teams_list = ["Man Utd", "Man City", "T Hotspur"]
# data = [
#     [1, 0, 0],
#     [1, 1, 0],
#     [0, 1, 2]
# ]
#
# # Print the table
# print(tabulate(data, headers=teams_list, tablefmt='orgtbl'))
# print(tabulate(table, headers, tablefmt="outline"))