<!-- ![MDAPy Logo](assets/img/logo.png) -->
<p align="center" width="100%">
  <img align="center" src="src/MDAPy/Logo/logo4.png">   
</p>

MDAPy is a Python Tool for Calculating and Evaluating Maximum Depositional Ages (MDA) Using Detrital Zircon U-Pb Geochronology. 

With the increase in the use of MDA methods, and the requirement for more rigorous testing and analysis of each, we introduce MDAPy, a free, open source, Python 3-based MDA toolset for efficiently calculating and comparing 10 MDA calculation methods: YSG, YC1s, YC2s, YDZ, MLA, YPP, YSP, Y3Za, Y3Zo, Tau. 

MDAPy is meant to act as an expansion to the MDA functionality offered by detritalPy, IsoplotR, and Isoplot, leveraging the open-source code offered within each and expanding on it to provide further functionality. While these software packages provide a large variety of tools, the MDA calculation functions form only a small portion of the functionality. MDAPy specializes solely in MDA calculations and provides one tool to calculate the full suite of MDA methods, as well as offers additional visualization and presentation functionality. Researchers will now have the ability to calculate and evaluate multiple MDAs for several large-n datasets all in one location, facilitating a greater comprehension of the data and the ability to make more informed decision on the best method, or combination of methods to apply to their data. 

The current version of MDAPy is accessible as a downloadable software package. This offline version can be downloaded and run locally on computers without a permanent or stable internet connection. To simplify the process we use a Docker container, which builds the application using the original source code, but does not require users to download Python or any required libraries. 

What is Docker? Docker is an open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your infrastructure so you can deliver software quickly. 

Instructions for installing and running MDAPy:

1. Download the code zip file from this GitHub page using the green code button at the top. 

2. Unzip and place the folder in an easy to locate area, like 'Documents' 

3. Download and sign up for Docker. 
- If using a newer computer download and sign up for an account here: https://www.docker.com/
- If using an older computer download and sign up for an account using an older version: https://docs.docker.com/desktop/previous-versions/archive-windows/

4. Once docker is downloaded, locate the terminal (Apple) or command prompt (PC)

5. Locate the folder where you put MDAPy in your terminal/command prompt. To do this type: 

This will show you what is in the directory you are in
```sh
ls
```


cd = change directory, find the folder where MDAPy is kept using cd 
```sh
cd 'Folder where MDAPy is kept' 
```

Go into the MDAPy folder where the docker files are kept

```sh
cd MDAPy
```

This will build the docker container of MDAPy, this will take a while the first time
```sh
docker-compose build
```

This will launch MDAPy on your computer

```sh
docker-compose up 
```


6. Open an internet browser and type in http://localhost:8080

Since you have built the container, the next time you want to use MDAPy, all you need to do is make sure Docker is open and type http://localhost:8080 into your browser!





