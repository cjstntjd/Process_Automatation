# Process_Automatation
A program that receives measurements from a power measurement device and corrects errors and stores the results to determine missing values.

Layers of Software
- 플랫폼 : 위의 용어설명에서도 언급한바 있지만 좀더 자세히 언급하 면 Bios 혹은 펌웨어로 설명되는 장치 드라이버 , 운영체제 그리고
GUI등을 총체적으로 포함하는 단위 집합으로서 컴퓨터와 주변기기 의 통신을 제어한다. 일반적으로 하드웨어와 패키지 형태로 제공되어 연산을 돕는 기능을 한다.

- User Develop Software : 사용자의 특화된 요구 기능을 수행하 고 충족시키기 위함에 뿌리를 둔다. 일반적으로 위에 언급한 응용소프 트웨어를변형해유저자신을위한새로운커스텀형태로존재하며 제어를 유저기반에 두기 때문에 특정한 형태가 없는것이 일반적이다.

Develop Software
소프트 웨어는 프로그래밍 언어와 관련된 유틸리티를 사용하여 제작되 는데 일반적으로 스크립터 인터프리터와 같은 단일 프로그램 (compiler or linker)등을 꼽을수 있고 다른 도구를 포함하게 된다 면 Integrated Develop Environment로 분류 가능하다.

Language
컴퓨팅리소스를 제어하는 도구로서 C언어 C++ c# 비주얼베이
직 ,cobol, ADA,JAVA, Python 등이 있고 아래 제작된 프로그램들 의 대부분은 python 으로 제작되었다.

2 Software Develop Procedure
소프트웨어 개발 방법론은 객체지향 CBD기반의 정보화 사업개발단계별프로세스및산출물을표준화하여실질적 인산업개발시구축사업자와의개발방법론제안에대한긴 장완화생산성및시스템의품질향상,개발과정의체계적
관리에 목적을 둔다.

실질적으로 정부에서는 관련 규정을 제정하여 국가 소프트웨어와 출판 소프트웨어에 대한 정보화 업무 규정 준수를 고려 하고 있다.

관련 규정 -특허청정보화업무규정(훈령제715조)
- 행안부 “정보시스템 구축운영지침 제 45조 , 행안부 제 2011-36조”
구성 개념
- 개발 방법론은 국제 표준 ISO/IEC 12207의 개발프로세스를 참조하 여 산업 환경의 전반적인 흐름에 맞추어 변형한다.

개발의 방법론에 해당하기 때문에 Method + Knowledge 형태로 구성되어 소프트 개발에 필요한 반복적인 과정 을 체계적으로 정리한것
에 해당한다.

요약하면 수많은 프로그램은 독립적이지 않고 각자 Dependency를 가지고 동작하기떄문에 체계적으로 개발하는 과정을 정립해 소프트 웨 어개발의분석사례를도식화한것에해당한다.

구조적 방법론
구조적 방법론은 절차 중심의 소프트웨어 개발 방법론으로 코드를 제한 된 구조에서 생성하여 순차적으로 실행시키는 특징을 갖는다. 알고리 즘 단위인 순차 , 선택,반복의 구조로 코드를 펴현하게 되므로 프로세스 단위로 문제를 해결하고 코드 보안을 유지 하며 유지 보수를 용이하게 만드는 장점이 있다.
일반적으로 폭포수 모델로 설명이 되는 개발 방법론적 접근에서 시스템 에대한요구와디자인이이루어지고구조가생성되고나면구현과정 에서 백트래킹이 일어나 진동하기도 한다.

정형화된 분석절차에 따라 사용자 요구사항을 파악하여 문서화 하는 체 계적인 분석 이론을 말한다. 프로그램의 로직을 중심으로 발전하였고 도형 중심의 분석이 주되며 자료 흐름도 기반으로 프로세스가 이루어 진 다.
정보 공학적 방법론
1980 년대 태동한 방법론으로 정보 시스템이 단순 업무지원뿐아니라 경 영 전략을 창출하는 MIS로 진화 하면서 회사의 경영 시스템을 수용하 는 전략적 도구로 발전하면서 태동된 방법론이다.
요약하면 과거에는 컴퓨터가 계산기처럼 단순 업무 지원을 했다면 80년 대에 들어서면서 컴퓨터를 이용해 사내 업무를 처리하게 되면서 프로그 램에 회사의 이념이나 프로세스를 담을 필요가 생겼다는 말이다.
따라서 정보공학 방법론은 설계와 구현 단계에서 데이터를 우선적으로 개발하고 문제 영역을 세분화 하고 Top-Down 방식으로 진행되어 기 존보다 빠른 결과물을 얻을수 있었다.

객체 지향 방법론
분석과 설계과정의 전단계를 데이터 중심으로 개발하는 방법론이다.
이 방법론은 개발 단계에서 반복과 점층적 모델을 사용하여 사용자의 요 구사항을 반영하고 모든 단계를 유기적으로 협력시켜 전체 프로세스의 방향성을 유지하고 “재 사용성”을 높이는데 초점을 둔다.


