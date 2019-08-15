# wordweb-import

This project contain scripts for extracting data from hyperhamlet and finally to import it to [Knora](https://www.knora.org/). Before this can be done you have to do the following steps first:
1. Export the database from [Hyperhamlet](http://www.hyperhamlet.unibas.ch/phpMyAdmin) via phpMyAdmin and import it into a mySQL database that should run on your local machine.
2. Make sure KNORA is running also on your local machine.
3. Install python3 if you don't have it

 
Creating Ontology and importing resources:

1. ./graphdb-se-docker-init-knora-test-minimal.sh (in Tab 1 of Terminal)  
2. sbt (in Tab 2 of Terminal)  
3. dockerComposeUp / dockerComposeRestart (in Tab 2 of Terminal)

## How to use this project


Load the data model definition file to Knora so it will create the ontology: 
```
$ knora-create-ontology wordweb_data_model_definition.json
```
Run the initial script:
```
$ python3 start_import.py
```
