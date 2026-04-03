# utils.py
import pandas as pd
import plotly.express as px

# Common courses across departments
_YEAR1_SEM1 = ["Matrices and Calculus", "Engineering Chemistry", "Programming for Problem Solving", "Basic Electrical Engineering", "Engineering Graphics"]

# Department-specific course structures
DEPARTMENT_COURSES = {
    "CSE": {
        (1,1): _YEAR1_SEM1,
        (1,2): ["Ordinary Differential Equations", "Applied Physics", "Data Structures", "Computer Organization", "Discrete Mathematics"],
        (2,1): ["Design and Analysis of Algorithms", "Database Management Systems", "Operating Systems", "Computer Networks", "Formal Languages and Automata Theory"],
        (2,2): ["Software Engineering", "Web Technologies", "Theory of Computation", "Microprocessors and Microcontrollers", "Professional Elective-I"],
        (3,1): ["Compiler Design", "Artificial Intelligence", "Machine Learning", "Computer Graphics", "Professional Elective-II"],
        (3,2): ["Data Mining", "Cloud Computing", "Information Security", "Professional Elective-III", "Open Elective-I"],
        (4,1): ["Big Data Analytics", "Internet of Things", "Professional Elective-IV", "Open Elective-II", "Project Phase-I"],
        (4,2): ["Deep Learning", "Professional Elective-V", "Open Elective-III", "Project Phase-II", "Seminar"]
    },
    "ECE": {
        (1,1): _YEAR1_SEM1,
        (1,2): ["Ordinary Differential Equations", "Applied Physics", "Network Theory", "Electronic Devices and Circuits", "Signals and Systems"],
        (2,1): ["Analog Electronic Circuits", "Digital Electronics", "Control Systems", "Electromagnetic Theory", "Communication Systems"],
        (2,2): ["Microprocessors and Microcontrollers", "Digital Signal Processing", "VLSI Design", "Antenna and Wave Propagation", "Professional Elective-I"],
        (3,1): ["Embedded Systems", "Wireless Communication", "Optical Communication", "Power Electronics", "Professional Elective-II"],
        (3,2): ["Radar and Navigation", "Satellite Communication", "Digital Image Processing", "Professional Elective-III", "Open Elective-I"],
        (4,1): ["Internet of Things", "5G Networks", "Professional Elective-IV", "Open Elective-II", "Project Phase-I"],
        (4,2): ["Advanced Communication Systems", "Professional Elective-V", "Open Elective-III", "Project Phase-II", "Seminar"]
    },
    "EEE": {
        (1,1): _YEAR1_SEM1,
        (1,2): ["Ordinary Differential Equations", "Applied Physics", "Network Theory", "Electrical Machines-I", "Power Systems"],
        (2,1): ["Electrical Machines-II", "Control Systems", "Power Electronics", "Analog Electronics", "Digital Electronics"],
        (2,2): ["High Voltage Engineering", "Renewable Energy Systems", "Microprocessors", "Electrical Measurements", "Professional Elective-I"],
        (3,1): ["Power System Protection", "Industrial Drives", "Embedded Systems", "Smart Grid Technology", "Professional Elective-II"],
        (3,2): ["Electric Vehicle Technology", "Power Quality", "Professional Elective-III", "Instrumentation", "Open Elective-I"],
        (4,1): ["Advanced Power Systems", "Professional Elective-IV", "Open Elective-II", "Project Phase-I", "Industrial Training"],
        (4,2): ["Energy Management", "Professional Elective-V", "Open Elective-III", "Project Phase-II", "Seminar"]
    },
    "MECH": {
        (1,1): _YEAR1_SEM1,
        (1,2): ["Ordinary Differential Equations", "Applied Physics", "Engineering Mechanics", "Thermodynamics", "Manufacturing Processes"],
        (2,1): ["Fluid Mechanics", "Heat Transfer", "Kinematics of Machinery", "Material Science", "Strength of Materials"],
        (2,2): ["Dynamics of Machinery", "Design of Machine Elements", "Metrology and Measurements", "CAD/CAM", "Professional Elective-I"],
        (3,1): ["Finite Element Analysis", "Refrigeration and Air Conditioning", "Automobile Engineering", "Operations Research", "Professional Elective-II"],
        (3,2): ["Robotics", "Composite Materials", "Professional Elective-III", "Mechatronics", "Open Elective-I"],
        (4,1): ["Advanced Manufacturing", "Professional Elective-IV", "Open Elective-II", "Project Phase-I", "Industrial Training"],
        (4,2): ["Product Design", "Professional Elective-V", "Open Elective-III", "Project Phase-II", "Seminar"]
    },
    "CIVIL": {
        (1,1): _YEAR1_SEM1,
        (1,2): ["Ordinary Differential Equations", "Applied Physics", "Mechanics of Solids", "Building Materials", "Surveying"],
        (2,1): ["Structural Analysis", "Geotechnical Engineering", "Water Resources Engineering", "Transportation Engineering", "Construction Technology"],
        (2,2): ["Design of Concrete Structures", "Environmental Engineering", "Hydraulics", "Estimating and Costing", "Professional Elective-I"],
        (3,1): ["Design of Steel Structures", "Foundation Engineering", "Highway Engineering", "Water Supply Engineering", "Professional Elective-II"],
        (3,2): ["Earthquake Engineering", "Traffic Engineering", "Professional Elective-III", "Remote Sensing", "Open Elective-I"],
        (4,1): ["Advanced Structural Design", "Professional Elective-IV", "Open Elective-II", "Project Phase-I", "Site Training"],
        (4,2): ["Construction Management", "Professional Elective-V", "Open Elective-III", "Project Phase-II", "Seminar"]
    },
    "IT": {
        (1,1): _YEAR1_SEM1,
        (1,2): ["Ordinary Differential Equations", "Applied Physics", "Data Structures", "Computer Organization", "Database Management Systems"],
        (2,1): ["Design and Analysis of Algorithms", "Operating Systems", "Computer Networks", "Software Engineering", "Web Technologies"],
        (2,2): ["Information Security", "Mobile Computing", "Cloud Computing", "Professional Elective-I", "Open Source Technologies"],
        (3,1): ["Big Data Analytics", "Internet of Things", "Artificial Intelligence", "Professional Elective-II", "Blockchain Technology"],
        (3,2): ["Machine Learning", "Cyber Security", "Professional Elective-III", "Data Science", "Open Elective-I"],
        (4,1): ["Digital Forensics", "Professional Elective-IV", "Open Elective-II", "Project Phase-I", "Industry Internship"],
        (4,2): ["Advanced Web Technologies", "Professional Elective-V", "Open Elective-III", "Project Phase-II", "Seminar"]
    },
    "CSE-DS": {
        (1,1): _YEAR1_SEM1,
        (1,2): ["Ordinary Differential Equations", "Applied Physics", "Data Structures", "Statistics and Probability", "Database Systems"],
        (2,1): ["Design and Analysis of Algorithms", "Machine Learning", "Data Mining", "Big Data Technologies", "Statistical Computing"],
        (2,2): ["Deep Learning", "Natural Language Processing", "Computer Vision", "Professional Elective-I", "Data Visualization"],
        (3,1): ["Advanced Machine Learning", "Big Data Analytics", "Time Series Analysis", "Professional Elective-II", "Cloud Computing"],
        (3,2): ["Reinforcement Learning", "Professional Elective-III", "Ethics in Data Science", "Open Elective-I", "Research Methodology"],
        (4,1): ["Advanced Analytics", "Professional Elective-IV", "Open Elective-II", "Capstone Project-I", "Industry Project"],
        (4,2): ["Data Science Applications", "Professional Elective-V", "Open Elective-III", "Capstone Project-II", "Seminar"]
    },
    "CSE-CS": {
        (1,1): _YEAR1_SEM1,
        (1,2): ["Ordinary Differential Equations", "Applied Physics", "Data Structures", "Computer Organization", "Discrete Mathematics"],
        (2,1): ["Design and Analysis of Algorithms", "Database Management Systems", "Operating Systems", "Computer Networks", "Theory of Computation"],
        (2,2): ["Compiler Design", "Software Engineering", "Web Technologies", "Cryptography", "Professional Elective-I"],
        (3,1): ["Artificial Intelligence", "Machine Learning", "Distributed Systems", "Professional Elective-II", "Computer Graphics"],
        (3,2): ["Information Security", "Cloud Computing", "Professional Elective-III", "Human Computer Interaction", "Open Elective-I"],
        (4,1): ["Advanced Topics in CS", "Professional Elective-IV", "Open Elective-II", "Project Phase-I", "Research Project"],
        (4,2): ["Emerging Technologies", "Professional Elective-V", "Open Elective-III", "Project Phase-II", "Seminar"]
    },
    "AIML": {
        (1,1): _YEAR1_SEM1,
        (1,2): ["Ordinary Differential Equations", "Applied Physics", "Data Structures", "Linear Algebra", "Probability and Statistics"],
        (2,1): ["Design and Analysis of Algorithms", "Machine Learning Fundamentals", "Neural Networks", "Computer Vision", "Natural Language Processing"],
        (2,2): ["Deep Learning", "Reinforcement Learning", "Big Data Technologies", "Professional Elective-I", "Statistical Learning"],
        (3,1): ["Advanced Machine Learning", "Computer Vision Applications", "NLP Applications", "Professional Elective-II", "AI Ethics"],
        (3,2): ["Generative AI", "Professional Elective-III", "AI in Healthcare", "Open Elective-I", "Research Methods"],
        (4,1): ["Advanced AI Techniques", "Professional Elective-IV", "Open Elective-II", "AI Project-I", "Industry Collaboration"],
        (4,2): ["AI Applications", "Professional Elective-V", "Open Elective-III", "AI Project-II", "Seminar"]
    }
}

