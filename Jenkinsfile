pipeline {
  agent any

  stages {
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
          docker build -t ghcr.io/ixone0/hotel-backend backend
          docker build -t ghcr.io/ixone0/hotel-frontend frontend
          docker push ghcr.io/ixone0/hotel-backend
          docker push ghcr.io/ixone0/hotel-frontend
        '''
      }
    }

    stage('Deploy') {
      steps {
        sh '''
          docker compose -p hotel down || true
          docker compose -p hotel pull
          docker compose -p hotel up -d
        '''
      }
    }
  }
}
