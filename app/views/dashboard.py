from mongo_service import MongoService
from flask import Blueprint, render_template, make_response


dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
@dashboard.route('/home')
def home():
    """
    Render the home page for the 'dashboard' module
    This returns the names and URLs of adjacent directories
    """
    return render_template("homescreen.html", tagname = 'home')





@dashboard.route('/policylist')
def policylist():
    """
    List of objects
    """
    mongo_service = MongoService()
    policies = mongo_service.find_policies(None)
    policies_ids = {polici["id"]: {"description": polici["description"], "device_actor": polici["device_actor"], "device_actee": polici["device_actee"]}for polici in policies}
    return render_template('policylist.html', tagname = 'policylist', policies_ids = policies_ids)

@dashboard.route('/pendingPolicies')
def pendingPolicies():

    return render_template('pendingPolicies.html')

@dashboard.route('/community')
def community():

  return render_template('community.html')


@dashboard.route('/addPolicy')
def addPolicy():
    return render_template('addPolicy.html', tagname='addPolicy')

@dashboard.route('/deletePolicy')
def deletePolicy():
    mongo_service= MongoService()
    policies = mongo_service.find_policies(None)
    policyid = [policy["id"] for policy in policies]
    return render_template('deletePolicy.html', tagname='deletePolicy', policyid=policyid)

@dashboard.route('/changePolicy')
def changePolicy():
    return render_template('changePolicy.html', tagname='changePolicy')


@dashboard.route('/notifications')
def notifications():

        return render_template('notifications.html', tagname= 'notifications')



@dashboard.route('/command')
def command():
    """
    Render the command page for the 'dashboard' module
    """
    return render_template('command.html', tagname = 'command')
