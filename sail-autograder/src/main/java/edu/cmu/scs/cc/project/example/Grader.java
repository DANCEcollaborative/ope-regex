package edu.cmu.scs.cc.project.example;

import edu.cmu.scs.cc.grader.Config;
import edu.cmu.scs.cc.grader.GradingProcessor;
import edu.cmu.scs.cc.grader.strategy.JsonGradeStrategy;
import edu.cmu.scs.cc.grader.strategy.RunnerGradeStrategy;
import java.io.File;
import org.apache.commons.io.FileUtils;

/**
 * Entry class.
 */
public class Grader {

    /**
     * When the grader is executed with command
     * <pre>java -jar java_grader.jar</pre>
     * <em>localMode</em> will be set to <b>true</b><br>
     *
     * When the grader is executed with command
     * <pre>java -jar java_grader.jar submissionFolder submissionFilename
     * feedbackFile scoreFile logFile graderFolder</pre>
     * <em>localMode</em> will be set to <b>false</b><br>
     *
     * AGS will always execute the grader with args and <em>localMode</em>
     * will be <b>false</b>
     *
     * @param args option args
     */
    public static void main(String[] args) {
        // init the config
        Config config = new Config(args);
        // create 1 or more GradeStrategy instance(s)

        try {
            FileUtils.copyFile(new File("/grader/runner.sh"), new File("/submission/runner.sh"));
            FileUtils.copyFile(new File("/grader/print_result.py"), new File("/submission/print_result.py"));
        } catch (Exception e) {
            e.printStackTrace();
        }

        SubRunnerGradeStrategy runnerGradeStrategy = new SubRunnerGradeStrategy(config, "/reference.yaml");
        runnerGradeStrategy.setLocalGraderFolder("/grader/");
        // pass GradeStrategy instance(s) into the GradingProcessor constructor
        GradingProcessor gradingProcessor = new GradingProcessor(
                config, runnerGradeStrategy);
        // and run the GradingProcessor
        gradingProcessor.run();
    }

}
