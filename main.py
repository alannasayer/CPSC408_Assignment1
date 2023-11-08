import sqlite3
import csv
import requests
#import_data_from_csv()

#generate_csv()
#database_operations()

conn = sqlite3.connect('/Users/alannasayer/Desktop/Fall 2023/CPSC 408/PythonApp/identifier.sqlite')
my_cursor = conn.cursor()

my_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Student'")
table_exists = my_cursor.fetchone()


if not table_exists:
    create_table_query = '''
    CREATE TABLE Student (
        StudentId INTEGER PRIMARY KEY,
        FirstName TEXT,
        LastName TEXT,
        GPA REAL,
        Major TEXT,
        FacultyAdvisor TEXT,
        Address TEXT,
        City TEXT,
        State TEXT,
        ZipCode TEXT,
        MobilePhoneNumber TEXT,
        isDeleted INTEGER
    )
    '''
    my_cursor.execute(create_table_query)
    conn.commit()


with open("/Users/alannasayer/Desktop/Fall 2023/CPSC 408/PythonApp/students.csv") as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        FirstName = row['FirstName']
        LastName = row['LastName']
        MobilePhoneNumber = row['MobilePhoneNumber']
        Address = row['Address']
        City = row['City']
        State = row['State']
        ZipCode = row['ZipCode']
        Major = row['Major']
        GPA = row['GPA']

        # Check if student already exists
        my_cursor.execute("SELECT * FROM Student WHERE FirstName=? AND LastName=? AND MobilePhoneNumber=?",
                          (FirstName, LastName, MobilePhoneNumber))
        exists = my_cursor.fetchone()

        if not exists:
            my_cursor.execute(
                "INSERT INTO Student ('FirstName', 'LastName', 'GPA', 'Major', 'Address', 'City', 'State', 'ZipCode', 'MobilePhoneNumber', 'isDeleted') "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                (FirstName, LastName, GPA, Major, Address, City, State, ZipCode, MobilePhoneNumber, 0)
            )
            conn.commit()
print('Data import complete.')



