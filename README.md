# CPSC408 Assignment1
# Alanna Sayer
# Professor German
# Files:
- main.py (application)
- students.csv (original data file)

# main.py
- This file displays the user and all their attributes. It allows the user to search by student, or various attributes such as GPA, major,city, and advisor. Also permits user to add or delete students in the database; it performs a soft delete. The code also enables the user to update existing students details. For adding, updating, or deleting students, it takes further input from the user, such as the students' details or the ID of the student to be deleted. After each insert or update, it commits the transaction to save the changes to the database.
The prompts are clear, simple, and user friendly so that people of all backgrounds, education levels, etc. can easily manipulate it. 

- I included the table creation of student inside here as well. If checks if the table is created. If it is not created then the script will run. If it is created, then it will be ignoted. 