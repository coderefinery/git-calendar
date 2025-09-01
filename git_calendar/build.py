import argparse
import os
from os.path import dirname, join
from pathlib import Path
import shutil
import subprocess
import sys
import time

from dateutil.tz import gettz
import jinja2
import markdown_it
import yaml

from . import yaml2ics

TEMPLATE_DIR = Path(__file__).parent/'templates'

def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('inputs', nargs='+', help="input files", type=Path)
    parser.add_argument('output', help="output directory", type=str)
    parser.add_argument('--index', '-i', help="output HTML index file", type=str)
    parser.add_argument('--html-body', '-b', help="output HTML body to be included in other pages", type=str)
    parser.add_argument('--timezone', action='append', help="zoneinfo timezone names", type=str, default=[])
    parser.add_argument('--edit-link', help='Link to edit, will be added to the generated page.')
    parser.add_argument('--base-url', help='Base url to append in front of all .ics files '
                        '(include trailing slash).',
                        default='')
    parser.add_argument('--jinja-template-dir', help='Jinja template dir.  See source for a starting point',
                        action='append', default=[])
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
        print(f"Writing {f} --> {output}")
        open(output, 'w').write(calendar.serialize())

        # Generate the rendered views in different timezones
        for tzdata in timezones:
            # text file dump:, may be useful for some people.
            # This is clearly a hack, calling the shell commands.  This should
            # be improved later.
            print(f"Writing {f} (in {tzdata['tz']}) --> out/{fics}.{tzdata['tzslug']}.txt")
            subprocess.check_output(
                fr"TZ={tzdata['tz']} mutt-ics {args.output}/{fics}  | sed 's/^Subject:/\n\n----------\nSubject:/' > {args.output}/{fics}.{tzdata['tzslug']}.txt",
                shell=True)
            # Convert to an .ics file in different timezones.  This shouldn't
            # be needed, but it seems that Thunderbird doesn't convert
            # timezones so this is useful for it.
            calendarTZ = calendar.clone()
            calendarTZ.normalize(gettz(tzdata['tz']))

            output_tz_txt = join(args.output, fbase+'.'+tzdata['tzslug']+'.ics')
            print(f"Writing {f}[{tzdata['tz']}] --> {output_tz_txt}")
            open(output_tz_txt, 'w').write(calendarTZ.serialize())




    if args.index or args.html_body:
        timestamp = subprocess.check_output('date', encoding='utf8').strip() # subprocess to get timezone
        git_hash = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], encoding='utf8').strip()

        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(args.jinja_template_dir + [TEMPLATE_DIR]),
            autoescape=jinja2.select_autoescape(['html', 'xml', '.j2.html',]),
        )
        env.filters['markdown'] = markdown_it.MarkdownIt().render
        template_context = dict(
            calendars=calendars,
            timezones=timezones,
            timestamp=timestamp,
            git_hash=git_hash,
            edit_link=args.edit_link,
            config=config,
            )

    if args.index:
        index_file = join(args.output, args.index)
        print(f'Writing index to {index_file}', file=sys.stderr)
        index    = env.get_template('index.j2.html').render(template_context)
        stylecss = env.get_template('style.css').render(template_context)
        with open(index_file, 'w') as f_index, open(join(args.output, 'style.css'), 'w') as f_style:
            f_style.write(stylecss)
            f_index.write(index)

    if args.html_body:
        htmlbody_file = join(args.output, args.html_body)
        template = env.get_template('body.j2.html')
        print(f'Writing HTML to {htmlbody_file}', file=sys.stderr)
        with open(htmlbody_file, 'w') as f:
            html = template.render(template_context)
            f.write(html)


if __name__ == "__main__":
    main(sys.argv[1:])
