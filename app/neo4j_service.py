''' 
Currently not being used, we will use models to query
'''

import json
from py2neo import data, Graph, NodeMatcher, Node, Relationship, RelationshipMatcher, database

class Neo4jService(object):
    """
    This object provides a set of helper methods for creating and retrieving nodes and relationships from
    a Neo4j database holding information about players, teams, fans, comments and their relationships.
    """

    # Note:
    # I tend to avoid object mapping frameworks. Object mapping frameworks are fun in the beginning
    # but tend to be annoying after a while. So, I did not create types Player, Team, etc.
    #


    # Connects to the DB and sets a Graph instance variable.
    # Also creates a NodeMatcher and RelationshipMatcher, which are a py2neo framework classes.
    def __init__(self,  auth=('neo4j', 'password'), host='localhost', port=7687, secure=False, ):
        self._graph = Graph(secure=secure,
                            bolt=True,
                            auth=auth,
                            host=host,
                            port=port)
        self._node_matcher = NodeMatcher(self._graph)
        self._relationship_matcher = RelationshipMatcher(self._graph)

    def run_q(self, qs, args):
        """

        :param qs: Query string that may have {} slots for parameters.
        :param args: Dictionary of parameters to insert into query string.
        :return:  Result of the query, which executes as a single, standalone transaction.
        """
        try:
            tx = self._graph.begin(autocommit=False)
            result = self._graph.run(qs, args)
            return result
        except Exception as e:
            print("Run exaception = ", e)

    def run_match(self, labels=None, properties=None):
        """
        Uses a NodeMatcher to find a node matching a "template."
        :param labels: A list of labels that the node must have.
        :param properties: A dictionary of {property_name: property_value} defining the template that the
            node must match.
        :return: An array of Node objects matching the pattern.
        """
        #ut.debug_message("Labels = ", labels)
        #ut.debug_message("Properties = ", json.dumps(properties))
        print("Labels = ", labels)
        print("Properties = ", json.dumps(properties))
        if labels is not None and properties is not None:
            result = self._node_matcher.match(labels, **properties)
        elif labels is not None and properties is None:
            result = self._node_matcher.match(labels)
        elif labels is None and properties is not None:
            result = self._node_matcher.match(**properties)
        else:
            raise ValueError("Invalid request. Labels and properties cannot both be None.")

        # Convert NodeMatch data into a simple list of Nodes.
        full_result = []
        for r in result:
            full_result.append(r)

        return full_result

    def find_nodes_by_template(self, label, tmp):
        """

        :param tmp: A template defining the label and properties for Nodes to return. An
         example is { "label": "Fan", "template" { "last_name": "Raj", "first_name": "Deepak" }}
        :return: A list of Nodes matching the template.
        """
        labels = label
        props = tmp
        result = self.run_match(labels=labels, properties=props)
        return result

    def convert_nested_json_to_str(self, data):
        newdata = {}
        for key, value in data.items():
            if type(value) == dict:
                newdata[key] = json.dumps(value)
            else:
                newdata[key] = value
        return newdata

    def create_node(self, label, **kwargs):
        cleandata = self.convert_nested_json_to_str(kwargs)
        n = Node(label, **cleandata)
        tx = self._graph.begin(autocommit=True)
        tx.create(n)
        return n

    def delete_node(self, node):
        tx = self._graph.begin(autocommit=True)
        tx.delete(node)
        return True

    def create_relationship(self, source_a, relationship, source_b):
        rl = Relationship(source_a, relationship, source_b)
        # tx = self._graph.begin(autocommit=True)
        self._graph.create(rl)
        return rl

    def find_relationships(self, source_label, source_id, relationship, template):

        # cypher = "MATCH (:%s {manager_id: '%s'}) - [%s] - (end_node) RETURN end_node" % (source_label, source_id, relationship)
        cypher = "MATCH (:%s {thing_id: '%s'}) - [%s:%s] - (end_node) RETURN end_node" % (source_label, source_id, relationship, relationship)
        results = self._graph.run(cypher)
        return [dict(row["end_node"]) for row in results]