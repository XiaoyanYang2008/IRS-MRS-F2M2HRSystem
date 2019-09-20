# SECTION 1 : PROJECT TITLE
### F2M2 HR System
![logo](webapp/resources/ReportCover.png)

# SECTION 2 : EXECUTIVE SUMMARY / PAPER ABSTRACT



# SECTION 3 : CREDITS / PROJECT CONTRIBUTION
| Official Full Name | Student ID (MTech Applicable)| Work Items (Who Did What) | Email (Optional) |
| :---: | :---: | :---: | :---: |
| TEA LEE SENG | A0198538J | Business idea generation, Google Assistant UI, API integration, Recommendation module | e0402079@u.nus.edu / TEALEESENG@gmail.com |
| NG SIEW PHENG | A0198525R  | Google Assistant UI, Search Event intent module, project video | e0402066@u.nus.edu |
| YANG XIAOYAN| A0056720L | Business idea generation, Google Assistant UI, API integration, Weather module, project report and video| e0401594@u.nus.edu |
| Tarun Rajkumar | A0198522X | Business idea generation, Google Assistant UI, data gathering and preparation, project report | e0402063@u.nus.edu |

# SECTION 4 : VIDEO OF SYSTEM MODELLING & USE CASE DEMO


## Developer Guide

To run Webhook server.
1. python3 -m venv IRS
2. source IRS/bin/activate
3. git clone https://github.com/XiaoyanYang2008/IRS-MRS-F2M2HRSystem.git
4. cd IRS-MRS-F2M2HRSystem
5. pip3 install -r requirements.txt
6. cd webapp/
7. python3 server.py
8. To debug, 
    - kill server.py at step 7, and 
    - runs pycharm community edition. 
    - open project on folder, IRS-CGC-SGEventsFinderChatbot. 
    - Mark webapps folder as Source Root, 
    - setup Project Interpreter with existing VirtualEnv" 
    - debug server.py
    - note: uses pycharm 2019.1.x. pycharm 2019.2.x needs to comments out server.py in pydevd_dont_trace_files.py under pycharm program folder. Refers bug report, https://youtrack.jetbrains.com/issue/PY-37609


HR system, 
http://server.leeseng.tech:5000/

