#!groovy
pipeline {
    agent any

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
        stage('Configure Sudoers') {
                steps {
                    sh '''
                        echo "${USER} ALL=(ALL) NOPASSWD: ALL" | tee -a /etc/sudoers
                    '''
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

                }
            }
        }

        stage('Checkout Repository') {
            steps {
                script {
                    def cloneUrl = env.CLONE_URL
                    def targetBranch = env.BRANCH_NAME
                    def releaseUrl = env.RELEASE_URL

                    echo 'Clone URL:'+ cloneUrl
                    echo 'Release URL:'+ releaseUrl

                    if (releaseUrl) {
                        echo "Checking out repository from clone URL: $cloneUrl"

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
                        if ! command -v python3.10 &> /dev/null
                        then
                            echo "Python 3.10 is not installed, installing now"
                            sudo apt update
                            sudo apt install software-properties-common
                            sudo add-apt-repository ppa:deadsnakes/ppa
                            sudo apt update
                            sudo apt install python3.10

                            # Check if Python 3.10 is now installed
                            if ! command -v python3.10 &> /dev/null
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
                // Set up the Python environment
                sh '''
                python3 -m venv .py310
                source .py310/bin/activate
                pip install -r requirements.txt
                '''
            }
        }


        stage('Run Unit Tests') {
            steps {
                script {
                    // Activate the Python virtual environment
                    sh 'source .py310/bin/activate'

                    // Run the unit tests
                    def unitTestResult = sh returnStatus: true, script: 'python -m unittest discover -s tests -p "test_*.py"'

                    // Log the unit test output
                    echo "Unit Test Output:\n${unitTestResult}"

                    // Check the unit test result
                    if (unitTestResult != 0) {
                        error('Unit tests failed. Exiting Jenkins pipeline.')
                    }

                    echo 'Unit tests passed.'

                }
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
