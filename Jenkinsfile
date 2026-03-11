pipeline {
  agent any

  environment {
    IMAGE_TAG = "${BUILD_NUMBER}"
    REGISTRY  = "ghcr.io/ixone0"
  }

  stages {

    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Login GHCR') {
      steps {
        withCredentials([usernamePassword(
          credentialsId: 'ghcr-creds',
          usernameVariable: 'GHCR_USER',
          passwordVariable: 'GHCR_TOKEN'
        )]) {
          sh 'echo $GHCR_TOKEN | docker login ghcr.io -u $GHCR_USER --password-stdin'
        }
      }
    }

    stage('Build & Push') {
      steps {
        sh '''
          docker build --pull -t $REGISTRY/hotel-backend:$IMAGE_TAG backend
          docker build --pull -t $REGISTRY/hotel-frontend:$IMAGE_TAG frontend

          docker push $REGISTRY/hotel-backend:$IMAGE_TAG
          docker push $REGISTRY/hotel-frontend:$IMAGE_TAG
        '''
      }
    }

    stage('Prepare Prod Env File') {
      steps {
        withCredentials([
          file(credentialsId: 'env-prod-file', variable: 'ENV_PROD_FILE')
        ]) {
          sh '''
            cp $ENV_PROD_FILE compose/.env.prod

            if grep -q "^IMAGE_TAG=" compose/.env.prod; then
              sed -i "s/^IMAGE_TAG=.*/IMAGE_TAG=$IMAGE_TAG/" compose/.env.prod
            else
              echo "IMAGE_TAG=$IMAGE_TAG" >> compose/.env.prod
            fi
          '''
        }
      }
    }

    stage('Deploy') {
      steps {
        sh '''
          docker compose \
            -f compose/docker-compose.prod.yml \
            --env-file compose/.env.prod \
            -p hotel down || true

          docker compose \
            -f compose/docker-compose.prod.yml \
            --env-file compose/.env.prod \
            -p hotel pull

          docker compose \
            -f compose/docker-compose.prod.yml \
            --env-file compose/.env.prod \
            -p hotel up -d
        '''
      }
    }
  }

  post {
    always {
      sh 'rm -f compose/.env.prod || true'
      sh 'docker logout ghcr.io || true'
    }
  }
}
