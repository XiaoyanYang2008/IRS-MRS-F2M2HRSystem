/*
 * Copyright 2015 Red Hat, Inc. and/or its affiliates.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package sg.edu.nus.iss.is2019.rs.hr.domain;

import java.util.List;

import org.optaplanner.examples.common.domain.AbstractPersistable;

import sg.edu.nus.iss.is2019.rs.hr.app.JsonClient.SearchResult;

public class Meeting extends AbstractPersistable {

//	private SearchResult sr;
	private String url;
	private double salary;
	private double nscore;
	private String topic;
    private List<Person> speakerList;
    private String content;
    private boolean entireGroupMeeting;
    /**
     * Multiply by {@link TimeGrain#GRAIN_LENGTH_IN_MINUTES} to get duration in minutes.
     */
    private int durationInGrains;

//    private List<RequiredAttendance> requiredAttendanceList;
//    private List<PreferredAttendance> preferredAttendanceList;

	

	
    public String getTopic() {
        return topic;
    }

    public void setTopic(String topic) {
        this.topic = topic;
    }

    public double getSalary() {
		return salary;
	}

	public void setSalary(double salary) {
		this.salary = salary;
	}

	public double getNscore() {
		return nscore;
	}

	public void setNscore(double nscore) {
		this.nscore = nscore;
	}

	public List<Person> getSpeakerList() {
        return speakerList;
    }

    public void setSpeakerList(List<Person> speakerList) {
        this.speakerList = speakerList;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public boolean isEntireGroupMeeting() {
        return entireGroupMeeting;
    }

    public void setEntireGroupMeeting(boolean entireGroupMeeting) {
        this.entireGroupMeeting = entireGroupMeeting;
    }

    public int getDurationInGrains() {
        return durationInGrains;
    }

    public void setDurationInGrains(int durationInGrains) {
        this.durationInGrains = durationInGrains;
    }

//    public List<RequiredAttendance> getRequiredAttendanceList() {
//        return requiredAttendanceList;
//    }
//
//    public void setRequiredAttendanceList(List<RequiredAttendance> requiredAttendanceList) {
//        this.requiredAttendanceList = requiredAttendanceList;
//    }
//
//    public List<PreferredAttendance> getPreferredAttendanceList() {
//        return preferredAttendanceList;
//    }
//
//    public void setPreferredAttendanceList(List<PreferredAttendance> preferredAttendanceList) {
//        this.preferredAttendanceList = preferredAttendanceList;
//    }
//
//    // ************************************************************************
//    // Complex methods
//    // ************************************************************************
//
//    public int getRequiredCapacity() {
//        return requiredAttendanceList.size() + preferredAttendanceList.size();
//    }

    public String getDurationString() {
        return (durationInGrains * TimeGrain.GRAIN_LENGTH_IN_MINUTES) + " minutes";
    }

    public String getUrl() {
		return url;
	}

	public void setUrl(String url) {
		this.url = url;
	}

	public String getLabel() {
        return topic;
    }

    @Override
    public String toString() {
        return topic;
    }
}
