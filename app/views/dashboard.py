from mongo_service import MongoService
from flask import Blueprint, render_template, make_response
from neo4j_service import Neo4jService

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
@dashboard.route('/home')
def home():
    """
    Render the home page for the 'dashboard' module
    This returns the names and URLs of adjacent directories
    """
    return render_template("homescreen.html", tagname = 'home')



@dashboard.route('/delete/<setup>')
def delete_setup(setup):
    """
    Render the thing description deletion page for the 'dashboard' module
    """
    nsrv_obj = Neo4jService()
    all_setups = nsrv_obj.run_q("MATCH (n)-[:belongsTo]->(m) RETURN m", {})
    setups_json = all_setups.data()
    setups_labels = list(set([list(node['m'].labels)[0] for node in setups_json]))
    nodes = list()
    if setups_labels:
        nodes = nsrv_obj.run_q("MATCH (n)-[:belongsTo]->(m) where m.name=$setup RETURN n", {"setup":setup}).data()
    clean_nodes = [node['n'] for node in nodes]
    return render_template("delete.html", tagname = 'delete', setup = setup, setup_nodes = clean_nodes, setups_labels = setups_labels)

@dashboard.route('/delete')
def delete():
    """
    Render the thing description deletion page for the 'dashboard' module
    """
    nsrv_obj = Neo4jService()
    all_setups = nsrv_obj.run_q("MATCH (n)-[:belongsTo]->(m) RETURN m", {})
    setups_json = all_setups.data()
    setups_labels = list(set([list(node['m'].labels)[0] for node in setups_json]))
    # for setup in setups_labels:
    nodes = list()
    if setups_labels:
        nodes = nsrv_obj.run_q("MATCH (n)-[:belongsTo]->(m) where m.name=$setup RETURN n", {"setup":setups_labels[0]}).data()
    clean_nodes = [node['n'] for node in nodes]
    return render_template("delete.html", tagname = 'delete', setup = setups_labels[0] if setups_labels else "", setup_nodes = clean_nodes, setups_labels = setups_labels)

@dashboard.route('/register')
def register():
    """
    Render the thing description register page for the 'dashboard' module
    """
    return render_template('register.html', tagname = 'register')

@dashboard.route('/register2')
def register2():
    """
    Render the thing description register page for the 'dashboard' module
    """
    return render_template('register2.html', tagname = 'register2')

@dashboard.route('/delete2')
def delete2():
    """
    Render the delete page for the 'dashboard' module
    """
    mongo_service = MongoService()
    things = mongo_service.find_things(None)
    thing_ids = [thing["id"] for thing in things]
    return render_template('delete2.html', tagname = 'delete2', thing_ids=thing_ids)

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
@dashboard.route('/thinglist')
def thinglist():

    mongo_service = MongoService()
    things = mongo_service.find_things(None)
    thing_ids = {thing["id"]: {"title": thing["title"]} for thing in things}
    return render_template('thinglist.html', tagname = 'thinglist', thing_ids = thing_ids)



@dashboard.route('/addDevice')
def addDevice():
    return render_template('addDevice.html', tagname='addDevice')

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
        # Get notifications data from database or other source
        mongo_service= MongoService()
#        notifications = mongo_service.get_notifications(None)
 #       notification_ids = {notification["number"]: {"content": notification["content"], "time": notification["time"], "date": notification["date"]} for notification in notifications}

        return render_template('notifications.html', tagname= 'notifications')



@dashboard.route('/command')
def command():
    """
    Render the command page for the 'dashboard' module
    """
    return render_template('command.html', tagname = 'command')
