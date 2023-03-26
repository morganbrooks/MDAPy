<!-- ![MDAPy Logo](assets/img/logo.png) -->
<p align="center" width="100%">
  <img align="center" src="src/MDAPy/Logo/logo4.png">   
</p>

## 1) Introduction
[**TODO**] TBD
<!-- $~$ -->
## 2) Instalation
### 2.1) Requirements
All Python 3 and R requirements are listed in files `requirements.txt` and `init.R`, respectively. However, from here forward we will assume that you are using `Python 3.8.10`, `R 4.1.2` and `git 2.25.1`. These were the versions tested during its release.

### 2.2) Set Up local environment

Clone the repository to your computer by running the following code in your terminal (or its ssh/cli equivalent):

```
git clone https://github.com/diegofcoelho/MDAPy.git
```

While you can install all dependecies listed in `requirements.txt` directly to your python library, we highly recommend the use of virtual environments (`pyenv`) to manage the correct versions necessary to run MDAPy.

If you are using Python 3, you should have `venv` module from the standard library installation. You can read about Python virtual environments [here](https://docs.python.org/3/library/venv.html). If for some reason you don't have it, run:
```
pip install virtualenv
```

Then access the repository folder and create its environment:
```(python, enviroment)
python3 -m venv /path/to/your/repository/venv
```
Then you can activate your environment and install the required packages: 
```
source <venv>/bin/activate

pip install -r requirements.txt
```
The R packages can be installed by running the code below in a terminal:

```
Rscript -e "install.packages('IsoplotR', 'dplyr', 'rjson', 'openxlsx')"
```
As the R Script is called from within the MDAPy package, we recommend the installation of these packages to your global R library.

And that is it! You can now start your MDAPy dashboard by running the command below:

``` 
python app.py

Dash is running on http://127.0.0.1:8050/

 * Serving Flask app 'app' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
```

Note that we assume the user is spinning the Dash application from within the `src` folder.

#### Docker Compose

The easiest way to work on the project without having to reload it constantly is by running:

```
docker-compose build
# and then
docker-compose up
```

That will spin up a version of the application that reloads automatically everytime the source code is altered. In essence it is a docker image that is linked directly to your source code and monitor changes. The application is kept running through Docker, but runs using the code in your computer.
This is also the preferred way of development since it does not install libraries in your host computer, only in the docker guest.

### IsoplotR
Explain about the package and its use here.
### 2.3) Heroku Deployment
Assuming you have Heroku properly configured in your systems, you can set your App to source to deploy from your repository and push to the Heroku branch.

### 2.4) Docker Deployment
#### 2.4.1) What is Docker?
Docker is an open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your infrastructure so you can deliver software quickly. With Docker, you can manage your infrastructure in the same ways you manage your applications. By taking advantage of Docker’s methodologies for shipping, testing, and deploying code quickly, you can significantly reduce the delay between writing code and running it in production.

You will see that we have a Dockerfile in the root of this repository containing the `recipe` to build a functional image of MDAPy. A few pages that may help you get familiarized with docker are shown below:
- [Docker Overview](https://docs.docker.com/get-started/overview/)
- [Docker Crash Course](https://docker-curriculum.com/)
- [Docker Tutorial for Beginners](https://www.youtube.com/watch?v=pTFZFxd4hOI)
- [Docker Tutorial for Beginners - A Full DevOps Course on How to Run Applications in Containers](https://www.youtube.com/watch?v=fqMOX6JJhGo)
- [Docker Tutorial for Beginners [FULL COURSE in 3 Hours]](https://www.youtube.com/watch?v=3c-iBn73dDE)

#### 2.4.2) Build a MDAPy Docker Image
Assuming that you know the basics, you could build a MDAPy Docker Image by running the following command in a terminal/prompt at the root of this repository:
```
build build -t <IMAGE_NAME> .
```

That will trigger the build of an image with the name given in the command above. To list all docker images available in your system:

```
docker image ls
```

And to run a container based on the image we just built:

```
docker run -t -i -p 127.0.0.1:8080:80 <IMAGE_NAME>
```

This will expose TCP port 80 in the container to port 8080 on the Docker host for connections to host IP 127.0.0.1. The flags `-t` and `-i` will allow you to kill the container running the process by pressing `Ctrl+C`.

#### 2.4.3) Deploy the Dockerfile to Google Cloud Platform (GCP)
Because of the amount of data and plots generated, you must guarantee that the App running under the container has enough resources, otherwise it will crash during executrion.

To build the image inside GCP:
```
docker build -f Dockerfile -t gcr.io/{PROJECT_ID}/{IMAGE}:{TAG} .
```

After the image is built, you can run it by typing:
```
gcloud run deploy APP_NAME --image=gcr.io/{PROJECT_ID}/{IMAGE}:{TAG} --platform=managed --region=us-central1   --timeout=900 --concurrency=80   --cpu=6  --memory=4096Mi  --max-instances=10 --allow-unauthenticated
```

There quite a few nuances regarding the deployment through GCP that might be worthy reading. If that is of your interest:


- [Deploy Dash to GCP in 5 minutes](https://medium.com/kunder/deploying-dash-to-cloud-run-5-minutes-c026eeea46d4)


- [Top 3 ways to run your containers on Google Cloud](https://www.youtube.com/watch?v=jh0fPT-AWwM)
- [GCP Deployment with GIT](https://medium.com/lfdev-blog/google-cloud-compute-deploy-com-git-d8feec8c933a)

- [How to Run Docker containers on GCP](https://www.cloudsavvyit.com/4589/how-to-run-docker-containers-on-google-cloud-platform/)


## 3) MDAPy Development

The MDAPy library was written in Python 3 and relies on a few well-known packages, such as `matplotlib`, `numpy`, `pandas`, `scipy` and their dependencies. The full requirement list can be seen [here](requirements.txt).

The dashboard is mostly written in Dash, which is a framework created by plotly and written on the top of `Flask`, `Plotly.js` and `React.js` for creating interactive web applications. With dash, you don't have to learn HTML, CSS and Javascript in order to create interactive dashboards, you only need python ([Dash for beginners](https://towardsdatascience.com/dash-for-beginners-create-interactive-python-dashboards-338bfcb6ffa4#:~:text=Dash%20is%20a%20python%20framework,dashboards%2C%20you%20only%20need%20python.)).

However, MDAPy can be used directly by loading the library or the sample [jupyter notebook](MDAPy/MDAPy.ipynb) included in this directory.

<!-- docker run -it -e PORT=80 -p 8080:80 mdapy --> 