def get_department_courses(department, year, semester):
    """Get courses for a specific department and semester"""
    return DEPARTMENT_COURSES.get(department, DEPARTMENT_COURSES.get("CSE", {})).get((year, semester), [])

# Backward compatibility - default to CSE if department not found
COURSE_STRUCTURE = DEPARTMENT_COURSES.get("CSE", {})

def get_feedback(sgpa, marks_dict):
    sorted_marks = sorted(marks_dict.items(), key=lambda x:x[1])
    weak_sub, weak_val = sorted_marks[0]
    strong_sub, strong_val = sorted_marks[-1]
    if sgpa>=8.5:
        status="Excellent"
    elif sgpa>=7:
        status="Good"
    else:
        status="Needs Attention"
    return {
        "status":status,
        "strength":f"{strong_sub} ({strong_val})",
        "weakness":f"{weak_sub} ({weak_val})",
        "advice":f"Maintain high standard in {strong_sub}. Focus on {weak_sub}."
    }

def plot_marks(marks):
    df = pd.DataFrame(list(marks.items()), columns=['Subject','Marks'])
    fig = px.bar(df, x='Subject', y='Marks', color='Marks', color_continuous_scale='RdYlGn')
    return fig

def plot_progress(labels, performance):
    fig = px.line(x=labels, y=performance, title="Semester Progress (SGPA)")
    return fig
