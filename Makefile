REPO_NAME := $(shell basename `git rev-parse --show-toplevel` | tr '[:upper:]' '[:lower:]')
GIT_TAG ?= $(shell git log --oneline | head -n1 | awk '{print $$1}')
IMAGE := $(REPO_NAME)
UID ?= bounds
GID ?= bounds


.PHONY: docker docker-push docker-pull enter

docker:
	docker build --tag $(IMAGE):$(GIT_TAG) . -f Dockerfile
	docker tag $(IMAGE):$(GIT_TAG) $(IMAGE):latest

docker-push:
	docker push $(IMAGE):$(GIT_TAG)
	docker push $(IMAGE):latest

docker-pull:
	docker pull $(IMAGE):$(GIT_TAG)
	docker tag $(IMAGE):$(GIT_TAG) $(IMAGE):latest

enter:
	docker run -it --rm -v $$(pwd):/code -w /code -u $(UID):$(GID) $(IMAGE) bash
	
experiment:
	docker run -it --rm -v $$(pwd):/code -w /code -u $(UID):$(GID) $(IMAGE) python3.10 main.py