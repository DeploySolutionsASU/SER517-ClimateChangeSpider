**************************  N-Quads ***************************
N-Quads statements consist of a sequence of terms like subject, predicate, object and graph 
label of an RDF triple and the graph is a part of the dataset. The sequence of these terms 
is terminated by a ‘.’ And a new line. All these terms are separated by white space. 
An example of N-Quags is as follows:
<http://example/subject > <http://example/predicate> <http://example/object> 
<http://example.com/graph> .
The IRIs of these terms are written only as absolute IRIs. These IRIs are enclosed with 
< and > signs.
There will be blank nodes in N-Quads. These blanks nodes are represented with _: and 
followed by a label which is represented as a series of characters. This blank node label 
is unique for each blank node.
Not only the subject, object can also have blank nodes in it.
An example of N-Quad with subject and object having blank node is:
_:abcdef <http://example.com/predicate> _:ghijkl <http://example.com/graph> .	

RESOURCE LINK:
https://www.w3.org/TR/2014/REC-n-quads-20140225/
