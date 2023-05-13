from flask import Flask, request, json, Response
from pymongo import MongoClient
from bson import ObjectId
from models import NewUser, UpdatedUser
import os

mongo_uri = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/'

client = MongoClient(mongo_uri)
db = client.admin
users = db.users

app = Flask(__name__)

@app.route('/users/', methods=['GET'])     # Read MongoDB Document, through API and METHOD - GET
def get_users():
    documents = users.find()
    output = []

    for data in documents:
        document = {}
        for item in data:
            document[item] = data[item]
        document['_id'] = str(document['_id'])

        output.append(document)

    return Response(response=json.dumps(output), status=200,
                    mimetype='application/json')

@app.route('/users/<id>', methods=['GET'])     # Read MongoDB Document, through API and METHOD - GET
def get_user(id):
    try:
        documents = users.find({'_id': ObjectId(id)})
    except:
        return Response(response=json.dumps({"Error": "No such user present!"}),
                        status=400, mimetype='application/json')

    data = documents[0]
    document = {}
    for item in data:
        document[item] = data[item]
    document['_id'] = str(document['_id'])

    return Response(response=json.dumps(document), status=200,
                    mimetype='application/json')

@app.route('/users/', methods=['POST'])     # Read MongoDB Document, through API and METHOD - GET
def write_user():
    data = request.json
    try:
        NewUser.parse_obj(data)
    except:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400, mimetype='application/json')
    response = users.insert_one(data)
    output = {'Status': 'Successfully Inserted',
                  'Document_ID': str(response.inserted_id)}
    return Response(response=json.dumps(output), status=200,
                    mimetype='application/json')

@app.route('/users/<id>/', methods=['DELETE'])   # Delete MongoDB Document, through API and METHOD - DELETE
def delete_user(id):
    response = users.delete_one({'_id': ObjectId(id)})
    output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
    return Response(response=json.dumps(output), status=200,
                    mimetype='application/json')

@app.route('/users/<id>/', methods=['PUT'])     # Update MongoDB Document, through API and METHOD - PUT
def update_user(id):
    data = request.json
    try:
        UpdatedUser.parse_obj(data)
    except:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400, mimetype='application/json')
    
    response = users.update_one({'_id': ObjectId(id)}, {"$set": data})
    output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
    return Response(response=json.dumps(output), status=200,
                    mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, port=5000)