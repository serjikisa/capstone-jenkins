/* groovylint-disable-next-line CompileStatic */
pipeline {
    agent any

    stages {
        stage('Cleanup') {
            steps {
                sh 'docker rm -f simplepy_instance'
                sh 'docker rmi -f simplepy'
            }
        }
        stage('Build') {
            steps {
                sh 'docker build . -t simplepy'
            }
        }
        stage('Unit test') {
            steps {
                sh 'docker run simplepy pytest -v'
            }
        }

        stage('Run app') {
            steps {
                sh 'docker run -p 5000:5000 -d --name=simplepy_instance simplepy'
            }
        }
    }
}
