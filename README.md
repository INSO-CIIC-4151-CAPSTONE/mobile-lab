# Capstone Project: MobiLab
### www.mobi-lab.online
---
## Description
<div style="text-align: justify">
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Laboratory tests are an essential procedure for human health, they are performed
    to observe changes in health and to follow up on a patient. They are usually
    administered by a physician or health professional who collects a sample of blood,
    urine, or other body fluid or tissue to obtain information for analysis, in short, routine
    monitoring. This helps physicians diagnose health conditions and detect diseases.
</div>
<div style="text-align: justify">
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This application will help people who for some reason can not get to the
    appointment, this is because they do not have transportation or they are
    handicapped or elderly. Some of the advantages are reducing the number of patients
    waiting, reducing focus of infection as we are going through a pandemic (Covid 19)
    is a very viable way to prevent the spread of this virus, patients would avoid long
    lines and therefore save them time.
</div>
<br/>


## Team:

| Name                      | Email                     | Dep. |
|---------------------------|---------------------------|------|
| Bryan O. Perez Perez      | bryan.perez13@upr.edu     | INSO |
| Gabriela Cardona Blas     | gabriela.cardona1@upr.edu | INSO |
| Francis J. Patron Fidalgo | francis.patron1@upr.edu   | CIIC |
---
## Supervisor: Dr. Wilson Rivera Gallego

## Django Documentation
https://docs.djangoproject.com/en/4.1/

# Set Up Repo:
 
1. Make sure you have installed python, pip, and a Python IDE(pycharm)
2. Activate venv in the directory that you cloned the repo (virtual enviorment)
3. Install dependencies:   
run inside repo directory: `pip3 install -r requirements.txt` 

 # Set Up a DB explorer
 
1. Install postgreSQL to your PC: https://www.postgresql.org/download/ 
2. Make sure when installing to check pgAdmin 4 (Should be checked automatically) You can use Data Grip as well
    https://www.jetbrains.com/datagrip/download/#section=windows
    
 # DB Configuration

"host": "ec2-34-199-68-114.compute-1.amazonaws.com"<br />
    "name": "d7hdohtgo1pqhh"<br />
    "user": "bcdyaoomxltesu" <br />
    "port": "5432" <br />
    "pass": "c09df90300130e30d569b72699b8ce054ccea344be0aa8e3877c74fc8b0ada85" <br />
    "url": "postgres://bcdyaoomxltesu:c09df90300130e30d569b72699b8ce054ccea344be0aa8e3877c74fc8b0ada85@ec2-34-199-68-114.compute-1.amazonaws.com:5432/d7hdohtgo1pqhh"<br />

# Terminal commands for DB table updates and run app
   1. py manage.py makemigrations 
   2. py manage.py migrate
   3. py manage.py runserver
   
 
