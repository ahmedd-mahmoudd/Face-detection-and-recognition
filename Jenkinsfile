
pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerlogin')
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    git branch: 'WebUI', credentialsId: 'githublogin', url: 'https://github.com/ahmedd-mahmoudd/Face-detection-and-recognition.git'
                }
            }
        }

         stage('Setup Virtual Environment') {
            steps {
                script {
                    sh 'python3 -m venv myenv'
                    sh '. myenv/bin/activate'
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    sh 'cd backend_server && pip3 install -r requirements.txt'
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
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerlogin') {
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
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerlogin') {
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
