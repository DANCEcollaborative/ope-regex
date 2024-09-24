package edu.cmu.scs.cc.project.example;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.dataformat.yaml.YAMLFactory;
import com.google.common.base.Stopwatch;
import edu.cmu.scs.cc.grader.Config;
import edu.cmu.scs.cc.grader.GradeWriter;
import edu.cmu.scs.cc.grader.model.Answer;
import edu.cmu.scs.cc.grader.util.CmdExecutor;
import edu.cmu.scs.cc.grader.util.QuestionEvaluator;
import edu.cmu.scs.cc.grader.util.QuestionEvaluator.ReferenceType;
import edu.cmu.scs.cc.grader.util.RunnerScriptExecutor;
import edu.cmu.scs.cc.grader.strategy.ScoreMapGradeStrategy;
import lombok.Getter;
import lombok.Setter;
import org.apache.commons.io.FileUtils;
import org.apache.commons.lang3.StringUtils;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Objects;
import java.util.Optional;
import java.util.concurrent.TimeUnit;
import java.util.function.Function;
import java.math.BigDecimal;


/**
 * <p>The grade strategy for runner questions in {@code runner.sh}.</p>
 *
 * The grader will read student answer and compare it with reference
 * answer.<br>
 * <br>
 * <p>Usage:
 * Use {@link #setReferenceYaml(String)} to set reference yaml.
 * <br>
 *
 * @author Marshall An (haokanga)
 */
@Getter
public class SubRunnerGradeStrategy extends ScoreMapGradeStrategy {

    /**
     * Dependency.
     */
    public Config config;

    /**
     * Dependency.
     */
    public GradeWriter gradeWriter;

    /**
     * Dependency.
     */
    public CmdExecutor cmdExecutor;
    /**
     * Dependency.
     */
    public QuestionEvaluator questionEvaluator;

    /**
     * Dependency.
     */
    public RunnerScriptExecutor runnerScriptExecutor;

    /**
     * The length of the mismatch portion to display when
     * the student answer is not the same as the reference answer
     * (assuming the answer type is String).
    */
    public static final int MISMATCH_DISPLAY_LENGTH = 100;

    /**
     * Add dependencies.
     *
     * @param config        as dep
     * @param referenceYaml the reference yaml file
     */
    public SubRunnerGradeStrategy(final Config config,
                               final String referenceYaml) {
        this.config = config;
        GradeWriter gradeWriter = new GradeWriter(config);
        this.cmdExecutor = new CmdExecutor(config, gradeWriter);
        QuestionEvaluator questionEvaluator = new QuestionEvaluator(cmdExecutor, gradeWriter);
        RunnerScriptExecutor runnerScriptExecutor = new RunnerScriptExecutor(config, cmdExecutor, gradeWriter);
        this.gradeWriter = gradeWriter;
        this.questionEvaluator = questionEvaluator;
        this.runnerScriptExecutor = runnerScriptExecutor;
        this.referenceYaml = referenceYaml;
    }

    /**
     * <p>Reference YAML under the root path of the resources directory.
     * Do not miss the "/" at the very beginning.</p>
     *
     * e.g. if the file is under "src/main/resources/p11.yaml",
     * the value should be set as "/p11.yaml"
     */
    @Setter
    public String referenceYaml;

    /**
     * The file name of the basic dataset and secret dataset
     */
    @Setter
    public String basicDatasetFolder, secretDatasetFolder;

    /**
     * The local folder that contains basic/secret dataset.
     * this is only used in {Config#localMode} testing
     * change these paths when you are using them.
     */
    @Setter
    public String localGraderFolder;

    /**
     * Id of the column which stores the elapsed time
     */
    public final String elapsedTimeId = "elapsed_time";

    /**
     * <p>If true, grading with secret dataset and secret ref answer.</p>
     * This flag also controls other grading behaviors that differ when using
     * secret dataset.
     * e.g. StdErr by executing student code is masked
     */
    public boolean gradingSecretTest = false;

    /**
     * questions that student gets correct
     */
    public int passedQuesNum;

    /**
     * If true, there will be 2 rounds of testing.
     * First with basic test and then secret test.
     */
    public Boolean hasSecretTest;

    /**
     * Deserialized reference answer instances.
     */
    public ArrayList<Answer> referenceAnswers = null;

    /**
     * The tpz column slug of total score.
     *
     * Default as null. If NonNull, calculate and write the total score into
     * the score file.
     */
    @Setter
    public String totalSlug = null;

