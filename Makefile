ICS=$(wildcard calendars/*.yaml)
OUT=$(patsubst calendars/%.yaml,out/%.ics,$(ICS))

build: $(OUT)
	rm -f out/index.html
	@echo "Available calendars:</br>" >> out/index.html
	@echo "<ul>" >> out/index.html
	files="$(shell cd out ; ls *.ics)" ; \
	for file in $${files}; do \
	    if test "$${file}" = "example.ics" -a -n "$(GITHUB_REPOSITORY)" -a "$(GITHUB_REPOSITORY)" != "coderefinery/git-calendar" ; then continue ; fi ; \
	    echo $${file} ; \
            TZ=Europe/Stockholm mutt-ics out/$$file  | sed 's/^Subject:/\n\n----------\nSubject:/' > out/$$file.stockholm.txt ; \
            TZ=Europe/Helsinki mutt-ics out/$$file  | sed 's/^Subject:/\n\n----------\nSubject:/' > out/$$file.helsinki.txt ; \
	    echo "<li><a href=\"$$file\">$$file</a>" >> out/index.html ; \
	    echo "(<a href=\"$$file.stockholm.txt\">text, Stockholm times</a>)" >> out/index.html ; \
	    echo "(<a href=\"$$file.helsinki.txt\">text, Helsinki times</a>)" >> out/index.html ; \
	    echo "</br></li>" >> out/index.html ; \
	done
	@echo "</ul>" >> out/index.html
	@echo "<br>" >> out/index.html
	@echo "To subscribe to a calendar:<br>" >> out/index.html
	@echo "<ul>" >> out/index.html
	@echo   "<li>Google calendar: Other calendars (left sidebar) → \"+\" to add new → From URL.</li>" >> out/index.html
	@echo "<li>Outlook web: Add Calendar → Subscribe from web.</li>" >> out/index.html
	@echo "<li>Thunderbird: Left sidebar → Calendar → \"+\" to add new → On the network → This location doesn't require credentials → paste URL → (carry on).  Please set to update every 60 minutes or less frequently.</li>" >> out/index.html
	@echo   "</ul>" >> out/index.html
	@echo -n "<br>Last update: $$(date) (git revision $(shell git rev-parse --short HEAD))" >> out/index.html

out/%.ics: calendars/%.yaml
	mkdir -p out
	python3 yaml2ics/yaml2ics.py $< > $@


clean:
	rm -r out || true

install:
	pip install -r requirements.txt
