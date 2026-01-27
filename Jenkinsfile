pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building Docker Image...'
                sh 'docker build -t meest-core .'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying...'
                sh 'docker compose up -d'
            }
        }
    }
}