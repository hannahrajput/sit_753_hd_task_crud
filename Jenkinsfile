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
                    sh 'zip -r flask_crud_app.zip . -x "tests/*" "*.git*" "venv/*" ".pytest_cache/*" "instance/*" "__pycache__/*" "sonar-scanner-*/**" ".scannerwork/*"'
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
                    sh '''
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install bandit
                        bandit -r flask_crud_app -x flask_crud_app/venv -ll
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                withCredentials([string(credentialsId: 'HEROKU_API_KEY', variable: 'HEROKU_API_KEY')]) {
                    sh '''
                        git remote remove heroku || true
                        git remote add heroku https://heroku:${HEROKU_API_KEY}@git.heroku.com/my-flask-crud-app.git
                        # Push HEAD explicitly to refs/heads/main
                        git push heroku HEAD:refs/heads/main -f
                    '''
                }
            }
        }



        stage('Release') {
            steps {
                echo 'Releasing application...'
                script {
                    def commitHash = sh(returnStdout: true, script: "git rev-parse --short HEAD").trim()
                    def version = new Date().format("yyyyMMdd-HHmmss") + "-" + commitHash

                    sh "echo ${version} > version.txt"

                    sh "git tag -a v${version} -m 'Release ${version}'"
                    sh "git push origin v${version}"

                    echo "Released version: ${version}"
                }
            }
        }


        stage('Monitoring') {
            steps {
                echo 'Monitoring application...'
                script {
                    def appUrl = "https://my-flask-crud-app.herokuapp.com"

                    def statusCode = sh(returnStdout: true, script: "curl -o /dev/null -s -w '%{http_code}' ${appUrl}").trim()
                    if (statusCode == "200") {
                        echo "✅ Application is UP and healthy (HTTP 200)"
                    } else {
                        error("❌ Health check failed! Status code: ${statusCode}")
                    }

                    sh "heroku logs --tail --app my-flask-crud-app --num 50"
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
