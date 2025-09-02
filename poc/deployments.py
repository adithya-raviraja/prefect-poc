from prefect.runner.storage import GitRepository
from poc.test_prefect_flow import test_flow_functions
from prefect.blocks.system import Secret
from prefect import flow as prefect_flow_class

DEPLOYMENT_CONFIGS = [
    {
        "name": "Test POC Deployment",
        "flow": test_flow_functions,
        "docker_image": "adithyaraviraja/docker-public-poc:0.0.1-poc",
        "work_pool_name": "poc-pool",
        "tags": ['poc'],
        "concurrency": 2,
        "job_variables": {
            "env": {
                "ENVIRONMENT": "local"
            }
        }
    }
]

GITHUB_URL = "https://github.com/adithya-raviraja/prefect-poc.git"
GITLAB_BRANCH = "main"
def create_deployment():
    access_token = Secret.load('access-token')
    gitlab_source = GitRepository(url=GITHUB_URL, credentials={"access_token": access_token},
                                    branch=GITLAB_BRANCH, name='async-tasks', pull_interval=15)
    for deployment in DEPLOYMENT_CONFIGS:
        try:
            flow = deployment['flow']
            if 'docker_image' in [None, '']:
                print(f'No docker image provided for {deployment["name"]}')
                continue
                
            flow_entrypoint = flow._entrypoint
            flow_entrypoint = flow_entrypoint.replace('.', '/')
            new_flow_entrypoint = flow_entrypoint[:flow_entrypoint.find(':')]
            new_flow_entrypoint += '.py'
            new_flow_entrypoint += flow_entrypoint[flow_entrypoint.find(':'):]
            prefect_flow_class.from_source(source=gitlab_source, entrypoint=f'{new_flow_entrypoint}').deploy(
                name=deployment['name'], work_pool_name=deployment.get('work_pool_name', 'common-pool'),
                job_variables=deployment['job_variables'], build=False, push=False, image=deployment['docker_image']
            )
        except Exception as e:
            print(f'Failed to create deployments {deployment["name"]} {str(e)}')
            continue
    
if __name__ == "__main__":
    create_deployment()
