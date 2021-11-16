# Dev Tools Setup
Recommandation usr MacOs or Linux or WindowsSubsystemLinux to interact with this project.

Minikube setup is require to test/run the application. 

[See this project to help you for the setup.](https://github.com/public-sysunicorns-info/minikube_local_setup)

## 1. VSCode
[Install VSCode](https://test.com)
[To see recommanded extensions use](https://code.visualstudio.com/docs/editor/extension-marketplace#_recommended-extensions)

## 2. Python

[Install on your system Python3.9](https://www.python.org/downloads/)

Version Python3.9 

End of Support : 2025-10

### 2.1 Setup / Install VirutalEnv (venv)
``` bash
#!/usr/bin/env bash

# Install Globally VirtualEnv (venv)
python3.9 -m pip venv

# Setup VirtualEnv in local project dir
python3.9 -m venv .venv
```

## 3. NPM Tooling

[Install nodejs for tooling execution](https://nodejs.org/en/download/) or [use brew for MacOs](https://formulae.brew.sh/formula/node)
``` bash
#!/usr/bin/env bash

# Install Package contains in package.json
npm install
```

### 3.1 Git Hook
Git hook is use to control and provide template for commit.

Hooks:
- [commitizen](http://commitizen.github.io/cz-cli/) :
Help to write better commit with fix format (take in account by semantic-release)
``` bash
#!/usr/bin/env bash

git add your_file_to_add_for_commit
# replace git commit and create commit with interaction
npx cz
```
- [commitlint](https://commitlint.js.org/#/) : Control commit format to be compliant with [@commitlint/config-conventional rules](https://github.com/conventional-changelog/commitlint/tree/master/%40commitlint/config-conventional)

How to install hook:
``` bash
#!/usr/bin/env bash

# Use hushky to setup git hook
npx husky install
```

### 3.2 Release Tools

Create manually release,tag and package on the Github with
[semantic-release](https://github.com/semantic-release/semantic-release) on git main branch.
How to create release manually:
``` bash
#!/usr/bin/env bash

# Get Token from Github -> Settings 
# -> Developper Settings -> Personnal Access Tokens
# Scope to claim : repo:*
export GITHUB_TOKEN=*********

./script/release.sh
```

## 4. Docker

### 4.1 Docker Login with [Github Container Registry (ghcr.io)](ghcr.io)
Add the capacity to interact with Github Container Registry for docker-cli [Github Docs](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
``` bash
#!/usr/bin/env bash

# Get Token from Github -> Settings 
# -> Developper Settings -> Personnal Access Tokens
# Scope to claim : write:packages, read:packages
export GITHUB_TOKEN=*********
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
```

### 4.2 Docker with Minikube
Connect docker-cli to minikube ( replase docker-desktop due to the new licence constraint )
``` bash
#!/usr/bin/env bash

# Setup Docker Config of docker-cli 
# to use minikube as dockerd backend
eval $(minikube -p minikube docker-env)
```

## 5. Skaffold
[How to install skaffold](https://skaffold.dev/docs/install/)

Prepare minikube/kube by creating manually the namespace (only first time)
``` bash
#!/usr/bin/env bash

kubectl create namespace websocket-example
```

Command to launch/update application on minikube
``` bash
#!/usr/bin/env bash

./script/skaffold-run.sh
```

[After installion, you can access to the api](https://api.websocket-example.minikube/docs)
