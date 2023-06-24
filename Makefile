PHONY: local
local: 
	cd ./react && yarn build; \
	cd ..; \
	pip install -r requirements.txt; \
	python upload_static_files.py; \
	sam local start-api