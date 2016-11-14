import facebook
import requests

def get_all_friends(token ,allFriends):
    graph=facebook.GraphAPI(token)
    friends=graph.get_object('me/friends',fields='id,name,location')

    while (True):
        for friend in friends['data']:
            try:
                name=friend["name"]
                loc=friend["location"]["name"]
                allFriends[friend["id"]]={
                    "name":name,
                    "location":loc,
                }
            except KeyError:
                pass
        try:   friends=requests.get(friends['paging']['next']).json()
        except KeyError:
            break

    return allFriends

def create_friends_instances(friends):
    instances = []
    instances.append("<?xml version=\"1.0\"?>\n")
    instances.append("<!DOCTYPE rdf:RDF [\n")
    instances.append("\t <!ENTITY owl \"http://www.w3.org/2002/07/owl#\" > \n")
    instances.append("\t <!ENTITY xsd \"http://www.w3.org/2001/XMLSchema#\" > \n")
    instances.append("\t <!ENTITY rdfs \"http://www.w3.org/2000/01/rdf-schema#\" > \n")
    instances.append("\t <!ENTITY rdf \"http://www.w3.org/1999/02/22-rdf-syntax-ns#\" > \n")
    instances.append("\t <!ENTITY sc \"http://www.semanticweb.org/ontologies/2016/12/Yatra\" > \n")
    instances.append("]> \n")
    instances.append("<rdf:RDF\n")
    instances.append("\t xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\" \n")
    instances.append("\t xmlns:rdfs=\"http://www.w3.org/2000/01/rdf-schema#\" \n")
    instances.append("\t xmlns:owl=\"http://www.w3.org/2002/07/owl#\" \n")
    instances.append("\t xmlns:xsd=\"http://www.w3.org/2001/XMLSchema#\" \n")
    instances.append("\t xmlns:sc=\"http://www.semanticweb.org/ontologies/2016/12/Yatra\">\n\n")

    for key, friend in friends.iteritems():
        instances.append(create_friend_rdf(friend, key))

    instances.append("</rdf:RDF>")
    return "".join(instances)


def create_friend_rdf(friend, i):
    rdf = []
    rdf.append("\t <NamedIndividual rdf:about=\"&sc;person" + str(i) + "\">\n")
    rdf.append("\t <rdf:type rdf:resource=\"&sc;Person\"/>\n")
    rdf.append("\t <sc:hasName rdf:datatype=\"&xsd;string\">" + friend["name"] + "</sc:hasName>\n")
    rdf.append("\t <sc:hasLocation rdf:datatype=\"&xsd;string\">" + friend["location"] + "</sc:hasLocation>\n")
    rdf.append("\t <sc:isFriendOf rdf:resource=\"&sc;person26\"/>\n")
    rdf.append("\t </NamedIndividual>\n\n")
    return "".join(rdf)


if __name__ == "__main__":
    tokens = [
        'EAACEdEose0cBABEjFHxGa7REOzDAxeHufPIW6ZAKIAKNkm52ZCq9so6QamY35rPbj0ZBa3BgwL2D7vOrh0HLNmulyD53BkZBsiIZB6rGpTqF8noCuZAh0gt9HnOgjEX1ZAQsyfMGJbzMTnSsJX8bZCW3059mMTRsEJQLEMx3KkW8ZCwZDZD']
    allFriends = {}
    for token in tokens:
        get_all_friends(token, allFriends)

        instances = create_friends_instances(allFriends)
        print instances
        text_file = open("friends.rdf", "w")
        text_file.write(instances)
        text_file.close()

