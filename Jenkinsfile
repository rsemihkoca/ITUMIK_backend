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

        stage('Run Docker Image with Tests') {
            steps {
                script {
                    def app = docker.image("${env.REPO_FOLDER_NAME.toLowerCase()}:${env.DOCKER_TAG_NAME}")

                    // Jenkins credentials binding
                    withCredentials([file(credentialsId: 'SECRET_FILE', variable: 'ENV_VALUES_FILE')]) {
                        script {
                            sh "cat \$SECRET_FILE"
                            def envValues = readFile(ENV_VALUES_FILE)
                            def valuesArray = envValues.split('\n').collect { "-e ${it}" }

                            dir(env.REPO_FOLDER_NAME) {

                                app.withRun('${valuesArray} -d --rm -itp 8008:8008 ') {
                                    c ->
                                    dir('main') {
                                        sh 'ls -a'
                                        sh 'pwd'
                                        sh """
                                        pytest * -v -o junit_family=xunit1 --cov=../main --cov-report xml:../reports/coverage-cpu.xml --cov-report html:../reports/cov_html-cpu --junitxml=../reports/results-cpu.xml
                                        """
                                    }
                                }
                                //sh 'docker run ${valuesArray} -p --rm -itp 8008:8008 -d mik_backend:v0.1.0-beta'
//                                 app.inside(" --env-file ${ENV_VALUES_FILE} -p 8008:8008") {
//                                         dir('main') {
//                                             sh 'ls -a'
//                                             sh 'pwd'
//                                             sh """
//                                                 python3 -m pytest * -v -o junit_family=xunit1 --cov=../main --cov-report xml:../reports/coverage-cpu.xml --cov-report html:../reports/cov_html-cpu --junitxml=../reports/results-cpu.xml
//                                             """
//
//                                     }
//                                 }
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