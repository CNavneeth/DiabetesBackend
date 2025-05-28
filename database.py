import pymongo
import bcrypt
import uuid
import jwt
import datetime
from config import SECRET_KEY  # Import SECRET_KEY from config.py
import base64
from dotenv import load_dotenv
from pymongo import MongoClient
import os
load_dotenv()  # load environment variables from .env

client = MongoClient(os.getenv("MONGO_URI"))
db = client["diabetesdb"]  # Replace with your database name
collection = db["users"]  # Replace with your collection name

# Function to insert patient data
def insert_patient(data):
    result = collection.insert_one(data)
    return str(result.inserted_id)  # Return the inserted document ID

# Function to retrieve patient data
def get_all_patients():
    return list(collection.find({}, {"_id": 0}))  # Exclude MongoDB ObjectId

# Function to find a specific patient by name
def find_patient_by_name(name):
    return collection.find_one({"name": name}, {"_id": 0})

# Function to delete a patient record
def delete_patient(name):
    result = collection.delete_one({"name": name})
    return result.deleted_count > 0  # Return True if a document was deleted


def create_user(username, password, dob,email):
    # Check if username already exists
    if collection.find_one({"username": username}):
        return {"error": "Username already exists!"}

    # Generate a unique user ID
    user_id = str(uuid.uuid4())

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Create user object
    user_data = {
        "user_id": user_id,
        "username": username,
        "password": hashed_password,  # Store hashed password
        "dob": dob,
        "email":email
    }

    # Insert user into database
    collection.insert_one(user_data)

    return {"message": "User account created successfully!", "user_id": user_id}


def authenticate_user(username, password):
    user = collection.find_one({"username": username})
    if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        payload = {
            "user_id": user["user_id"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expires in 1 hour
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return {"message": "Login successful!", "token": token}
    
    return {"error": "Invalid username or password!"}

def get_user_profile(user_id):
    """Fetch user profile data excluding password."""
    user = collection.find_one({"user_id": user_id}, {"_id": 0, "password": 0})
    
    if user:
        return user  # Return user details if found
    else:
        return {"error": "User not found"}
def update_profile_pic(user_id, image_file):
    """Update the user's profile picture in MongoDB."""
    image_data = base64.b64encode(image_file.read()).decode("utf-8")
    collection.update_one(
        {"user_id": user_id}, {"$set": {"profile_pic": image_data}}
    )
    return "Profile picture updated successfully"

def update_user_profile(user_id, username, dob, email, profile_pic):
    update_data = {"username": username, "dob": dob, "email": email}

    if profile_pic:
        # Convert image to base64 string before storing
        update_data["profile_pic"] = base64.b64encode(profile_pic.read()).decode("utf-8")

    result = collection.update_one({"user_id": user_id}, {"$set": update_data})
    return result.modified_count > 0

    
