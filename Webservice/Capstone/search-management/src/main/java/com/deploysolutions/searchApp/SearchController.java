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
import javax.ws.rs.QueryParam;
import javax.ws.rs.core.MediaType;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;


@Path("/")
public class SearchController {
	
	@POST
    @Produces(MediaType.APPLICATION_JSON)
 	@Consumes(MediaType.APPLICATION_JSON)
 	@Path("/results")
 	public  String search(@QueryParam("searchLevel") String searchLevel, String query)  {
		
		StringBuilder sbResponse = new StringBuilder();		
		JSONParser parser = new JSONParser(); 
		JSONObject json  = new JSONObject();

		//Escape the parenthesis
		query.replace("\"", "\\\"");
		query.replace("(", "\\\\(");
		query.replace(")", "\\\\)");
		

 		try {
 			
 			//URL url = new URL ("http://localhost:9200/article/_search?pretty");
 			URL url = new URL ("https://search-cc14-prototype-s5q5rjhkogrxzrmfzutzt4umnm.ca-central-1.es.amazonaws.com/" +searchLevel+"/_search?pretty");
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
			os.close();  
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
			System.out.println(e.getMessage());
		}
 			return json.toJSONString();
}

}
