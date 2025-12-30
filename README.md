### Title: Colonoscopy Surveillance Triage Automation Tool

### Short Description: 

A backend service that converts unstructured colonoscopy and histopathology reports into guielines-based surveilance recommendations, automating routine follow-up tasks while keeping humans in the loop

### 1. Problem:
Manual review of histopathology reports to determine surveillance intervals is a time-consuming and error-prone process requiring significant clinician time and effort.  The current workflow depends heavily on manual look-ups and paper records.

### 2. Solution:
This system:
* Parses free text into strutured JSON using an LLM to process free text
* Applies current guidelines in a deterministic, rules-based process
* Automates roughly 80% of cases, flagging complex or ambiguous cases for human review
* Logs all inputs and outputs for auditing and quality control
Key principles:
* Human-in-the-loop design
* Deterministic and rule-based using current guidelines
* LLM DOES NOT make any clinical decisions or recommendations

### 3. Architecture:
Workflow:

```mermaid
graph TD;
    A[Unstructured Clinical Text] --> B[LLM Text Parsing];
    B --> C[Rules Engine]
    C --> 



```
### Backend
* FastAPI with a single endpoint /triage that runs the logic of application

### Frontend
* Streamlit - a very simple UI where a user can cut and paste their data into a window and get a recommendedation

### Logging
* Inputs to the model and outputs logged to file and also to console

### Docker
* Dockerfiles for FastAPI and Streamlit
* Orchestration using Docker compose

### Next steps
* Working on deidentification functionality for use with real world data
* Identifiers hashed with keyed hashing vs. using encryption such as AES-256


    

