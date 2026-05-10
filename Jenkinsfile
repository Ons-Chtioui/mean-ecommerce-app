pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = 'ecommerce'
        FASTAPI_IMAGE        = 'ecommerce-fastapi'
        FRONTEND_IMAGE       = 'ecommerce-frontend'
    }

    stages {

        stage('Checkout') {
            steps {
                echo '📥 Checking out source code...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo '📦 Installing Python dependencies...'
                dir('backend-python') {
                    sh 'pip install --no-cache-dir -r requirements.txt'
                }
            }
        }

        stage('Test') {
            steps {
                echo '🧪 Running automated tests (excluding connectivity tests)...'
                dir('backend-python') {
                    sh 'pytest tests/ -m "not connectivity" -v --cov=. --cov-report=xml --cov-report=term-missing'
                }
            }
            post {
                always {
                    // Archive test coverage report
                    dir('backend-python') {
                        archiveArtifacts artifacts: 'coverage.xml', allowEmptyArchive: true
                    }
                }
                failure {
                    echo '❌ Tests failed — aborting pipeline'
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                echo '🐳 Building Docker images...'
                script {
                    try {
                        sh 'docker compose build --no-cache'
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        error("Docker build failed: ${e.message}")
                    }
                }
            }
            post {
                failure {
                    echo '❌ Docker build failed — check build logs above'
                    archiveArtifacts artifacts: '**/docker-build.log', allowEmptyArchive: true
                }
            }
        }

        stage('Deploy') {
            steps {
                echo '🚀 Deploying all services...'
                sh 'chmod +x deploy.sh'
                sh './deploy.sh'
            }
            post {
                success {
                    echo '✅ Deployment successful!'
                    echo '   Frontend:  http://localhost:80'
                    echo '   API:       http://localhost:8000'
                    echo '   API Docs:  http://localhost:8000/docs'
                }
                failure {
                    echo '❌ Deployment failed'
                }
            }
        }
    }

    post {
        always {
            echo '🏁 Pipeline finished'
        }
        success {
            echo '✅ Pipeline completed successfully'
        }
        failure {
            echo '❌ Pipeline failed — review the logs above'
        }
    }
}
