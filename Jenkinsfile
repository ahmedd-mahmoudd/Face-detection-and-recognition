
pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerlogin')
        MONGO_URL = credentials('MONGO_URL')
        SECRETKEY = credentials('SECRETKEY')
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
        
        stage('Putting env variable') {
            steps {
                script {
                    env.MONGO_URL = MONGO_URL
                    env.SECRETKEY = SECRETKEY
                }
                
            }
        }
        
        stage('Run Python Tests') {
            steps {
                script {
                    sh 'cd tests && python3 -m pytest --junitxml=output/test-result.xml'
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
                sh 'deactivate' 
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
