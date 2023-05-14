# Policy DB Implementation (Fall 22)

This project is to implement policy DB by storing policies in DB, and alert users when potential there is a potential conflit in a command before it is being excuted. 


## To Bootstrap the Project
### Create MongoDB cluster

Create and Atlas account from Atlas UI using the steps in https://www.mongodb.com/docs/atlas/getting-started/ and deploy MongoDB cluster from the previous page. Once the setup is done get the PyMongo connection link to this DB by clicking 'Connect' on the DB deployment and choosing the connection as MongoDB Drivers -> Python 3.6

Helpful Tip: When adding IP address to trusted list for the cluster, add 0.0.0.0/0 to allow access from any IP address

Once the above setup is done, go to `app/mongo_service.py` and change the atlas connection URI

      atlas_uri = "xxxxxxx"
      db_name = 'xxxxxx'

db_name can be specified as anything and when the app is running it would create db with this name and 'things' and 'policies' collections once you register a thing or policy

You might also want to setup neo4j db if you intend to use the old project to LinkingIOT by following the steps in previous project.

### Install dependencies and run Flask app
Once the above is done, you can create a virtual environment (e.g., python3 venv or similar) to install dependencies and run the flask app.

run the command `pip install setuptools==58`

Install dependencies by running `pip install -r requirements.txt` under app directory.

If you are facing issues with building wheel for cryptography due to open ssl issue then set these flags and retry the installation (might be an issue only in Apple Silicon)

  `export LDFLAGS="-L/opt/homebrew/opt/openssl@1.1/lib"`
  
  `export CPPFLAGS="-I/opt/homebrew/opt/openssl@1.1/include"`

Start the app by running `python3 new_app.py`

If you also want to run the old project then use `python3 app.py` along with neo4j installation and steps from previous project

For registration of things and policies. Open `http://127.0.0.1:5000/`. Use the things directory under policy_db_setup for registering things, policies directory under policies for registering policies in the respective UI.

If you are facing issues with certificate verification, you may set `tlsAllowInvalidCertificates=True` in `MongoClient` for testing purpose, or you may [install `certifi`](https://stackoverflow.com/questions/68123923/pymongo-ssl-certificate-verify-failed-certificate-verify-failed-unable-to-ge). 

### Run the command
To check a command, upload a command in json format and click Execute. Use the command*.json in commands directory under policy_db_setup directory.

command1.json should ask the user to double check and command2.json and command3.json should deny the user request with an alert message.
