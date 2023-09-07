
pipeline {
    agent { label 'docker' }
    environment {
        DOCKERHUB_CREDENTIALS = credentials('DockerCredentialsUserPassword')
    }

    stages {
        stage('Run Python Tests') {
            steps {
                script {
                    sh 'python -m unittest discover tests'
                }
            }
        }

        stage('Build and Push Backend Image') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', DOCKERHUB_CREDENTIALS) {
                        def backendImage = docker.build('xahmedmahmoudx/backend-server:latest', './backend_server')
                        backendImage.push()
                    }
                }
            }
        }

        stage('Build and Push Frontend Image') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', DOCKERHUB_CREDENTIALS) {
                        def frontendImage = docker.build('your-dockerhub-username/my-frontend:latest', './my-frontend')
                        frontendImage.push()
                    }
                }
            }
        }
    }

    post {
        failure {
            echo "One or more tests failed. Skipping image builds and pushes."
        }
    }
}
