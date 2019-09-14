package sg.edu.nus.iss.is2019.rs.hr.app;

import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;

import javax.ws.rs.client.Client;
import javax.ws.rs.client.ClientBuilder;
import javax.ws.rs.client.Entity;
import javax.ws.rs.core.Form;
import javax.ws.rs.core.MediaType;

public class JsonClient {
	
	String url = "http://server.leeseng.tech:5000/api_search";
	

	public static void main(String[] args) {

		JsonClient jc = new JsonClient();
		
		Map<String, SearchResult> dataMap = jc.search("http://localhost:5000/api_search", "Java");

		
		
		System.out.println(dataMap.get("https://www.linkedin.com/in/m-zaki-ahmat-7831a880/").getNScore());
		

	}
	
	public Map<String, SearchResult> search(String searchText)
	{
		return search(url, searchText);
	}

	public Map<String, SearchResult> search(String url, String searchText) {
		System.out.println("URL:"+url);
		
		Form form = new Form();
		form.param("search", searchText);
		
		Client client = ClientBuilder.newClient();
		String result = client.target(url).request(MediaType.APPLICATION_JSON)
				.post(Entity.entity(form, MediaType.APPLICATION_FORM_URLENCODED_TYPE), String.class);
		
		System.out.println(result);
		
		String[] rs = result.split("\\\\n");
		
		Map<String, SearchResult> dataMap = new HashMap<String, JsonClient.SearchResult>();
		
		JsonClient jt = new JsonClient();
		
		for (String record : rs) 
		{
			SearchResult sr = jt.new SearchResult();
			String[] r = record.split(",");
			if(r.length<5)
				continue;
				
			sr.setId(r[0]);
			sr.setName(r[1]);
			sr.setProfileURL(r[2]);
			sr.setScore(r[3]);
			sr.setNScore(r[4]);
			sr.setExpectedMonthlySalary(r[5]);
			System.out.println(sr.getScore()+" : "+sr.getProfileURL());
			dataMap.put(sr.getProfileURL(), sr);
		}
		System.out.println(rs.length);
		return dataMap;
	}

	public class SearchResult implements Serializable{
		
		public SearchResult()
		{}
		
		private String id;


		private String name;
		private String profileURL;
		private String score;
		private String NScore;
		private String expectedMonthlySalary;

		public String getExpectedMonthlySalary() {
			return expectedMonthlySalary;
		}

		public void setExpectedMonthlySalary(String expectedMonthlySalary) {
			this.expectedMonthlySalary = expectedMonthlySalary;
		}

		public String getName() {
			return name;
		}

		public void setName(String name) {
			this.name = name;
		}

		public String getProfileURL() {
			return profileURL;
		}

		public void setProfileURL(String profileURL) {
			this.profileURL = profileURL;
		}

		public String getScore() {
			return score;
		}

		public void setScore(String score) {
			this.score = score;
		}

		public String getNScore() {
			return NScore;
		}

		public void setNScore(String nScore) {
			NScore = nScore;
		}
		
		public String getId() {
			return id;
		}

		public void setId(String id) {
			this.id = id;
		}
	}

}
