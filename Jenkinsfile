#!groovy
pipeline {
    environment {
        PIP_REQUIRE_VIRTUALENV = '1'
    }
    options {
        buildDiscarder(logRotator(numToKeepStr: '3'))
    }
    agent {
        dockerfile {
            // Use the specified Dockerfile for the agent
            filename 'Dockerfile'
            // Mount the Python package dependencies directory as a Docker volume
            args '-v $HOME/.cache/pip:/root/.cache/pip'
        }
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

        stage('Build') {
            steps {
                sh 'docker build -t myimage:intermediate .'
            }
        }

        stage('Test') {
            steps {
                sh 'docker run --rm myimage:intermediate \
                    python3 -m pytest * -v -o junit_family=xunit1 \
                    --cov=../../main --cov-report xml:../test-results/coverage-cpu.xml \
                    --cov-report html:../test-results/cov_html-cpu \
                    --junitxml=../test-results/results-cpu.xml'
            }
        }

        stage('Publish Test Results') {
            steps {
                junit 'test-results/results-cpu.xml'
            }
        }

        stage('Publish Coverage Report') {
            steps {
                cobertura autoUpdateHealth: false, autoUpdateStability: false, \
                    coberturaReportFile: 'test-results/coverage-cpu.xml', \
                    failUnhealthy: false, failUnstable: false
            }
        }

        stage('Finalize') {
            steps {
                sh 'docker build -t myimage:final .'
                // Additional steps after building the final image if needed
            }
        }
    }
}
