from cProfile import label
import json
from logging import Logger, error
from operator import ne
from flask import Blueprint, config, request, url_for, redirect, Response, make_response, jsonify, session, render_template
from flask import current_app as app
from flask_login import current_user as user
from mongo_service import MongoService
from utils import is_json_request, format_thing_description, transform_links

policy_api = Blueprint('policy_api', __name__)
ERROR_JSON = {"error": "Invalid request."}
WARNING_JSON = {"error": "Invalid request."}

class AttributeDict:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if isinstance(value, dict):
                self.__dict__[key] = AttributeDict(**value)
            else:
                self.__dict__[key] = value
    def __getattr__(self, key):
        # First, try to return from _response
        try:
            return self.__dict__['_response'][key]
        except KeyError:
            pass
        except AttributeError:
            pass

@policy_api.route('/register2', methods=['POST'])
def register2():
    """Register thing description at the target location. 
    If the current directory is the target location specified by `location` argument, the operation is processed locally
    
    Args:
        All of the following arguments are required and passed in the request URL.
        td (JSON str): the information of the thing description to be registered in JSON format
    Returns:
        HTTP Response: if the register is completed, a simple success string with HTTP status code 200 is returned
            Otherwise a reason is returned in the response and HTTP status code is set to 400
    """
    if not is_json_request(request, ["td"]):
        return jsonify(ERROR_JSON), 400
    
    body = request.get_json()
    thing_description = body["td"]
    mongo_service = MongoService()
    mongo_service.create_thing(thing_description)
    
    return make_response("Created", 200)

@policy_api.route('/policylist', methods=['POST'])
def policylist():
    if not is_json_request(request, ["td"]):
        return jsonify(ERROR_JSON), 400

    mongo_service = MongoService()
    mongo_service.find_policies()
    return make_response("Worked", 200)

@policy_api.route('/thinglist', methods=['POST'])
def thinglist():
    if not is_json_request(request, ["td"]):
        return jsonify(ERROR_JSON), 400

    mongo_service = MongoService()
    mongo_service.find_things()
    return make_response("Worked", 200)

@policy_api.route('/addPolicy', methods=['POST'])
def addPolicy():

    mongo_service = MongoService()
    mongo_service.add_policy()
    return make_response("Worked", 200)

@policy_api.route('/changePolicy', methods=['POST'])
def changePolicy():
    return

@policy_api.route('/deletePolicy', methods=['POST', 'DELETE'])
@policy_api.route('/deletePolicy/<policyid>', methods=['POST', 'DELETE'])
def deletePolicy(policyid):

    mongo_service = MongoService()
    mongo_service.delete_policy(policyid)
    return make_response(("Worked", 200))


@policy_api.route('/deleteDevice', methods=['POST', 'DELETE'])
@policy_api.route('/deleteDevice/<thing_id>', methods=['POST', 'DELETE'])
def deleteDevice(thing_id):
    mongo_service = MongoService()
    mongo_service.delete_thing(thing_id)
    return

@policy_api.route('/addDevice', methods=['POST'])
def addDevice():
    if not is_json_request(request, ["td"]):
        return jsonify(ERROR_JSON), 400

    body = request.get_json()
    thing_description = body["td"]
    mongo_service = MongoService()
    mongo_service.create_thing(thing_description)

    return make_response("Created", 200)

@policy_api.route('/notifications')
def notifications():
    mongo_service= MongoService(None)
    mongo_service.get_notifications()
    return

@policy_api.route('/delete2', methods=['POST', 'DELETE'])
@policy_api.route('/delete2/<thing_id>', methods=['POST', 'DELETE'])
def delete2(thing_id):
    """
        Deletes a thing
    """
    mongo_service = MongoService()
    mongo_service.delete_thing(thing_id)
    return make_response("Deleted", 200)

@policy_api.route('/policy', methods=['POST'])
def policy():
    if not is_json_request(request, ["td"]):
        return jsonify(ERROR_JSON), 400
    
    body = request.get_json()
    policy = body["td"]
    mongo_service = MongoService()
    mongo_service.create_policy(policy)
    
    return make_response("Created", 200)

@policy_api.route('/command', methods=['POST'])
def command():
    if not is_json_request(request, ["td"]):
        return jsonify(ERROR_JSON), 400
    
    body = request.get_json()
    command = body["td"]
    mongo_service = MongoService()
    criteria = dict()
    criteria["$or"] = [{"device_actor.type":"*"}, {"device_actor.type":command["device_actor"]["type"]}]
    criteria["action"] = command["action"]
    policies = mongo_service.find_policies(criteria)
    for policy in policies:
        actor_criteria = dict()
        actee_criteria = dict()
        actor_criteria["id"] = command["device_actor"]["id"]
        actee_criteria["@type"] = policy["device_actee"]["type"]
        actors = transform_links(mongo_service.find_things(actor_criteria))
        actees = transform_links(mongo_service.find_things(actee_criteria))
        things = transform_links(mongo_service.find_things(None))
        devices = [AttributeDict(**device) for device in things]
        for actor in actors:
            for actee in actees:
                device_actor = AttributeDict(**actor)
                device_actee = AttributeDict(**actee)
                if eval(policy["relation"]):
                    if eval(policy["assertion"], locals()):
                        error = ERROR_JSON
                        error["error"] = policy["response"]
                        error["message"] = policy["alert"]
                        return jsonify(error), 400
    return make_response("Success", 200)