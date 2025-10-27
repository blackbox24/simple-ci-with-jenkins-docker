// Jenkinsfile
pipeline {
    agent {
        docker {
            image 'python:3.12-slim'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    
    environment {
        IMAGE_NAME = 'task-manager'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh '''
                    pip install --no-cache-dir -r requirements.txt
                    pip install pytest
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh 'pytest tests/ -v'
            }
            post {
                always {
                    junit '**/test-results/*.xml'  // Add --junitxml=test-results/results.xml to pytest for reports
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    def image = docker.build("${IMAGE_NAME}:${IMAGE_TAG}")
                    image.inside('-e FLASK_APP=run.py') {
                        sh 'pytest tests/ -v'
                    }
                }
            }
        }
        
        // Optional Deploy stage
        /*
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-credentials') {
                        def image = docker.image("${IMAGE_NAME}:${IMAGE_TAG}")
                        image.push()
                        image.push('latest')
                    }
                    sh 'echo "Deploying to production..."'
                }
            }
        }
        */
    }
    
    post {
        always {
            cleanWs()
        }
    }
}