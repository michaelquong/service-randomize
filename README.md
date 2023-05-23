# service-randomize

Demo: Service outlining containerization and helm chart example.

Locally, Application is available at the following:
1. Locally direct via source, http://localhost:5000/docs
2. Locally via Container, http://localhost:5000/docs
3. Locally deployed to Minikube & port-forwarded, http://localhost:8080/docs

## About the Application
An API Service using Flask framework and integrated with [flask-smorest](https://flask-smorest.readthedocs.io/en/latest/) which is Marshmallow-based REST API framework which helps to serialize and deserialize data. It relies on the marshmallow ecosystem to automatically generate OpenAPI Specifications for documentation purposes.

The main functionality of the Randomize service is to take in a word from a JSON body and provide a randomized version of the given word. The `api/randomizes` expects the following JSON body as input:
```
{
    "word": "word_to_randomize"
}
```
The subsequent output will show a randomized version of the string with additional metadata like creation date, and original string.
Example output:
```
{
  "original": "string",
  "created": "2023-05-23T02:37:57.698Z",
  "id": 0,
  "updated": "2023-05-23T02:37:57.698Z",
  "jumbled": "gsntri"
}
```

To try application directly from source, run:
```
make dev

# Additional commands if starting from scratch.
# `make db_upgrade` to apply all database updates.
```
Command runs application in full verbose debug mode which include auto refresh on file changes.

### OpenAPI Documentation 
Documentation at `/docs` is automatically generated via flask-smorest library which tries to take into account Docstrings to provide enough information regarding API endpoint usage.

### Storage Persistence
For local development, Sqlite is used to maintain word records and API usage history audits. For production, Sqlite is to be replaced by Postgresql. Database management is handled via [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/). Flask-migrate provides flask commands to initialize, migrate and upgrade the reflected database tables. During development, any changes to our database models need to be kept up to date during deployments with Flask-Migrate commands.
Steps to following when updating models:
1. Run `make migrations` to reflect all the necessary database changes required. This creates a new [versions](./migrations/versions/) entry containing the delta of changes made.
2. Review and update the new migration version entry as necessary to match your required database changes.
3. Include your new migration version as part of your Pull Request.

During local development, run `make db_upgrade` to apply migrations to your local SQLite database.

During next deployment, the database migrations will automatically be managed during container startup. Container's [entrypoint.sh](./entrypoint.sh) manages the responsibilities of applying the necessary upgrades.

*Notes: Since database upgrades has currently being managed automatically. It is critical that there development changes to models have a degree of flexibility and backwards compatibility. Currently, assuming automatically managing database upgrades is more beneficial than manually applying them.*

*Caveats: Currently, database interactions are managed by [SQLalchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/) ORM models. This allows us to leverage their automatic input parametrization functionality. In future updates, all filtering requirements (such as `.ilike`) will be sanitized by [SQLalchemy utilities](https://sqlalchemy-utils.readthedocs.io/en/latest/orm_helpers.html#sqlalchemy_utils.functions.escape_like).*

## About the Containerization
Application [Dockerfile](./Dockerfile) is a multi-staged dockers file which is separated by category:
1. Application runtime, Python 3.8 base image. Changes affecting runtime should be applied here.
2. Application library dependencies. Application's [requirements.txt](./requirements.txt) are compiled here. Any additional libraries to aid dependency compilation should be added here.
3. Application image. Combines the outputs from the above with source code to build the required application image.

Additionally, an [entrypoint.sh](./entrypoint.sh) is available for anything that needs to be done before just before application startup. Example, currently, database upgrades are utilizing this.

Update Dockerfile and/or entrypoint.sh according. To build the Docker image run:
```
make image
```
Command will create a `my/app:latest` images locally.
*Notes: application versioning and tagging of images are currently not implemented. All my/app images will automatically be tagged latest. Because of this, images are also not pushed to any registry. This can be accommodated in the future with additional makefile targets/instructions.*

To run the image as a container locally, run the following after building image.
```
make container
```
This will run `my/app:latest` on exposed port `5000` with a volume mounted to `docker-volume:data -> container:/var/opt/myapp/instance/`. The volume mount provides an option to reuse SQLite db. Application will run on [Gunicorn](https://docs.gunicorn.org/en/stable/index.html) WSGI server which is suitable for production.

## About the Deployment
A minimalistic [Helm chart](./helm/) is available to be used to deploy the application image minikube/kubernetes. Values.yaml overlay file, [localvalues.yaml](./helm/localvalues.yaml), is available to override values for local deployment for testing purposes only (like minikube).

Additional, environment specific overlay values files can be added here to support additional environments.

### Deployment to Minikube
*Notes: Assumes proper knowledge of Minikube installation is already done. Otherwise, consult relavent documentation accordingly. Additional requirements are Docker engine & client and Kubectl.*

*Caveats: Since we are currently not pushing our images to a registry, `localvalues.yaml` will overlay pullPolicy to Never such that Helm does not cause Minikube to hang due to imagepullbackoff errors. To ensure that Minikube is able to find built application Docker image locally, run the following if image relate errors occur:*
```
# Ensure local Minikube instance fins local images
eval $(minikube docker-env) # set environment
make image # Optionally, rebuild Application Image
```

To deploy to Minikube, run:
```
make deployment/local
```
This will automatically set the following:
- release name: `randomize`
- namespace: `local-dev`

*Notes: the make command assumes the release name and namespace to deploy the application to. The assumption is that multiple environments would be deployed to the same cluster. If this is not the deployment model/topology. Adjust make targets accordingly.*

Once the application is deployed to Minikube, the application will be available after the follow port-forwarding commands:
```
export POD_NAME=$(kubectl get pods --namespace local-dev -l "app.kubernetes.io/name=randomize,app.kubernetes.io/instance=randomize" -o jsonpath="{.items[0].metadata.name}")
  export CONTAINER_PORT=$(kubectl get pod --namespace local-dev $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
  kubectl --namespace local-dev port-forward $POD_NAME 8080:$CONTAINER_PORT
```
*Notes: Port-forwarding should only be done locally, for quick testing purposes only. For proper networking, Ingress configurations should be enabled and set appropriately in Helm chart.*

*TODO: Persistent Volume mounting for Minikube. Current charts do not persist data as the solution to persist data in Minikube is not easily reusable when deploying to Kubernetes. Only available option is to create a persistent volume (PV) yaml on Hostpath (from a specific [list](https://minikube.sigs.k8s.io/docs/handbook/persistent_volumes/) of supported mount points) and a persistence volume claim yaml claiming the respective PV.*


### Deployment to Kubernetes
TBD

## Developer Experience
To help with the development experience, pre-commit is an optional tool to automate and adhere to pep8 guidelines. The `pre-commit` and `.pre-commit-config` is set up to style and lint code changes before they are committed to branch. It is required to fix all caught rules that were not able to be automatically corrected. This is an optional tool and to opt in, run:
```
pip install -r requirements-dev.txt
pre-commit install
```


## TODO

### Security
- Authentication and Authorization via JWT (using flask-jwt-extended)
- Require JWT access by providing `Authentication: bearer TOKEN` header values for audit history route (`/api/histories`)
- Figure out password management requirements. If there is some kind of vault system in place and if application should be Vault aware. Update deployment and configurations accordingly.
- Update application configuration to respect environment variables. Have an easier time passing environment values to adjust application configuration.

### Testing
- Implement pytest Testing framework. Complete `conftest.py` fixtures for test_app() and test_db() testing data.
- Setup makefile targets to run pytest commands for unit, integration and other test formats needed using markers and directory structures.

### Deployment
- Update Helm Charts to enable Postgresql as a possible dependency chart. Update values.yaml to configure Postgesql options that match application requirements.
- Update Helm Chart to support PV and PVC for data persistence on Kubernetes. Identify the Storage Class provider to enable automatic storage configuration and provisioning.
- Update Helm Chart sanity tests such that `helm test randomize` release passes test cases on each deploy.
- Include Docker image tagging and pushing to registry as a makefile target.
- Enable and configure Ingress.yaml for more appropriate Kubernetes deployment.

### MISC
- In depth error handling to reduce 500 server errors. To reduce the number of uncaught errors, and provide users with better context and status codes.
- Look into requirements for custom Error Exception classes to provide better context of caught errors.
- Implement Application logger to define logging format and log message consistency. For better log scraping experience.
- Pin library dependencies for more consistent experiences during later stages for code hardening. When deploying to higher tiers of environments, library dependencies should be pinned to appropriate values to ensure build consistency if required.
