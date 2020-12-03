# DeployApp
This is a code that deploy a Machine Learning Model using [Flask](https://palletsprojects.com/p/flask/), [Docker](https://www.docker.com/) and [CloudFoundry](https://www.ibm.com/cloud/cloud-foundry)

The steps for the deployment are in this link, 
[deploy-a-python-machine-learning-model-as-a-web-service/](https://developer.ibm.com/technologies/artificial-intelligence/tutorials/deploy-a-python-machine-learning-model-as-a-web-service/) 

However the link have some outdated issues, so here is a kind of template to deploy the machine learning model as an app.
Note this steps are done assuming you got a windows machines.

## File Structure 

The repo contain the following information 
   - app.py           :  python flask application that call the model
   - clf.pkl          :  binary model  
   - manifest.yml     :  the [manifest](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest.html) to deploy the solution
   - requirements.txt :  python libraries need it to run the application
   - runtime.txt      :  the python enviroment to run the application
   - Dockerfile       :  the [dockerfile](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/) to buil your docker image


# Machine Learning model
The model is already saved as *.pkl*, the name is clf, we are not getting into detail  about how the model was build. But you could follow the [link](https://developer.ibm.com/technologies/artificial-intelligence/tutorials/deploy-a-python-machine-learning-model-as-a-web-service/) and create your own.

This model will recieve 19 features input and will return 0 or 1. 


# Expose the model as a web service (Python Flask)
Exposing the model as a web service can be done by creating a Python Flask application with an endpoint that can take a JSON body of features and return a prediction based on those features.

The code is in `app.py` 
Inline-style: 
![Image](./images/APP.png?raw=true)

# Runing the App Locally
to make sure everything is working properly run your Python application from the terminal or your Python IDE. From the terminal, run the following command:
```
$ python app.py
```
If you see something like the images bellow the code is running properly and you can test it now, make sure you are running inside your ´DeployApp´ directory

![Image](./images/APP_call.png?raw=true)

Next step is to actually run the application.

Please coppy this code in your terminal window to test it

```
$ Invoke-RestMethod -Method POST -Uri http://localhost:9099/predict -Body '{"features":[2.0,0.0,6.0,0.0,20.0,17.0,17.0,13.0,-999.0,0.0,5.0,8.0,57.0,59.0,58.0,0.0,2.0,3.0,21278.8]}'
```

If you see the results bellow you succefully run your application

![Image](./images/APP_test.png?raw=true)

In some situations dependencies are needed to be resolved locally

known dependencies:

**lightgbm**   
```
pip install lightgbm
```

# Configure Docker for deployment
To configure the Docker you need 2 files, the  `Dockerfile`, the application dependencies defined in the `requirements.txt` , this docker file was built for a linux machine, you could build your own by following the instruction.

Note: The machine learning model requiered the `libgmp1` to be able to run.

![Image](./images/APP_doc.png?raw=true)

## Create the Docker configuration

For this step, make sure you have a docker account and that you are logged in, also that you are on `DeployApp` directory, we are going to call the application `python-ml-service` and do the following:

```
$ docker image build -t <your-docker-user-name>/python-ml-service .
```

After you built it, you can push that image to you Docker Hub, so it can be reused by you our anyone else that have access to your repository. For example team members. To do that just type:

```
$ docker push <your-docker-user-name>/python-ml-service
```
## Test the Docker configuration  
Then, to run it and see if your docker image in a defined port ( we choose in the python code to run in 9099), do the following:

```
$ docker run -d -p 9099 <your-docker-user-name>/python-ml-service
$ docker ps
```
You shoud get something like this 

![Image](./images/APP_doc_test2.png?raw=true)

Look for the values in the PORT column and you should see something similar to "0.0.0.0:32769->9099/tcp" and run the following command:
  
```
$Invoke-RestMethod -Method POST -Uri http://localhost:32768/predict -Body '{"features":[2.0,0.0,6.0,0.0,20.0,17.0,17.0,13.0,-999.0,0.0,5.0,8.0,57.0,59.0,58.0,0.0,2.0,3.0,21278.8]}'
```
 
 And a predicion value should show up. Everything went well and you are ready to deploy it in IBM Cloud Foundary Apps! :-)
 

# Configure the Cloud Foundry Docker deployment 
What we want is acutally to create an API tha runs on the cloud, so client can have acces to it. To do it using Cloud Foundry we need a YAML `manifestfile`  and the `runtime.txt`, 

## Create manifest file 
Manifests provide consistency and reproducibility, and can help you automate deploying apps, more info [here](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest.html)

For this application this how you create the manisfest file, from the docker image

![Image](./images/APP_yml.png?raw=true)


Note: the .yml file is very sisentive to tabs and spaces, there is an actuall application that help you to check if the file is properly set or not [YAML Lint](http://www.yamllint.com/)

# Deploy the application from the CLI

## Test the deployment

To do this step, you need to have the IBM Cloud CLI.
 First step, you need to login an target the Cloud Foundary
 
```
$ ibmcloud login 
```
 
 (As an alternative to this, you can use ` $ ibmcloud login -sso ` which will generate you a code on the web)
 
 Now, go to https://cloud.ibm.com/iam/apikeys and create an IBM Could API Key and copy the API key.
 Then go back to the console and do the following:
 
```
$ ibmcloud target --cf <api-key>
```

 If it gives an error, it's ok, type again the following and all should be fine.
 
```
$ ibmcloud target --cf
```
 
 Now you are ready to push your application to Cloud Foundry, for this particular case the application required bigger disk quote than the default so you have to allocate the space by using -k command, for this case 2GB was enough:
 
 ```
 $ ibmcloud cf push -k 2G
 ```

 
 Last but not least, you can make your predictions with a POST with the following command:

```
  $ Invoke-RestMethod -Method POST -Uri http://<HOSTNAME>.<REGION>.mybluemix.net/predict - Body '{"features":[2.0,0.0,6.0,0.0,20.0,17.0,17.0,13.0,-999.0,0.0,5.0,8.0,57.0,59.0,58.0,0.0,2.0,3.0,21278.8]}'
```

And there you have your prediction :-D

# Check if the application is running
Now log into your ibmcloud account and go to (https://cloud.ibm.com/cloudfoundry/public)

You will see you app running, and from there you are free to do whatever you want. 

![Image](./images/AP_running.png?raw=true)



















