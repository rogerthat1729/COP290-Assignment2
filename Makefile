.all : clean

clean: run
	@cd code; rm -rf __pycache__

run:
	@cd code; python3 main.py;
	