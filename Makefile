###########################
## Environment variables ##
###########################
include .env

export ALIAS = flashback 		# must match name field in environment.yaml

export PROJECT_ID = $(GCP_PROJECT_ID)
export GOOGLE_APPLICATION_CREDENTIALS ?= $(HOME)/$(CREDENTIALS)

#############
## Install ##
#############

mamba:
	mamba env update -n $(ALIAS) --file environment.yml --prune \
		|| \
	mamba env create --file environment.yml

#############
## Testing ##
#############

tests:
	pytest src/flashback/


################
## Formatting ##
################

format:
	black .

###############
## Terraform ##
###############

export TF_VAR_project_id = $(GCP_PROJECT_ID)
export TF_VAR_region = $(PROJECT_REGION)
export TF_VAR_secret_flashback_webhook = $(SECRET_FLASHBACK_WEBHOOK)

terraform:
	cd infrastructure && terraform init && terraform apply -auto-approve

