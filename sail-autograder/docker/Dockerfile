FROM openjdk:8-jre-slim

# if AGS_V2_ENABLED is true, the grader will communicate with grading document service
# Disable AGS_V2_ENABLED during local test (`-e AGS_V2_ENABLED='false'`)
ENV AGS_V2_ENABLED true

################################################################################
# Add external datasets / configuration / etc...that are required by your grader
################################################################################

# install python 3
RUN apt-get update && apt-get install -y python3-pip
COPY src/main/resources/requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# add the grader executable and resources to the docker image.
ADD target/java_grader.jar /grader/java_grader.jar
ADD src/main/resources/runner.sh /grader/runner.sh
ADD src/main/resources/print_result.py /grader/print_result.py

# the grader exists in the "/grader" directory, however all submission files including student tar file exist in submission directory
# DO NOT MODIFY THIS LINE
WORKDIR /submission

# the main grading command
# DO NOT MODIFY THIS LINE
ENTRYPOINT ["java", "-XX:-OmitStackTraceInFastThrow", "-ea", "-Dfile.encoding=UTF-8", "-jar", "/grader/java_grader.jar"]