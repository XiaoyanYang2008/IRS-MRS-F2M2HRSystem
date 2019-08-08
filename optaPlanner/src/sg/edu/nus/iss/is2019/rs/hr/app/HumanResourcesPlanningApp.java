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

package sg.edu.nus.iss.is2019.rs.hr.app;

import org.optaplanner.examples.common.app.CommonApp;
import org.optaplanner.persistence.common.api.domain.solution.SolutionFileIO;
import org.optaplanner.persistence.xstream.impl.domain.solution.XStreamSolutionFileIO;

import sg.edu.nus.iss.is2019.rs.hr.domain.MeetingSchedule;
import sg.edu.nus.iss.is2019.rs.hr.persistence.MeetingSchedulingXlsxFileIO;
import sg.edu.nus.iss.is2019.rs.hr.swingui.MeetingSchedulingPanel;

/**
 * in term of UI, 1 time slot. 
 * rooms is number of teams.
 * resume search needs to return linked in name list, distance score, 
 * other info reads from protobuf DB, e.g. monthly salary.
 * @author leeseng
 *
 */
public class HumanResourcesPlanningApp extends CommonApp<MeetingSchedule> {

    public static final String SOLVER_CONFIG
            = "sg/edu/nus/iss/is2019/rs/hr/solver/HumanResourcePlanningSolverConfig.xml";

    public static final String DATA_DIR_NAME = "humanresources";

    public static void main(String[] args) {
        prepareSwingEnvironment();
        new HumanResourcesPlanningApp().init();
    }

    public HumanResourcesPlanningApp() {
        super("Team building",
                "Assign meetings a starting time and a room.",
                SOLVER_CONFIG, DATA_DIR_NAME,
                MeetingSchedulingPanel.LOGO_PATH);
    }

    @Override
    protected MeetingSchedulingPanel createSolutionPanel() {
        return new MeetingSchedulingPanel();
    }

    @Override
    public SolutionFileIO<MeetingSchedule> createSolutionFileIO() {
        return new MeetingSchedulingXlsxFileIO();
    }

}
