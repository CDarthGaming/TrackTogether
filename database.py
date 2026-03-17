import sqlite3

# Connect to your users database
conn = sqlite3.connect("modules.db")
cursor = conn.cursor()

# Replace YOUR_USER_ID with your actual user ID
username = "Tristan"  # <-- change this to your ID

# Give admin permissions
cursor.execute("UPDATE users SET admin = 1 WHERE username = ?", (username,))
conn.commit()
conn.close()

print("Admin permissions granted!")

# import sqlite3

# # Connect to your database
# conn = sqlite3.connect("assignments.db")
# cursor = conn.cursor()

# courses = ["Games Development", "Software Engineering", "Computer Science", "Computing", "Cyber Security", "Computer Networks & Security"]

# for course in courses:
#     cursor.execute("INSERT INTO courses (course_name) VALUES (?)", (course,))

# modules = [
#     ("Introduction to Software Development", "COC001"),
#     ("Investigating IT", "COC002"),
#     ("Problem-solving for Computing", "COC003"),
#     ("Study Skills 1 - Learning How to Learn", "COC004"),
#     ("Study Skills 2 - Developing Academic Skills", "COC005"),
#     ("Foundation Mathematics", "MAC101"),
#     ("The Computing Challenge", "CO1007"),
#     ("Introduction to Networking", "CO1008"),
#     ("Games Concepts", "CO1301"),
#     ("Programming", "CO1409"),
#     ("Computer Systems and Security", "CO1508"),
#     ("Systems Analysis and Database Design", "CO1605"),
#     ("Web Technologies", "CO1707"),
#     ("The Agile Professional", "CO2007"),
#     ("Introduction to Network Routing", "CO2008"),
#     ("Information Security Management", "CO2010"),
#     ("Database Systems", "CO2011"),
#     ("Games Development 1", "CO2301"),
#     ("Software Development", "CO2401"),
#     ("Advanced Programming with C++", "CO2402"),
#     ("Cross Platform Development", "CO2404"),
#     ("Computer Graphics", "CO2409"),
#     ("Computational Thinking", "CO2412"),
#     ("Network Management", "CO2516"),
#     ("Digital Evidence and Incident Response", "CO2517"),
#     ("Interacting with the Internet of Things", "CO2519"),
#     ("Cyber Security", "CO2528"),
#     ("Human-Computer Interaction", "CO2702"),
#     ("Web Applications", "CO2717"),
#     ("User Experience", "CO2722"),
#     ("Wireless and Mobile Networks", "CO3006"),
#     ("Cloud Computing", "CO3007"),
#     ("Honours Degree Project", "CO3008"),
#     ("Games Development 2", "CO3301"),
#     ("Mathematics and Technologies for Games", "CO3303"),
#     ("Distributed Systems", "CO3404"),
#     ("Advanced Software Modelling", "CO3408"),
#     ("Secure Software and Malware Analysis", "CO3410"),
#     ("Advanced Network Routing", "CO3513"),
#     ("Penetration Testing", "CO3517"),
#     ("Artificial Intelligence", "CO3519"),
#     ("Advanced Cyber Security", "CO3520"),
#     ("Data Science", "CO3722")
# ]

# for code, name in modules:
#     cursor.execute("INSERT INTO modules (module_name, module_code) VALUES (?, ?)", (code, name))

# # ---------------------------------------------------
# # Example course_modules relationships
# # Many modules are shared among courses
# # ---------------------------------------------------
# # Get course ids
# cursor.execute("SELECT id, course_name FROM courses")
# course_map = {name: cid for cid, name in cursor.fetchall()}

# # Get module ids
# cursor.execute("SELECT id, module_code FROM modules")
# module_map = {code: mid for mid, code in cursor.fetchall()}

# # Define which modules belong to which courses
# course_modules = {
#     "Computer Science": ["CS101", "CS102", "CS201", "CS202"],
#     "Software Engineering": ["CS101", "CS102", "SE101", "SE102"],
#     "Cyber Security": ["CS101", "CS102", "CY101", "CY102"]
# }

# # Insert into junction table
# for course_name, module_codes in course_modules.items():
#     course_id = course_map[course_name]
#     for code in module_codes:
#         module_id = module_map[code]
#         cursor.execute(
#             "INSERT INTO course_modules (course_id, module_id) VALUES (?, ?)",
#             (course_id, module_id)
#         )

# # Commit and close
# conn.commit()
# conn.close()

# print("Database initialized with example courses, modules, and course-module links.")




# import sqlite3

# # Connect to the database
# conn = sqlite3.connect("modules.db")
# cursor = conn.cursor()

# # -------------------------
# # Example courses
# # -------------------------
# courses = ["Games Development", "Software Engineering", "Computer Science", "Computing", "Cyber Security", "Computer Networks & Security"]

# # Insert courses
# for course in courses:
#     cursor.execute("INSERT OR IGNORE INTO courses (name) VALUES (?)", (course,))

# # Fetch course IDs for later use
# cursor.execute("SELECT id, name FROM courses")
# course_ids = {name: cid for cid, name in cursor.fetchall()}

