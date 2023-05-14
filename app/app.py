from flask import Flask
from views.api import api
from views.policy_api import policy_api
from views.dashboard import dashboard
from config import config_dict
from neomodel import install_labels
from models import * 

def main(init_db=True, debug=True, host='localhost'):
    app = Flask(__name__)
    app.register_blueprint(dashboard, url_prefix = '/')
    app.register_blueprint(api, url_prefix = '/api')
    app.register_blueprint(api, url_prefix = '/policy_api')
    app.config.update(**config_dict)
    print(app.config)
    # Initialize all constraints in DB
    install_labels(ThingDescription) 
    app.run(debug = debug, host= host, port= app.config["server_port"])

if __name__ == "__main__":
    main()