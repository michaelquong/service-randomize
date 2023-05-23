PORT = 5000
FLASK := FLASK_APP=run.py flask
GUNICORN := gunicorn --bind :$(PORT) run:app

.PHONY: venv dev production
.venv:
	python3 -m venv .venv

dev:
	@FLASK_ENV=development $(FLASK) run --debug

production:
	@$(GUNICORN)


## data management
.PHONY: db_upgrade
instance/project.db: ## initialize new db.
	@flask db init

migrations: ## update db migrations directory for Alembic
	@flask db migrate -m "Latest db updates created: $(date --utc +%Y%m%d_%H%M%SZ)"

db_upgrade: ## apply latest db migrations
	@flask db upgrade


IMAGE := my/app
## application package
.PHONY: image container
image:
	@docker build -t $(IMAGE):latest .

container:
	docker run -d -p $(PORT):$(PORT) -v data:/var/opt/myapp/instance/:rw $(IMAGE):latest


APP := randomize
## application deployment
.PHONY: deployment/local deployment/production
deployment/local:
	helm upgrade -i $(APP) ./helm/$(APP) -f ./helm/localvalues.yaml --namespace local-dev --create-namespace --wait

deployment/production:
	helm upgrade -i $(APP) ./helm/$(APP) -f ./helm/prodvalues.yaml --namespace production --create-namespace --wait
