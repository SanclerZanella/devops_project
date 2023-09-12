pipeline {
    agent any

    // Create environment variable
    environment {
        // Re-utilised email subject
        EMAIL_SUBJECT = 'Pipeline Status: '
        registry = "sanclerzanella/my-repo"
        registryCredential = 'docker_hub'
        dockerImage = ""
    }

    options {
        // Discard 5 days old builds or max build of 20
        buildDiscarder(logRotator(numToKeepStr: '20', daysToKeepStr: '5'))
    }

    stages {
        stage('checkout') {
            /*
                Responsible for checking out the source code from GIT so that subsequent stages can build, test, and deploy the code.
            */
            steps {
                script {
                    // Trigger the pipeline each 30 minutes
                    properties([pipelineTriggers([pollSCM('H/30 * * * *')])])

                    // Define source repository
                    checkout([$class: 'GitSCM', branches: [[name: 'main']], userRemoteConfigs: [[url: 'https://github.com/SanclerZanella/git_class.git']]])
                }
            }
        }
        stage('run backend server') {
            steps {
                script {
                    // Retrieve the database credentials to run the REST API
                    withCredentials([usernamePassword(credentialsId: 'DB_Credentials', usernameVariable: 'DB_USERNAME', passwordVariable: 'DB_PASSWORD')]) {
                        if (checkOs() == 'Windows') {
                            bat 'start/min python rest_app.py \$DB_USERNAME \$DB_PASSWORD'
                        } else {
                            sh 'nohup python rest_app.py \$DB_USERNAME \$DB_PASSWORD &'
                        }
                    }
                }
            }
        }
        stage('run frontend server') {
            steps {
                script {
                    if (checkOs() == 'Windows') {
                        bat 'start/min python web_app.py'
                    } else {
                        sh 'nohup python web_app.py &'
                    }
                }
            }
        }
        stage('run backend test') {
            steps {
                script {
                    if (checkOs() == 'Windows') {
                        bat 'start/min python backend_testing.py'
                    } else {
                        sh 'nohup python backend_testing.py &'
                    }
                }
            }
        }
        stage('run frontend test') {
            steps {
                script {
                    if (checkOs() == 'Windows') {
                        bat 'start/min python frontend_testing.py'
                    } else {
                        sh 'nohup python frontend_testing.py &'
                    }
                }
            }
        }
        stage('run combined test') {
            steps {
                script {
                    if (checkOs() == 'Windows') {
                        bat 'start/min python combined_testing.py'
                    } else {
                        sh 'nohup python combined_testing.py &'
                    }
                }
            }
        }
        stage('clear environment') {
            steps {
                script {
                    if (checkOs() == 'Windows') {
                        bat 'start/min python clean_environment.py'
                    } else {
                        sh 'nohup python clean_environment.py &'
                    }
                }
            }
        }
        stage('build an push docker image') {
            steps {
                script {
                    dockerImage = docker.build registry + ":$BUILD_NUMBER"
                    docker.withRegistry("", registryCredential){
                        dockerImage.push()
                    }
                }
            }
        }
    }

    post {
        success {
            // Email notification for when the pipeline build succeeds
            emailext (
                to: 'sanclerzjj@gmail.com',
                subject: "${EMAIL_SUBJECT}Successful",
                body: 'The Jenkins pipeline completed successfully.',
                mimeType: 'text/plain',
                replyTo: 'sanclerzjj@gmail.com',
                attachLog: true,
                compressLog: true,
                recipientProviders: [[$class: 'CulpritsRecipientProvider']],
                presendScript: 'import jenkins.plugins.mailer.tasks.MimeMessageBuilder\n\nmsg.setContent(msg.getContent(), "text/html")',
                from: 'sanclerzjj@gmail.com'
            )
        }
        failure {
            // Email notification for when the pipeline build fails
            emailext (
                to: 'sanclerzjj@gmail.com',
                subject: "${EMAIL_SUBJECT}Failed",
                body: 'Please check the Jenkins build status.',
                mimeType: 'text/plain',
                replyTo: 'sanclerzjj@gmail.com',
                attachLog: true,
                compressLog: true,
                recipientProviders: [[$class: 'CulpritsRecipientProvider']],
                presendScript: 'import jenkins.plugins.mailer.tasks.MimeMessageBuilder\n\nmsg.setContent(msg.getContent(), "text/html")',
                from: 'sanclerzjj@gmail.com'
            )
        }
        always {
            if (checkOs() == 'Windows') {
                bat 'docker rmi $registry:$BUILD_NUMBER'
            } else {
                sh 'docker rmi $registry:$BUILD_NUMBER'
            }
        }
    }
}

def checkOs(){
    /*
        Check the system OS
    */
    if (isUnix()) {
        def uname = sh script: 'uname', returnStdout: true
        if (uname.startsWith("Darwin")) {
            return "Macos"
        }
        else {
            return "Linux"
        }
    }
    else {
        return "Windows"
    }
}