    /**
     * The tpz column slug of honor state.
     *
     * Default as null. If NonNull, calculate and write the honor state into
     * the score file.
     */
    @Setter
    public String honorState = null;

    /**
     * The state of setup function in the runner.
     *
     * Default as true. If false, the setup function is disabled and will not
     * be executed in the runner.
     */
    @Setter
    public boolean setupEnable = true;

    /**
     * The state of clean function in the runner.
     *
     * Default as true. If false, the clean function is disabled and will not
     * be executed in the runner.
     */
    @Setter
    public boolean cleanupEnable = true;

    /**
     * {@link Function} represents a function that accepts one argument and produces a result.
     * The function here accepts the questionId and returns the student StdOut.
     *
     * The default approach is to run
     * {@link RunnerScriptExecutor#runQuestion(String, boolean)} and
     * retrieve the StdOut.
     *
     * Can be replaced if needed.
     */
    @Setter
    public Function<String, String> getStudentStdOut = (questionId) -> {
        try {
            boolean showStdErr = config.qaMode || !gradingSecretTest;
            return runnerScriptExecutor.runQuestion(
                    questionId, showStdErr).getStdOut();
        } catch (IOException e) {
            gradeWriter.logStudentExceptionAndQuit(e);
            return null;
        }
    };

    /**
     * Read reference answer from YAML file using UTF-8 encoding.
     * DO NOT use relative paths which is dependent on the current working
     * directory, e.g. {@code FileInputStream}.
     * Use {@link Class#getResourceAsStream(String)} instead.
     *
     * Set the variables below:
     * {@link #referenceAnswers}
     * {@link #hasSecretTest}
     * {@link #basicDatasetFolder}
     * {@link #secretDatasetFolder}
     *
     * @throws IOException when IO error occurs
     */
    public void readReferenceYaml() throws IOException {
        gradeWriter.writeLogln("referenceYaml:\t" + referenceYaml);
        try (InputStream is = SubRunnerGradeStrategy.class.getResourceAsStream(referenceYaml)) {
            Reader reader = new InputStreamReader(is, "UTF-8");
            ObjectMapper mapper = new ObjectMapper(new YAMLFactory());
            JsonNode root = mapper.readTree(reader);
            Answer[] answerArray = mapper.treeToValue(root.get("questions"),
                    Answer[].class);
            // save all the reference answers to an arraylist, except the one for elapsed time
            referenceAnswers = new ArrayList<>(Arrays.asList(answerArray));
            referenceAnswers.removeIf(ans -> ans.getId().equals(elapsedTimeId));
            try {
                JsonNode metadata = root.get("metadata");
                if (metadata == null) {
                    gradeWriter.logUnexpectedExceptionAndQuit(
                            new RuntimeException("Missing metadata in project yaml."));
                } else {
                    hasSecretTest = getAsBooleanOrQuit(metadata, "secret_data");
                    JsonNode datasetFolder = metadata.get("dataset_folder");
                    if (datasetFolder != null) {
                        basicDatasetFolder =
                                getAsTextOrNull(datasetFolder, "basic");
                        secretDatasetFolder =
                                getAsTextOrNull(datasetFolder, "secret");
                    }
                }
            } catch (Exception e) {
                gradeWriter.logUnexpectedExceptionAndQuit(e);
            }
        }
    }

    private String getAsTextOrNull(JsonNode parentNode, String key) {
        JsonNode node = parentNode.get(key);
        if (node == null) {
            return null;
        } else {
            return node.asText(null);
        }
    }

    private boolean getAsBooleanOrQuit(JsonNode parentNode, String key) {
        JsonNode node = parentNode.get(key);
        if (node == null) {
            gradeWriter.logUnexpectedExceptionAndQuit(
                    new RuntimeException(
                            String.format("Missing %s in the project yaml.", key)));
            return false;
        } else {
            return node.asBoolean();
        }
    }

