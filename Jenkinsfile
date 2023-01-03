pipeline {
    agent any
    
    environment {
        build_number = "${env.BUILD_ID}"
    }

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
        
        stage("docker build and push to docker hub") {
            
            steps {
                sh "docker build -t ajmaldocker07/openai-node:${build_number} ."
                withCredentials([usernamePassword(credentialsId: 'docker_id', passwordVariable: 'docker_password', usernameVariable: 'docker_user_name')]) {
                    sh "docker login -u $docker_user_name  -p $docker_password"
                    sh "docker push ajmaldocker07/openai-node:${build_number}"
                    sh "docker rmi ajmaldocker07/openai-node:${build_number}"
                } 
            }  
        }
        
        stage("sed in helm") {
            
            steps {
                
                dir("../openai-helm") {
                    sh "git pull origin main"
                }
                
                dir("../") {
                    sh """
                       sed -i  "18 s/version: [^ ]*/version: ${build_number}/" ./openai-helm/helm-chart/Chart.yaml
                       sed -i  "s/tag: [^ ]*/tag: ${build_number}/" ./openai-helm/helm-chart/values.yaml
                       """
                }
            }
        }
        
        
        stage("push code to helm chart") {
            
            steps {
                        withAWS(credentials: 'aws-credential', region: 'ap-northeast-1') {
                            
                            dir("../openai-helm") {
                                sh "helm package helm-chart/"
                                sh "aws ecr get-login-password | helm registry login  --username AWS -p \$(aws ecr get-login-password --region ap-northeast-1)  765596098884.dkr.ecr.ap-northeast-1.amazonaws.com"
                                sh "helm push  gaming-helm-${build_number}.tgz oci://765596098884.dkr.ecr.ap-northeast-1.amazonaws.com"  
                                sh "rm gaming-helm-${build_number}.tgz"
                            }
                        }
            }
        }
        
        stage("change github helm chart") {
            steps {
                dir("../openai-helm") {
                    withCredentials([usernamePassword(credentialsId: 'helmchart-git', passwordVariable: 'password', usernameVariable: 'username')]) {
                        sh """
                            git add .
                            git commit -m 'jenkins build ${build_number} ' 
                            git push https://${username}:${password}@github.com/Ajmal-MP/openai-helm.git
                           """
                        
                    }
                }
            }
        }

    }
    post {
	       always {
		       sh 'docker logout'
	       }
    }    
}

















