pipeline {
    agent any

    environment {
        IMAGE_NAME = "meest-core"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Inject Secrets') {
            steps {
                script {
                    // Просто копируем файл. Права теперь работают нормально.
                    withCredentials([file(credentialsId: 'meest-env-file', variable: 'MY_ENV_VAR')]) {
                        sh 'cp $MY_ENV_VAR .env'
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Starting Deployment...'
                sh 'docker compose down'
                sh 'docker compose up -d --build'
            }
        }

        stage('Verify') {
            steps {
                sleep 10
                sh 'docker ps'
            }
        }
    }
}