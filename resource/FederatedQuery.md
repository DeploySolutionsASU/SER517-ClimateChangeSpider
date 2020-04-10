The data from one SPARQL end point can be used to query the data of the other SPARQL endpoint.
This can be done using a query type called the federated query.
Federated Query helps in taking a query and provide a solution based on the information from 
many different sources.

The federated query can be implemented in top-to-bottom order. In this top-to-down order approach,
if the variable is above the invocation of a remote source, then that variable is passed as a 
parameter to the source. 

The federated query is built using the SERVICE keyword. This keyword helps in taking the whole query
inside the SERVICE as a whole and executes the query. If a subquery in a SPARQL query is labeled with 
"SERVICE" then this means that the subquery should be sent as a whole, without attempts of dividing 
it into smaller fragments and that two SERVICE group patters or sub queries should not be merged into
single request.

An example of a federated query is as follows : 
PREFIX place: <http://www.semanticweb.org/aj/ontologies/2019/10/Place#>
select ?place_name ?acc_name ?acc_rating ?acc_review
where {
  ?subject place:name ?acc_name;
           place:rating ?acc_rating;
           place:review_text ?acc_review;
           place:ref_lat ?lat;
           place:ref_long ?lng.
  
  SERVICE <http://localhost:3030//placeDetails/sparql>{
	SELECT distinct ?place_name ?lat ?lng
	WHERE {
  		?subject place:name "Arizona State University, Tempe Campus";
           place:name ?place_name;
           place:geometry_lat ?lat;
           place:geometry_lng ?lng.
  } 
  }  
}
LIMIT 1000

Explanation : 
The inner most query with in the SERVICE gets executed first bi hitting the end point of the dataset and the 
results of that query will be used for the execution of the outer query.
