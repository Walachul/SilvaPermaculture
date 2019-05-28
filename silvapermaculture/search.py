from silvapermaculture import app
#This module is created for interaction with the Elasticsearch index

#Function that adds element to the index of Elasticsearch. Uses model as the SQLAlchemy model
def add_element_index(index,model):
    #Check to see if Elasticsearch server is configured or not.
    #The application runs witouth errors if the Elasticsearch server doesn't run.
    if not app.elasticsearch:
        return
    payload={}
    for field in model.__searchit__:
        payload[field] = getattr(model,field)
    app.elasticsearch.index(index=index, doc_type=index, id=model.id,
                            body=payload)

#Function that removes indexed elements. Uses model as the SQLAlchemy model
def remove_element_from_index(index,model):
    if not app.elasticsearch:
        return
    app.elasticsearch.delete(index=index, doc_type=index, id=model.id)

#Function that searches the fields specified to be searched in
#the models.py with the variable __searchit_
def search_index(index,query,page,per_page):
    if not app.elasticsearch:
        return [], 0
    search = app.elasticsearch.search(index=index, doc_type=index,
                                      body={'query':{'multi_match':{'query':query, 'fields': ['*']}},
                                            'from':(page -1)*per_page, 'size':per_page})
    #List comprehension used to get the IDs of elements found
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    #Return IDS and total number of elements from the elasticsearch
    return ids, search['hits']['total']
