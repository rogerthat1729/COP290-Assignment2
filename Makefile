.DO_IT : run

run:
	@python3 run.py $(type) $(file)
	@rm -rf *.mp3
	@rm -rf *.mp4
	@rm -rf *.pdf
	