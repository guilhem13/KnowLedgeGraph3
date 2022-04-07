# Arxiv ontology API 

It's a simple API which can : 
- return entities of an uploading pdf thanks to AWS comprehend Service(front)
- return ontology made with 500 papers in zip format (front)
- manage the sqlachemey arxiv database 's(front)
- Process papers to generate ontology (back)

***

### Features included 

 *  Feature 1 : return entities of an uploading pdf
      * Endpoint : /getner
      * Type : POST
 *  Feature 2 : get ontology made with 500 papers  
      * Endpoint : /get/ontology
      * Type : GET
 *  Feature 3 : get the size of the database
      * Endpoint : /arxiv/sizebdd
      * Type : GET
 *  Feature 4 : get the ontology made by the TLA pipeline directly from arxiv API with X papers
      * Endpoint : /arxiv/pipeline/
      * Type : GET 

***
## Installation 

Code has been made with Python 3.8.10

Create a virtualenv and activate it if virtual environment not there:

```shell
python3 -m venv venv
. venv/bin/activate
```
Install Packages 

```shell
pip install -r requirements.txt
```

***
## Run 

In production 

```shell
python3 app.py
```
In developement 

```shell
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```
if flask run doesn't work make : 

```shell
python -m flask run
```
***
## Run with docker

All features are available on dockerfile ** except the entrypoint getner with AWS ressources **.
Because it needs AWS credentials.  
### Installation

```shell
docker build -t projetpythonapi .
```
### Installation

```shell
docker run -d -p 5000:5000 projetpythonapi
```

***
## Usage

***

## Entrypoint /getner 
(This feature is not available with the dockerfile. For that you need to create a shared volume to put the "credentials file" at runtime 
like that => docker run -v $HOME/.aws/credentials:/home/app/.aws/credentials:ro projetpythonapi
)It's recommanded to not use the dockerfile to this entrypoint !


You have to add you AWS security token. For that: 
- Be sure to start your Lab
- Create a folder in your computer  => ~/.aws/ 
- Add a credentials file inside this folder 
- Then you have  ~/.aws/credentials
- Inside this credentials file add the content of the AWS CLI with vi or vim

The AWS CLI looks like that : 

```shell
[default]
aws_access_key_id=********
aws_secret_access_key=********
aws_session_token=**********
```
Once that, you can use this entrypoint 

You can watch the documentation with => http://localhost:5000/apidocs/

Usage of the entrypoint: 
- Directly by the web interface via http://localhost:5000/getner
- By curl 
```shell
curl -F 'file=@document.pdf' localhost:5000/getner
```

## Entrypoint /arxiv/sizebdd

- No requirements to do 
- It returns the size of database "bddarxiv.db"
- It's documentation is available on http://localhost:5000/apidocs/

## Entrypoint /arxiv/feedbdd/<nb_paper>
- No requirements to do 
- Update the database (add more papers) inside the database by specifing the number of papers to add
- It's documentation is available on http://localhost:5000/apidocs/

## Entrypoint /get/onotlogy
- No requirements to do 
- It returns the ontology file main by the backend script main.py with XXX papers. 
- It's documentation is available on http://localhost:5000/apidocs/

## Entrypoint /arxiv/pipeline/
- launch Cermine by doing 
```shell
docker run -p 8072:8080 elifesciences/cermine:1.13
```
- the ontology made by the TLA pipeline directly from arxiv API with X papers
- It's documentation is available on http://localhost:5000/apidocs/


### Launch the main.py backend script which generates the ontology file for X papers

- 1) Check if the port 5000 is available
- 2) You have to launch the ServiceNer webservice. The procedure is available on its Readme.md file with docker 
- 3) You also have to launch the Cermine by doing.
```shell
docker run -p 8072:8080 elifesciences/cermine:1.13
```
- Launch the backend script by doing => python3 main.py - i X

Where X is the number of papers to process to create the ontology

ServicerNER and App are not supposed being run in the same time on the same computer because they have the same port !

