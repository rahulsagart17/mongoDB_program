from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Replace this with your MongoDB Atlas connection string
MONGO_URI =  "mongodb+srv://rahul:rahulsagart01@cluster0.eyngtcp.mongodb.net/?retryWrites=true&w=majority"

try:
    # Connect to MongoDB Atlas
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)

    # Test connection

    client.admin.command("ping")
    print("Connected to MongoDB Atlas successfully!")

    # Create database and collection
    db = client["collegeDB"]
    students = db["students"]

    # -----------------------------------
    # 1. INSERT / UPSERT STUDENT DOCUMENTS
    # -----------------------------------
    student_data = [
        {
            "student_id": 201,
            "name": "Aarav",
            "age": 23,
            "department": "CSE",
            "cgpa": 8.7,
            "skills": ["Python", "MongoDB", "ML"]
        },
        {
            "student_id": 202,
            "name": "Diya",
            "age": 24,
            "department": "ECE",
            "cgpa": 9.1,
            "skills": ["Java", "IoT"]
        },
        {
            "student_id": 203,
            "name": "Rohan",
            "age": 22,
            "department": "CSE",
            "cgpa": 7.9,
            "skills": ["Python", "SQL"]
        }
    ]

    for student in student_data:
        students.update_one(
            {"student_id": student["student_id"]},
            {"$set": student},
            upsert=True
        )

    print("\nStudent documents inserted/updated.")

    # -------------------------
    # 2. DISPLAY ALL STUDENTS
    # -------------------------
    print("\nAll student records:")
    for student in students.find({}, {"_id": 0}):
        print(student)

    # ----------------------------------
    # 3. CONDITIONAL QUERY: CGPA > 8.0
    # ----------------------------------
    print("\nStudents with CGPA greater than 8.0:")
    for student in students.find(
        {"cgpa": {"$gt": 8.0}},
        {"_id": 0}
    ):
        print(student)

    # -------------------------
    # 4. UPDATE A STUDENT
    # -------------------------
    students.update_one(
        {"student_id": 201},
        {"$set": {"cgpa": 9.0}}
    )

    print("\nUpdated student 201:")
    print(students.find_one({"student_id": 201}, {"_id": 0}))

    # --------------------------------
    # 5. QUERY ARRAY FIELD: Python
    # --------------------------------
    print("\nStudents having Python skill:")
    for student in students.find(
        {"skills": "Python"},
        {"_id": 0}
    ):
        print(student)

    # --------------------------------
    # 6. AGGREGATION: AVERAGE CGPA
    #    DEPARTMENT-WISE
    # --------------------------------
    print("\nDepartment-wise average CGPA:")
    pipeline = [
        {
            "$group": {
                "_id": "$department",
                "average_cgpa": {"$avg": "$cgpa"},
                "student_count": {"$sum": 1}
            }
        },
        {"$sort": {"_id": 1}}
    ]

    for result in students.aggregate(pipeline):
        print(result)

    # -------------------------
    # 7. CREATE INDEXES
    # -------------------------
    students.create_index("name")
    students.create_index("student_id", unique=True)

    print("\nIndexes created:")
    print(students.index_information())

    # -------------------------
    # 8. DELETE A STUDENT
    # -------------------------
    delete_result = students.delete_one({"student_id": 203})
    print("\nDeleted student count:", delete_result.deleted_count)

    # -------------------------
    # 9. DISPLAY FINAL RECORDS
    # -------------------------
    print("\nFinal student records:")
    for student in students.find({}, {"_id": 0}):
        print(student)

except PyMongoError as error:
    print("MongoDB error:", error)

finally:
    try:
        client.close()
        print("\nMongoDB connection closed.")
    except NameError:
        pass