CBD 분석 방법론
Component Based Development 분석방법론으로 문제를 조 각으로 나누어 각각 컴포넌트를 구성한후 다시 조합하는 재 사용성에 초 점을 둔 방식이다.
아무리 복잡한 시스템이라고 할지라도 단계별로 나누어 생각하게 되기 때문에 전체 시스템이나 프로그램에 영향을 주지 않고 빠르게 문제를 해 결한다는 장점이 있다.


Agile 방법론
이전 방식들은 개발과정에서 과도한 문서나 형식적인 절차가 많다는 단
점이 있었다.
이는 끊임 없는 비용의 누수를 발생시켰고 이를 해결하기 위해 에자일
이라는 새로운 방법론이 대두되었다.
에자일 방법론은 고객과의 협력을 중시하고 프로세스나 도구에 국학되 지 않는 자기 적응적 방식을 채택하는데 일정한 주기를 가지고 프로토 타입을 만들어 내어 고객의 요구사항을 반영하기 쉽고 변화에 빠르게 대 응할수 있다는 장점이 있다.

INDEX
1 . Introduction 
2.OverallDescription
3.SystemFeatures
4.Functional & Nonfunctional Req 
5.Conclusions


1. Introduction

A. Intro
This document focuses on the G-EMC team's description of the requirements, objectives, and scope terms associated with the creation of a webbase-based task scheduling program.

B. Purpose
The purpose of this SRS is to:
Produce a common task scheduler aimed at realizing open software that is unaffected by security within the scope of UL Korea SUW G- EMC's work.
The page is customized for G-EMC internal work procedures and is designed in consideration of flexibility and procedural characteristics in response to random unexpected situations in the work. The development and design of the service were led by Dankook University's mobile system engineering interns, and copyrights on the entire design and layout are given to the 2020 UL Korea intern.

C. Project Scope
The scope of the project is as follows.
Function 1. Show the team's scope of work clearly
Functional2. Modification of team work will be possible
Function 3. Make it visible to facilitate communication within the team.
Function 4. Automatically generate test results and reports
Function 5. Report periodically to the responsible person in charge Function 6. Maintenanceable design method

The above functions encourage the accuracy, professionalism, and communication between team members, and facilitate the convenience of employees through quick task identification.

2. Overall Description
This chapter describes the overall flow and outline of the project. It looks at the project from the needs of the project, from the perspective of the employees and from the perspective of the Director, and also describes the functional aspects of what should be included.
system requirements
In the case of the G-EMC team, there is a great deal of work, and it is inevitable that many employees will be able to perform complex tasks simultaneously. Therefore, the Director wants to see a system that can observe the staff's work and the team's overall progress at a glance.
Product Function
1. There will be a channel in which team members can share 2. Sharing work among team members will be possible
3. The person in charge will be able to identify all the tasks 4. Stay true to security
5. You will be able to automatically print your report. 6. Flexible system for each test mode
Additional staff requirements are collected to produce meaningful work schedulers to meet the above needs
Based on the information received from Director Choi and Song Hye-rim, the entire flow chart is planned and applied to the system.

Program Tools
- Python 3.7
- Flask
- html
- css
- JavaScript 
- Ajax
- Atom
- Sklearn
- Keras 
- Excel
- Word


Restriction
The constraints are as follows:
Too busy employees.
Complex tasks and unstructured ways of doing things Developer's Low Work Degree
Poor development (small computing resources)
No Server Access
An environment in which maintenance costs cannot be borne


4. Functional & Nonfunctional Req

Target User : G-EMC members Functions

The system covers both the overall operation and the overall work within the team. Therefore, employees who do not have an understanding of their duties should be able to quickly grasp the progress of the work and provide a boundering and guideline to understand how much they are joined in the work.
In this sense, the overall flow of system operation is expressed as follows.
1. Generate ID (first team member with face recognition) 2. User Login (Database-Based Access Allowed)
3. Creating a login user access project
4. Creating a team-wide project viewer
5. Grant project-specific access and access to data 6. Setting Up Mode
7. Test start based on test plan
8. Daily cumulative test results
9. Base Accumulated Results
10. Data Base Sharing and Business Identity 11. Sending Notifications to Managers

NON- Functions

- team-to-team communication
- Increased business understanding


5. Conclusion

This document contains the outline of the project.
It is important to recognize that all content is only a high-level matter, and that future changes or employee requirements may result in different outcomes.
Additionally, the project will be carried out in a wide range of ways that can include these realistic situations, since not all team members share the results in establishing the work plan.
Therefore, important documents must be produced by themselves and, in the case of high-grade security documents or tasks, it is right to handle them individually.
We would like to thank Choi Chang-young for allowing me to proceed with the project.
