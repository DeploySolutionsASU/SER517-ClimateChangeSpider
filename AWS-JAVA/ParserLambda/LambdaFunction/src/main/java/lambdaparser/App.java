package lambdaparser;

import com.amazonaws.auth.DefaultAWSCredentialsProviderChain;
import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.amazonaws.services.lambda.runtime.events.S3Event;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3Client;
import com.amazonaws.services.s3.event.S3EventNotification.S3EventNotificationRecord;
import com.amazonaws.services.s3.model.GetObjectRequest;
import com.amazonaws.services.s3.model.PutObjectRequest;
import com.amazonaws.services.s3.model.S3Object;
import com.amazonaws.services.sqs.AmazonSQS;
import com.amazonaws.services.sqs.AmazonSQSClientBuilder;
import com.amazonaws.services.sqs.model.SendMessageRequest;
import org.apache.jena.rdf.model.Model;
import org.apache.jena.util.FileManager;
import org.json.JSONObject;
import software.amazon.ion.SystemSymbols;

import java.io.*;
import java.util.*;


/**
 * Handler for requests to Lambda function.
 */
public class App implements RequestHandler<S3Event, String> {

    public String handleRequest(S3Event s3event, Context context) {
        S3EventNotificationRecord record = s3event.getRecords().get(0);
        String s3BucketName = record.getS3().getBucket().getName();
        String s3FileName = record.getS3().getObject().getUrlDecodedKey();
        S3Object fullObject = null;

        try {

            AmazonS3 s3Client = new AmazonS3Client(DefaultAWSCredentialsProviderChain.getInstance());
            fullObject = s3Client.getObject(new GetObjectRequest(s3BucketName, s3FileName));
            List<String> lines = displayTextInputStream(fullObject.getObjectContent());
            fileValidator(s3Client, s3FileName, lines);
            System.out.println("Parsing done!!");
            updateJobStatus(s3FileName);
            String message = "https://climatechange-parsed-files.s3.amazonaws.com/" + s3FileName
                    + "," + s3FileName;
            sendSQSMessage(sqsQueues.get("import_q"), message);
        } catch(Exception ex) {
            System.out.println("error-- "+ ex);
        }

        return "Parser";
    }

    private void updateJobStatus(String s3FileName) {
        Map<String, Object> payload = new HashMap<>();
        payload.put("Op", "update_item");
        payload.put("Table", "FilePartitions");

        Map<String,String> keyHashMap = new HashMap<>();
        keyHashMap.put("PartitionID", s3FileName);
        payload.put("Key", keyHashMap);
        payload.put("UpdateExpression", "SET FileStatus = :status");

        Map<String,String> expressionAttsHashMap = new HashMap<>();
        expressionAttsHashMap.put(":status", "parsed");
        payload.put("Key", keyHashMap);
        payload.put("ExpressionAttributeValues", expressionAttsHashMap);
        JSONObject json = new JSONObject(payload);
        sendSQSMessageToFIFO(sqsQueues.get("status_q"), json.toString());
    }


    private Map<String,String> sqsQueues = new HashMap<String, String>() {
        {
            put("import_q", "https://sqs.us-east-1.amazonaws.com/967866184802/import_queue");
            put("status_q", "https://sqs.us-east-1.amazonaws.com/967866184802/status_queue.fifo");
        }
    };


    private void sendSQSMessage(String queueUrl, String payload) {
        final AmazonSQS sqs = AmazonSQSClientBuilder.defaultClient();
        sqs.sendMessage(new SendMessageRequest(queueUrl,
                payload));

    }

    private void sendSQSMessageToFIFO(String queueUrl, String payload) {
        final AmazonSQS sqs = AmazonSQSClientBuilder.defaultClient();
        SendMessageRequest sendMessageRequest = new SendMessageRequest(queueUrl,
                payload);
        sendMessageRequest.setMessageGroupId("status_update");
        sendMessageRequest.setMessageDeduplicationId(java.util.UUID.randomUUID().toString());
        sqs.sendMessage(sendMessageRequest);
    }

    public void fileValidator(AmazonS3 s3Client, String fname, List<String> fileData) throws IOException {
        File fileDir = new File("/tmp/" + fname);
        Writer out = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(fileDir), "UTF8"));
        for (String line : fileData
        ) {
            if(!line.isEmpty()) {
                out.append(line).append("\r\n");
            }
        }
        out.flush();
        out.close();

        HashSet<Integer> errorLineNo = new HashSet<>();
        try {
            Model data = FileManager.get().loadModel("/tmp/" + fname);
        } catch (Exception ex) {
            if (ex.toString().contains("RiotException")) {
                String result = ex.toString().split("line:")[1].trim().split(", col")[0];
                errorLineNo.add(Integer.valueOf(result));
            }
        }

        if (errorLineNo.size() == 0) {
            PutObjectRequest request = new PutObjectRequest("climatechange-parsed-files", fname,
                    new File("/tmp/" + fname));
            s3Client.putObject(request);
            File file = new File("/tmp/" + fname);
            if(file.delete()) {
                System.out.println("File in tmp deleted successfully");
            }
            return;
        }

        for (Integer lineNo : errorLineNo) {
            fileData.remove(lineNo - 1);
        }

        fileValidator(s3Client, fname, fileData);
    }

    private List<String> displayTextInputStream(InputStream input) throws IOException {
        List<String> allLines = new ArrayList<>();
        BufferedReader reader = new BufferedReader(new InputStreamReader(input));
        String line = null;
        while ((line = reader.readLine()) != null) {
            allLines.add(line);
        }
        return allLines;
    }

}
