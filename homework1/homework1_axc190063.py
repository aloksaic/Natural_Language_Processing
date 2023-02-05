# Homework 1
# Aloksai Choudari

import sys  # To get the system parameter
import re
import pickle
import pathlib


# Person class with values and display method
class Person:
    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

    # Display method for employee info
    def display(self):
        print('Employee id:', self.id)
        print('\t', self.first, self.mi, self.last)
        print('\t', self.phone)


# Function for processing the data file
def process_lines(employees):
    # Checks for the correct file path
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
        quit()

    # Open file for reading on operating systems'
    # rel_path = sys.argv[1]
    # with open(pathlib.Path.cwd().joinpath(rel_path), 'r') as f:
    #     line = f.read().splitlines()

    # Open the file input for reading
    f = open(str(sys.argv[1]), 'r')
    # Ignore heading line
    line = f.readline()

    # Read in one line at a time
    while True:
        line = f.readline().strip()
        # Checks for the end of line
        if not line:
            break

        # Split the comma in the line
        temp = line.split(',')

        # Capitalize the first letter of names
        temp[0] = temp[0].capitalize()
        temp[1] = temp[1].capitalize()

        # Check for a middle initial in each name
        if len(temp[2]) != 1:
            temp[2] = 'X'

        # Checks the ID
        while re.match('[A-Za-z][A-Za-z]\d{4}', temp[3]) == None:
            print('ID invalid: ', temp[3])
            print('ID is two letters followed by 4 digits')
            temp[3] = input('Please enter a valid id: ')

        # Checks the phone number
        while re.match('\w{3}-\w{3}-\w{4}', temp[4]) == None:
            print('Phone', temp[4], 'is invalid')
            print('Enter phone number in form 123-456-7890')
            temp[4] = input('Enter phone number: ')

        # Put information into a dictionary
        employee = Person(temp[0], temp[1], temp[2].capitalize(), temp[3], temp[4])
        employees[temp[3]] = employee


# Main function
if __name__ == '__main__':
    employees = {}
    process_lines(employees)

    # Pickle the employees
    pickle.dump(employees, open('employees.pickle', 'wb'))

    # Read the pickle back in
    employees_in = pickle.load(open('employees.pickle', 'rb'))

    print('\nEmployee list:')
    for employee in employees:
        employees[employee].display()
