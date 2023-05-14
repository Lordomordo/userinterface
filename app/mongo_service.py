from pymongo import MongoClient

class MongoService(object):
    def __init__(self):
        atlas_uri = "mongodb://Kleriakanus:test123@ac-s2miieu-shard-00-00.s0mnged.mongodb.net:27017,ac-s2miieu-shard-00-01.s0mnged.mongodb.net:27017,ac-s2miieu-shard-00-02.s0mnged.mongodb.net:27017/?ssl=true&replicaSet=atlas-vihgip-shard-0&authSource=admin&retryWrites=true&w=majority"
        db_name = 'Cluster0'
        self.client = MongoClient(atlas_uri)
        self.database = self.client[db_name]

    def create_policy(self, policy):
        new_policy = self.database["policies"].insert_one(policy)

    def create_thing(self, thing):
        new_thing = self.database["things"].insert_one(thing)
    
    def delete_thing(self, thing_id):
        query = {"id": thing_id}
        things = self.database["things"]
        things.delete_one(query)

    def find_policies(self, criteria):
        policies = self.database["policies"].find(criteria)
        return policies
    
    def find_things(self, criteria):
        things = self.database["things"].find(criteria)
        return things

    def drop_collection(self, name):
        collection = self.database[name]
        collection.drop()

    def get_notifications(self, criteria):
        notifications = self.database["notifications"].find(criteria)
        return notifications