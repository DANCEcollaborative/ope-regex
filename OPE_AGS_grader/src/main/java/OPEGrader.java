import edu.cmu.scs.cc.grader.Config;
import edu.cmu.scs.cc.grader.GradeWriter;
import edu.cmu.scs.cc.grader.GradingProcessor;
import edu.cmu.scs.cc.grader.strategy.JsonGradeStrategy;

public class OPEGrader {
    public static void main(String[] args) {
        // init the config
        Config config = new Config(args);

        // So that solutions are not printed
        GradeWriter gradeWriter = new GradeWriter(config);

        // create 1 or more GradeStrategy instance(s)
        JsonGradeStrategy jsonGradeStrategy = new JsonGradeStrategy(config, "/OPE_score.yaml");

        jsonGradeStrategy.gradeWriter = gradeWriter;

        // pass GradeStrategy instance(s) into the GradingProcessor constructor
        GradingProcessor gradingProcessor = new GradingProcessor(config, jsonGradeStrategy);

        // and run the GradingProcessor
        gradingProcessor.run();
    }
}
