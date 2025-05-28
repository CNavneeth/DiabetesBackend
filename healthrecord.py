import pymongo
from bson import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient
import os
load_dotenv()  # load environment variables from .env

client = MongoClient(os.getenv("MONGO_URI"))
db = client["diabetesdb"]  # Replace with your database name
collection = db["health_records"]
cancer_collection = db["cancer_records"]
heart_collection = db["heart_records"]
def add_health_record(record):
    try:
        collection.insert_one(record)
        return {"success": True, "message": "Record added successfully"}
    except Exception as e:
        return {"success": False, "error": str(e)}
    
def add_cancer_record(cancer_record):
    try:
        cancer_collection.insert_one(cancer_record)
        return {"success": True, "message": "Record added successfully"}
    except Exception as e:
        return {"success": False, "error": str(e)}
def add_heart_record(heart_record):
    try:
        heart_collection.insert_one(heart_record)
        return {"success": True, "message": "Record added successfully"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_user_records(user_id):
    try:
        records = list(collection.find({"user_id": user_id}))

        # Convert ObjectId to string for frontend compatibility
        for record in records:
            record["_id"] = str(record["_id"])

        return {"success": True, "records": records}
    except Exception as e:
        return {"success": False, "error": str(e)}
    
def get_cancer_records(user_id):
    try:
        records = list(cancer_collection.find({"user_id": user_id}))

        # Convert ObjectId to string for frontend compatibility
        for record in records:
            record["_id"] = str(record["_id"])

        return {"success": True, "records": records}
    except Exception as e:
        return {"success": False, "error": str(e)}
    
def get_heart_records(user_id):
    try:
        records = list(heart_collection.find({"user_id": user_id}))

        # Convert ObjectId to string for frontend compatibility
        for record in records:
            record["_id"] = str(record["_id"])

        return {"success": True, "records": records}
    except Exception as e:
        return {"success": False, "error": str(e)}

def delete_user_record(record_id):
    try:
        if not record_id:
            return {"success": False, "error": "Invalid record ID"}

        print(f"Deleting record with ID: {record_id}")  # Debugging log

        result = collection.delete_one({"_id": ObjectId(record_id)})

        if result.deleted_count > 0:
            return {"success": True, "message": "Record deleted successfully"}
        else:
            return {"success": False, "message": "No matching record found"}
    except Exception as e:
        print(f"Error during deletion: {e}")  # Log the error
        return {"success": False, "error": str(e)}
    
def delete_cancer_record(record_id):
    try:
        if not record_id:
            return {"success": False, "error": "Invalid record ID"}

        print(f"Deleting record with ID: {record_id}")  # Debugging log

        result = cancer_collection.delete_one({"_id": ObjectId(record_id)})

        if result.deleted_count > 0:
            return {"success": True, "message": "Record deleted successfully"}
        else:
            return {"success": False, "message": "No matching record found"}
    except Exception as e:
        print(f"Error during deletion: {e}")  # Log the error
        return {"success": False, "error": str(e)}
    
def delete_heart_record(record_id):
    try:
        if not record_id:
            return {"success": False, "error": "Invalid record ID"}

        print(f"Deleting record with ID: {record_id}")  # Debugging log

        result = heart_collection.delete_one({"_id": ObjectId(record_id)})

        if result.deleted_count > 0:
            return {"success": True, "message": "Record deleted successfully"}
        else:
            return {"success": False, "message": "No matching record found"}
    except Exception as e:
        print(f"Error during deletion: {e}")  # Log the error
        return {"success": False, "error": str(e)}

