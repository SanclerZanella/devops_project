pipeline {
    agent any

    environment {
        EMAIL_SUBJECT = 'Pipeline Status: '
        EMAIL_RECIPIENTS = 'sanclerzjj@gmail.com'
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '20', daysToKeepStr: '5'))
    }

    stages {
        stage('checkout') {
            steps {
                script {
                    properties([pipelineTriggers([pollSCM('H/30 * * * *')])])
                    checkout([$class: 'GitSCM', branches: [[name: 'main']], userRemoteConfigs: [[url: 'https://github.com/SanclerZanella/git_class.git']]])
                }
            }
        }
        stage('run backend server') {
            steps {
                script {
                    if (checkOs() == 'Windows') {
                        bat 'start/min python rest_app.py'
                    } else {
                        sh 'nohup python rest_app.py &'
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
    }

    post {
        success {
            emailext (
                to: '${EMAIL_RECIPIENTS}',
                subject: "${EMAIL_SUBJECT}Successful",
                body: 'The Jenkins pipeline completed successfully.',
                mimeType: 'text/plain',
                replyTo: '${EMAIL_RECIPIENTS}',
                attachLog: true,
                compressLog: true,
                recipientProviders: [[$class: 'CulpritsRecipientProvider']],
                presendScript: 'import jenkins.plugins.mailer.tasks.MimeMessageBuilder\n\nmsg.setContent(msg.getContent(), "text/html")',
                from: '${EMAIL_RECIPIENTS}'
            )
        }
        failure {
            emailext (
                to: '${EMAIL_RECIPIENTS}',
                subject: "${EMAIL_SUBJECT}Failed",
                body: 'Please check the Jenkins build status.',
                mimeType: 'text/plain',
                replyTo: '${EMAIL_RECIPIENTS}',
                attachLog: true,
                compressLog: true,
                recipientProviders: [[$class: 'CulpritsRecipientProvider']],
                presendScript: 'import jenkins.plugins.mailer.tasks.MimeMessageBuilder\n\nmsg.setContent(msg.getContent(), "text/html")',
                from: '${EMAIL_RECIPIENTS}'
            )
        }
    }
}

def checkOs(){
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
