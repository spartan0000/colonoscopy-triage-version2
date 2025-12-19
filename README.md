### Building a different version of the triage app that uses a rules based system rather than relying on an LLM to reason through the triage decision.  Much more deterministic and easier to track/log

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


    

