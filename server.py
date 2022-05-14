from flask import Flask,Response,request
from pymongo import MongoClient
import json
app = Flask(__name__)
from bson.objectid import ObjectId
# Create Databasse Clinet  to intract with mongodb

try:

    # connection = "mongodb://localhost:27017/inventory"
    # client = MongoClient(connection)
    mongo = MongoClient(host='localhost',port=27017,serverSelectionTimeoutMS=1000)

    db = mongo.company # database named company will be created

    mongo.server_info() # Trigger exception if cannot connect to database

except Exception as e:
    print("Cannot connec to database")



# Create a route for enter into the server

@app.route("/users",methods=["POST"])
def create_user():
    try:

        user = {'first_name':request.form['first_name'],"last_name":request.form['last_name']}
        response = db.users.insert_one(user)
        print(response.inserted_id)

        return Response(
            response = json.dumps({"message":"user created","id":f"{response.inserted_id}"}),
            status= 200,
            mimetype="application/json"
        )

    except Exception as e:
        print(e)



@app.route("/users",methods = ['GET'])
def get_users():

    try:
        data = list(db.users.find())

        for user in data:
            user['_id']=str(user['_id'])
        return Response(
            response=json.dumps(data),
            status=200,
            mimetype="application/json"
        )

    except Exception as e:
        print(e)
        return Response(
            response=json.dumps({"message": "cannot read users"}),
            status=500,
            mimetype="application/json"
        )

# Update user record

@app.route("/users/<id>",methods = ['PATCH'])
def update_user(id):

    try:

        dbresponse = db.users.update_one(
            {"_id":ObjectId(id)},
            {"$set":{"first_name":request.form['first_name']}}
         )
        print(dbresponse.modified_count)


        if dbresponse.modified_count ==1:
            return Response(
                response=json.dumps({"message": "User updated"}),
                status=200,
                mimetype="application/json"
            )

        return Response(
            response=json.dumps({"message": "Nothing to update"}),
            status=200,
            mimetype="application/json"
        )


    except Exception as e:
        print(e)
        return Response(
            response=json.dumps({"message": "Sorry user cannot updated"}),
            status=500,
            mimetype="application/json"
        )


# Delete a user record

@app.route("/users/<id>",methods = ['DELETE'])

def delete_user(id):

    try:

        result = db.users.delete_one({"id":ObjectId(id)})
        if result.deleted_count == 1:
            return Response(
                response=json.dumps({"message": "User deleted","id":f"{id}"}),
                status=200,
                mimetype="application/json"
            )
        return Response(
            response=json.dumps({"message": f"User not found for id {id}", "id": f"{id}"}),
            status=200,
            mimetype="application/json"
        )


    except Exception as e:
        print(e)
        return Response(
            response=json.dumps({"message": "Sorry user cannot deleted"}),
            status=500,
            mimetype="application/json"
        )


if __name__ == "__main__":
    app.run(port=5555,debug=True)

