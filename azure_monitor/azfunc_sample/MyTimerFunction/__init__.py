import logging
import azure.functions as func
import mysql.connector
import ssl
import os, uuid

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from opencensus.extension.azure.functions import OpenCensusExtension
from opencensus.trace import config_integration

config_integration.trace_integrations(['mysql'])
config_integration.trace_integrations(['requests'])

OpenCensusExtension.configure()

def main(myTimerFunction: func.TimerRequest) -> None:
    
    logging.info('Python Timer trigger function processed a request.')

    #sql server
    #server = os.getenv('DB_SERVER')
    #database = os.getenv('DB_DATABASE')
    #username = os.getenv('DB_USERNAME')
    #password = os.getenv('DB_PASSWORD')
    #driver= '{ODBC Driver 17 for SQL Server}'

    server = os.getenv('DBHOST')
    database = os.getenv('DBNAME')
    username = os.getenv('DBUSER')
    password = os.getenv('DBPASS')
    
    crtpath = 'BaltimoreCyberTrustRoot.crt.pem'
    #crtpath = 'DigiCertGlobalRootCA.crt.pem'

    ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

    # Connect to MySQL
    cnx = mysql.connector.connect(
        user=username, 
        password=password, 
        host=server, 
        port=3306,
        ssl_ca=crtpath,
        tls_versions=['TLSv1.2']
    )

    logging.info(cnx)
    
    # Show databases
    cursor = cnx.cursor()
    cursor.execute("SHOW DATABASES")
    result_list = cursor.fetchall()
    
    # Build result response text
    result_str_list = []
    for row in result_list:
        row_str = ', '.join([str(v) for v in row])
        result_str_list.append(row_str)
    result_str = '\n'.join(result_str_list)

    #add a random file to storage account...
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # Create a unique name for the container
    container_name = 'files'

    # Create the container
    try:
        container_client = blob_service_client.create_container(container_name)
    except:
        logging.info("Container exists?")

    # Create a local directory to hold blob data
    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    logging.info(ROOT_DIR)

    local_path = ROOT_DIR + "\\tmp\data"

    try:
        os.mkdir(local_path)
    except:
        logging.info("Folder exists?")

    # Create a file in the local data directory to upload and download
    local_file_name = str(uuid.uuid4()) + ".txt"
    upload_file_path = os.path.join(local_path, local_file_name)

    # Write text to the file
    file = open(upload_file_path, 'w')
    file.write("Hello, World!")
    file.close()

    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

    logging.info("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

    # Upload the created file
    with open(upload_file_path, "rb") as data:
        blob_client.upload_blob(data)
