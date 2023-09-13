
pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerlogin')
        dockerpsw = credentials('DockerPSW')
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
        
        stage('Build Backend Image') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                script {
                       sh'docker build -t xahmedmahmoudx/backend-server:latest ./backend_server'
                    }
                
            }
        }

        stage('Scan Backend Image') {
            steps {
                script {
                    sh 'trivy image xahmedmahmoudx/backend-server:latest'
                }
            }
        }

        stage('Push Backend Image') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            
            steps {
                script {
                    sh '''docker login -u xahmedmahmoudx -p $dockerpsw
                        docker push xahmedmahmoudx/backend-server:latest'''
                }
            }
                
            
        }

        stage('Build Frontend Image') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                script {
                    sh '''
                        docker build -t xahmedmahmoudx/my-frontend:latest ./my-frontend
                    '''
                }
            }
        }

        stage('Scan Frontend Image') {
            steps {
                script {
                    sh 'trivy image xahmedmahmoudx/my-frontend:latest'
                }
            }
        }

        stage('Push Frontend Image') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                script {
                    sh '''docker login -u xahmedmahmoudx -p $dockerpsw
                        docker push xahmedmahmoudx/my-frontend:latest'''
                }
            }
        }
    }

    post {
        always {
            script {
               sh 'exit' 
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
