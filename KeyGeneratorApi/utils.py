from azure.storage.fileshare import ShareFileClient


def get_numbers_file(file_name: str) -> list[int]:
    file_client = ShareFileClient.from_connection_string(
        conn_str="DefaultEndpointsProtocol=https;AccountName=keygenapi;AccountKey=aIBjq6SkBUvT+jVn3qzcSA9i7qzuNPkRlip/Qs0su9j9gU7sdcbq+lH1t4EBy+t7u8zftCrwNOsm+ASt/zJsFA==;EndpointSuffix=core.windows.net",
        share_name="keygenapi",
        file_path=file_name
    )

    data = file_client.download_file().readall().decode().split('\n')
    return [int(n) for n in data if n.strip()]
