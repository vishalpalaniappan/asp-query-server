import sqlite3
import json
import os
from datetime import datetime

class EventWriter:
    '''
        This class writes the IO events to the database. 
    '''

    def __init__(self, db):
        self.conn = db.conn
        self.cursor = self.conn.cursor()
        self.createIoEventsTable()    

    def createIoEventsTable(self):
        '''
            Create the table to store all the systems.
        '''
        sql = '''
            CREATE TABLE IF NOT EXISTS IOEVENTS 
            (
                id INT AUTO_INCREMENT PRIMARY KEY,
                system_id VARCHAR(100) NOT NULL,
                system_ver VARCHAR(100),
                deployment_id VARCHAR(100),
                program_execution_id VARCHAR(100),
                start_ts TIMESTAMP,
                end_ts TIMESTAMP,
                adli_execution_id VARCHAR(100),
                adli_execution_index VARCHAR(100),
                node_type VARCHAR(100),
                node TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        '''
        self.cursor.execute(sql)

    def checkIfFieldExists(self, table, column, value):
        '''
            Checks if the database has the given field.
        '''
        query = f"""
            SELECT 1 FROM {table}
            WHERE {column} = %s
            LIMIT 1
        """
        self.cursor.execute(query, (value, ))

        return True if self.cursor.fetchone() else False
        
    def addEventsToDb(self, logFile):
        '''
            Add system io events to the database.
        '''
        header = logFile.decoder.header


        # Get system information
        systemInfo = header.sysinfo
        metadata = systemInfo.get("metadata")
        sysId = metadata.get("systemId")
        sysVer = metadata.get("systemVersion")
        deploymentId = systemInfo.get("adliSystemExecutionId")
        
        # Get execution information
        execInfo = header.execInfo
        programId = execInfo.get("programExecutionId")
        ts = execInfo.get("timestamp")

        # Get program information
        programInfo = header.programInfo
        
        # If the program has already been processed, then return.
        fileExists = self.checkIfFieldExists("IOEVENTS", "program_execution_id", programId)
        if (fileExists):
            print(f"File {programId} has already been processed.")
            return

        if len(logFile.decoder.systemIoNodes) > 0:
            # Create table data for each io node
            event_data = []
            for event in logFile.decoder.systemIoNodes:
                node = event["node"]
                adliExecutionId = node["adliExecutionId"]
                adliExecutionIndex = node["adliExecutionIndex"]
                node_type = event["node_type"]
                nodeStr = json.dumps(node)
                dt_string = datetime.fromtimestamp(float(ts))
                event_data.append((sysId, sysVer, deploymentId, programId, dt_string, None, adliExecutionId, adliExecutionIndex, node_type, nodeStr))        


            sql = f''' INSERT INTO IOEVENTS(
                system_id, system_ver, deployment_id, \
                program_execution_id, start_ts, end_ts, \
                adli_execution_id, adli_execution_index, \
                node_type, node
                )
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) '''
            self.cursor.executemany(sql, event_data)
            self.conn.commit()
            
            print(f"Added System IO events from {programInfo['name']} to database.")