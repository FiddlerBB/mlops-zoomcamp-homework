include .env
export $(shell sed 's/=.*//' .env)

infra-plan:
	terraform plan

infra-apply:
	terraform apply --auto-approve

infra-destroy:
	terraform destroy