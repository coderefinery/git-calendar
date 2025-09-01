# YAML to ics calendar

This repository turns yaml files into .ics calendars (importable into
different programs) using
[yaml2ics](https://github.com/scientific-python/yaml2ics) and GitHub
actions.  Or, you can use git-calendar directly.

This repository provides a working template for the action to build +
publish to Github Pages, including files into other files, and some
minimal HTML index pages.  All of the important logic is in
[yaml2ics](https://github.com/scientific-python/yaml2ics), so if you
want to roll your own site and build system (which isn't hard) for the
.ics files, consider using yaml2ics directly.



## Example deployments

The CodeRefinery calendar
* [Built calendar site](https://coderefinery.github.io/calendar/)
  (the auto-generated landing page)
* [Source repository](https://github.com/coderefinery/calendar)
* Optional: [Calendars inserted into
  website](https://coderefinery.org/calendars/) ([source](https://github.com/coderefinery/coderefinery.org/blob/main/content/calendars.md))



## General principles

One defines events in YAML, and they get built to `.ics` files which
can be served as a static site.  These can then be imported to various
calendar clients.

There's a command line program, `git-calendar`, which takes YAML files
as input (one of which can be named `_config.yaml`).  The last
argument is the output directory to which to write.

A typical repository layout:

- `calendars/*.yaml` contains the input calendars.
- `output/` is the web root for web deployment
- `output/*.ics` is the build calendars
- `output/index.html` gets built and serves as a landing page with
  links to the .ics files

For now, see `calendars/example.yaml` for an example, or any of the
test calendars in yaml2ics.  This documentation should be improved.



## Usage - Github action

This can be used as Github action (see EXAMPLE REPO for the full file).

```yaml
      - uses: actions/checkout@v4
      - name: git-calendar action
        uses: coderefinery/git-calendar@action-test
        with:
          input_dir: calendars    # the default, not required
          output_dir: output      # the default, not required
          index_file: index.html  # the default, set to '' to not
        create
        htmlbody_file: body.html  # Only the part inside <body> for inclusion in other files
```

This action will automatically deploy to Github Pages.  You can set
`with: pages_deploy: false` to disable this.  The action will also
setup Python and install this Python library.  If you already set up
Python, it may be easier to code up your own action than use this.



## Usage - Raw Github action

If you want to program the action yourself, below is the base.  You
probably can probably figure out how to integrate this to a Github
Pages deployment and all.
```yaml
    - name: build
      shell: bash
      run: |
        git-calendar calendars/*.yaml output/ --index=index.html --edit-link=https://github.com/$GITHUB_REPOSITORY
```



## Usage - command line

This is a Python package, install as normal (yes, in a virtual environment, etc...):
```console
$ pip install git-calendar
```

Then run:

```console
$ git-calendar calendars/*.yaml output/ --index=index.html --edit-link=https://github.com/$GITHUB_REPOSITORY
```

There are more options, not currently documented.



## Usage - via raw yaml2ics

Don't forget this is just a wrapper around
[yaml2ics](https://github.com/scientific-python/yaml2ics) - if you
only need a .ics file and not index.html, including calendars in
others, etc., then maybe that is your starting point:

```console
$ python yaml2ics.py example/test_calendar.yaml example/another_calendar.yaml > out.ics
```



## Status

Beta as of 2025, it works but may require code changes still to get
around corner cases.  As of 2025 issues will probably be responded to.



## See also

* This directly uses https://github.com/scientific-python/yaml2ics as
  the yaml to ical generator - if you want to create your own build
  system, use that directly.
* yaml2ics uses https://github.com/ics-py/ics-py/
* Another (old, unmaintained, not really usable) yaml-to-ics is
  https://github.com/priyeshpatel/yaml-to-ical
