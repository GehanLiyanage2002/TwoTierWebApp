pipeline {
    agent any

    environment {
        IMAGE_NAME = "student-flask-app"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/GehanLiyanage2002/TwoTierWebApp.git'
            }
        }

        stage('Build Docker Images') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                sh '''
                # Stop old containers if any
                docker compose down || true

                # Start containers in detached mode
                docker compose up -d
                '''
            }
        }
    }

    post {
        always {
            
            sh 'docker image prune -f || true'
        }
        success {
            echo "Deployment successful! Visit http://52.184.82.99:5000"
        }
        failure {
            echo "Deployment failed. Check container logs for details."
        }
    }
}
