# Face Detection and Recognition

This repository contains code and resources for face detection and recognition project intended to be depoloyed on AWS cloud using jenkins pipeline and Terraform. 


## Introduction

In this project, we aim to develop a system for face detection and recognition using computer vision techniques that will be used later to be deployed on AWS or any cloud provider. The system will be able to detect faces in images or video streams and recognize the individuals based on their facial features. This code is splitted into 3 main parts to be deployed
1- Frontend (HTML, Css, javascript) and using and nginx server  ---> Docker image
2- Backend (Python, Flask, WSGI, OpenCV, bcrypt)   ----> Docker image
3- mongoDB for Authentication  ----> Cloud mongoDB (you can use local mongoDB through the setEnvVar.sh file)

![Solution diagram](https://github.com/ahmedd-mahmoudd/Face-detection-and-recognition/blob/WebUI/images/terraform.jpg)

## Installation

To Test this project locally, you need to install docker and docker-compose on your machine. 

### First
you need to set the environmnet variables and this can be done by running the setEnvVar.sh file (note: you might need to give it permission to run by running the following command: chmod +x ./backend/setEnvVar.sh) by running the following command:

```bash
source ./setEnvVar.sh
```
### Second
you need to build the docker images for the frontend and backend by running the following command:

```bash
docker-compose build
```
### Third
you need to run the docker images for the frontend and backend by running the following command:

```bash
docker-compose up
```

To run the project on AWS, you need to install Jenkins and Terraform on your machine and then you can use the Jenkinsfile and the terraform files to deploy the project on AWS.

### First

You will need to set the environment variables using the setEnvVar.sh file as mentioned above. and using jenkins credentials to store the dockerhub credentials.

### Second

Run the pipeline on Jenkins and the pipeline will build the docker images and push them to dockerhub. (Note: you need to change the dockerhub username in the Jenkinsfile)

### Third

Run the terraform files to deploy the project on AWS. (Note: you need to change the AWS credentials in the terraform files)

