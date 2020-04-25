package com.deploysolutions.searchApp;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import javax.ws.rs.Consumes;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;


@Path("/searchC")
public class SearchController {
	
	@POST
    @Produces(MediaType.APPLICATION_JSON)
 	@Consumes(MediaType.APPLICATION_JSON)
 	@Path("/search")
 	public  String search(String query)  {
		
		StringBuilder sbResponse = new StringBuilder();
		
		JSONParser parser = new JSONParser(); 
		JSONObject json  = new JSONObject();
		JSONObject queryJson  = new JSONObject();
		try {
			queryJson = (JSONObject) parser.parse(query);
		} catch (ParseException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}

		

 		try {
// 			query = "{\r\n" + 
// 					"    \"query\": {\r\n" + 
// 					"        \"query_string\": {\r\n" + 
// 					"            \"query\": \"*\",\r\n" + 
// 					"            \"default_field\": \"value_of_desc\"\r\n" + 
// 					"        }\r\n" + 
// 					"    }\r\n" + 
// 					"}";
 			query = "{\r\n" + 
 					"    \"query\": {\r\n" + 
 					"        \"query_string\": {\r\n" + 
 					"            \"query\": \"(Climate AND change)(Climate AND Breakdown) OR Flooding OR Flood\",\r\n" + 
 					"            \"default_field\": \"value_of_desc\"\r\n" + 
 					"        }\r\n" + 
 					"    }\r\n" + 
 					"}";
 			URL url = new URL ("http://localhost:9200/article/_search?pretty");
			HttpURLConnection con = (HttpURLConnection)url.openConnection();
			con.setDoOutput(true);
			con.setDoInput(true);
			con.setUseCaches(false);
			con.setRequestProperty( "Content-Type", "application/json" );
			con.setRequestProperty("Accept", "application/json");
			con.setRequestMethod("POST");

			
			OutputStream os = con.getOutputStream();
			OutputStreamWriter osw = new OutputStreamWriter(os, "UTF-8");    
			osw.write(query);
			osw.flush();
			osw.close();
			os.close();  //don't forget to close the OutputStream
			con.connect();
			
 		try(BufferedReader br = new BufferedReader(
 				  new InputStreamReader(con.getInputStream(), "utf-8"))) {
 				    String responseLine = null;
 				    while ((responseLine = br.readLine()) != null) {
 				        sbResponse.append(responseLine.trim());

 				    }
 				   br.close();
 				}
 		
			 json = (JSONObject) parser.parse(sbResponse.toString());


		} catch (Exception e) {
			// TODO Auto-generated catch block
			System.out.println(e.getMessage());
			e.printStackTrace();
		}
 		System.out.println(json.toJSONString());
 			return json.toJSONString();
}

}
