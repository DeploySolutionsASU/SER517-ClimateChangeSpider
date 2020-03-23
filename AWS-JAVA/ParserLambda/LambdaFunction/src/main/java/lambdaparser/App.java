package lambdaparser;

import java.io.*;
import java.util.*;

import com.amazonaws.auth.DefaultAWSCredentialsProviderChain;
import com.amazonaws.services.s3.AmazonS3Client;
import com.amazonaws.services.s3.model.PutObjectRequest;
import org.apache.jena.rdf.model.Model;
import org.apache.jena.util.FileManager;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.amazonaws.services.lambda.runtime.events.S3Event;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.event.S3EventNotification.S3EventNotificationRecord;
import com.amazonaws.services.s3.model.GetObjectRequest;
import com.amazonaws.services.s3.model.S3Object;


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
        } catch(Exception ex) {
            System.out.println("error "+ ex);
        }

        return "";
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
            PutObjectRequest request = new PutObjectRequest("s3parsedfiles", fname,
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