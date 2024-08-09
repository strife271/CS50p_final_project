import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

# Global list to store workout data
workout_data = []


def open_form():
    # Create a new window for the form
    form_window = tk.Toplevel(root)
    form_window.title("Workout Data Entry")

    def submit_data():
        name = entry_name.get()
        date = entry_date.get()
        exercise_type = entry_exercise_type.get()
        weight = entry_weight.get()
        sets = entry_sets.get()
        reps = entry_reps.get()

        # Store the data in the global workout_data list
        workout_data.append({
            "Name": name,
            "Date": date,
            "Exercise Type": exercise_type,
            "Weight": weight,
            "Sets": sets,
            "Reps": reps
        })

        # Ask the user if they want to submit another form
        if messagebox.askyesno("Data Submitted",
                               "Your workout data has been submitted! Do you want to submit another form?"):
            clear_form()  # Clear the form for new entry
        else:
            form_window.destroy()  # Close the form window

    def clear_form():
        # Clear all the entry fields
        entry_name.delete(0, tk.END)
        entry_date.delete(0, tk.END)
        entry_exercise_type.delete(0, tk.END)
        entry_weight.delete(0, tk.END)
        entry_sets.delete(0, tk.END)
        entry_reps.delete(0, tk.END)

    # Create labels and entry fields for each data point
    label_name = tk.Label(form_window, text="Name:")
    label_name.grid(row=0, column=0, padx=10, pady=5)
    entry_name = tk.Entry(form_window)
    entry_name.grid(row=0, column=1, padx=10, pady=5)

    label_date = tk.Label(form_window, text="Date (YYYY-MM-DD):")
    label_date.grid(row=1, column=0, padx=10, pady=5)
    entry_date = tk.Entry(form_window)
    entry_date.grid(row=1, column=1, padx=10, pady=5)

    label_exercise_type = tk.Label(form_window, text="Exercise Type:")
    label_exercise_type.grid(row=2, column=0, padx=10, pady=5)
    entry_exercise_type = tk.Entry(form_window)
    entry_exercise_type.grid(row=2, column=1, padx=10, pady=5)

    label_weight = tk.Label(form_window, text="Weight (lbs):")
    label_weight.grid(row=3, column=0, padx=10, pady=5)
    entry_weight = tk.Entry(form_window)
    entry_weight.grid(row=3, column=1, padx=10, pady=5)

    label_sets = tk.Label(form_window, text="Sets:")
    label_sets.grid(row=4, column=0, padx=10, pady=5)
    entry_sets = tk.Entry(form_window)
    entry_sets.grid(row=4, column=1, padx=10, pady=5)

    label_reps = tk.Label(form_window, text="Reps:")
    label_reps.grid(row=5, column=0, padx=10, pady=5)
    entry_reps = tk.Entry(form_window)
    entry_reps.grid(row=5, column=1, padx=10, pady=5)

    # Create a submit button
    submit_button = tk.Button(form_window, text="Submit", command=submit_data)
    submit_button.grid(row=6, column=0, columnspan=2, pady=10)


def save_data():
    with open("workout_data.txt", "w") as file:
        for entry in workout_data:
            file.write(
                f"{entry['Name']},{entry['Date']},{entry['Exercise Type']},{entry['Weight']},{entry['Sets']},{entry['Reps']}\n")
    messagebox.showinfo("Save Data", "Workout data has been saved successfully!")


def show_chart():
    if not workout_data:
        messagebox.showwarning("Show Chart", "No data available to show.")
        return

    exercise_types = [entry['Exercise Type'] for entry in workout_data]
    weights = [int(entry['Weight']) for entry in workout_data]

    plt.bar(exercise_types, weights, color='blue')
    plt.xlabel('Exercise Type')
    plt.ylabel('Weight (lbs)')
    plt.title('Weight Lifted by Exercise Type')
    plt.show()


def print_data():
    if not workout_data:
        messagebox.showwarning("Print Data", "No data available to print.")
        return

    print("Workout Data:")
    for entry in workout_data:
        print(
            f"Name: {entry['Name']}, Date: {entry['Date']}, Exercise Type: {entry['Exercise Type']}, Weight: {entry['Weight']} lbs, Sets: {entry['Sets']}, Reps: {entry['Reps']}")
    messagebox.showinfo("Print Data", "Workout data has been printed to the console.")


def exit_program():
    root.quit()


# Create the main window (parent form)
root = tk.Tk()
root.title("Workout Tracker Main Menu")

# Create buttons for each menu option
button_open_form = tk.Button(root, text="Open Form", command=open_form)
button_open_form.grid(row=0, column=0, padx=20, pady=10)

button_save_data = tk.Button(root, text="Save Data", command=save_data)
button_save_data.grid(row=1, column=0, padx=20, pady=10)

button_show_chart = tk.Button(root, text="Show Chart", command=show_chart)
button_show_chart.grid(row=2, column=0, padx=20, pady=10)

button_print_data = tk.Button(root, text="Print Data", command=print_data)
button_print_data.grid(row=3, column=0, padx=20, pady=10)

button_exit_program = tk.Button(root, text="Exit Program", command=exit_program)
button_exit_program.grid(row=4, column=0, padx=20, pady=10)

# Run the main event loop
root.mainloop()
