#!groovy
pipeline {
    agent any
    environment {
        PIP_REQUIRE_VIRTUALENV = '1'
    }
    options {
        buildDiscarder(logRotator(numToKeepStr: '3'))
    }

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

        stage('Clean Workspace') {
            steps {
                script {
                    // Delete the workspace directory
                    deleteDir()
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

                    env.RELEASE_URL = json.release.url
                    env.CLONE_URL = json.repository.clone_url
                    env.RELEASE_NAME = json.release.name
                    env.AUTHOR_LOGIN = json.release.author.login
                    env.REPO_FULL_NAME = json.repository.full_name
                    env.BRANCH_NAME = json.release.target_commitish
                    env.REPO_FOLDER_NAME = json.repository.name

                }
            }
        }

        stage('Checkout Repository') {
            steps {
                script {
                    def cloneUrl = env.CLONE_URL
                    def targetBranch = env.BRANCH_NAME
                    def releaseUrl = env.RELEASE_URL
                    def repoFolderName = env.REPO_FOLDER_NAME
                    echo 'Clone URL:'+ cloneUrl
                    echo 'Release URL:'+ releaseUrl

                    if (releaseUrl) {
                        echo "Checking out repository from clone URL: $cloneUrl"
                        sh "mkdir -p $repoFolderName"

                        // change the current directory to the new directory
                        dir("$repoFolderName") {
                            withCredentials([sshUserPrivateKey(credentialsId: 'GITHUB_CREDENTIAL_ID', keyFileVariable: 'KEY')]) {
                                checkout([
                                    $class: 'GitSCM',
                                    branches: [[name: "*/$targetBranch"]],
                                    doGenerateSubmoduleConfigurations: false,
                                    extensions: [],
                                    submoduleCfg: [],
                                    userRemoteConfigs: [[url: cloneUrl]]
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

        stage('Setup Python') {
            steps {
                script {
                    // Checking if Python 3.10 is installed and installing if it's not
                    sh '''
                        echo "Checking if Python 3.10 is installed..."
                        if ! command -v python3.10
                        then
                            echo "Python 3.10 is not installed, installing now"
                            yes | apt -qq update
                            yes | apt -qq install software-properties-common
                            yes | add-apt-repository ppa:deadsnakes/ppa
                            yes | apt -qq update
                            yes | apt -qq install python3.10
                            yes | apt -qq install python3.10 python3.10-venv
                            ln -sf /usr/bin/python3.10 /usr/bin/python3
                            echo "Installed python version: "
                            python3 --version

                            # Check if Python 3.10 is now installed
                            if ! command -v python3.10
                            then
                                echo "Failed to install Python 3.10"
                                exit 1
                            fi

                        else
                            echo "Python 3.10 is already installed"
                        fi
                    '''
                }
            }

        }


        stage('Setup environment') {
            steps {
                script{
                    def currentDir = pwd()
                    def repoFolderName = env.REPO_FOLDER_NAME
                    echo "Current working directory: $currentDir"
                    // Set up the Python environment
                    dir("$repoFolderName") {
                        sh '''
                        python3 -m ensurepip --upgrade
                        mkdir -p py310
                        python3 -m venv py310
                        . py310/bin/activate
                        pip install -r requirements.txt
                        '''
                    }
                }
            }
        }


        stage('Run Unit Tests') {
            steps {
                script {
                    def repoFolderName = env.REPO_FOLDER_NAME
                    def pythonPath = "${env.WORKSPACE}/${repoFolderName}"
                    def venvDir = "py310/bin/activate"

                    echo "Current working directory: ${env.WORKSPACE}"

                    dir(repoFolderName) {
                        // Activate the Python virtual environment and run tests
                        withEnv(["PYTHONPATH=${pythonPath}"]) {
                            sh """#!/bin/bash
                                . ${venvDir}
                                cd main/tests
                                python3 -m pytest * -v -o junit_family=xunit1 \
                                --cov=../../main --cov-report xml:../test-results/coverage-cpu.xml \
                                --cov-report html:../test-results/cov_html-cpu \
                                --junitxml=../test-results/results-cpu.xml
                            """
                        }
                    }
                }
            }
        }

        stage('Post Test Actions') {
            steps {
                junit '../test-results/results-cpu.xml'
                cobertura coberturaReportFile: '../test-results/coverage-cpu.xml'
            }
        }

        stage('Build') {
            steps {
                script {
                    // Build your project here
                    echo 'Building...'
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    // Run tests here
                    echo 'Running tests...'
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Deploy your project here
                    echo 'Deploying...'
                }
            }
        }
    }
}
