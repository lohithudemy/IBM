# IBM
------------------------------------------
Below are the steps to deploy a Catalog-service web app along with Redis.
_**Took me approx 3hrs to setup and validate the application.**_

### Dockerize the Catalog-service Application:
------------------------------------------
1. Create a Workspace folder and copy source code along with the requirements here.
~~~
$mkdir IBM
~~~
2. Create a Dockerfile
~~~
FROM python:3.9

WORKDIR /code
#code will be the directory in the pod to the copy the files

COPY ./requirements.txt /code/requirements.txt
#Copy the text file to Pod working directory

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
#1 of best practice, --no-cache-dir, avoids caching the packages on to system.
# Also upgrade the packages

COPY ./main.py /code/
#Copy .py file to Pod Working directory

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
$command to run the fastapi webapp 
~~~
3. Build the image and push to dockerhub.
~~~
$docker build -t IBM_web_app .

$docker tag IBM_web_app:latest lohith007/IBM_web_app:latest

$docker push lohith007/IBM_web_app:latest
~~~
#### Below docker image is pulled for deploying Catalog-service

_lohith007/IBM_web_app_

### Setting up Kubernetes in GKE:
-----------------------------
1. Create a cluster in GKE under a project.
~~~
$gcloud container clusters create my-cluster --num-nodes=1 --zone us-central1-c
#gcloud creates a cluster with 1 node.(Without --num-nodes, by default 3 nodes will be created)
~~~	
2. Connecting to the Kubernetes clusters
~~~
$gcloud container clusters get-credentials my-cluster --zone us-central1-c --project <project-name>
~~~
3. Verify state and details of the Kubernetes cluster (Can be verified in Console as well)
~~~
$gcloud container clusters describe my-cluster --zone us-central1-c 
~~~
Once the cluster is ready, we can run the kubectl commands and start deploying the Redis and Catalog-service application.
First we shall deploy our Redis and Catalog-service application in "Staging" namespace. 
Once fully validated, we can proceed with our deployment in production namespace.

### Deploying Redis Database:
-------------------------
1. Creating Namespaces(staging/production) for our deployments
~~~
$kubectl create namespace staging
$kubectl create namespace production
~~~
2. Deploying a redis POD into the new namespace(staging)
~~~
$kubectl apply -f redis-deploy.yml --namespace=staging
$kubectl apply -f redis-service.yml --namespace=staging
~~~
3. Verify the deployment
~~~
$kubectl get deployments --namespace=staging
$kubectl get pods --namespace=staging
~~~
If any issues seen in the deployment, review the issue with following few commands.
~~~
$kubectl logs deployment/<deployment-name> --namespace=staging
**#This prints the pods (containers) logs to your terminal**

$kubectl describe pod <pod-name> --namespace=staging
**#This describes the current state of the pod and other vital details to validate.**

$kubectl logs pod <pod-name> --namespace=staging
#Gives pod logs

$kubectl logs pod <pod-name> --namespace=staging -c my-container <container-name>
#Gives pod container logs (stdout, multi-container case)
~~~	
4. Verify the Service deployment
~~~
$kubectl get services --namespace=staging
$kubectl get all --namespace=staging
#Shows details of all the deployed objects
~~~
5. Get the Redis connection string from the Redis POD.
~~~
Step1: kubectl exec -ti pod/<Redis Pod name> -- bash 
#logs into the pod to bash terminal
Step2: apt update
Step3: apt-get install dnsutils
Step4: nslookup <Service name>
~~~
EX:
~~~
nslookup redis 
#We need to give service name(redis) here
~~~
Server:         10.80.0.10
Address:        10.80.0.10:53

Name:   redis.staging.svc.cluster.local

Address: 10.80.7.133


If NO issues/errors, we should be good to proceed to Catalog-service application deployment

### Deploying the Catalog-service Web App:
--------------------------------------
1. Namespaces were created as part of Redis deployment. This is 1 time creation.

2. Deploying a Catalog-service server into the new namespace(staging)
~~~
$kubectl apply -f catalog-service-deploy.yml --namespace=staging
$kubectl apply -f catalog-app-service.yml --namespace=staging 
#Deploy the service file with type LoadBalancer for accessing the Webapplication from outside the GCP platform
~~~
3. Verify the deployment
~~~
$kubectl get deployments --namespace=staging
$kubectl get pods --namespace=staging
~~~
##### If any issues seen in the deployment, review the issue with following few commands.
~~~
$kubectl logs deployment/<deployment-name> --namespace=staging
#This prints the pods (containers) logs to your terminal

$kubectl describe pod <pod-name> --namespace=staging
#This describes the current state of the pod and other vital details to validate.

$kubectl logs <pod-name> --namespace=staging
#Gives pod logs

$kubectl logs pod <pod-name> --namespace=staging -c my-container <container-name>
#Gives pod container logs (stdout, multi-container case)
~~~	
4. Verify the Service deployment
~~~
$kubectl get services --namespace=staging
$kubectl get services -watch
#We can see when the "External IP" gets assigned to the Catalog-service app POD.
~~~	
5. We can access the Catalog-service WebApp from the browser:
~~~
$kubectl get service --namespace=staging
#Look for external IP w.r.t catalog servicename
~~~

Test the web application in the browser

**External IP**/docs

![image](https://user-images.githubusercontent.com/35722516/185856564-4b79f9d3-37bc-4782-830e-e8943650e77a.png)
![image](https://user-images.githubusercontent.com/35722516/185856933-b7f986dc-435d-4d7d-a723-9fb095f2b6fe.png)



