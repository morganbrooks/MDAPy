![MDAPy Logo](assets/img/logo.png)     
# MDAPy
[**TODO**] TBD

Brief description here

## 1) Introduction
[**TODO**] TBD
<!-- $~$ -->
## 2) Instalation
### 2.1) Requirements
All Python 3 and R requirments are listed in `requirements.txt` and `init.R`, respectively. However, from here forward we will assume that you are using `Python 3.8.10`, `R 4.1.2` and `git 2.25.1`. These were the versions tested during its release.

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

And that is it! You can now start your MDAPy dashboard by running:

```
python app.py

Dash is running on http://127.0.0.1:8050/

 * Serving Flask app 'app' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
```
### IsoplotR
Explain about the package and its use here.
### 2.3) Heroku Deployment
Assuming you have Heroku properly configured in your systems, you can set your App to source to deploy from your repository and push to the Heroku branch.

### 2.4) Docker Deployment
[**TODO**] TBD