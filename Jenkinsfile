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
            token: 'TOKEN_backend',
            printContributedVariables: false,
            printPostContent: false,
            silentResponse: false
        )
    }
    stages {

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
                        currentBuild.result = 'ABORTED'
                        error('Pipeline aborted.')
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

        stage('Checkout Repository') {
            steps {
                script {
                    if (env.RELEASE_URL) {
                        echo "Checking out repository from clone URL: ${env.CLONE_URL}"
                        sh "mkdir -p ${env.REPO_FOLDER_NAME}"

                        // Change the current directory to the new directory
                        dir(env.REPO_FOLDER_NAME) {
                            withCredentials([usernamePassword(credentialsId: 'GITHUB_CREDENTIAL_ID', usernameVariable: 'GITHUB_USER', passwordVariable: 'GITHUB_TOKEN')]) {
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
                    sh 'docker images | awk \'/mik_backend|mik_frontend/ { print $3 }\' | xargs docker rmi'
                }
            }
        }

        stage('Build Test Docker Image') {
            steps {
                echo 'Building Test Docker Image...'
                script {
                    // Image name: <repo-name>:<tag-name> (e.g. myimage:latest) must be lowercase
                    dir(env.REPO_FOLDER_NAME) {
                    sh 'ls -a'
                    sh 'pwd'
                    def dockerImage = docker.build(
                    "${env.REPO_FOLDER_NAME.toLowerCase()}:${env.DOCKER_TAG_NAME}-test",
                    "--file Dockerfile --build-arg DOCKER_BUILDKIT=1 --target test-image .")
                    }
                }
            }
        }


        stage('Unit Tests') {
            steps {
                script {
                    def app = docker.image("${env.REPO_FOLDER_NAME.toLowerCase()}:${env.DOCKER_TAG_NAME}-test")

                    // Jenkins credentials binding
                    withCredentials([file(credentialsId: 'SECRET_FILE', variable: 'ENV_VALUES_FILE')]) {
                        script {
                            //sh "cat \"\$ENV_VALUES_FILE\""
                            def envValues = readFile("${ENV_VALUES_FILE}")
                            def valuesArray = envValues.split('\n').collect { "-e ${it}" } .join(" ")
                            // println valuesArray
                            dir(env.REPO_FOLDER_NAME) {
                                app.inside("--env-file \"\$ENV_VALUES_FILE\" -d --rm -p 8008:8008") {
                                    c ->
                                    dir('main') {
                                        sh 'ls -a'
                                        sh 'pwd'
                                        //sh 'python -c "import os; print(os.environ[\'DB_PASSWORD\'])"'
                                        //sh 'python -c "import os; [print(key, \'=\', value) for key, value in os.environ.items() if key != \'PATH\']"'

                                        sh """
                                        if grep -q docker /proc/1/cgroup; then
                                            echo inside docker
                                        else
                                            echo on host
                                            exit
                                        fi
                                        """
                                        sh """
                                        python3 -m pytest * -v -o junit_family=xunit1 --cov=../main --cov-report xml:../reports/coverage-cpu.xml --cov-report html:../reports/cov_html-cpu --junitxml=../reports/results-cpu.xml
                                        """
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        stage('Push Final Image') {
            steps {
               script {
                     dir(env.REPO_FOLDER_NAME) {
                         echo "Building the final image"
                         docker.build("${env.REPO_FOLDER_NAME.toLowerCase()}:${env.DOCKER_TAG_NAME}", "--file Dockerfile --build-arg DOCKER_BUILDKIT=1 --target runtime-image .")

                         echo "Pushing the image to docker hub"
                         def localImage = "${env.REPO_FOLDER_NAME.toLowerCase()}:${env.DOCKER_TAG_NAME}"

                         // username in the DockerHub
                         def repositoryName = "${AUTHOR_LOGIN}/${localImage}"

                         // Create a tag that going to push into DockerHub
                         sh "docker tag ${localImage} ${repositoryName} "
                         docker.withRegistry("", "DOCKERHUB_CREDENTIALS_ID") {
                           def app = docker.image("${repositoryName}");
                           app.push()
                     }
                  }
               }
            }
        }

        stage('Update Manifests File') {
            steps {
                script {
                    // Define manifest repo and folder details
                    def manifestRepoURL = 'https://github.com/rsemihkoca/ITUMIK_manifests.git'
                    def manifestRepoFolderName = 'ITUMIK_manifests'
                    def manifestFolder = 'backend'
                    def manifestFile = "${manifestRepoFolderName}/${manifestFolder}/frontend-application.yaml"
                    def newImage = "${env.AUTHOR_LOGIN}/${env.REPO_FOLDER_NAME.toLowerCase()}:${env.DOCKER_TAG_NAME}"

                    withCredentials([usernamePassword(credentialsId: 'GITHUB_CREDENTIAL_ID', usernameVariable: 'GITHUB_USER', passwordVariable: 'GITHUB_TOKEN')]) {

                        sh "git clone ${manifestRepoURL}"

                        // Check if manifest file exists
                        if (fileExists(manifestFile)) {
                            echo "Updating manifest file with new image: ${newImage}"

                            // Read the manifest file
                            def manifestContent = readFile(manifestFile)

                            // Replace the old image with the new image
                            manifestContent = manifestContent.replaceAll("${env.AUTHOR_LOGIN}/${env.REPO_FOLDER_NAME.toLowerCase()}:v[0-9\\\\.]+", newImage)

                            // Write the updated content back to the file
                            writeFile(file: manifestFile, text: manifestContent)

                            echo "Manifest file updated successfully."

                            // Optional: Push changes back to the repository
                            dir(manifestRepoFolderName) {
                                sh "git config user.email rsemihkoca@outlook.com"
                                sh "git config user.name rsemihkoca"
                                sh "git remote set-url origin ${manifestRepoURL}"
                                sh "git remote -v"
                                sh "git add ."
                                sh "git commit -m '${newImage}'"

                                // Use GIT_ASKPASS to provide the token instead of embedding in URL
                                sh """
                                   # Set up GIT_ASKPASS
                                   echo '#!/bin/sh' > askpass.sh
                                   echo 'echo \$GITHUB_TOKEN' >> askpass.sh
                                   chmod +x askpass.sh
                                   export GIT_ASKPASS="\$PWD/askpass.sh"

                                   git push origin main
                                """
                            }

                        } else {
                            error("Manifest file '${manifestFile}' does not exist.")
                        }

                    }
                }
            }
        }
    }
}