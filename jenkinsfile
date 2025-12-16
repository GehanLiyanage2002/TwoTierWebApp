pipeline {
    agent any

    environment {
        IMAGE_NAME = "flask-app"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/GehanLiyanage2002/TwoTierWebApp.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t $IMAGE_NAME:latest .
                '''
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                sh '''
                docker compose down || true
                docker compose up -d --build
                '''
            }
        }
    }

    post {
        always {
            sh 'docker image prune -f || true'
        }
        success {
            echo "Deployment completed successfully"
        }
        failure {
            echo "Deployment failed"
        }
    }
}
