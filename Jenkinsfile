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
            printContributedVariables: false,
            printPostContent: false,
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

                        // Change the current directory to the new directory
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
                            sh "cat \"\$ENV_VALUES_FILE\""
                            def envValues = readFile("${ENV_VALUES_FILE}")
                            def valuesArray = envValues.split('\n').collect { "-e ${it}" } .join(" ")
                            println valuesArray
                            dir(env.REPO_FOLDER_NAME) {
                                app.inside("--env-file \"\$ENV_VALUES_FILE\" -d --rm -p 8008:8008") {
                                    c ->
                                    dir('main') {
                                        sh 'ls -a'
                                        sh 'pwd'
                                        sh 'python -c "import os; print(os.environ[\'DB_PASSWORD\'])"'
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

        stage('Push Docker Image') {
            steps {
                echo 'Pushing Docker Image...'
                script {
                    withCredentials([usernamePassword( credentialsId: 'DOCKERHUB_CREDENTIALS_ID', usernameVariable: 'USER', passwordVariable: 'PASSWORD')]) {
                        def app = docker.image("${env.Author_LOGIN}/${env.REPO_FOLDER_NAME.toLowerCase()}:${env.DOCKER_TAG_NAME}")
                        withDockerRegistry([credentialsId: 'DOCKERHUB_CREDENTIALS_ID', url: ""]) {
                            app.push() // Docker imajını Docker Hub'a gönderin
                        }
                    }
                }
            }
        }

        stage('Generate Cobertura Report') {
            steps {
                echo 'Generating Cobertura Report...'
                dir(env.REPO_FOLDER_NAME) {
                    sh 'cobertura-report.sh'
                }
            }
        }

        stage('Generate JUnit Report') {
            steps {
                echo 'Generating JUnit Report...'
                dir(env.REPO_FOLDER_NAME) {
                    sh 'junit-report.sh'
                }
            }
        }

        stage('Send Email Notification') {
            steps {
                echo 'Sending email notification...'
                emailext(
                    subject: "Pipeline Name: ${env.JOB_NAME} (Duration: ${currentBuild.durationString})",
                    body: "Build completed successfully! Here are the build details:",
                    to: 'rsemihkoca@outlook.com',
                    attachLog: true,
                    attachmentsPattern: 'reports/**/*'
                )
            }
        }
    }
}