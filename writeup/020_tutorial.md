Before you start the OPE session, follow the steps in the OPE primer to access your environment:

1. Log in to the [AWS console](https://752574329361.signin.aws.amazon.com/console) with your AWS credential -- see the AWS IAM username and password in your [Sail profile](https://projects.sailplatform.org/profile).
1. Visit the [Cloud9 console](https://console.aws.amazon.com/cloud9/home/shared) and select the region as `N.Virginia`.
1. Click on the top-left menu icon to open the navigation bar and select the `Shared with me` tab. You should be able to see a Cloud9 session shared with you.

Once you join the OPE session on Cloud9, one of the members from your OPE team should run the below command to setup the OPE environment in the Cloud9 Terminal: 

    wget https://clouddatascience.blob.core.windows.net/ope-problem-representation/sail/v1/env_setup_oneshot.sh  && yes | sh env_setup_oneshot.sh

Then follow the instructions in the `README.md` file, and start your work on `task1.py`. The function docstring will provide a link to an html file that describes the task in detail.

At the end of the session, do not forget to submit the solution using the `submitter` executable. **Every team member** must submit in person to get the result of the session.

Run the executable using the command `./submitter`. Your submission password can be found by clicking on the button at the top right corner of this page. 
  
      ./submitter
      Enter your Sail() username:
      <Type your Sail() username>
      Enter your submission password:
      <Type your Sail() password>

After running the `./submitter` command, you can check your submission result and feedback on the submission tab of the project on Sail().