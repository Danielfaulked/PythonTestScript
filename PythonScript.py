pip install azure-identity azure-keyvault-secrets azure-storage-blob
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobServiceClient, BlobSasPermissions, generate_blob_sas
from datetime import datetime, timedelta

def get_secret_from_vault(vault_url, secret_name):
    credential = DefaultAzureCredential()
    secret_client = SecretClient(vault_url=vault_url, credential=credential)
    secret = secret_client.get_secret(secret_name)
    return secret.value

def list_mp4_files(connection_string, container_name):
    service = BlobServiceClient.from_connection_string(connection_string)
    container = service.get_container_client(container_name)

    print("Listing all .mp4 files:")
    blob_list = container.list_blobs()
    for blob in blob_list:
        if blob.name.endswith('.mp4'):
            sas_token = generate_blob_sas(
                account_name=service.account_name,
                container_name=container_name,
                blob_name=blob.name,
                account_key=service.credential.account_key,
                permission=BlobSasPermissions(read=True),
                expiry=datetime.utcnow() + timedelta(hours=1)
            )
            sas_url = f"https://{service.account_name}.blob.core.windows.net/{container_name}/{blob.name}?{sas_token}"
            print(sas_url)

# Replace with your vault URL and secret name
vault_url = 'https://my-key-vault.vault.azure.net/'
secret_name = 'my-secret'

# Replace with your container name
container_name = 'my-container'

connection_string = get_secret_from_vault(vault_url, secret_name)
list_mp4_files(connection_string, container_name)
