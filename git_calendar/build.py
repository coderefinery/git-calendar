import argparse
import os
from os.path import dirname, join
from pathlib import Path
import shutil
import subprocess
import sys
import time

import markdown_it
import jinja2
import yaml

import yaml2ics

TEMPLATE_DIR = Path(__file__).parent/'templates'

def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('inputs', nargs='+', help="input files", type=Path)
    parser.add_argument('--output', '-o', help="output directory", type=str)
    parser.add_argument('--index', '-i', help="output HTML index file", type=str)
    parser.add_argument('--html-body', '-b', help="output HTML body to be included in other pages", type=str)
    parser.add_argument('--timezone', action='append', help="zoneinfo timezone names", type=str, default=[])
    parser.add_argument('--edit-link', help='Link to edit, will be added to the generated page.')
    parser.add_argument('--base-url', help='Base url to append in front of all .ics files '
                        '(include trailing slash).',
                        default='')
    args = parser.parse_args(argv)

    calendars = [ ]
    timezones = [ ]
    config = None
    for timezone in args.timezone:
        timezones.append({'tz': timezone, 'tzslug': timezone.replace('/', '-')})
    if not os.path.exists(args.output):
        os.mkdir(args.output)

    for f in args.inputs:
        if f.stem == '_config':
            print(f"processing config metadata {f}", file=sys.stderr)
            config = yaml.safe_load(open(f))
            continue
        print(f"processing {f}", file=sys.stderr)
        calendar = { }
        calendar['data'] = yaml.safe_load(open(f))
        calendar['fbase'] = fbase = os.path.splitext(os.path.basename(f))[0]
        calendar['fics'] = fics = fbase + '.ics'
        calendar['furl'] = args.base_url + fics
        if not calendar['data'].get('index-ignore', False):
            calendars.append(calendar)
        output = join(args.output, fics)

        calendar = yaml2ics.files_to_calendar([f])
        open(output, 'w').write(calendar.serialize())

        # Generate the rendered views in different timezones
        for tzdata in timezones:
            # This is clearly a hack, calling the shell commands.  This should
            # be improved later.
            subprocess.check_output(
                fr"TZ={tzdata['tz']} mutt-ics out/{fics}  | sed 's/^Subject:/\n\n----------\nSubject:/' > out/{fics}.{tzdata['tzslug']}.txt",
                shell=True)

    if args.index or args.html_body:
        timestamp = subprocess.check_output('date', encoding='utf8').strip() # subprocess to get timezone
        git_hash = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], encoding='utf8').strip()

        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader([TEMPLATE_DIR]),
            autoescape=jinja2.select_autoescape(['html', 'xml', '.j2.html',]),
        )
        env.filters['markdown'] = markdown_it.MarkdownIt().render

    if args.index:
        template = env.get_template('index.j2.html')
        print(f'Writing index to {args.index}', file=sys.stderr)
        index = template.render(
            calendars=calendars,
            timezones=timezones,
            timestamp=timestamp,
            git_hash=git_hash,
            edit_link=args.edit_link,
            config=config,
            )
        shutil.copy(TEMPLATE_DIR/'style.css', Path(args.index).parent/'style.css')
        open(args.index, 'w').write(index)

    if args.html_body:
        template = env.get_template('body.j2.html')
        print(f'Writing HTML to {args.html_body}', file=sys.stderr)
        with open(args.html_body, 'w') as f:
            html = template.render(
                calendars=calendars,
                timezones=timezones,
                timestamp=timestamp,
                git_hash=git_hash,
                edit_link=args.edit_link,
                config=config,
                )
            f.write(html)


if __name__ == "__main__":
    main(sys.argv[1:])
