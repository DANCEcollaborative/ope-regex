PROJECT_ID=ope-author-practice-xvjlkkm3
TASK_ID=a6802abd-e9ad-48aa-934c-0b35ce1e320a
LMS_NAME=sail2
COURSE_TYPE=foundation-data-science
ARTIFACT_VERSION=v1
IMAGE_NAME=graders.azurecr.io/grader/$(LMS_NAME)/$(PROJECT_ID)/$(TASK_ID)
MAINCLASS = edu.cmu.scs.cc.project.example.Grader

#################
## package maven jar
#################
## Step 1: package the grader as a JAR
clean:
	mvn clean

package: clean src pom.xml
	mvn package -Dpackage.mainClass=${MAINCLASS} -s settings.xml

## Step 2: build the Docker image for local test
local-image-build:
	docker build --rm -t ${IMAGE_NAME}/local -f target/docker/Dockerfile .

## Step 3: create "submissionFolder" and copy the sample solution into "submissionFolder"
create-submission-folder:
	rm -rf ./submission
	mkdir -p ./submission
	cp -r ./sample_submission/*  ./submission/

## Step 4:
## Run the local container to local test
local-image-run: package local-image-build create-submission-folder
	docker run -it --rm -v "$(CURDIR)/submission:/submission" -e AGS_V2_ENABLED=false ${IMAGE_NAME}/local
## you can now view the 3 local files: feedback, log, score

################################################################################
# DOCKER AGSV2
################################################################################

ags-image-build: clean package
	docker build --rm -t $(IMAGE_NAME):$(ARTIFACT_VERSION) -f target/docker/Dockerfile .

login :
	az login
	az acr login -n graders

## Step 5:
## Deploy to AGSv2
ags-image-deploy : login ags-image-build
	docker push $(IMAGE_NAME):$(ARTIFACT_VERSION)