    /**
     * <p>The default approach to grade student answers.</p>
     *
     * <p>It supports 2 grading types:</p>
     *
     * 1.   run student program remotely, grade the output remotely
     * e.g. P1.1 P1.2
     *
     * 2.   run student program locally to generate the output in JSON format,
     * grade the output remotely
     * e.g. P3.1
     *
     *
     * If {@link SubRunnerGradeStrategy#hasSecretTest} is true,
     * test with both basic and secret dataset.
     *
     * Execute student code in the {@code runner} script to get student answer.
     * @param stopwatch the stopwatch instance for tracking elapsed time
     */
    public void testDataset(Stopwatch stopwatch) {

        gradeWriter.writeEmptyLine();
        if (hasSecretTest) {
            if (!gradingSecretTest) {
                gradeWriter.writeFeedbackln("Test: Basic dataset");
            } else {
                gradeWriter.writeFeedbackln("Test: Secret dataset");
            }
        }
        gradeWriter.writeEmptyLine();

        passedQuesNum = 0;
        for (Answer referenceAnswer : referenceAnswers) {
            gradeQuestion(referenceAnswer);
            gradeWriter.writeElapsedTime(stopwatch);
        }
        gradeWriter.writeFeedbackln(String.format(
                "Total: %d/%d questions passed!", passedQuesNum, referenceAnswers.size()));
    }


    /**
     * <p>Copy original output to student folder.</p>
     *
     * <p>{@link FileUtils#copyDirectory(File, File)} is used:</p>
     * <p>This method copies the specified directory and all its child
     * directories and files to the specified destination.
     * The destination is the new location and name of the directory.</p>
     * <p>The destination directory is created if it does not exist.
     * If the destination directory did exist, then this method merges
     * the source with the destination, with the source taking precedence.</p>
     *
     * @throws IOException if IO error occurs
     */
    public void copyDirectoryToSubmissionFolder(String folderName) throws IOException {
        String srcParentPath = config.isLocalMode() ?
                localGraderFolder : config.getGraderFolder();
        listDirectory(srcParentPath + folderName);
        FileUtils.copyDirectory(
                FileUtils.getFile(srcParentPath + folderName),
                FileUtils.getFile(config.getSubmissionFolder())
        );
        listDirectory(config.getSubmissionFolder());
    }

    /**
     * Log the ls -la of a directory.
     *
     * @param directory to list
     * @throws IOException when IO error occurs
     */
    private void listDirectory(String directory) throws IOException {
        gradeWriter.writeLogln("ls -la " + directory);
        gradeWriter.writeLogln(
                cmdExecutor.execute("ls -la " + directory, true).getStdOut());
    }

    /**
     * <p>Print the feedback given one question and correctness.</p>
     *
     * Example:
     * <pre>
     * q1: PASSED
     *
     * q1: FAILED
     * Make sure you deal with encoding properly.
     * Your Answer: 120
     * </pre>
     * <p>If {Config#qaMode} always print stu and ref answers so we
     * can collect and finalize correct reference answers.</p>
     * <p>If {Answer#code} is not null, execute the reference code to get
     * reference answer.</p>
     * Else, refer to {Answer#answer} or {Answer#secret} based on
     * {@link #gradingSecretTest}.
     * If {@link #gradingSecretTest} is false, show student StdErr in feedback
     * to help them debug.
     * <p>Explain why student answer is not correct.</p>
     * <p>show reference answer if it is original dataset
     * show ref answer of secret dataset if {@link Config#qaMode} is true
     * during QA Phase.</p>
     *
     * @param referenceAnswer reference answer
     */
    public void gradeQuestion(final Answer referenceAnswer) {
        String questionId = referenceAnswer.getId();
        gradeWriter.writeLogln("Grading " + questionId);
        String studentStdOut = getStudentStdOut.apply(questionId);
        String referenceAnswerType = referenceAnswer.getType();

        ReferenceType referenceType;
        if (referenceAnswer.getCode() != null) {
            referenceType = ReferenceType.CODE;
        } else if (gradingSecretTest) {
            referenceType = ReferenceType.SECRET;
        } else {
            referenceType = ReferenceType.ANSWER;
        }
        String referenceStdOut = StringUtils.trimToEmpty(
            questionEvaluator.getReferenceStdOut(referenceAnswer, referenceType)
        );

        // compare with student StdOut
        boolean correctness = questionEvaluator.gradeByType(
            referenceAnswer, referenceStdOut, studentStdOut
        );

        if (correctness) {
            // PASSED
            passedQuesNum++;
            gradeWriter.writeFeedbackln(referenceAnswer.getId() + ": PASSED");
        } else {
            // FAILED
            gradeWriter.writeFeedbackln(referenceAnswer.getId() + ": FAILED");
        }

        if (referenceAnswerType.equals("Range")) {
            gradeWriter.writeFeedbackln("Your performance output is: " + studentStdOut + ".");
        }

        if (config.qaMode || !correctness) {
            switch(referenceAnswerType) {
                case "String":
                    showStringAnswerMismatch(
                        gradeWriter, referenceStdOut, studentStdOut,
                        referenceAnswer, config.qaMode || !gradingSecretTest
                    );
                    break;
                case "Range":
                    showExpectedRange(gradeWriter, referenceStdOut);
                    break;
                default:
                    break;
            }
        }

        updateScore(referenceAnswer, correctness);
    }

