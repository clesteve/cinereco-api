from application import application
from flask import jsonify, request
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id=application.config["AWS_ID"],
                          aws_secret_access_key=application.config["AWS_SECRET"],
                          region_name="eu-west-3")
users = dynamodb.Table('users')


@application.route("/users/<email>")
def getUser(email):
    resp = users.get_item(Key={"email": email})
    return jsonify(resp["Item"])
