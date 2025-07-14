install:
	pip install -r requirements.txt

test:
	pytest tests/

lint:
	flake8 src/ pipelines/ tests/ deployment/

format:
	black .

docker-build:
	docker build -t ecommerce-return-app .

docker-run:
	docker run -p 8000:8000 ecommerce-return-app
