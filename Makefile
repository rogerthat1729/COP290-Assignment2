.all : clean

clean: run
	@cd code; rm -rf __pycache__

run: install
	@cd code; python3 main.py;

install:
	@pip install -r requirements.txt
	