    /**
     * When the answer type is <pre>String</pre>
     * and there is a mismatch between the student answer and reference answer,
     * display a portion of both answers around the first point of mismatch.
     *
     * @param gradeWriter           the object for writing feedback and logging error messages
     * @param referenceStdOut       the reference answer string
     * @param studentStdOut         the student answer string
     * @param referenceAnswer       the Answer object parsed from reference.yaml
     * @param showReferenceAnswer   the flag to indicate whether reference answer should be shown
     */
    public void showStringAnswerMismatch(GradeWriter gradeWriter, String referenceStdOut, String studentStdOut, Answer referenceAnswer, boolean showReferenceAnswer) {
        gradeWriter.writeFeedbackln("\tYour answer does not match the reference answer, " +
                "these are the characters around the first point of mismatch");

        int referenceDisplayLength = Math.min(referenceStdOut.length(), MISMATCH_DISPLAY_LENGTH);
        int studentDisplayLength = Math.min(studentStdOut.length(), MISMATCH_DISPLAY_LENGTH);
        String referenceStdOutSubstring = "", studentStdOutSubstring = "";

        // if student answer is empty, display the head of the reference answer up to referenceDisplayLength
        if (studentStdOut == null || studentStdOut == "") {
            referenceStdOutSubstring = referenceStdOut.substring(0, referenceDisplayLength);
            studentStdOutSubstring = studentStdOut;
        }

        // otherwise, display the portion of the student answer and reference answer
        // around the first point of mismatch
        else {
            int minLen = Math.min(referenceStdOut.length(), studentStdOut.length());
            int indexOfDifference = 0;

            // find the first mismatch position
            for (int i = 0 ; i != minLen ; i++) {
                if (referenceStdOut.charAt(i) != studentStdOut.charAt(i)) {
                    indexOfDifference = i;
                    break;
                }
            }

            // determine the substrings of the student answer and reference answer to display
            // based on the first mismatch position
            if (indexOfDifference <= MISMATCH_DISPLAY_LENGTH / 2) {
                referenceStdOutSubstring = referenceStdOut.substring(0, referenceDisplayLength);
                studentStdOutSubstring = studentStdOut.substring(0, studentDisplayLength);
            }
            else {
                final int range = MISMATCH_DISPLAY_LENGTH - 10;
                int tempReferenceDisplayLength = Math.min(referenceStdOut.length(), indexOfDifference + range);
                int tempStudentDisplayLength = Math.min(studentStdOut.length(), indexOfDifference + range);
                referenceStdOutSubstring = "... " + referenceStdOut.substring(indexOfDifference - 10, tempReferenceDisplayLength);
                studentStdOutSubstring =  "... " + studentStdOut.substring(indexOfDifference - 10, tempStudentDisplayLength);
            }
        }

        gradeWriter.explainStudentMistake(
            referenceAnswer,
            referenceStdOutSubstring,
            studentStdOutSubstring,
            showReferenceAnswer
        );
    }

    /**
     * When the answer type is Range and the student answer does not lie in
     * the expected range, print out the expected range.
     *
     * @param gradeWriter           the object for writing feedback and logging error messages
     * @param referenceStdOut       the reference answer string
     */
    public void showExpectedRange(GradeWriter gradeWriter, String referenceStdOut) {
        String[] referenceRange = referenceStdOut.split("-");
        gradeWriter.writeFeedbackln("The expected range is between " + referenceRange[0] + " and " + referenceRange[1] + ".");
    }

    /**
     * Update {@link #studentScores} given one question
     * and correctness.
     *
     * @param referenceAnswer reference answer
     * @param correctness     correctness
     */
    public void updateScore(final Answer referenceAnswer,
                            final boolean correctness) {

        switch (referenceAnswer.getScoreType()) {
            case "Number":
                updateScore(referenceAnswer.getId(),
                        correctness ? Double.valueOf(referenceAnswer.getScore()) : 0.0);
                break;
            case "Boolean":
                updateScore(referenceAnswer.getId(),
                        correctness ? Boolean.valueOf(referenceAnswer.getScore()) : false);
                break;
            default:
                gradeWriter.logUnexpectedExceptionAndQuit(new RuntimeException(
                        String.format("Unsupported reference answer score type: %s.",
                                referenceAnswer.getScoreType())));
        }
    }

