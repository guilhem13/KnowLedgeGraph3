# Arxiv ontology API 

It's a simple API which can : 
- return entities of an uploading pdf thanks to AWS comprehend Service(front)
- return ontology made with 1000 papers in zip format (front)
- manage arxiv database 's API  (front)
- Process papers to generate ontology (back)

***

### Features included 

 *  Feature 1 : return entities of an uploading pdf
      * Endpoint : /getner
      * Type : POST
 *  Feature 2 : get ontology made with 1000 papers  
      * Endpoint : /get/ontology
      * Type : GET
 *  Feature 3 : get the size of the database
      * Endpoint : /arxiv/sizebdd
      * Type : GET
 *  Feature 4 : get the size of the database
      * Endpoint : /arxiv/sizebdd
      * Type : GET 

***
## Installation 

Code has been made with Python 3.8.10

Create a virtualenv and activate it:

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
python3 webapp.py
```
In developement 

```shell
export FLASK_APP=webapp.py
export FLASK_ENV=development
flask run
```
if flask run doesn't work make : 

```shell
python -m flask run
```
***
## Run with docker

All feature are available on dockerfile excep the entrypoint getner with AWS ressources.  
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
(This feature is not available with the dockerfile.)

You have to add you AWS security token. For that: 
- Be sure to start your Lab
- Create a folder in your computer  => ~/.aws/ 
- Add a credentials file inside this folder 
- Then you have  ~/.aws/credentials
- Inside this credentials file add the content of the AWS CLI with vi or vim

The cloud access aws looks like that : 

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

No requirements to do 
It returns the size of database "bddarxiv.db"
It's documentation is available on http://localhost:5000/apidocs/

## Entrypoint /arxiv/feedbdd/<nb_paper>
No requirements to do 
Update the database (add more papers) inside the database by specifing the number of papers to add
It's documentation is available on http://localhost:5000/apidocs/

## Entrypoint /get/onotlogy
no requirements to do 
It returns the ontology file main by the backend script main.py with XXX papers. 
It's documentation is available on http://localhost:5000/apidocs/

### Launch the main.py backend script which generates the ontology file 

You have to launch the ServiceNer webservice. The procedure is available on its Readme.md file 
You also have to launch the Cermine by doing.

```shell
docker run -p 8072:8080 elifesciences/cermine:1.13
```
launch the script by doing => python3 main.py - i X
Where X is the number od papers to process to create the ontology
## Entrypoint /arxiv/pipeline/<nb_paper>

No requirements to do 
It's documentation is available on http://localhost:5000/apidocs/
