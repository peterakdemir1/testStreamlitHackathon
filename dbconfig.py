from pymongo.mongo_client import MongoClient
import certifi
from hacknjit2023_models.image import Image
from hacknjit2023_models.user import User
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()

class DbConnection:
    CA = certifi.where()
    # uri = f"mongodb+srv://host:{os.getenv('DB_PASSWORD')}@cluster0.hx0xfxy.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp"
    # uri = f"mongodb+srv://dev:{os.getenv('DB_PASSWORD2')}@petertest.w16mw.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp"
    uri = f"mongodb+srv://host2:{os.getenv('DB_PASSWORD3')}@cluster0.hx0xfxy.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp"
    client = MongoClient(uri, tlsCAFile=CA)

    def __init__(self):
        # Send a ping to confirm a successful connection
        try:    
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    def get_db(self):
        return self.client['hacknjit2023']
        # return self.client['shekhmus']    

class UsersDao:
    def __init__(self, db_conn: DbConnection):
        self.DB_CONN = db_conn
        self.DB = self.DB_CONN.get_db()
        self.COLLECTION = self.DB['users']

    def insert_one(self, user: dict):
        try:
            res = self.COLLECTION.insert_one(user)
            if not res.inserted_id:
                raise Exception
            return user
        except Exception as e:
            print(e)
            return None
    
    def update_one(self, user, newUser):
        try:
            if user == {} or user == None:
                return
            res = self.COLLECTION.update_one(user, {'$set': newUser})
            if not res.upserted_id:
                raise Exception
            return newUser
        except Exception as e:
            print(e)
            return None


    def find_any(self, user: dict={}):
        return [user for user in self.COLLECTION.find(user)]

class ImagesDao:
    def __init__(self, db_conn: DbConnection):
        self.DB_CONN = db_conn
        self.DB = self.DB_CONN.get_db()
        self.COLLECTION = self.DB['images']
    
    def insert_one(self, image: dict):
        try:
            res = self.COLLECTION.insert_one(image)
            if not res.inserted_id:
                raise Exception
            return image
        except Exception as e:
            # print(e)
            return None
    
    def find_any(self, image: dict={}):
        return [image for image in self.COLLECTION.find(image)]
    
    def get_images_by_user(self, username: str):
        query = {"username": username}
        images = self.COLLECTION.find(query)
        user_images = []
        for image in images:
            image_bytes = image["image_bytes"]
            user_images.append(image_bytes)

# class SolvedDao:
#     def __init__(self, db_conn: DbConnection):
#         self.DB_CONN = db_conn
#         self.DB = self.DB_CONN.get_db()
#         self.COLLECTION = self.DB['solved']

#     def insert_one(self, solve: dict):
#         try:
#             res = self.COLLECTION.insert_one(solve)
#             if not res.inserted_id:
#                 raise Exception
#             return solve
#         except Exception as e:
#             # print(e)
#             return None

#     def find_any(self, solve: str):
#         return [solve for solve in self.COLLECTION.find(solve)]
    
@st.cache_resource
def cache_db_conn():
    return DbConnection()

DB_CONN = cache_db_conn()

@st.cache_resource
def cache_daos(_db_conn):
    return UsersDao(_db_conn), ImagesDao(_db_conn)#, SolvedDao(_db_conn)

# users_dao, images_dao, solved_dao  = cache_daos(DB_CONN)
users_dao, images_dao  = cache_daos(DB_CONN)