# ASP-QUERY-SERVER
This websocket server handles queries from the Automated System Viewer to extract and filter through system level traces. 

> [!NOTE]  
> This repo is in development and there are core features being added and explored.

# System Diagram
![Simplified AQS System Diagram](docs/system_diagram2.jpg)

# How does it work?
The diagnostic data that ASP works with is the execution of the program and its variable values, so to gain system level diagnostic insight, the relationship between the programs has to be established. In this case, the relationship between the programs can be inferred using the variable values as a request moves through the system. For example, as a request moves through the system, it will have a unique identifier. While this information can be automaticaly inferred, for now, the ADLI tool allows the program to log a unique identifier when a trace starts and ends. 

## System Processor
- The SystemProcessor class identifies all the log files which belong to the system (currently, they are in a known folder).
- It uses the Cdl class to extract the program execution data from each log file and gathers the unique traces from each program. 
- It processes each unique trace and assembles the sub-traces from each program in the order they appear.
- It groups unique traces if they start and end at the same location, these traces have the same **Trace Type**.
- It allows the traces to be queried by timestamp, specific variable value or by UID (this will evolve)
    
Note: I think that for a given **trace type**, there are specific variables associated with it, it would be great to allow the user to select the variable and filter the traces for a specific variable value (ex. specific user, specific job type)

## CDL Reader
The Cdl class uses the clp-ffi-py library to decompress the CDL file and extract the program execution data. Some of the data that is extracted are:
- Execution Sequence
- Call stack for a given position
- Variable Stack for a given position
- Exception Information
- Unique Traces

## Queries
Coming soon

In the current version of this program, the sample_system_logs folder contains all the log files belonging to the current system. In the future, once CDL log files are ingested by CLP, the features CLP provides will be used to improve the performance of this system.
