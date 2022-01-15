# This is the setup guide of the inventory management application.
# The application supports 4 options:
* Running the project locally
* Ansible deployment (through jenkins server)
* Docker deployment (through jenkins server)
* Kubernetes deployment (through jenkins server)

# Jenkins server setup
- Create ssh connection by generating a ssh key
- Create a virtual machine and add the ssh key
- Add inbound port rules for ports 8080, 443, 80 in virtual machine
- Ssh to the virtual machine
- Install jenkins server in the virtual machine (https://www.jenkins.io/doc/book/installing)
- Run http://<put virtual machine's ip here>:8080/
- Create jenkins account and login
- Login to github and add a webhook

# Option 1) Run the project locally
##  Clone & run project locally
```bash
git clone https://github.com/stas33/inventory-management-project.git
python -m venv env
source env/bin/activate
pip install -r requirements.txt
cp inventoryproject/.env.example inventoryproject/.env
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
## Edit inventoryproject/.env file to define
```vim
SECRET_KEY='test123'
DATABASE_URL=sqlite:///./db.sqlite3
```
## Edit settings.py file 
```vim
- Uncomment line 155
- Comment out line 157
```
##Run development server
```bash
python manage.py runserver
```
# Option 2) Ansible deployment
## Clone project locally
```bash
git clone https://github.com/stas33/inventory-management-project.git
```
## Edit inventoryproject/.env file to define
```vim
SECRET_KEY='test123'
DATABASE_URL='postgres://dbuser:pass123@db:5432/test_db'
```
## Setup of vms, ssh keys, credentials, installation, pipeline
- Ssh from local pc to the first virtual machine
- Create ssh connection by generating a new ssh key
- Install ansible in the first virtual machine (https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
- Create a second virtual machine and add the ssh key
- Add inbound port rules for ports 8000, 5432, 443, 80 in the second virtual machine
- Ssh to the second virtual machine
- Install ansible in the second virtual machine
- Login to jenkins server (in first virtual machine)
- Go to Dashboard->Manage Jenkins->Manage Credentials->Add
- Select Ssh username with private key->Enter id, username and paste private key
- Go to Dashboard->New Item->Pipeline project
- Select Github hook trigger for GITScm polling
- Select Definition->Pipeline script from SCM
- Select Scm->Git
- Paste repo url (https://github.com/stas33/inventory-management-project.git)
- Set branch to main
- Set script path to Jenkinsfile
- Click save and build
- Run http://<put second virtual machine's ip here>:8000/
- Go to the project's repo in the second virtual machine and run  python manage.py create superuser

# Option 3) Docker deployment
## Clone project locally
```bash
git clone https://github.com/stas33/inventory-management-project.git
```
## Edit inventoryproject/.env file to define
```vim
SECRET_KEY='test123'
DATABASE_URL='postgres://dbuser:pass123@db:5432/test_db'
```

## Setup of vms, ssh keys, credentials, installation, pipeline

- Create a third virtual machine and add the ssh key you created in the first virtual machine
- Add inbound port rules for ports 8000, 5432, 80 in the third virtual machine
- Ssh to the third virtual machine 
- Install docker and docker compose (https://docs.docker.com/engine/install/ , https://docs.docker.com/compose/install/)
- Login to jenkins server (in first virtual machine)
- Go to Dashboard->Manage Jenkins->Manage Credentials->Add
- Select Ssh username with private key->Enter id, username and paste private key
- Go to Dashboard->New Item->Pipeline project
- Select Github hook trigger for GITScm polling
- Select Definition->Pipeline script from SCM
- Select Scm->Git
- Paste repo url (https://github.com/stas33/inventory-management-project.git)
- Set branch to main
- Set script path to Jenkinsfile2
- Click save and build
- Run http://<put third virtual machine's ip here>/
- Go to the project's repo in the third virtual machine and run  python manage.py create superuser

# Option 4) Kubernetes deployment
## Clone project locally
```bash
git clone https://github.com/stas33/inventory-management-project.git
```
## Edit inventoryproject/.envkub file to define
```vim
SECRET_KEY=test123
DATABASE_URL=postgresql://dbuser:pass123@pg-cluster-ip/test_db
ALLOWED_HOSTS=django.westeurope.cloudapp.azure.com
```
## Setup of vms, ssh keys, installation

- Create a fourth virtual machine and add the ssh you created in the second virtual machine
- Add inbound port rules for ports 8000, 8888, 80, 16443 in the fourth virtual machine
- Install docker and docker compose in the first virtual machine
- Ssh to the fourth virtual machine 
- Install kubernetes (https://kubernetes.io/docs/setup/)
- Install microk8s (https://ubuntu.com/tutorials/install-a-local-kubernetes-with-microk8s#1-overview)
- Create and scp .kube/config file to local pc

## microk8s enable storage and dns ingress inside the repository of the fourth virtual machine 
```bash
microk8s enable storage dns ingress
```
## Apply the following commands in the local repository
## Persistense Volume
```bash
kubectl apply -f k8s/db/postgres-pvc.yaml
```
## Secrets
* pg secret

```bash
kubectl create secret generic pg-user \
--from-literal=PGUSER=<put user name here> \
--from-literal=PGPASSWORD=<put password here>
```

## Configmaps
```bash
kubectl create configmap django-config --from-env-file=inventoryproject/.envkub
```
## Deployments
* Postgres
```bash
kubectl apply -f k8s/db/postgres-deployment.yaml
```
* django
```bash
kubectl apply -f k8s/django/django-deployment.yaml
```

## Services
* Postgres
```bash
kubectl apply -f k8s/db/postgres-clip.yaml
```

* django
```bash
kubectl apply -f k8s/django/django-clip.yaml
```

## Ingress

```bash
kubectl apply -f k8s/django-ingress.yaml
```
## Get pods

```bash
kubectl get pods
```

## Get terminal access and create a superuser

```bash
kubectl exec -it <put pod name here> bash
python manage.py createsuperuser
```

## Setup of credentials, pipeline
- Create a domain name (the same as in allowed hosts above)
- Login to jenkins server
- Go to Dashboard->Manage Jenkins->Manage Credentials->Add
- Select Username with passowrf->Enter as username 'docker-passwd', your password and an id
- Go to Dashboard->New Item->Pipeline project
- Select Github hook trigger for GITScm polling
- Select Definition->Pipeline script from SCM
- Select Scm->Git
- Paste repo url (https://github.com/stas33/inventory-management-project.git)
- Set branch to main
- Set script path to Jenkinsfile3
- Click save and build
- Run http://<put the domain name here>/

# Dummy data instructions - Check also dummy_data.txt
## After running the project
- Go to admin panel (http://<put ip or domain name here>/admin) and login as superuser
- Add groups (with specific order): 1) admin 2) manager 3) employee 4) customer 5) pending employee 6) pending manager
- Go to Users: <superuser> -> choosegroup: admin
- Go to the login page (http://<put ip or domain name here>/)
- Select register as user and register 2 managers and 2 employees -> check dummy_data.txt
- Select register as customer and register 2 customers -> check dummy_data.txt 
- Go to admin panel (http://<put ip or domain name here>/admin) and login as superuser
- Select Add company and then add 3 companies (Name-Address-Postcode)
- Go to admin panel
- Select Add Categories
- Add the following categories: Computers, Phones, TVs, Monitors, IT Equipment
- Select Add Products and add the following products -> check dummy_data.txt
