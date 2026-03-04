# Knowledge Graph Design (Neo4j)

## Node Label
- `:Concept {name, domain, difficulty}`

## Relationship
- `(:Concept)-[:PREREQUISITE_FOR]->(:Concept)`

## Sample Cypher
```cypher
MERGE (a:Concept {name: 'Algebra'})
MERGE (f:Concept {name: 'Functions'})
MERGE (c:Concept {name: 'Calculus'})
MERGE (a)-[:PREREQUISITE_FOR]->(f)
MERGE (f)-[:PREREQUISITE_FOR]->(c)
MERGE (a)-[:PREREQUISITE_FOR]->(c);
```

## Root-Cause Query
```cypher
MATCH (p:Concept)-[:PREREQUISITE_FOR]->(t:Concept {name: $target})
RETURN p.name AS prerequisite;
```
