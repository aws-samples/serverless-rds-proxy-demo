# serverless-rds-proxy-demo

This project contains source code and supporting files for a serverless application that you can deploy with the SAM CLI.

This project assumes you already have RDS Aurora Mysql cluster up and running. An RDS proxy instance
is also setup with force IAM authentication enabled. You can choose to create rds cluster with proxy following 
steps [below](#deploy-rds-aurora-cluster-with-rds-proxy) to have aurora cluster and 
RDS proxy setup.

## Architecture

![architecture.png](architecture.png) WIP


## Deploy the sample application

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

## Deploy RDS Aurora Cluster with RDS Proxy

This stack will take care of provisioning RDS Aurora Mysql along with RDS proxy fronting it inside
a VPC with 3 private subnet. Required parameters needed by [next step](#deploy-serverless-workload-using-rds-aurora-as-backend)
is also provided as stack output.

```bash
    sam build -t rds-with-proxy.yaml --use-container
    sam deploy -t rds-with-proxy.yaml --guided
```
## Deploy serverless workload using RDS Aurora as backend

To build and deploy your application for the first time, run the following in your shell:

```bash
    sam build --use-container
    sam deploy --guided
```


## Load testing

### Installing artillery

We will use [artillery](https://artillery.io/docs/guides/overview/welcome.html) to generate some load towards both the apis. 
Install Artillery via npm:

```
    npm install -g artillery@latest
```

### Checking your installation

If you used npm to install Artillery globally, run the following command in your preferred command line interface:

```
    artillery dino
```

You should see an ASCII dinosaur printed to the terminal. Something like this:

![img.png](img.png)

### Testing

We can generate load on both the APIs via:

```
    artillery run load-no-proxy.yml
```

```
    artillery run load-proxy.yml
```