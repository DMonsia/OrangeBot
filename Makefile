.ONESHELL:

.PHONY: build
build:
	docker build -t dmonsia/orangebot .

.PHONY: run
run:
	docker run -d \
		--name orangebot \
		-p 8000:8000 \
		-v ${DATA_FILE}:/app/data \
		dmonsia/orangebot