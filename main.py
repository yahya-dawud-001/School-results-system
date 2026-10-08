import sqlite3

conn = sqlite3.connect("school.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    student_class TEXT,
    maths INTEGER,
    english INTEGER,
    science INTEGER,
    computer INTEGER,
    total INTEGER,
    average REAL,
    grade TEXT
)
""")
conn.commit()

def get_grade(avg):
    if avg >= 70:
        return "A"
    elif avg >= 60:
        return "B"
    elif avg >= 50:
        return "C"
    elif avg >= 40:
        return "D"
    else:
        return "F"

def add_student():
    name = input("Enter name: ").strip()
    student_class_name = input("Enter student_class e.g SSS3: ").strip()
    try:
        maths = int(input("Maths score: "))
        english = int(input("English score: "))
        science = int(input("Science score: "))
        computer = int(input("Computer score: "))
    except ValueError:
        print("Score must be number!")
        return

    total = maths + english + science +computer
    average = round(total / 4, 2)
    grade = get_grade(average)

    cursor.execute("""
        INSERT INTO results (name, student_class, maths, english, science, computer, total, average, grade)
        VALUES (?,?,?,?,?,?,?,?,?)
    """, (name, student_class_name, maths, english, science, computer, total, average, grade))
    conn.commit()
    print(f"\nAdded {name} | Total:{total} Avg:{average} Grade:{grade}")

def search_student():
    search_name = input("\nEnter name to search: ").strip()
    found = False
    for row in cursor.execute("SELECT * FROM results WHERE LOWER(name) = LOWER(?)", (search_name,)):
        print(f"{row[0]} | {row[1]} | {row[2]} | M:{row[3]} E:{row[4]} S:{row[5]} C:{row[6]} | Total:{row[7]} Avg:{row[8]} Grade:{row[9]}")
        found = True
    if not found:
        print(f"No student found with name '{search_name}'")

def show_all():
    rows = cursor.execute("SELECT * FROM results ORDER BY average DESC").fetchall()
    if not rows:
        print("No records yet.")
        return
    print("\n--- ALL RESULTS (Sorted by Average) ---")
    position = 1
    for row in rows:
        print(f"{position}. {row[1]} ({row[2]}) | M:{row[3]} E:{row[4]} S:{row[5]} C:{row[6]}| Total:{row[7]} Avg:{row[8]} Grade:{row[9]} | Pos:{position}")
        position += 1

def delete_student():
    id_to_delete = input("Enter ID to delete: ")
    cursor.execute("DELETE FROM results WHERE id =?", (id_to_delete,))
    conn.commit()
    if cursor.rowcount > 0:
        print("Deleted successfully.")
    else:
        print("ID not found.")

def edit_student():
    id_to_edit = input("Enter ID to edit: ")
    cur = cursor.execute("SELECT * FROM results WHERE id =?", (id_to_edit,)).fetchone()
    if not cur:
        print("ID not found.")
        return
    print(f"Editing {cur[1]} - leave blank to keep old")
    name = input(f"New name ({cur[1]}): ") or cur[1]
    student_class_name = input(f"New student_class ({cur[2]}): ") or cur[2]
    try:
        maths_input = input(f"New Maths ({cur[3]}): ")
        maths = int(maths_input) if maths_input else cur[3]
        english_input = input(f"New English ({cur[4]}): ")
        english = int(english_input) if english_input else cur[4]
        science_input = input(f"New Science ({cur[5]}): ")
        science = int(science_input) if science_input else cur[5]
        computer_input = input(f'New computer({cur[6]}):')
        computer = int(computer_input) if computer_input else cur[6]
    except ValueError:
           print("Invalid number")
           jreturn

    total = maths + english + science + computer
    average = round(total / 4, 2)
    grade = get_grade(average)

    cursor.execute("""
        UPDATE results SET name=?, student_class=?, maths=?, english=?, science=?, total=?, average=?, grade=? WHERE id=?
    """, (name, student_class_name, maths, english, science, computer, total, average, grade, id_to_edit))
    conn.commit()
    print("Updated successfully.")

# MAIN MENU
while True:
    print("\n=== SCHOOL RESULT SYSTEM LEVEL 2 ===")
    print("1. Add Student")
    print("2. Search Student")
    print("3. Show All + Position")
    print("4. Delete Student")
    print("5. Edit Student")
    print("6. Exit")
    choice = input("Choose: ").strip()

    if choice == "1":
        add_student()
    elif choice == "2":
        search_student()
    elif choice == "3":
        show_all()
    elif choice == "4":
        delete_student()
    elif choice == "5":
        edit_student()
    elif choice == "6":
        print("Goodbye! Data saved in school.db")
        break
    else:
        print("Invalid choice.")

conn.close()