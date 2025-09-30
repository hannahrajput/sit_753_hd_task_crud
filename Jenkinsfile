pipeline {
    agent any

    environment {
        SONAR_HOST_URL = "https://sonarcloud.io" 
        SONAR_TOKEN_ID = "SONAR_TOKEN"
    }

    stages {

        stage('Build') {
            steps {
                echo 'Building Python artefact...'
                script {
                    sh 'zip -r flask_crud_app.zip . -x "tests/*" "*.git*" "venv/*" ".pytest_cache/*" "instance/*" "__pycache__/*" "sonar-scanner-*/**"'
                }
            }
        }

        stage('Test') {
            steps {
                echo 'Running pytest...'
                script {
                    sh '''
                    python3 -m venv venv
                    bash -c "source venv/bin/activate && pip install -r requirements.txt && python3 -m pytest tests/ --disable-warnings"
                '''

                }
            }
        }

        stage('Code Quality') {
            steps {
                withCredentials([string(credentialsId: "${SONAR_TOKEN_ID}", variable: 'SONAR_TOKEN')]) {
                    echo 'Running SonarCloud Analysis...'
                    sh '''
                        # Download SonarScanner CLI if not already downloaded
                        if [ ! -f sonar-scanner-cli-7.2.0.5079-linux-x64.zip ]; then
                            curl -sSLo sonar-scanner-cli-7.2.0.5079-linux-x64.zip https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-7.2.0.5079-linux-x64.zip
                            unzip -o sonar-scanner-cli-7.2.0.5079-linux-x64.zip
                        fi

                        # Run SonarScanner using full path
                        java -jar sonar-scanner-7.2.0.5079-linux-x64/lib/sonar-scanner-cli-7.2.0.5079.jar

                    '''
                }
            }
        }


        stage('Security') {
            steps {
                echo 'Running security scan (bandit)...'
                script {
                    sh 'pip install bandit'
                    sh 'bandit -r . -ll'
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Starting Flask app in test environment...'
                script {
                    sh 'python app.py &'
                }
            }
        }

        stage('Release') {
            steps {
                echo 'Simulating release step (manual promotion or ZIP deploy)...'
            }
        }

        stage('Monitoring') {
            steps {
                echo 'Checking app health...'
                script {
                    def status = sh(script: 'curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/', returnStdout: true).trim()
                    if (status != '200') {
                        error "App is down! Status code: ${status}"
                    } else {
                        echo "App is healthy. Status code: ${status}"
                    }
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
