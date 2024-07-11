import os
import subprocess
import yaml

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.appconfiguration import AzureAppConfigurationClient


def set_profile():
    credential = DefaultAzureCredential()
    
    key_vault_name = 'BillTestDbtLocal'
    key_vault_url = f'https://{key_vault_name}.vault.azure.net/'
    secret_client = SecretClient(vault_url=key_vault_url, credential=credential)
    app_config_connection_string = secret_client.get_secret('appConfigConnectionString').value
    app_config_client = AzureAppConfigurationClient.from_connection_string(app_config_connection_string)
    
    parameters = {
        'server': app_config_client.get_configuration_setting(key='server').value,
        'port': int(app_config_client.get_configuration_setting(key='port').value),
        'database': app_config_client.get_configuration_setting(key='database').value,
        'schema': app_config_client.get_configuration_setting(key='schema').value,
        'encrypt': app_config_client.get_configuration_setting(key='encrypt').value == 'True',
        'trust_cert': app_config_client.get_configuration_setting(key='trust_cert').value == 'True',
        'threads': int(app_config_client.get_configuration_setting(key='threads').value)
      }
    
    parameters['user'] = secret_client.get_secret('dbuser').value
    os.environ['DB_PASSWORD'] = secret_client.get_secret('dbpassword').value
    parameters['password'] = '{{ env_var("DB_PASSWORD") }}'
    
    with open('worker/profiles_template.yml', 'r') as file:
        profiles = yaml.safe_load(file)
    
    profiles['non-prod']['outputs']['dev'].update(parameters)
    
    with open('worker/profiles.yml', 'w') as file:
        yaml.dump(profiles, file, default_flow_style=False)
    

if __name__ == '__main__':
    set_profile()
    result = subprocess.run(["dbt", "debug"], cwd='worker', capture_output=True)
    
    if result.returncode == 0:
        result = subprocess.run(["dbt", "seed"], cwd='worker', capture_output=True)

        if result.returncode == 0:
            result = subprocess.run(["dbt", "run"], cwd='worker', capture_output=True)
    else:
        print(result.stdout)
    
    

