# actionplans.py
import pymongo
from bson import ObjectId
from datetime import datetime  # Correct import
from pymongo.errors import PyMongoError
from dotenv import load_dotenv
from pymongo import MongoClient
import os
load_dotenv()  # load environment variables from .env

client = MongoClient(os.getenv("MONGO_URI"))
db = client["diabetesdb"]  # Replace with your database name
action_plan_collection = db["action_plans"]

def add_action_plan(user_id, plan):
    try:
        collection = db["action_plans"]  # Ensure you're using the correct collection name
        
        # Prepare the action plan document to be inserted
        action_plan = {
            "user_id": user_id,
            "plan": plan,
            "createdAt": datetime.now()  # Use datetime.now() to get current time
        }

        # Log the data you're trying to insert
        print(f"Attempting to insert action plan for user {user_id}: {action_plan}")
        
        # Insert into the MongoDB collection
        result = collection.insert_one(action_plan)
        
        # Log the inserted ID for confirmation
        print(f"Successfully inserted action plan with ID: {result.inserted_id}")
        
        return {"success": True, "message": "Action plan saved successfully!"}
    except PyMongoError as e:
        # If there is a MongoDB error, print and return the error
        print(f"Error inserting into MongoDB: {e}")
        return {"success": False, "message": f"An error occurred: {e}"}
    except Exception as e:
        # Catch any other general errors
        print(f"Error: {e}")
        return {"success": False, "message": f"An unexpected error occurred: {e}"}

def get_action_plans(user_id):
    try:
        # Fetch action plans from the MongoDB collection based on user_id
        plans = list(action_plan_collection.find({"user_id": user_id}))
        
        # Convert ObjectId to string for JSON serialization
        for plan in plans:
            plan["_id"] = str(plan["_id"])
        
        return {"success": True, "plans": plans}
    except PyMongoError as e:
        return {"success": False, "message": f"MongoDB error: {e}"}
    except Exception as e:
        return {"success": False, "message": f"An error occurred: {e}"}
    
def delete_plans_for_user(user_id):
    # Assuming you have a collection named 'action_plans' in your database
    try:
        # Delete the plans for the user from the database
        # Replace with your actual database logic
        collection = db['action_plans']
        result = collection.delete_many({'user_id': user_id})
        return result.deleted_count > 0
    except Exception as e:
        print(f"Error deleting plans: {e}")
        return False