pipeline {
    agent any

    environment {
        IMAGE_NAME = "flask-crud-app"
        DOCKER_TAG = "latest"
        SONAR_HOST_URL = "http://sonarqube:9000" 
        TRIVY_CACHE_DIR = "/tmp/trivy"
    }

    stages {

        stage('Build') {
            steps {
                echo 'Building Docker image...'
                script {
                    sh "docker build -t ${IMAGE_NAME}:${DOCKER_TAG} ."
                }
            }
        }

        stage('Test') {
            steps {
                echo 'Running pytest...'
                script {
                    sh "docker run --rm -v \$(pwd):/app -w /app ${IMAGE_NAME}:${DOCKER_TAG}python -m pytest tests/ --disable-warnings"
                }
            }
        }

        stage('Code Quality') {
            steps {
                withCredentials([string(credentialsId: 'SONAR_AUTH_TOKEN', variable: 'SONAR_AUTH_TOKEN')]) {
                    sh '''
                        # Download SonarScanner CLI if not already downloaded
                        if [ ! -f sonar-scanner-cli-7.2.0.5079-linux-x64.zip ]; then
                            curl -sSLo sonar-scanner-cli-7.2.0.5079-linux-x64.zip https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-7.2.0.5079-linux-x64.zip
                            unzip -o sonar-scanner-cli-7.2.0.5079-linux-x64.zip
                        fi

                        # Run SonarScanner with auth token
                        java -jar sonar-scanner-7.2.0.5079-linux-x64/lib/sonar-scanner-cli-7.2.0.5079.jar \
                        -Dsonar.projectKey=FlaskCRUD \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=http://sonarqube:9000 \
                        -Dsonar.login=$SONAR_AUTH_TOKEN
                    '''
                }
            }
        }

        stage('Security') {
            steps {
                echo 'Running Trivy security scan...'
                script {
                    sh "docker run --rm -v \$(pwd):/app -w /app aquasec/trivy fs --exit-code 1 --cache-dir ${TRIVY_CACHE_DIR} ."
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying app to test environment...'
                script {
                    sh "docker stop flask-crud-container || true"
                    sh "docker rm flask-crud-container || true"
                    sh "docker run -d -p 5000:5000 --name flask-crud-container ${IMAGE_NAME}:${DOCKER_TAG}"
                }
            }
        }

        stage('Release') {
            steps {
                echo 'Promoting app to production...'
                script {
                    sh "docker stop flask-crud-prod || true"
                    sh "docker rm flask-crud-prod || true"
                    sh "docker run -d -p 5001:5000 --name flask-crud-prod ${IMAGE_NAME}:${DOCKER_TAG}"
                }
            }
        }

        stage('Monitoring') {
            steps {
                echo 'Monitoring app health...'
                script {
                    sh """
                    STATUS=\$(curl -s -o /dev/null -w '%{http_code}' http://localhost:5001/)
                    if [ "\$STATUS" != "200" ]; then
                        echo "App is down! Status code: \$STATUS"
                        exit 1
                    else
                        echo "App is healthy. Status code: \$STATUS"
                    fi
                    """
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs!'
        }
    }
}
