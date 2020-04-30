# SEPA Development

An overview of our development pipeline and workflow. 


![Development Workflow](readme-resources/dev-workflow.png?raw=true "Dev Workflow")

#### Notes: 
* Each developer has a local environment that includes a local mysql database, a local Django virtual environment, and local Docker containers. 
* In order to replicate the AWS environment, your Socket-Server Docker containers must be able to connect to your local MySQL database. 
* Code is developed and tested locally **before** being committed to source control. 
* Code is reviewed and then merged into the master branch of each repository. 
* This triggers a build process in which AWS will package and build each service before deploying to their respective endpoints. 

## Django Web App Application 

### Prerequisites: 

* Github
    * You must have a Github account. Signup at <https://github.com/>
    * You must have downloaded and installed git or Github desktop.
    * You must have accepted the invitation to join the "dev" team. 
      Check your email associated with your github account.
* Docker. 
  * You must have a Docker account. <https://www.docker.com/get-started>
  * You must have downloaded and installed Docker Community for Desktop. 
  * A quick overview of Docker: <https://docker-curriculum.com/>

* MySQL
    * You must download and install MySQL Community Server 5.7 here: <https://dev.mysql.com/downloads/mysql/5.7.html>
        * tutorial for windows 10: <https://blog.zedfox.us/install-mysql-5-7-windows-10/>
	   * tutorial for OSX: <https://gist.github.com/nrollr/3f57fc15ded7dddddcc4e82fe137b58e>
  * *NOTE: For local development, you will need a Database Client such as MySQL Workbench, TablePlus, or Sequel Pro. Download and install whichever client you like best. (I like workbench and Tableplus).*

* Python 3.6
 
* The pip utility, *matching your Python version 3.6* . This is used to install and list dependencies for your project, so that Elastic Beanstalk knows how to set up your application's environment.
* The virtualenv package. This is used to create an environment used to develop and test your application, so that the environment can be replicated by Elastic Beanstalk without installing extra packages that aren't needed by your application. A Virtual Environment, put simply, is an isolated working copy of Python which
allows you to work on a specific project without affecting other projects.

### Getting Started: 

Current URL of our Web UI: <http://web-app.eba-xee4gc2x.ap-southeast-2.elasticbeanstalk.com/>

* Create a directory on your local machine named "Web-UI"
* Navigate to the newly created directory before cloning the the github repository. 
    * `git clone https://github.com/SEPA-17/Web-UI.git`
* Open the repository in your IDE, then *ensure you're are working on the development branch*.
* Run the following commands in a shell to create and run an isolated Python development environment, then install the dependencies required to run our Django web application.
    * For Unix based Systems: 
      * `~$ virtualenv ~/eb-virt`
      * `~$ source ~/eb-virt/bin/activate`
      * `(eb-virt)~$ pip install -r requirements.txt`
    * For Windows: 
      * `C:\> virtualenv %HOMEPATH%\eb-virt`
      * `C:\>%HOMEPATH%\eb-virt\Scripts\activate `
      * `(eb-virt) C:\>pip install -r requirements.txt`
* These commands will start an isolated virtualenv named *eb-virt*
* Activate the virtualenv
* Install the dependencies listed in requirements.txt into the virtualenv. 

Following this, you are now free to develop on your local machine.
After you have made some changes, you must *test them locally* before committing them to Github. To do this, you need to start a local webserver so you can view the application on your browser. 

From your project root directory: 

* run `python manage.py runserver`

Expect the following result:

![Local Server](readme-resources/localserver.png?raw=true "Local Server")


You can now navigate to <http://127.0.0.1:8000/> to view your application. 

*Note: Django version 2.1.1 is the latest stable version compatible with Elastic Beanstalk's Python 3.6 platform. Any update of Django to a version later than 2.1.1 will break our configuration. **Don't do this***

Before committing your changes to source control, ensure that any packages you have decided to install in your local *virtualenv* are included in `requirements.txt` so that other team members can install the same packages. 
* run `pip freeze -r requirements.txt`

Lastly, commit your changes to the development branch of the Web-UI. 
Open a pull request to merge your changes into master and trigger deployment. 

