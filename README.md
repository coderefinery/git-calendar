# yaml to ics calendar

This repository turns yaml files into icl calendars (importable into
different programs) using
[yaml2ics](https://github.com/scientific-python/yaml2ics) and GitHub
actions.

This repository provides a working template for the action to build +
publish to Github Pages, and some minimal HTML index pages.  All of
the important logic is in
[yaml2ics](https://github.com/scientific-python/yaml2ics), so if you
want to roll your own site and build system (which isn't hard) for the
.ics files, consider using yaml2ics directly.

This is sort of alpha: it works and is used, but code editing or
asking for clarifications is probably needed.  Documentation should be
improved.



## Example

The CodeRefinery calendar
* [Built calendar site](https://coderefinery.github.io/calendar/)
  (main landing page for most projects)
* [Source repository](https://github.com/coderefinery/calendar)
* Optional: [Calendars inserted into
  website](https://coderefinery.org/calendars/) ([source](https://github.com/coderefinery/coderefinery.org/blob/main/content/calendars.md))



## Usage

To use, look at
[git-calendar-template](https://github.com/coderefinery/git-calendar-template)
for a sample repository that uses this.  Generate your own repository
from that template and go from there.

This repository can also be installed as a Python pip package.

Usage in short:

- `calendars/*.yaml` contains the input calendars.
- `./build.sh` builds the outputs.  Edit this script as
  needed, or copy the command to your own build script.
  - `out/index.html` gets build and serves as a landing page
  - Calendars get build to `out/*.ics`
  - The Github Actions workflow file deploys `out/` to the `gh-pages`
  branch.

- **First time deployment note:** you have to go to settings and
  toggle pages off and on again the first time to enable Github Pages,
  after that Github Actions will automatically deploy.

For now, see `calendars/example.yaml` for an example, or any of the
test calendars in yaml2ics.  This documentation should be improved.



## Status

Alpha, it works but may require code changes still to get around
corner cases.



## See Also

* This directly uses https://github.com/scientific-python/yaml2ics as
  the yaml to ical generator - if you want to create your own build
  system, use that directly.
* yaml2ics uses https://github.com/ics-py/ics-py/
* Another (old, unmaintained, not really usable) yaml-to-ics is
  https://github.com/priyeshpatel/yaml-to-ical
