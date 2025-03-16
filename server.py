#!/usr/bin/env python

import asyncio
import argparse
from websockets.asyncio.server import serve
from application.queryHandler import handle_query

async def main():
    '''
        Creates a websocket at the provided port and initializes
        the query handler. 
    '''
    parser = argparse.ArgumentParser(description='WebSocket server for ASV queries')

    parser.add_argument('--host',
                        default='localhost',
                        help='Host to bind the server to')
                        
    parser.add_argument('--port',
                        type=int,
                        default=8765,
                        help='Port to bind the server to')
    
    args = parser.parse_args()

    print(f"Starting WebSocket server on {args.host}:{args.port}")
    async with serve(handle_query, args.host, args.port) as server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())