# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import sys
import os
import asyncio
from six.moves import input
import threading
from azure.iot.device.aio import IoTHubModuleClient
import logging

import ptvsd
ptvsd.enable_attach(('0.0.0.0',  5678))

async def main():
    try:
        logging.info ( "IoT Hub Client for Python" )

        # The client object is used to interact with your Azure IoT hub.
        module_client = IoTHubModuleClient.create_from_edge_environment()

        # connect the client.
        await module_client.connect()

        # event indicating when we can close this program
        finished = threading.Event()

        # Define behavior for receiving a twin desired properties patch
        # NOTE: this could be a coroutine or function
        def twin_patch_handler(patch):

            ptvsd.break_into_debugger()

            logging.info("the data in the desired properties patch was: {}".format(patch))

            # update the reported properties
            #reported_properties = {"temperature": random.randint(320, 800) / 10}
            #print("Setting reported temperature to {}".format(reported_properties["temperature"]))
            #await module_client.patch_twin_reported_properties(reported_properties)
    
        # set the received data handlers on the client       
        module_client.on_twin_desired_properties_patch_received = twin_patch_handler
       

        # NOTE: This sample will NOT exit waiting for twin patches
        finished.wait()

        # Once it is received, shut down the client
        await module_client.shutdown()

    except Exception as e:
        logging.fatal( "Unexpected error %s " % e )
        raise

if __name__ == "__main__":

    # Set logging parameters
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)-15s] [%(threadName)-12.12s] [%(levelname)s]: %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)       # write in stdout
        ]
    )

    # Call Main function
    asyncio.run(main())