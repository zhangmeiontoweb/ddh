from SPARQLWrapper import SPARQLWrapper,JSON
import csv
import json

sparql = SPARQLWrapper("https://dbpedia.org/sparql")

def main(entity,predicate):
    return get_sparql(entity,predicate,len(predicate))


def get_sparql(entity,predicate,l):
    fin_res = list()
    fin_qu = list()
    out_qu1 = extend_tree(True, entity[0]['uri'], predicate)
    in_qu1 = extend_tree(False, entity[0]['uri'], predicate)
    if len(out_qu1)>0:
        qu1 = out_qu1
    else:
        qu1 = in_qu1
    r1, q1 = get_result(qu1)
    print("q1:"+q1)
    fin_qu.append(q1)
    if l == 1:
        fin_res = r1
    elif l >1:
        if len(entity)>1:
            out_qu2 = extend_tree(True,entity[1]['uri'],predicate)
            in_qu2 = extend_tree(False,entity[1]['uri'],predicate)
            if len(out_qu2)==0 and len(in_qu2) ==0:
                out_qu2 = extend_tree(True, r1, predicate)
                in_qu2 = extend_tree(False, r1, predicate)
                if len(out_qu2) > 0:
                    qu2 = out_qu2
                else:
                    qu2 = in_qu2
                r2, q2 = get_result(qu2)
                fin_res = r2
                fin_qu.append(q2)
            else:
                if len(out_qu2) > 0:
                    qu2 = out_qu2
                else:
                    qu2 = in_qu2
                r2, q2 = get_result(qu2)
                fin_res = [x for x in r1 if x in r2]
                fin_qu.append(q2)
        else:
            out_qu2 = extend_tree(True, r1, predicate)
            in_qu2 = extend_tree(False, r1, predicate)
            if len(out_qu2) > 0:
                qu2 = out_qu2
            else:
                qu2 = in_qu2
            r2, q2 = get_result(qu2)
            fin_res = r2
            fin_qu.append(q2)

    return fin_res,fin_qu

def get_result(query_re):
    print(query_re)
    fin_result = list()
    fin_query = ''
    query_list = query_re['query'].split('?x')
    i = 1
    query_list[0] = query_list[0] + '?x'
    while i < len(query_list) - 1:
        query_list[i] = query_list[i] + '<' + query_re['p'] + '>'
        i = i + 1
    query = ''.join(query_list).replace('?e', '?x')
    fin_query = query
    fin_result = execute_sparql(query)
    print(query)
    print(fin_result)

    return  fin_result,fin_query

def extend_tree(out,entity,predicate):
    edge = dict()
    if isinstance(entity,list):
        values = ""
        for e in entity:
            values = values+"<"+ e+">"+" "
    else:
        values ="<" + entity + ">"
    if out:
        query = "SELECT distinct ?x WHERE { ?entity ?x ?e. VALUES ?entity {"+values+"}}"
        result = execute_sparql(query)
        for p in predicate:
            if p['uri'] in result:
                edge['p'] = p['uri']
                edge['query'] = query
        print(result)
    else:
        query = "SELECT distinct ?x WHERE { ?e ?x ?entity VALUES ?entity {" + values + "}}"
        result = execute_sparql(query)
        for p in predicate:
            if p['uri'] in result:
                edge['p'] = p['uri']
                edge['query'] = query
        # print(result)
    return edge

def execute_sparql(query):
    re = list()
    try:
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if results is None:
            return re
        else:
            for x in results['results']['bindings']:
                re.append(x['x']['value'])
            return re
    except:
        return re

if __name__ == "__main__":
    # question = "What is the currency of Republic of Montenegro (1992-2006) ?"
    # query = "SELECT DISTINCT ?uri WHERE { <http://dbpedia.org/resource/Harding_Academy_(Memphis)> <http://dbpedia.org/property/nickname> ?uri. <http://dbpedia.org/resource/Lyons_Township_High_School> <http://dbpedia.org/property/nickname> ?uri . }"
    # entity = [
    #   {
    #     "label": "Republic of Montenegro",
    #     "uri": "http://dbpedia.org/resource/Republic_of_Montenegro_(1992–2006)"
    #   }
    # ]
    # predicate = [
    #   {
    #     "label": "currency",
    #     "uri": "http://dbpedia.org/property/currency"
    #   }
    # ]
    # print(main(entity,predicate))
    print(execute_sparql("SELECT distinct ?x WHERE { ?x <http://dbpedia.org/ontology/company> ?xntity VALUES ?xntity {<http://dbpedia.org/resource/DreamWorks_Television>}}"))
    # qus = list()
    # labels = list()
    # f = open("test_paper.txt", "w", encoding="UTF-8")
    # with open('test2.csv', 'r') as file_csv:
    #     file_input = csv.reader(file_csv)
    #     for obj in file_input:
    #         qus.append(obj[1])
    #         labels.append(obj[2])
    # qus = qus[:40]
    # with open("FullyAnnotated_LCQuAD5000left.json", "r", encoding='UTF-8') as load_f:
    #     file_obj = json.load(load_f)
    #     i = 1
    #     for quObj in file_obj:
    #         if quObj['question'] in qus:
    #             try:
    #                 ind = qus.index(quObj['question'])
    #                 label = int(labels[ind])
    #                 query = quObj['sparql_query']
    #                 entity = quObj['entity mapping']
    #                 predicate = quObj['predicate mapping']
    #                 fin_res,fin_query = main(entity,predicate)
    #                 # print(fin_query)
    #                 f.write(str(i) + "\n\r")
    #                 f.write("question: " + quObj['question'] + "\n\r")
    #                 f.write("label: " + str(label) + "\n\r")
    #                 f.write("sparql: " + query + "\n\r")
    #                 f.write("test_sparql: " + str(fin_query) + "\n\r")
    #                 f.write("test_result: " + str(fin_res) + "\n\r\n\r")
    #             except:
    #                 continue
    #             i = i + 1
    #         else:
    #             continue