ICS=$(wildcard calendars/*.yaml)
OUT=$(patsubst calendars/%.yaml,out/%.ics,$(ICS))

build:
	mkdir -p out
	python $(MAKEFILE_DIR)/build.py calendars/*.yaml --yaml2ics='python $(MAKEFILE_DIR)/yaml2ics/yaml2ics.py' -o out -i out/index.html --timezone=Europe/Helsinki --timezone=Europe/Stockholm

THIS_MAKEFILE := $(word $(words $(MAKEFILE_LIST)),$(MAKEFILE_LIST))
MAKEFILE_DIR := $(dir $(realpath $(THIS_MAKEFILE)))

clean:
	rm -r out || true

install:
	pip install -r requirements.txt
