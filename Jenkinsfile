pipeline {
    agent any
    stages {
        stage('Setup Python') {
            steps {
                script {
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
                        else
                            echo "Python 3.10 is already installed"
                        fi
                    '''
                }
            }
        }
        stage('Checkout') {
            steps {
                echo "Cloning the git repository..."
                git 'https://github.com/your-username/your-repo.git'
            }
        }
        stage('Set up Python environment') {
            steps {
                script {
                    echo "Creating Python 3.10 virtual environment..."
                    sh 'python3.10 -m venv py310'

                    echo "Activating the virtual environment..."
                    sh 'source py310/bin/activate'

                    echo "Installing dependencies from requirements.txt..."
                    sh 'pip install -r requirements.txt'
                }
            }
        }
        // Ek aşamalarını burada belirt
    }
}
