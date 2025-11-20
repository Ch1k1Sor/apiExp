pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "tierraconnect-api"
        DOCKER_TAG = "${BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Clonando repositorio...'
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Construyendo imagen Docker...'
                script {
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                    docker.build("${DOCKER_IMAGE}:latest")
                }
            }
        }
        
        stage('Test') {
            steps {
                echo 'Ejecutando pruebas...'
                script {
                    docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").inside {
    sh """
    python - << 'EOF'
import app
print("API importada correctamente")
EOF
    """
}

                }
            }
        }
        
        stage('Deploy') {
            steps {
                echo 'Desplegando contenedor...'
                script {
                    sh '''
                        docker stop tierraconnect-api || true
                        docker rm tierraconnect-api || true
                        docker run -d \
                            --name tierraconnect-api \
                            -p 5000:5000 \
                            ${DOCKER_IMAGE}:${DOCKER_TAG}
                    '''
                }
            }
        }
        
        stage('Verify') {
            steps {
                echo 'Verificando despliegue...'
                sh 'sleep 5'
                sh 'curl http://localhost:5000 || exit 1'
            }
        }
    }
    
    post {
        success {
            echo '✅ Pipeline ejecutado exitosamente'
        }
        failure {
            echo '❌ Pipeline falló'
        }
    }

}