# boolean to keep track of if user wants to continue
keep_going = True
while keep_going == True:
    print('What option would you like to execute:')
    print('1) Show all students and all of their attributes')
    print('2) Add new students')
    print('3) Update students')
    print('4) Delete students by StudentId')
    print('5) Search/Display students by Major, GPA, City, State, and Advisor')
    print('6) Exit')

    while True:
        user_input = input("Enter a number between 1 and 6: ")

        try:
            x = float(user_input)
            if 1 <= x < 6:
                break  # Exit the loop if a valid number is entered
            elif x == 6:
                keep_going = False
                break
            else:
                print("Invalid input. Please enter a number between 1 and 6.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Display all students and their attributes if user_input equals 1
    if x == 1:
        # Execute SELECT statement to retrieve all records from Student table
        my_cursor.execute("SELECT * FROM Student")
        all_rows = my_cursor.fetchall()

        # Print each row to standard output
        for student in all_rows:
            print(student)

    # Add new students if user_input equals 2
    if x == 2:
        first_name = input('Enter First Name: ')
        last_name = input('Enter Last Name: ')

        # Prompt for GPA and validate the input format
        while True:
            gpa = input('Enter GPA (format example: 4 or 4.0): ')
            if gpa.replace('.', '', 1).isdigit():
                break
            else:
                print("Invalid GPA. Please use the format 4 or 4.0.")

        major = input('Enter Major: ')
        faculty_advisor = input('Enter Faculty Advisor: ')
        address = input('Enter Address: ')
        city = input('Enter City: ')

        # Validate the state input against a list of valid states
        while True:
            state = input('Enter State: ').lower()
            if state in ["alabama", "alaska","arizona", "arkansas", "california",
                            "colorado", "connecticut", "delaware", "florida", "georgia",
                            "hawaii", "idaho", "illinois", "indiana", "iowa", "kansas",
                            "kentucky", "louisiana", "maine", "maryland", "massachusetts",
                            "michigan", "minnesota", "mississippi", "missouri", "montana",
                            "nebraska", "nevada", "new hampshire", "new jersey",
                            "new mexico", "new york", "north carolina", "north dakota",
                            "ohio", "oklahoma", "oregon", "pennsylvania", "rhode island",
                            "south carolina", "south dakota", "tennessee", "texas", "utah",
                            "vermont", "virginia", "washington", "west virginia",
                            "wisconsin", "wyoming"]:
                break
            else:
                print("Invalid state. Please enter a correct state name.")

        # Ensure the zip code is a valid 5-digit number
        while True:
            zipcode = input('Enter a 5-digit Zip Code: ')
            if zipcode.isdigit() and len(zipcode) == 5:
                break
            else:
                print("Invalid zip code. A valid zip code has 5 digits.")

        phone_number = input('Enter Mobile Phone Number: ')
        is_deleted = 0

        # Insert the new student record into the database
        my_cursor.execute(
            "INSERT INTO Student (FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber, isDeleted) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
            (first_name, last_name, gpa, major, faculty_advisor, address, city, state, zipcode, phone_number,
             is_deleted))

        # Commit the transaction to the database
        conn.commit()

        print('New student has been added successfully.')
        print(' ')

    # if user_input = 3 update students
    if x == 3:
        valid_fields = ["Major", "Advisor", "Phone Number"]
        print("You can update the following fields: " + ", ".join(valid_fields))
        for i, field in enumerate(valid_fields, 1):
            print(f"{i}) {field}")

        # Get user input for the field to update
        while True:
            user_choice = input("Select a field to update (1-3): ")
            try:
                choice_index = int(user_choice)
                if 1 <= choice_index <= 3:
                    break
                else:
                    print("Please enter a number between 1 and 3.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        # Ask for the student ID
        while True:
            student_id_input = input("Enter the student ID for the update: ")
            try:
                student_id = int(student_id_input)
                # Confirm existence of studentID in the database
                my_cursor.execute("SELECT * FROM Student WHERE studentID = ?", (student_id,))
                if my_cursor.fetchone():
                    break
                else:
                    print(f"Student ID {student_id} not found.")
            except ValueError:
                print("Please enter a valid student ID.")

        # Updating the chosen field
        if choice_index == 1:
            new_value = input("Enter the new major: ")
            my_cursor.execute("UPDATE Student SET Major = ? WHERE StudentID = ?", (new_value, student_id))
            print("Major has been updated successfully.")

        if choice_index == 2:
            new_value = input("Enter the new advisor: ")
            my_cursor.execute("UPDATE Student SET FacultyAdvisor = ? WHERE StudentID = ?", (new_value, student_id))
            print("Advisor has been updated successfully.")

        if choice_index == 3:
            new_value = input("Enter the new phone number: ")
            my_cursor.execute("UPDATE Student SET MobilePhoneNumber = ? WHERE StudentID = ?", (new_value, student_id))
            print("Phone number has been updated successfully.")

        conn.commit()

    if x == 4:
        # Deleting a student by ID
        while True:
            student_id_to_delete = input("Enter the StudentID of the student to delete: ")
            try:
                student_id = int(student_id_to_delete)
                # Check for the student's existence before deletion
                my_cursor.execute("SELECT * FROM Student WHERE studentID = ?", (student_id,))
                if my_cursor.fetchone():
                    break
                else:
                    print(f"Student ID {student_id} not found.")
            except ValueError:
                print("Please enter a valid student ID.")

        # Soft delete the student
        my_cursor.execute("UPDATE Student SET isDeleted = 1 WHERE StudentID = ?", (student_id,))
        conn.commit()

    if x == 5:
        # Display students by various criteria
        search_options = ["Major", "GPA", "City", "State", "Advisor"]
        print("Search for students by:")
        for index, option in enumerate(search_options, 1):
            print(f"{index}) {option}")

        # Get user input for search criteria
        while True:
            search_choice = input("Enter a number (1-5) to choose a search criterion: ")
            try:
                search_index = int(search_choice)
                if 1 <= search_index <= 5:
                    break
                else:
                    print("Invalid input! Choose a number between 1 and 5.")
            except ValueError:
                print("Invalid input! Enter a number.")

        # Perform the search based on user input
        if search_index == 1:
            my_cursor.execute("SELECT DISTINCT Major FROM Student")
            majors = [row[0] for row in my_cursor.fetchall()]
            search_major = input("Enter the major to search for: ")
            query = "SELECT * FROM Student WHERE Major = ? AND isDeleted = 0"

        elif search_index == 2:
            search_gpa = input("Enter the GPA to search for: ")
            query = "SELECT * FROM Student WHERE GPA = ? AND isDeleted = 0"

        elif search_index == 3:
            search_city = input("Enter the city to search for: ")
            query = "SELECT * FROM Student WHERE City = ? AND isDeleted = 0"

        elif search_index == 4:
            search_state = input("Enter the state to search for: ")
            query = "SELECT * FROM Student WHERE State = ? AND isDeleted = 0"

        elif search_index == 5:
            search_advisor = input("Enter the advisor to search for: ")
            query = "SELECT * FROM Student WHERE FacultyAdvisor = ? AND isDeleted = 0"

        my_cursor.execute(query, (locals()[f"search_{search_options[search_index - 1].lower()}"],))
        for student in my_cursor.fetchall():
            print(student)



# Close the connection
conn.close()
#my_cursor.close()








