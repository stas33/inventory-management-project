pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                // Get some code from a GitHub repository
                git branch: 'test1', url: 'https://github.com/stas33/inventory-management-project.git'


            }
        }
        stage('Test') {
            steps {
                sh '''
                    python3 -m venv env
                    source env/bin/activate
                    pip install -r requirements.txt
                    cp inventoryproject/.env.example inventoryproject/.env
                    ./manage.py test companies'''
            }
        }

        stage('Deploy') {
            steps {
                sshagent (credentials: ['ssh-deployment1']) {

                sh '''
                    pwd
                    echo $WORKSPACE
                    ansible-playbook -i ~/workspace/ansible-project-inventory/hosts.yml -l deploymentservers ~/workspace/ansible-project-inventory/playbooks/postgres.yml
                    ansible-playbook -i ~/workspace/ansible-project-inventory/hosts.yml -l deploymentservers ~/workspace/ansible-project-inventory/playbooks/inventory-project-install.yml
                    '''
                }
            }
        }
    }
}