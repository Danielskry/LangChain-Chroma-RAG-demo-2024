import streamlit as st
import asyncio
import websockets
import json

st.title("QA WebSocket Client")

mode = st.selectbox("Choose mode", ["Ingest", "Retrieve"])

if mode == "Ingest":
    if st.button("Start Ingestion"):
        status_container = st.empty()
        
        async def connect_to_ingest():
            uri = "ws://web:5000/ingest"  # Use service name defined in docker-compose
            try:
                async with websockets.connect(uri) as websocket:
                    while True:
                        try:
                            message = await websocket.recv()
                            status_container.write(f"< {message}")
                        except websockets.ConnectionClosedOK:
                            status_container.write("Ingestion completed successfully.")
                            break
            except Exception as e:
                status_container.write(f"Error: {e}")
        
        asyncio.run(connect_to_ingest())

elif mode == "Retrieve":
    query = st.text_input("Enter your query:")
    if st.button("Send Query"):
        async def connect_to_retrieve(query):
            uri = "ws://web:5000/retrieve"  # Use service name defined in docker-compose
            async with websockets.connect(uri) as websocket:
                await websocket.send(query)
                response_container = st.empty()
                full_response = ""
                while True:
                    try:
                        response = await websocket.recv()
                        if response:
                            if response.startswith("Full response:"):
                                full_response = response[len("Full response: "):]
                                response_container.markdown(full_response.strip())
                            else:
                                # Correctly concatenate tokens without adding unnecessary spaces
                                if full_response and not full_response[-1].isspace() and not response[0].isspace():
                                    if not response[0].isalnum() and not full_response[-1].isalnum():
                                        full_response += response
                                    else:
                                        full_response += " " + response
                                else:
                                    full_response += response

                                # Ensure there's a space after punctuation marks in the current response
                                full_response = full_response.replace(" .", ". ").replace(" ,", ", ").replace(" !", "! ").replace(" ?", "? ").replace(" ;", "; ").replace(" :", ": ")
                                
                                response_container.markdown(full_response.strip())
                        else:
                            response_container.text("Received an empty response.")
                    except websockets.ConnectionClosed:
                        response_container.text("Connection closed by the server")
                        break
        
        asyncio.run(connect_to_retrieve(query))
