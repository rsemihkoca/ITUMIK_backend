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
            env.RELEASE_NAME = json.release.name
            env.AUTHOR_LOGIN = json.release.author.login
            env.REPO_FULL_NAME = json.repository.full_name
            env.BRANCH_NAME = json.release.target_commitish
            env.REPO_FOLDER_NAME = json.repository.name

          }
        }
      }

      stage('Build Docker Image') {
        steps {
          sh 'ls -a'
          echo 'Building Docker Image...'
          script {
          def dockerImage = docker.build("mik_backend:v0.1.0-beta", "-f ${env.WORKSPACE}/Dockerfile ${env.WORKSPACE}")          }
        }
      }

      stage('Run Container and Test') {
        steps {
          script {
            echo 'Running Docker Container and Tests...'
            def app = docker.image('mik_backend:v0.1.0-beta')
            def customEnv = [
              "DB_COLLECTION_NAME=MIK_Collection",
              "DB_NAME=MIK_Database",
              "DB_PASSWORD=iBmz2iInhubGNl8N",
              "DB_USERNAME=python_client",
              "MQTT_CLEAN_SESSION=False",
              "MQTT_CLIENT_ID=999",
              "MQTT_CLUSTER_URL=77de85f1ab254b9a81b50e2967d53988.s2.eu.hivemq.cloud",
              "MQTT_KEEPALIVE=10",
              "MQTT_PASSWORD=Z>!=z\"6kC;_MYzx",
              "MQTT_PORT=8883",
              "MQTT_USERNAME=python_client"
            ]

            app.inside("-e ${customEnv.join(' -e ')} -p 8008:8008") {
              sh "python3 -m pytest * -v -o junit_family=xunit1 --cov=../main --cov-report xml:../reports/coverage-cpu.xml --cov-report html:../reports/cov_html-cpu --junitxml=../reports/results-cpu.xml"
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

        stage('Finalize') {
          steps {
            sh 'docker build -t myimage:final .'
            // Additional steps after building the final image if needed
          }
        }
  }

}