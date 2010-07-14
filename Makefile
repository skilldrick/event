ifeq ($(TERM),cygwin) #This is only true in cygwin so:
PYTHON=/cygdrive/c/Python26/python.exe #we're using cygwin
else
PYTHON=python #we're using linux
endif

main:
	$(PYTHON) event.py
test:
	$(PYTHON) testall.py
guitest:
	$(PYTHON) event.py --test
clean:
	$(PYTHON) reset.py
