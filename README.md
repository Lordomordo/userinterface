# userinterface
This is the project for implementing a management system to manage policies for a IoT System.
To use the code provided here, a policy server is needed. The code for that is found in the following github project: https://github.com/hitext5/master_thesis_python.git

Whenever you want to start the management system you need a policy server. Therefore it should always be up and running before starting the code for the interface.

After cloning the code, you should add all the necessary requirements.

At the moment in the main.py file, there is a mongoDB selected as database for the project. In case you want to use your own, you should set up a new database and input the database in line 16 behind the atlas_uri. 
Afterwards you also have to change the database in the file "mongo_service.py", behind the atlas_uri again.

To start the programm, the new_app main method should be executed.
After doing so, in the console should pop up that the server has been started and if you click on the localhost, the interface will be opened on a new site.
From there on, you can use the system as you want to.