    /**
     * Test all the questions on basic dataset.
     * @param stopwatch the stopwatch instance for tracking elapsed time
     */
    public void testBasicDataset(Stopwatch stopwatch) {
        assert !gradingSecretTest;
        testDataset(stopwatch);
    }

    /**
     * Test all the questions on secret dataset.
     * {@link SubRunnerGradeStrategy#gradingSecretTest} is set to true.
     * @param stopwatch the stopwatch instance for tracking elapsed time
     */
    public void testSecretDataset(Stopwatch stopwatch) {
        gradingSecretTest = true;
        testDataset(stopwatch);
    }

    /**
     * Calculate the final student score and put to {@link #studentScores}.
     *
     * @param totalSlug the total slug
     */
    public void updateTotalScore(final String totalSlug) {
        assert !studentScores.containsKey(totalSlug);
        studentScores.putIfAbsent(totalSlug,
                studentScores.values().stream().filter(x -> x instanceof Double).mapToDouble(x -> (double) x).sum());
    }

    /**
     * Calculate the honor state and put to {@link #studentScores}.
     *
     * @param honorState the honor slug
     */
    public void updateHonorState(final String honorState) {
        assert !studentScores.containsKey(honorState);
        studentScores.putIfAbsent(honorState,
                studentScores.values().stream().filter(x -> x instanceof Boolean).allMatch(x -> (boolean) x));
    }


    /**
     * Print final score.
     */
    public void writeScoresAsFeedback() {
        gradeWriter.writeFeedbackln(String.format(
                "Your score: %.2f/%.2f",
                studentScores.entrySet().stream().filter(x -> x.getValue() instanceof Double).mapToDouble(x -> (double) x.getValue()).sum(),
                referenceAnswers.stream().filter(x -> x.getScoreType().equals("Number")).map(Answer::getScore).mapToDouble(Double::parseDouble).sum()));
    }

    /**
     * Runner grading workflow.
     */
    @Override
    public HashMap<String, Comparable> grade() {
        try {
            readReferenceYaml();
            Objects.requireNonNull(hasSecretTest);
            if (setupEnable) {
                try {
                    runnerScriptExecutor.setup();
                } catch (IOException e) {
                    gradeWriter.logUnexpectedExceptionAndQuit(e);
                }
            }
            // init student score with full score
            initStudentScores();
            Stopwatch stopwatch = Stopwatch.createStarted();
            testBasicDataset(stopwatch);
            if (hasSecretTest) {
                copyDirectoryToSubmissionFolder(secretDatasetFolder);
                testSecretDataset(stopwatch);
            }

            super.updateScore(elapsedTimeId, stopwatch.elapsed(TimeUnit.SECONDS) + "s");
            writeScoresAsFeedback();
            if (cleanupEnable) {
                try {
                    runnerScriptExecutor.cleanup();
                } catch (IOException e) {
                    gradeWriter.logUnexpectedExceptionAndQuit(e);
                }
            }
            // exclude optional questions
            for (Answer answer : referenceAnswers) {
                if (answer.getScoreType().equals("Number")) {
                    if (Double.parseDouble(answer.getScore()) == 0) {
                        studentScores.remove(answer.getId());
                    }
                }
            }

            Optional.ofNullable(totalSlug).ifPresent(this::updateTotalScore);
            Optional.ofNullable(honorState).ifPresent(this::updateHonorState);
            return studentScores;
        } catch (Exception e) {
            gradeWriter.logUnexpectedExceptionAndQuit(e);
            return null;
        }
    }

    /**
     * Initialize the student score with full score
     *
     * TODO(bug, medium): do not start with full score, start with 0!
     */
    public void initStudentScores() {
        for (Answer referenceAnswer : referenceAnswers) {
            switch (referenceAnswer.getScoreType()) {
                case "Number":
                    studentScores.put(referenceAnswer.getId(), Double.valueOf(referenceAnswer.getScore()));
                    break;
                case "Boolean":
                    studentScores.put(referenceAnswer.getId(), Boolean.valueOf(referenceAnswer.getScore()));
                    break;
                default:
                    gradeWriter.logUnexpectedExceptionAndQuit(
                            new RuntimeException(
                                    String.format("Unsupported reference answer score type: %s.",
                                            referenceAnswer.getScoreType())
                            ));
                    break;
            }
        }
    }

}