pipeline {
    agent any

    stages {


        stage('getting code from git') {
            steps {
                git branch: 'main', url: 'https://github.com/Ajmal-MP/JenkinsCI-ArgoCD.git'
            }
        }

        stage('Sonar analysis') {
            
            environment {
                scannerHome = tool 'SonarQube'
            }
            steps {         
                     withSonarQubeEnv('SonarQube') {
                                    withCredentials([string(credentialsId: 'sonar-secret', variable: 'SONAR_TOKEN')]) {
                                                
                                                sh '''
                                                ${scannerHome}/bin/sonar-scanner \
                                                    -Dsonar.login=$SONAR_TOKEN  \
                                                '''
                                    }
                            }
                    }            
            
        } 
        
        
        stage('Quality Gate') {
            steps {
                timeout(time: 1, unit: 'HOURS') {
                waitForQualityGate abortPipeline: true
              }
            }
        }
        
        
    }
}
