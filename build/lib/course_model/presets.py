# course_model/presets.py

"""
This module defines the preset data structures for different school types.
Each school type includes default levels and subjects, which can be
customized or overridden by the user.
"""

preset_data = {
    "primary": {
        "levels": [f"Primary {i}" for i in range(1, 7)],
        "subjects": [
            "Mathematics",
            "English Language",
            "Basic Science",
            "Social Studies",
            "Civic Education",
            "Creative Arts",
            "Physical and Health Education"
        ]
    },
    "secondary": {
        "levels": ["JSS1", "JSS2", "JSS3", "SS1", "SS2", "SS3"],
        "subjects": {
            "core": [
                "English Language",
                "Mathematics",
                "Civic Education",
                "Basic Science and Technology",
                "Cultural and Creative Arts",
                "Physical and Health Education",
                "French Language"
            ],
            "electives": [
                "Agricultural Science",
                "Computer Studies",
                "Business Studies",
                "Home Economics",
                "Fine Art",
                "Music",
                "Yoruba Language",
                "Igbo Language",
                "Hausa Language"
            ],
            "senior_secondary_science": [
                "Physics",
                "Chemistry",
                "Biology",
                "Further Mathematics"
            ],
            "senior_secondary_art": [
                "Literature in English",
                "Government",
                "Economics",
                "Christian Religious Studies",
                "Islamic Religious Studies",
                "Geography"
            ],
            "senior_secondary_commercial": [
                "Financial Accounting",
                "Commerce",
                "Office Practice"
            ]
        }
    },
    "university": {
        "levels": ["Year 1", "Year 2", "Year 3", "Year 4"],
        "subjects": {
            "Faculty of Sciences": {
                "Computer Science": [
                    "Introduction to Programming",
                    "Data Structures and Algorithms",
                    "Operating Systems",
                    "Database Management"
                ],
                "Physics": [
                    "Classical Mechanics",
                    "Electromagnetism",
                    "Quantum Physics",
                    "Thermodynamics"
                ],
                "Chemistry": [
                    "General Chemistry",
                    "Organic Chemistry",
                    "Inorganic Chemistry",
                    "Physical Chemistry"
                ],
                "Mathematics": [
                    "Calculus I",
                    "Linear Algebra",
                    "Differential Equations",
                    "Real Analysis"
                ]
            },
            "Faculty of Engineering": {
                "Civil Engineering": [
                    "Engineering Mechanics",
                    "Structural Analysis",
                    "Fluid Mechanics",
                    "Geotechnical Engineering"
                ],
                "Electrical Engineering": [
                    "Circuit Theory",
                    "Electronics",
                    "Digital Systems Design",
                    "Power Systems"
                ],
                "Mechanical Engineering": [
                    "Thermodynamics",
                    "Mechanics of Materials",
                    "Machine Design",
                    "Fluid Dynamics"
                ]
            },
            "Faculty of Arts": {
                "History and International Studies": [
                    "World History I",
                    "African History",
                    "Diplomatic History",
                    "International Relations"
                ],
                "English and Literary Studies": [
                    "Introduction to Literature",
                    "African Literature",
                    "Drama",
                    "Poetry"
                ],
                "Linguistics": [
                    "Phonetics and Phonology",
                    "Morphology",
                    "Syntax",
                    "Semantics"
                ]
            },
            "Faculty of Social Sciences": {
                "Economics": [
                    "Microeconomics",
                    "Macroeconomics",
                    "Econometrics",
                    "Development Economics"
                ],
                "Political Science": [
                    "Introduction to Political Science",
                    "Public Administration",
                    "International Politics",
                    "Political Theory"
                ],
                "Sociology": [
                    "Introduction to Sociology",
                    "Social Stratification",
                    "Research Methods",
                    "Demography"
                ]
            }
        }
    }
    # Add more school types as needed
}
