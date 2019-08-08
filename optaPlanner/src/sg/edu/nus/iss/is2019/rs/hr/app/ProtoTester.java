package sg.edu.nus.iss.is2019.rs.hr.app;

import java.io.File;
import java.io.FileInputStream;

import hr.domain.ResumeDBOuterClass.Resume;
import hr.domain.ResumeDBOuterClass.ResumeDB;

public class ProtoTester {

	public static void main(String[] args) throws Exception {
		// TODO Auto-generated method stub
		FileInputStream fileInputStream = new FileInputStream(new File("../webapp/resumeDB.pb"));
		ResumeDB db = ResumeDB.parseFrom(fileInputStream);
		
		for (Resume r : db.getResumesList()) {
			System.out.println(r.getRawResume());
		}
			
	}

}
