import argparse
import os
import subprocess
import sys
import time

import jinja2
import yaml



def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('inputs', nargs='+', help="input files")
    parser.add_argument('--output', '-o', help="output directory", type=str)
    parser.add_argument('--index', '-i', help="output index file", type=str)
    parser.add_argument('--yaml2ics', help="yaml2ics path", type=str, default='yaml2ics')
    parser.add_argument('--timezone', action='append', help="zoneinfo timezone names", type=str, default=[])
    args = parser.parse_args(argv)

    calendars = [ ]
    timezones = [ ]
    for timezone in args.timezone:
        timezones.append({'tz': timezone, 'tzslug': timezone.replace('/', '-')})

    for f in args.inputs:
        calendar = { }
        calendar['data'] = yaml.safe_load(open(f))
        calendar['fbase'] = fbase = os.path.splitext(os.path.basename(f))[0]
        calendar['fics'] = fics = fbase + '.ics'
        cmd = f'{args.yaml2ics} {f} > {args.output}/{fics}'
        print(cmd)
        subprocess.run(cmd, shell=True, check=True)
        calendars.append(calendar)
        for tzdata in timezones:
            cmd = fr'TZ={tzdata["tz"]} mutt-ics out/{fics} | sed "s/^Subject:/\n\n----------\nSubject:/" > out/{fics}.{tzdata["tzslug"]}.txt'
            print(cmd)
            os.system(cmd)

    if args.index:
        timestamp = subprocess.check_output('date', encoding='utf8').strip() # subprocess to get timezone
        git_hash = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], encoding='utf8').strip()


        env = jinja2.Environment(
            #loader=PackageLoader('yourapplication', 'templates'),
            loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
            autoescape=jinja2.select_autoescape(['html', 'xml'])
        )
        template = env.get_template('index.html.j2')
        print(f'Writing index to {args.index}')
        index = template.render(
            calendars=calendars,
            timezones=timezones,
            timestamp=timestamp,
            git_hash=git_hash,
            )
        open(args.index, 'w').write(index)



if __name__ == "__main__":
    main(sys.argv[1:])