# # -------------------------
# # Example modules (code + name)
# # -------------------------
# modules = [
#     ("Introduction to Software Development", "COC001"),
#     ("Investigating IT", "COC002"),
#     ("Problem-solving for Computing", "COC003"),
#     ("Study Skills 1 - Learning How to Learn", "COC004"),
#     ("Study Skills 2 - Developing Academic Skills", "COC005"),
#     ("Foundation Mathematics", "MAC101"),
#     ("The Computing Challenge", "CO1007"),
#     ("Introduction to Networking", "CO1008"),
#     ("Games Concepts", "CO1301"),
#     ("Programming", "CO1409"),
#     ("Computer Systems and Security", "CO1508"),
#     ("Systems Analysis and Database Design", "CO1605"),
#     ("Web Technologies", "CO1707"),
#     ("The Agile Professional", "CO2007"),
#     ("Introduction to Network Routing", "CO2008"),
#     ("Information Security Management", "CO2010"),
#     ("Database Systems", "CO2011"),
#     ("Games Development 1", "CO2301"),
#     ("Software Development", "CO2401"),
#     ("Advanced Programming with C++", "CO2402"),
#     ("Cross Platform Development", "CO2404"),
#     ("Computer Graphics", "CO2409"),
#     ("Computational Thinking", "CO2412"),
#     ("Network Management", "CO2516"),
#     ("Digital Evidence and Incident Response", "CO2517"),
#     ("Interacting with the Internet of Things", "CO2519"),
#     ("Cyber Security", "CO2528"),
#     ("Human-Computer Interaction", "CO2702"),
#     ("Web Applications", "CO2717"),
#     ("User Experience", "CO2722"),
#     ("Wireless and Mobile Networks", "CO3006"),
#     ("Cloud Computing", "CO3007"),
#     ("Honours Degree Project", "CO3008"),
#     ("Games Development 2", "CO3301"),
#     ("Mathematics and Technologies for Games", "CO3303"),
#     ("Distributed Systems", "CO3404"),
#     ("Advanced Software Modelling", "CO3408"),
#     ("Secure Software and Malware Analysis", "CO3410"),
#     ("Advanced Network Routing", "CO3513"),
#     ("Penetration Testing", "CO3517"),
#     ("Artificial Intelligence", "CO3519"),
#     ("Advanced Cyber Security", "CO3520"),
#     ("Data Science", "CO3722")
# ]

# # Insert modules
# for code, name in modules:
#     cursor.execute("INSERT OR IGNORE INTO modules (name, code) VALUES (?, ?)", (name, code))

# # Fetch module IDs for later use
# cursor.execute("SELECT id, code FROM modules")
# module_ids = {code: mid for mid, code in cursor.fetchall()}

# # -------------------------
# # Associate modules with courses & years
# # -------------------------
# # Format: (course_name, module_code, year)
# course_module_assignments = [
#     ("Computer Science", "CO1007", 1),
#     ("Computer Science", "CO1008", 1),
#     ("Computer Science", "CO1409", 1),
#     ("Computer Science", "CO1508", 1),
#     ("Computer Science", "CO1605", 1),
#     ("Computer Science", "CO1707", 1),
#     ("Computing", "CO1007", 1),
#     ("Computing", "CO1008", 1),
#     ("Computing", "CO1409", 1),
#     ("Computing", "CO1508", 1),
#     ("Computing", "CO1605", 1),
#     ("Computing", "CO1707", 1),
#     ("Computer Games Development", "CO1007", 1),
#     ("Computer Games Development", "CO1008", 1),
#     ("Computer Games Development", "CO1409", 1),
#     ("Computer Games Development", "CO1508", 1),
#     ("Computer Games Development", "CO1605", 1),
#     ("Computer Games Development", "CO1707", 1),
#     ("Software Engineering", "CO1007", 1),
#     ("Software Engineering", "CO1008", 1),
#     ("Software Engineering", "CO1409", 1),
#     ("Software Engineering", "CO1508", 1),
#     ("Software Engineering", "CO1605", 1),
#     ("Software Engineering", "CO1707", 1),
#     ("Cyber Security", "CO1007", 1),
#     ("Cyber Security", "CO1008", 1),
#     ("Cyber Security", "CO1409", 1),
#     ("Cyber Security", "CO1508", 1),
#     ("Cyber Security", "CO1605", 1),
#     ("Cyber Security", "CO1707", 1),
#     ("Computer Networks & Security", "CO1007", 1),
#     ("Computer Networks & Security", "CO1008", 1),
#     ("Computer Networks & Security", "CO1409", 1),
#     ("Computer Networks & Security", "CO1508", 1),
#     ("Computer Networks & Security", "CO1605", 1),
#     ("Computer Networks & Security", "CO1707", 1),
#     ("Software Engineering", "SE101", 1),
#     ("Software Engineering", "SE201", 2),
#     ("Cyber Security", "CY101", 1),
#     ("Cyber Security", "CY201", 2),
#     # Modules can exist in multiple courses
#     ("Software Engineering", "CS101", 1),
#     ("Cyber Security", "CS101", 1)
# ]

# # Insert associations
# for course_name, module_code, year in course_module_assignments:
#     cursor.execute("""
#         INSERT OR IGNORE INTO course_modules (course_id, module_id, year)
#         VALUES (?, ?, ?)
#     """, (course_ids[course_name], module_ids[module_code], year))

# # Commit and close
# conn.commit()
# conn.close()

# print("Courses, modules, and associations populated successfully!")