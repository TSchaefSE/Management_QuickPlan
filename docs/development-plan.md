# Development Plan

## 3. Deliverable Schedule

### 3.1 Project Schedule

The project will follow a Waterfall development model, where each major phase is completed before the next begins. After the System Design Phase, partial overlap will occur between Backend and Frontend development activities.

The total estimated project duration is **9 weeks**.

---

## 3.2 Work Breakdown Structure (WBS)

### Requirements and Planning Phase (Week 1)

The team will rely on the Course Project Guidelines to define system requirements and utilize planning documents and GitHub for organization.

#### Activities

* 1.1 Review project guidelines to confirm scope and features
* 1.2 Identify in-scope and out-of-scope features
* 1.3 Define functional requirements (project info, requirements management, effort tracking)
* 1.4 Define non-functional requirements (validation, usability, testing)
* 1.5 Define required data fields (projects, requirements, risks, team members, effort logs)
* 1.6 Define report structures (person-hours by requirement and phase)
* 1.7 Develop WBS, activity list, and duration estimates
* 1.8 Establish GitHub repository structure and team workflow
* 1.9 Approve requirements baseline

---

### System Design Phase (Week 2)

Focus on architecture, data design, backend logic planning, and UI/UX structure.

#### 2.1 Application Architecture

* 2.1.1 Define Flask application structure using sketches/storyboards
* 2.1.2 Define route-to-backend interaction flow
* 2.1.3 Define backend-to-template data flow

#### 2.2 Backend Data Structure and Processing

* 2.2.1 Define CSV structures for all entities
* 2.2.2 Define column names and identifiers
* 2.2.3 Define relationships between records
* 2.2.4 Plan integration with Pandas DataFrames

#### 2.3 User Interface and Experience

* 2.3.1 Design general information page
* 2.3.2 Design requirements input page
* 2.3.3 Design effort logging page
* 2.3.4 Design dashboard/reporting page
* 2.3.5 Define shared layout using template inheritance

#### 2.4 Planned Testing

* 2.4.1 Identify unit test targets
* 2.4.2 Define integration tests
* 2.4.3 Define acceptance scenarios

---

### Development Environment and Project Setup (Week 3)

This phase establishes a consistent shared development environment to ensure seamless collaboration and transfer of work between team members.

#### Activities

##### 3.1 Repository and Project Setup

* Create shared GitHub repository
* Initialize project folder structure

##### 3.2 Project Structure Standardization

* Create folders for application code, templates, static files, CSV data, and tests

##### 3.3 Local Development Environment

* Configure PyCharm or VS Code environments for all team members

##### 3.4 Dependency Management

* Install Flask and Pandas
* Ensure consistent dependency versions across team

##### 3.5 Flask Application Initialization

* Create initial Flask application entry point

##### 3.6 Base Template Development

* Create base HTML template for general information page

##### 3.7 Data Initialization

* Create starter CSV files with headers

##### 3.8 Environment Verification

* Verify all team members can run Flask app and render templates

---

### Backend Development (Weeks 3–5)

Focus on implementing core application logic using Python and Pandas.

#### 4.1 Data Access and Storage

* Implement CSV read/write utilities
* Implement row insertion and updates
* Generate unique identifiers
* Validate CSV structure at startup

#### 4.2 Input Validation and Business Rules

* Validate effort entries
* Validate IDs
* Enforce required fields
* Validate categories

#### 4.3 Project Management Logic

* Add/update project records
* Retrieve project summaries
* Manage risk data and updates

#### 4.4 Requirements Management Logic

* Add/edit/list requirements
* Filter requirements by type

#### 4.6 Effort Monitoring Logic

* Log person-hours
* Categorize effort phases
* Support date-based logging
* Link entries to team members and requirements

#### 4.7 Reporting and Aggregation

* Aggregate hours using Pandas
* Compute totals by phase and requirement
* Prepare data for frontend display

---

### Frontend Development (Weeks 4–6)

Develop user-facing interface using Flask templates and HTML.

#### 5.1 Shared UI Components

* Create base template
* Implement navigation
* Create reusable forms
* Apply consistent styling

#### 5.2 General Project Management UI

* Develop project info form
* Develop team and risk input views
* Connect forms to backend

#### 5.3 Requirements UI

* Create input, list, and edit views
* Render data dynamically

#### 5.4 Effort Monitoring UI

* Create logging forms
* Implement selection controls
* Display effort history
* Connect to backend

#### 5.5 Dashboard and Reporting UI

* Create dashboard page
* Display aggregated data
* Render summaries in tables/views

---

### Integration and Testing (Weeks 7–8)

Validate system functionality through testing.

#### 6.1 Backend Unit Testing

* Test CSV operations
* Test validation logic
* Test aggregation functions

#### 6.2 Flask Integration Testing

* Test form submissions
* Test backend interactions
* Test dashboard rendering

#### 6.3 System Testing

* Execute full workflows (project, requirements, risks, effort, reporting)

#### 6.4 Defect Correction and Regression Testing

* Fix backend, data, routing, and UI issues
* Re-test after fixes

---

### Deployment Phase (Week 9)

Prepare and deliver final application.

#### Activities

* 7.1 Finalize repository structure
* 7.2 Verify all required files
* 7.3 Configure Waitress WSGI server
* 7.4 Package application using PyInstaller
* 7.5 Conduct final team review
* 7.6 Submit completed project
