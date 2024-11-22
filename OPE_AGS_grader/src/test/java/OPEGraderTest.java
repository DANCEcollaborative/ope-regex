import edu.cmu.scs.cc.grader.Config;
import edu.cmu.scs.cc.grader.GradeWriter;
import edu.cmu.scs.cc.grader.strategy.JsonGradeStrategy;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.powermock.core.classloader.annotations.PowerMockIgnore;
import org.powermock.modules.junit4.PowerMockRunner;

import java.nio.file.Paths;
import java.util.HashMap;

@RunWith(PowerMockRunner.class)
@PowerMockIgnore({"javax.net.ssl.*"})
public class OPEGraderTest {
    private JsonGradeStrategy strategy;

    private static String globalPath = Paths.get("src", "test", "resources").toString();

    @Mock
    private Config config;

    @Mock
    private static GradeWriter gradeWriter;

    public void stubMethodsWithTestFolder(String testFolder) {
        // use Mockito to set the submission folder during unit test
        // in order to read from the test sample submission folder
        Mockito.when(config.getSubmissionFolder()).thenReturn(Paths.get(globalPath, testFolder).toFile().getAbsolutePath() + "/");
        // write to a local "feedback" file under the test sample submission folder
        Mockito.when(config.getFeedbackFile()).thenReturn("feedback");
        // write to a local "log" file under the test sample submission folder
        Mockito.when(config.getLogFile()).thenReturn("log");
        strategy = new JsonGradeStrategy(config,"/OPE_score.yaml");
    }

    @Test
    public void testGradeValid() {
        stubMethodsWithTestFolder("pass");
        HashMap<String, Comparable> score = strategy.grade();
        Assert.assertEquals( 1.0, score.get("task1"));
        Assert.assertEquals( 1.0, score.get("task2"));
        Assert.assertEquals( 1.0, score.get("task3"));
        Assert.assertEquals( 1.0, score.get("task4"));
        Assert.assertEquals( 1.0, score.get("task5"));
        Assert.assertEquals( 1.0, score.get("task6"));
        Assert.assertEquals( 1.0, score.get("task7"));
        Assert.assertEquals( 1.0, score.get("task8"));
    }

    @Test
    public void testGradeInvalid() {
        stubMethodsWithTestFolder("fail");
        HashMap<String, Comparable> score = strategy.grade();
        Assert.assertEquals( 1.0, score.get("task1"));
        Assert.assertEquals( 0.0, score.get("task2"));
        Assert.assertEquals( 1.0, score.get("task3"));
        Assert.assertEquals( 1.0, score.get("task4"));
        Assert.assertEquals( 1.0, score.get("task5"));
        Assert.assertEquals( 1.0, score.get("task6"));
        Assert.assertEquals( 1.0, score.get("task7"));
        Assert.assertEquals( 1.0, score.get("task8"));
    }
}
