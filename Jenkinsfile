#!groovy

pipeline {

    options {
        buildDiscarder(logRotator(numToKeepStr: '3'))
    }
    agent any
    triggers {
        GenericTrigger(
            genericVariables: [
                [key: 'payload', value: '$']
            ],
            causeString: 'GitHub event',
            token: 'TOKEN',
            printContributedVariables: true,
            printPostContent: true,
            silentResponse: false
        )
    }
    stages {
        stage('Print PWD') {
            steps {
                echo 'Current working directory: ' + pwd()
            }
        }
        stage('Clean Workspace') {
            steps {
                script {
                    // Delete the workspace directory
                    deleteDir()
                }
            }
        }
        stage('Check Docker Installation') {
            steps {
                script {
                    try {
                        // Check Docker version
                        sh 'docker --version'

                        // Check Docker info
                        sh 'docker info'

                        // List Docker images
                        sh 'docker images'

                        // List Docker containers
                        sh 'docker ps -a'
                    } catch (Exception e) {
                        // Handle any errors or failures
                        error("Failed to check Docker installation: ${e.getMessage()}")
                    }
                }
            }
        }


        stage('Parse Payload') {
            steps {
                script {
                    // Get the 'payload' from the environment
                    def payloadString = env.payload
                    if (payloadString == null || payloadString.isEmpty()) {
                        error("Payload is empty. Aborting the build.")
                    }

                    // Parse the JSON payload
                    def json = readJSON text: payloadString

                    echo "Payload: ${json.action}"

                    if (json.action != 'published' || !json.release) {
                        echo "Skipping build as the action is not 'published' or release information is missing."
                        return
                    }

                    echo 'Release URL: ' + json.release.url
                    echo 'Release Name: ' + json.release.name
                    echo 'Author Login: ' + json.release.author.login
                    echo 'Repository Full Name: ' + json.repository.full_name
                    echo 'Tag Name: ' + json.release.tag_name

                    env.RELEASE_URL = json.release.url
                    env.CLONE_URL = json.repository.clone_url
                    env.AUTHOR_LOGIN = json.release.author.login
                    env.REPO_FULL_NAME = json.repository.full_name
                    env.BRANCH_NAME = json.release.target_commitish
                    env.REPO_FOLDER_NAME = json.repository.name
                    env.DOCKER_TAG_NAME = json.release.tag_name
                }
            }
        }

        stage('Checkout Repository') {
            steps {
                script {
                    if (env.RELEASE_URL) {
                        echo "Checking out repository from clone URL: ${env.CLONE_URL}"
                        sh "mkdir -p ${env.REPO_FOLDER_NAME}"

                        // change the current directory to the new directory
                        dir(env.REPO_FOLDER_NAME) {
                            withCredentials([sshUserPrivateKey(credentialsId: 'GITHUB_CREDENTIAL_ID', keyFileVariable: 'KEY')]) {
                                checkout([
                                    $class: 'GitSCM',
                                    branches: [[name: "*/${env.BRANCH_NAME}"]],
                                    doGenerateSubmoduleConfigurations: false,
                                    extensions: [],
                                    submoduleCfg: [],
                                    userRemoteConfigs: [[url: "${env.CLONE_URL}"]]
                                ])
                            }
                        }

                        echo 'Repository checked out successfully.'
                    } else {
                        echo "Release URL is missing. Skipping repository checkout."
                    }
                }
            }
        }
        stage('Prune Docker Images') {
            steps {
                script {
                    sh "docker image prune -f"
                }
            }
        }


        stage('Build Docker Image') {
            steps {

                echo 'Building Docker Image...'
                script {
                    // Image name: <repo-name>:<tag-name> (e.g. myimage:latest) must be lowercase
                    dir(env.REPO_FOLDER_NAME) {
                        sh 'ls -a'
                        sh 'pwd'
                        def dockerImage = docker.build("${env.REPO_FOLDER_NAME.toLowerCase()}:${env.DOCKER_TAG_NAME}", "-f Dockerfile .")
                    }
                }
            }
        }

        stage('Run Container and Test') {
            steps {
                script {
                    echo 'Running Docker Container and Tests...'
                    def app = docker.image("${env.REPO_FOLDER_NAME.toLowerCase()}:${env.DOCKER_TAG_NAME}")

                    // Jenkins Secrets from .env file
//                     def db_collection_name = sh(script: 'cat ${SECRET_FILE} | grep DB_COLLECTION_NAME | cut -d "=" -f 2', returnStdout: true).trim()
//                     def db_name = sh(script: 'cat ${SECRET_FILE} | grep DB_NAME | cut -d "=" -f 2', returnStdout: true).trim()
//                     def db_password = sh(script: 'cat ${SECRET_FILE} | grep DB_PASSWORD | cut -d "=" -f 2', returnStdout: true).trim()
//                     def db_username = sh(script: 'cat ${SECRET_FILE} | grep DB_USERNAME | cut -d "=" -f 2', returnStdout: true).trim()
//                     def mqtt_clean_session = sh(script: 'cat ${SECRET_FILE} | grep MQTT_CLEAN_SESSION | cut -d "=" -f 2', returnStdout: true).trim()
//                     def mqtt_client_id = sh(script: 'cat ${SECRET_FILE} | grep MQTT_CLIENT_ID | cut -d "=" -f 2', returnStdout: true).trim()
//                     def mqtt_cluster_url = sh(script: 'cat ${SECRET_FILE} | grep MQTT_CLUSTER_URL | cut -d "=" -f 2', returnStdout: true).trim()
//                     def mqtt_keepalive = sh(script: 'cat ${SECRET_FILE} | grep MQTT_KEEPALIVE | cut -d "=" -f 2', returnStdout: true).trim()
//                     def mqtt_password = sh(script: 'cat ${SECRET_FILE} | grep MQTT_PASSWORD | cut -d "=" -f 2', returnStdout: true).trim()
//                     def mqtt_port = sh(script: 'cat ${SECRET_FILE} | grep MQTT_PORT | cut -d "=" -f 2', returnStdout: true).trim()
//                     def mqtt_username = sh(script: 'cat ${SECRET_FILE} | grep MQTT_USERNAME | cut -d "=" -f 2', returnStdout: true).trim()
                    def db_collection_name = sh(script: 'cat ${SECRET_FILE} | grep DB_COLLECTION_NAME | awk -F "=" \'{for(i=2; i<=NF; i++) printf "%s ", $i}\'', returnStdout: true).trim()
                    def db_name = sh(script: 'cat ${SECRET_FILE} | grep DB_NAME | awk -F "=" \'{for(i=2; i<=NF; i++) printf "%s ", $i}\'', returnStdout: true).trim()
                    def db_password = sh(script: 'cat ${SECRET_FILE} | grep DB_PASSWORD | awk -F "=" \'{for(i=2; i<=NF; i++) printf "%s ", $i}\'', returnStdout: true).trim()
                    def db_username = sh(script: 'cat ${SECRET_FILE} | grep DB_USERNAME | awk -F "=" \'{for(i=2; i<=NF; i++) printf "%s ", $i}\'', returnStdout: true).trim()
                    def mqtt_clean_session = sh(script: 'cat ${SECRET_FILE} | grep MQTT_CLEAN_SESSION | awk -F "=" \'{for(i=2; i<=NF; i++) printf "%s ", $i}\'', returnStdout: true).trim()
                    def mqtt_client_id = sh(script: 'cat ${SECRET_FILE} | grep MQTT_CLIENT_ID | awk -F "=" \'{for(i=2; i<=NF; i++) printf "%s ", $i}\'', returnStdout: true).trim()
                    def mqtt_cluster_url = sh(script: 'cat ${SECRET_FILE} | grep MQTT_CLUSTER_URL | awk -F "=" \'{for(i=2; i<=NF; i++) printf "%s ", $i}\'', returnStdout: true).trim()
                    def mqtt_keepalive = sh(script: 'cat ${SECRET_FILE} | grep MQTT_KEEPALIVE | awk -F "=" \'{for(i=2; i<=NF; i++) printf "%s ", $i}\'', returnStdout: true).trim()
                    def mqtt_password = sh(script: 'cat ${SECRET_FILE} | grep MQTT_PASSWORD | awk -F "=" \'{for(i=2; i<=NF; i++) printf "%s ", $i}\'', returnStdout: true).trim()
                    def mqtt_port = sh(script: 'cat ${SECRET_FILE} | grep MQTT_PORT | awk -F "=" \'{for(i=2; i<=NF; i++) printf "%s ", $i}\'', returnStdout: true).trim()
                    def mqtt_username = sh(script: 'cat ${SECRET_FILE} | grep MQTT_USERNAME | awk -F "=" \'{for(i=2; i<=NF; i++) printf "%s ", $i}\'', returnStdout: true).trim()

                    def customEnv = [
                        "DB_COLLECTION_NAME=${db_collection_name}",
                        "DB_NAME=${db_name}",
                        "DB_PASSWORD=${db_password}",
                        "DB_USERNAME=${db_username}",
                        "MQTT_CLEAN_SESSION=${mqtt_clean_session}",
                        "MQTT_CLIENT_ID=${mqtt_client_id}",
                        "MQTT_CLUSTER_URL=${mqtt_cluster_url}",
                        "MQTT_KEEPALIVE=${mqtt_keepalive}",
                        "MQTT_PASSWORD=${mqtt_password}",
                        "MQTT_PORT=${mqtt_port}",
                        "MQTT_USERNAME=${mqtt_username}"
                    ]

                    dir(env.REPO_FOLDER_NAME) {

                        app.inside("-e ${customEnv.join(' -e ')} -p 8008:8008") {
                            dir('main') {
                                sh 'ls -a'
                                sh 'pwd'
                                sh "python3 -m pytest * -v -o junit_family=xunit1 --cov=../main --cov-report xml:../reports/coverage-cpu.xml --cov-report html:../reports/cov_html-cpu --junitxml=../reports/results-cpu.xml"
                            }
                        }
                    }
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                echo 'Pushing Docker Image...'
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
                        dockerImage.push("mik_backend:v0.1.0-beta")
                    }
                }
            }
        }

//                 stage('Finalize') {
//                     steps {
//                         sh 'docker build -t myimage:final .'
//                         // Additional steps after building the final image if needed
//                     }
//                 }
    }
}