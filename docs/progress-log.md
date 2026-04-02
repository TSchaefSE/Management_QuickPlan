
# Progress Log

## Week 1 – Requirements and Planning

**Date Range:** March 16 – March 22, 2026 *(Pre-repository setup)*

* Reviewed Course Project Guidelines to confirm project scope and required features
* Identified in-scope and out-of-scope system functionality
* Defined functional requirements (project information, requirements management, effort tracking)
* Defined non-functional requirements (input validation, usability, testing expectations)
* Identified required data fields for projects, requirements, risks, team members, and effort logs
* Developed initial Work Breakdown Structure (WBS)
* Planned repository structure and team workflow approach

---

## Week 2 – System Design

**Date Range:** March 23 – March 29, 2026 *(Pre-repository setup)*

* Defined overall Flask application architecture
* Outlined route-to-backend interaction flow
* Planned backend-to-template data flow
* Designed CSV data structures and relationships
* Defined expected column names and identifiers
* Planned integration of Pandas for data processing
* Created UI sketches and mockups for:

  * General Information page
  * Requirements page
  * Effort Logging page
  * Dashboard and reporting page
* Defined shared layout using Flask template inheritance
* Identified testing strategy (unit, integration, system testing)

---

## Week 3 – Development Environment and Project Setup

**Date Range:** March 30 – April 5, 2026

This phase has been successfully completed, with all required setup tasks implemented and verified.

### Completed Tasks 

**3.1 Repository and Project Setup**

* Created GitHub repository (`Management_QuickPlan`)
* Initialized project folder structure

**3.2 Project Structure Standardization**

* Established standard directory structure:

  * `app/` (application logic)
  * `app/templates/` and `app/static/` (UI components)
  * `data/` (CSV storage)
  * `docs/` (documentation)
  * `tests/` (testing placeholder)

**3.3 Local Development Environment**

* Configured development environment using PyCharm
* Set up project interpreter

**3.4 Dependency Management**

* Created Python virtual environment
* Installed required libraries (Flask, Pandas)
* Established `requirements.txt` for dependency consistency

**3.5 Flask Application Initialization**

* Implemented initial Flask application entry point (`run.py`)
* Created application package structure (`app/__init__.py`, `routes.py`)

**3.6 Base Template Development**

* Created initial HTML template (`base.html`)
* Verified template rendering through Flask

**3.7 Data Initialization**

* Created initial CSV file structure with headers for:

  * Projects
  * Requirements
  * Risks
  * Effort logs

**3.8 Environment Verification**

* Successfully ran Flask development server locally
* Verified application renders correctly in browser
* Confirmed environment is functional for continued development

---

### Phase Outcome

* Fully functional local development environment established
* Consistent project structure implemented
* Application successfully runs and renders initial UI
* Team-ready environment prepared for development phase

---

### Transition to Next Phase

The project is now ready to proceed into:

* UI layout development
* Backend implementation
* Feature-specific development branches

---

## Week 3 – Contribution Breakdown
### April 1, 2026

## Contributor: Tyler Schaefer

### Activities Completed

- Created GitHub repository and established project structure  
- Configured virtual environment and installed Flask and Pandas  
- Implemented core Flask application with Blueprint-based routing  
- Developed reusable base template with top navigation bar and sidebar  

- Designed and implemented all primary UI screens aligned with mockups:
  - Dashboard  
  - Project Information  
  - Effort Logging  
  - Requirements Management  
  - Reports  
  - User Profile  

- Implemented HTML form structures for data entry across multiple pages  

- Wired GET and POST request handling for:
  - Effort Logs  
  - Requirements  
  - User Profile  

- Implemented GET-based filtering structure for Reports page  
- Established consistent frontend-backend interaction pattern across the application  
- Integrated dynamic navigation highlighting using `active_page` context  
- Verified application routing and page rendering across all views  

---

### Notes

- Application runs successfully with full navigation between all pages  
- All major UI components and forms are implemented and functional  
- Backend request handling is operational for all core user interactions  
- Data persistence (CSV integration) has not yet been implemented  
- Reports currently use placeholder data and static visualizations  
- Next phase will focus on integrating CSV-based data storage and enabling dynamic reporting functionality  

