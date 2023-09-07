
pipeline {
    agent { label 'docker' }
    environment {
        DOCKERHUB_CREDENTIALS = credentials('DockerCredentialsUserPassword')
    }

    stages {
         stage('Setup Virtual Environment') {
            steps {
                script {
                    sh 'python3 -m venv myenv'
                    sh 'source myenv/bin/activate'
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    sh 'pip install -r backend_server/requirements.txt'
                }
            }
        }

        stage('Run Python Tests') {
            steps {
                script {
                    sh 'cd tests && pytest --junitxml=output/test-results.xml'
                }
            }
        }
        
      stage('Run Python Tests') {
            steps {
                script {
                    sh 'cd tests && pytest --junitxml=output/test-results.xml'
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
        always {
            script {
                sh 'deactivate' // Deactivate the virtual environment
            }
            cleanWs()
        }
        success {
            echo "All tests passed. Proceeding with image builds and pushes."
        }
        failure {
            echo "One or more tests failed. Skipping image builds and pushes."
        }
    }
}
