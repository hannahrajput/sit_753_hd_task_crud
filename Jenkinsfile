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
                    // Create a ZIP file of your app
                    sh 'zip -r flask_crud_app.zip . -x "tests/*" "*.git*"'
                }
            }
        }

        stage('Test') {
            steps {
                echo 'Running pytest...'
                script {
                    sh 'python -m pip install --upgrade pip'
                    sh 'pip install -r requirements.txt'
                    sh 'python -m pytest tests/ --disable-warnings'
                }
            }
        }

        stage('Code Quality') {
            steps {
                withCredentials([string(credentialsId: "${SONAR_TOKEN_ID}", variable: 'SONAR_TOKEN')]) {
                    echo 'Running SonarCloud Analysis...'
                    sh '''
                        # Ensure sonar-project.properties exists in repo root
                        java -jar sonar-scanner-cli.jar \
                        -Dsonar.login=$SONAR_TOKEN
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
