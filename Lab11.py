import matplotlib
matplotlib.use('Agg')  # Use the headless Agg backend
import matplotlib.pyplot as plt
import os

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

def read_assignments_file(file_path):
    """Reads the assignments file and extracts assignments with their IDs and point values."""
    assignments = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 3):
            name = lines[i].strip()
            id_ = int(lines[i + 1].strip())
            points = int(lines[i + 2].strip())
            assignments[id_] = (name, points)
    return assignments

def read_submissions_folder(folder_path):
    """Reads all submission files in the folder and aggregates the data."""
    submissions = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                for line in file:
                    parts = line.strip().split('|')
                    if len(parts) == 3:
                        student_id = int(parts[0])
                        assignment_id = int(parts[1])
                        score = float(parts[2])
                        submissions.append((student_id, assignment_id, score))
    return submissions

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
    percentage = round((total_points / 1000) * 100)
    return f"{percentage}%"

def calculate_assignment_stats(assignment_name, assignments, submissions):
    """Calculates min, max, and average scores for a specific assignment."""
    assign_id = next((id_ for id_, (name, _) in assignments.items() if name == assignment_name), None)
    if not assign_id:
        return "Assignment not found"
    
    # Extract scores for the given assignment ID
    scores = [score for _, assign, score in submissions if assign == assign_id]
    if not scores:
        return "No submissions found for this assignment."

    # Calculate min, average, and max
    min_score = round(min(scores))  # Round to nearest whole number
    avg_score = round(sum(scores) / len(scores))  # Round the average
    max_score = round(max(scores))  # Round to nearest whole number

    # Format the output
    return f"Min: {min_score}%\nAvg: {avg_score}%\nMax: {max_score}%"

def plot_assignment_histogram(assignment_name, assignments, submissions):
    """Plots a histogram for a specific assignment."""
    assign_id = next((id_ for id_, (name, _) in assignments.items() if name == assignment_name), None)
    if not assign_id:
        return "Assignment not found"
    scores = [score for _, assign, score in submissions if assign == assign_id]

    plt.figure()
    plt.hist(scores, bins=[50, 60, 70, 80, 90, 100], edgecolor='black')
    plt.title(f"Histogram of Scores for {assignment_name}")
    plt.xlabel("Score Range")
    plt.ylabel("Number of Students")
    file_name = f"{assignment_name}_histogram.png"
    plt.savefig(file_name)  # Save the plot to a file
    print(f"Plot saved as '{file_name}'")
    return None

def main():
    students = read_students_file('data/students.txt')
    assignments = read_assignments_file('data/assignments.txt')
    submissions = read_submissions_folder('data/submissions')

    print("1. Student grade\n2. Assignment statistics\n3. Assignment graph\n")
    selection = input("Enter your selection: ").strip()

    if selection == "1":
        student_name = input("What is the student's name: ").strip()
        result = calculate_student_grade(student_name, students, assignments, submissions)
        print(result)
    elif selection == "2":
        assignment_name = input("What is the assignment name: ").strip()
        result = calculate_assignment_stats(assignment_name, assignments, submissions)
        print(result)
    elif selection == "3":
        assignment_name = input("What is the assignment name: ").strip()
        result = plot_assignment_histogram(assignment_name, assignments, submissions)
        if result:
            print(result)
    else:
        print("Invalid selection.")

if __name__ == "__main__":
    main()
