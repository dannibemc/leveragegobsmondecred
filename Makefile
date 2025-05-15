.PHONY: test clean

test:
	pytest test_utils.py --disable-warnings -v

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -r {} +
