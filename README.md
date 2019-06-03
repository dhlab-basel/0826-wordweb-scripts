# wordweb-import


Creating Ontology and importing resources:

1. ./graphdb-se-docker-init-knora-test-minimal.sh (in Tab 1 of Terminal)  
2. sbt (in Tab 2 of Terminal)  
3. dockerComposeUp / dockerComposeRestart (in Tab 2 of Terminal)


4. knora-create-ontology wordweb_data_model_definition.json  
5. python3 wordweb_create-resource.py
