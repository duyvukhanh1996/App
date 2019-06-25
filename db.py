import pymongo
from bson.objectid import ObjectId

uri = 'mongodb://duyvukhanh:123456a@ds059125.mlab.com:59125/vukhanhduy'

client = pymongo.MongoClient(uri)
db = client.vukhanhduy
experience = db.experiences
gallery = db.gallery
users = db.users

# def update_food_by_id(food_id,name,price):
#     collection.update_one({"_id":ObjectId(food_id)},
#     {"$set":{"name":name,"price":price}})

# def get_food_by_id(food_id):
#     return collection.find_one({"_id":  ObjectId(food_id)})

# def get_all():
#     return list(collection.find())


# def insert_food(name:str, price:int):
#     collection.insert_one({"name": name, "price": price})

# def delete_food_by_id(food_id):
#     collection.delete_one({"_id":  ObjectId(food_id)})

def insert_experience(name: str, content: dict, youtube_embed_link: str, picture_link:str):
    experience.insert_one({"name":name,"content":content,"youtube_embed_link":youtube_embed_link,"picture_link":picture_link})

def get_experience_by_name(name):
    return experience.find_one({"name":name})

def get_all_experience():
    return list(experience.find())

def get_all_users():
    return list(users.find())

def insert_users(username: str, password: str):
    users.insert_one({"username":username,"password":password})
    
def insert_image(owner: str, link: str):
    gallery.insert_one({"owner":owner,"link":link})

def get_all_images():
    return list(gallery.find())

def get_image_by_owner(owner:str):
    return list(gallery.find({"owner": owner}))

def delete_image_by_id(food_id):
    gallery.delete_one({"_id":ObjectId(food_id)})



    


