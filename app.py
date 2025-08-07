class Student:
    def __init__(self):
        # Initialize student with an empty name, marks list, and average
        self.name = ""
        self.m1 = 0
        self.m2 = 0
        self.m3 = 0
        self.rn = 0
        self.average = 0.0
        self.grade = ''
        self.subjects = ['Maths', 'English', 'Science']
        self.marks = [self.m1, self.m2, self.m3]

    def average_marks(self, m1, m2, m3):
        return (m1 + m2 + m3) / 3
    
    # Calculate grade based on average marks
    def calculate_grade(self, average):
        if average >= 90:
            return 'A+'
        elif average >= 80:
            return 'A'
        elif average >= 70:
            return 'B'
        elif average >= 60:
            return 'C'
        elif average >= 50:
            return 'D'
        elif average >= 40:
            return 'E'
        else:
            return 'F'

    # Obtain student details and calculate average marks and grade
    def obtain(self): 
        print("Please enter the student's name:")
        self.name = input("Name: ")
        print("Please enter the marks for three subjects:")
        
        # Add extra subjects
        option = input("Would you like to add more subjects? (y/n): ")
        while option.lower() == 'y':
            subject = input("Enter the subject name: ")
            if subject not in self.subjects:
                self.subjects.append(subject)
                print(f"Subject {subject} added successfully.")
            else:
                print(f"Subject {subject} already exists.")
            option = input("Would you like to add another subject? (y/n): ")

        # Prompt for marks for each subject
        for subject in self.subjects:
            while True:
                try:
                    mark = int(input(f"Subject {subject}: "))
                    if 0 <= mark <= 100:
                        self.marks.append(mark)
                        break
                    else:
                        print(f"Invalid marks for {subject}. Please enter a value between 0 and 100.")
                except ValueError:
                    print(f"Invalid input. Please enter an integer value for {subject}.")
          
        while True:
                try:
                    p = int(input(f"Enter roll number: "))
                    if 0 <= self.rn <= 100:
                        self.rn = p
                        break
                    else:
                        print(f"Invalid format for roll number. Please enter a value between 0 and 100.")
                except ValueError:
                    print(f"Invalid input. Please enter an integer value for roll number.")

        self.average = self.average_marks(self.m1, self.m2, self.m3)    
        self.grade = self.calculate_grade(self.average)
        return self.name, self.m1, self.m2, self.m3, self.average, self.rn

def main():
    student = Student()
    student.obtain()
    print("********************************")
    print(f"Student Name: {student.name}")
    print(f"Marks: {student.m1}, {student.m2}, {student.m3}")
    print(f"Average Marks: {student.average}")
    print(f"Grade: {student.grade}")
    print(f"Roll number: {student.rn}")
    option = input("Would you like to enter another student's details? (y/n)")
    while option.lower() == 'y':
        main()
    else:
        print("Thank you for using the Student Results System!")

if __name__ == '__main__':
    main()
