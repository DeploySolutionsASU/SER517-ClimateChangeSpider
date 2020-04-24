package com.deploysolutions.searchApp;

import com.amazonaws.services.dynamodbv2.AmazonDynamoDB;
import com.amazonaws.services.dynamodbv2.AmazonDynamoDBClientBuilder;
import com.amazonaws.services.dynamodbv2.document.DynamoDB;
import com.amazonaws.services.dynamodbv2.document.Table;
import com.amazonaws.services.dynamodbv2.model.Select;
import com.amazonaws.services.dynamodbv2.document.spec.QuerySpec;
import com.amazonaws.services.dynamodbv2.document.utils.ValueMap;
import com.amazonaws.services.dynamodbv2.document.ItemCollection;
import com.amazonaws.services.dynamodbv2.document.QueryOutcome;
import com.amazonaws.client.builder.AwsClientBuilder;
import com.amazonaws.regions.Regions;

import java.util.ArrayList;
import java.util.HashMap;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

import org.elasticsearch.client.Request;

@Path("/Status")
public class StatusController {
	
	 	@GET
	    @Produces(MediaType.APPLICATION_JSON)
	 	@Path("/status")
	    public Response getStatus() {

		 // This client will default to US West (Oregon) - For Local only
//	 		AmazonDynamoDB client = AmazonDynamoDBClientBuilder.standard().withEndpointConfiguration(
//	 				new AwsClientBuilder.EndpointConfiguration("http://localhost:8000", "us-west-2"))
//	 				.build(); 
		 
		 AmazonDynamoDB client = AmazonDynamoDBClientBuilder.standard().build();

		 //DynamoDB Client
		 DynamoDB dynamoDB = new DynamoDB(client);
		 
		 Table table = dynamoDB.getTable("FileDownloads");
		 
		 HashMap<String, String> nameMap = new HashMap<String, String>();
	        nameMap.put("#fs", "FileStatus");

	        HashMap<String, Object> valueMap = new HashMap<String, Object>();
	        valueMap.put(":status", "Imported");
		 
		QuerySpec spec = new QuerySpec().withKeyConditionExpression("#fs = :status")
				.withNameMap(nameMap)
	            .withValueMap(valueMap);
		spec.withSelect(Select.COUNT);
		ItemCollection<QueryOutcome> items = table.query(spec);
		float completedCount = items.getTotalCount();	
		
		//float completedCount = 25;
		
		QuerySpec totalSpec = new QuerySpec();
		totalSpec.withSelect(Select.COUNT);
		ItemCollection<QueryOutcome> totalItems = table.query(totalSpec);
		float totalCount = totalItems.getTotalCount();
		
		//float totalCount = 400;
		float toBeCompleted = (completedCount / totalCount)* 100;
		System.out.print("To be Completed" +toBeCompleted);
		
		String response =  "{\n percentage_completed :"+ String.valueOf(toBeCompleted) + " %\n}";

		return  Response.ok(response, MediaType.APPLICATION_JSON).build();
		
	 }
	 	


}
