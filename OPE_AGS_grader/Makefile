################################################################################
# DOCKER
################################################################################

PROJECT_ID=ope-author-regular-ex-mt8s2z4c
TASK_ID=f979cfa9-40d6-4138-bfe6-52bf25da7e6e
LMS_NAME=sail2
COURSE_TYPE=ppp
ARTIFACT_VERSION=v1
IMAGE_NAME=graders.azurecr.io/grader/$(LMS_NAME)/$(COURSE_TYPE)/$(PROJECT_ID)/$(TASK_ID)
MAINCLASS=OPEGrader


local-all: ope-task-local-deploy

ope-task-local-deploy: clean package local-image-build create-submission-folder local-image-run


## Step 1: Package grader as JAR
clean:
	mvn clean
	@echo ${IMAGE_NAME}

package: clean src pom.xml
	@echo "[SUCCESS]: build"
	mvn package -Dpackage.mainClass=${MAINCLASS}

## Step 2: build the Docker image for local test
local-image-build:
	docker build --rm -f target/docker/Dockerfile --platform linux/amd64 --tag ${IMAGE_NAME}:${ARTIFACT_VERSION}  .

## Step 3: create "submissionFolder" and copy the sample solution into "submissionFolder"
create-submission-folder:
	-rm -r ./submission/${TASK_ID}
	mkdir -p ./submission/${TASK_ID}
	cp -r sample_submission/${TASK_ID}/* ./submission/${TASK_ID}

## Step 4:
## Run the local container to local test
local-image-run:
	docker run -it --rm -v $(CURDIR)/submission/$(TASK_ID):/submission/ -e AGS_V2_ENABLED=false ${IMAGE_NAME}:${ARTIFACT_VERSION}
## you can now view the 3 local files: feedback, log, score


###############################
######## Docker AGS v2 ########
###############################

all: ope-task-ags-deploy

ope-task-ags-deploy: login ags-image-build ags-image-deploy

ags-image-build ags-image-deploy: IMAGE_NAME = graders.azurecr.io/grader/$(LMS_NAME)/$(COURSE_TYPE)/$(PROJECT_ID)/$(TASK_ID)

ags-image-build: clean package
	docker build --rm -f target/docker/Dockerfile --platform linux/amd64 --tag ${IMAGE_NAME}:${ARTIFACT_VERSION}  .

login:
	az acr login -n graders --subscription 4171bf4b-8249-4372-a624-0728a3edb99b

ags-image-deploy: login ags-image-build
	docker push $(IMAGE_NAME):$(ARTIFACT_VERSION)
