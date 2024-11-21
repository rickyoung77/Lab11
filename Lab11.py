import matplotlib
import matplotlib.pyplot as plt
import os

# Force Matplotlib to use the TkAgg backend for interactive plotting
matplotlib.use('TkAgg')

# Helper function to read and process the students.txt file
def read_students_file(file_path):
    """Reads the students file and extracts IDs and names."""
    data = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            student_id = int(line[:3])  # First three characters are the ID
            student_name = line[3:].strip()  # Rest is the name
            data[student_id] = student_name
    return data

# Helper function to read and process the assignments.txt file
def read_assignments_file(file_path):
    """Reads the assignments file and extracts assignments with their IDs and point values."""
    assignments = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 3):  # Process every 3 lines
            name = lines[i].strip()  # Assignment name
            id_ = int(lines[i + 1].strip())  # Assignment ID
            points = int(lines[i + 2].strip())  # Point value
            assignments[id_] = (name, points)
    return assignments

# Function to read all submissions from a folder
def read_submissions_folder(folder_path):
    """Reads all submission files in the folder and aggregates the data."""
    submissions = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):  # Only process files
            with open(file_path, 'r') as file:
                for line in file:
                    parts = line.strip().split('|')  # Split by '|'
                    if len(parts) == 3:  # Ensure the file has the expected format
                        student_id = int(parts[0])
                        assignment_id = int(parts[1])
                        score = float(parts[2])
                        submissions.append((student_id, assignment_id, score))
    return submissions

# Function to load all data
def load_data():
    """Load all data from the files."""
    # Process the students file
    students = read_students_file('data/students.txt')

    # Process the assignments file
    assignments = read_assignments_file('data/assignments.txt')

    # Process the submissions folder
    submissions = read_submissions_folder('data/submissions')

    return students, assignments, submissions

# Function to calculate a student's grade
def calculate_student_grade(student_name, students, assignments, submissions):
    """Calculates the total grade for a specific student."""
    student_id = next((id_ for id_, name in students.items() if name == student_name), None)
    if not student_id:
        return "Student not found"
    total_points = sum(
        assignments[assign_id][1] * (score / 100)
        for student, assign_id, score in submissions
        if student == student_id
    )
    return f"{round((total_points / 1000) * 100)}%"

# Function to calculate assignment statistics
def calculate_assignment_stats(assignment_name, assignments, submissions):
    """Calculates min, max, and average scores for a specific assignment."""
    assign_id = next((id_ for id_, (name, _) in assignments.items() if name == assignment_name), None)
    if not assign_id:
        return "Assignment not found"
    scores = [score for _, assign, score in submissions if assign == assign_id]
    return f"Min: {min(scores)}%\nAvg: {sum(scores) / len(scores):.2f}%\nMax: {max(scores)}%"

# Function to plot a histogram of assignment scores
def plot_assignment_histogram(assignment_name, assignments, submissions):
    """Plots a histogram for a specific assignment."""
    assign_id = next((id_ for id_, (name, _) in assignments.items() if name == assignment_name), None)
    if not assign_id:
        return "Assignment not found"
    scores = [score for _, assign, score in submissions if assign == assign_id]

    plt.figure()  # Create a new figure
    plt.hist(scores, bins=[50, 60, 70, 80, 90, 100], edgecolor='black')
    plt.title(f"Histogram of Scores for {assignment_name}")
    plt.xlabel("Score Range")
    plt.ylabel("Number of Students")
    plt.show(block=True)  # Open the plot in a new window
    return None

# Main program
def main():
    # Load the data
    students, assignments, submissions = load_data()

    # Display the menu
    print("1. Student grade\n2. Assignment statistics\n3. Assignment graph\n")
    selection = input("Enter your selection: ").strip()

    # Handle user selection
    if selection == "1":
        student_name = input("What is the student's name: ").strip()
        print(calculate_student_grade(student_name, students, assignments, submissions))
    elif selection == "2":
        assignment_name = input("What is the assignment name: ").strip()
        print(calculate_assignment_stats(assignment_name, assignments, submissions))
    elif selection == "3":
        assignment_name = input("What is the assignment name: ").strip()
        result = plot_assignment_histogram(assignment_name, assignments, submissions)
        if result:
            print(result)
    else:
        print("Invalid selection.")

# Run the program
if __name__ == "__main__":
    main()

