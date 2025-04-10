# Database Structure

### SYSTEM TABLE

Name: SYSTEMSTABLE

| Column Name        |  Data Type  |  Description |
|--------------------|:-----------:|--------------------------------------------------:|
| system_id          |  INTEGER    | Unique System Id (eg 823642)                      |
| version            |  STRING     | Version of the system (eg "0.1")                  |
| name               |  STRING     | Name of the system (Distributed Sorting System)   |
| description        |  STRING     | Description of the system                         |
| programs           |  STRING     | JSON String representation of list of file names  |


### Deployments

Name: <sys_id>_<sys_ver>_deployments

| Column Name        |  Data Type  |  Description |
|--------------------|:-----------:|------------------------------------------------:|
| deployment_id      |  INTEGER    | Deployment Id (eg 554233)                       |
| ts                 |  DATE       | Timestamp of the deployment (eg unix ts)        |

### Programs

Name: <sys_id>_<sys_ver>_programs

| Column Name        |  Data Type  |  Description |
|--------------------|:-----------:|------------------------------------------------:|
| name               |  STRING     | Name of Program                                 |
| description        |  STRING     | Description of program                          |
| language           |  STRING     | Language of the program (eg. python)            |
| fileTree           |  STRING     | JSON String of the filetree for the program     |


### Traces

Name: <sys_id>_<sys_ver>_traces

| Column Name        |  Data Type  |  Description |
|--------------------|:-----------:|------------------------------------------------:|
| deploymen_id       |  INTEGER    | Deployment Id (eg 554233)                       |
| trace_id           |  INTEGER    | Trace Id (eg 235234)                            |
| startTs            |  DATE       | Name of Program                                 |
| endTs              |  DATE       | Description of program                          |
| traceType          |  NUMBER     | Language of the program (eg. python)            |
| traces             |  STRING     | JSON String of the traces for this program      |