# -*- coding: utf-8 -*-
"""
@@@  @@@  @@@@@@   @@@@@@@   @@@@@@@@  @@@@@@@@@@    @@@@@@
@@@  @@@  @@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@@@@  @@@@@@@@
@@!  @@@      @@@  @@!  @@@  @@!       @@! @@! @@!  @@!  @@@
!@!  @!@      @!@  !@!  @!@  !@!       !@! !@! !@!  !@!  @!@
@!@!@!@!  @!@!!@   @!@  !@!  @!!!:!    @!! !!@ @!@  @!@!@!@!
!!!@!!!!  !!@!@!   !@!  !!!  !!!!!:    !@!   ! !@!  !!!@!!!!
!!:  !!!      !!:  !!:  !!!  !!:       !!:     !!:  !!:  !!!
:!:  !:!      :!:  :!:  !:!  :!:       :!:     :!:  :!:  !:!
::   :::  :: ::::   :::: ::   :: ::::  :::     ::   ::   :::
 :   : :   : : :   :: :  :   : :: ::    :      :     :   : :



Copyright 2021 by Henrique Duarte Moura.
All rights reserved.

This file is part of the simple python header,
and is released under the "MIT License Agreement".
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

Please see the LICENSE file that should have been included as part of this package.
"""
from pyfiglet import Figlet
import datetime
import argparse

parser = argparse.ArgumentParser("Simple header generator")
parser.add_argument('--name', default="Henrique Duarte Moura", type=str)
parser.add_argument('--email', default="Henrique.DuarteMoura@imec.be", type=str)
parser.add_argument('--project', default="the simple test project", type=str)
parser.add_argument('--year', default=datetime.datetime.now().date().year, type=int)
parser.add_argument('--figlet', default="h3dema", type=str)
parser.add_argument('--font', default="poison", type=str)

parser.add_argument('--version', default="0.1.0", type=str)

parser.add_argument('--private', action='store_const', dest="kind_licence", const="private")
parser.add_argument('--public', action='store_const', dest="kind_licence", const="public")
parser.set_defaults(kind_licence="private")


parser.add_argument('--company', default="imec", type=str)

args = parser.parse_args()

f = Figlet(font=args.font)
name_fig = f.renderText(args.figlet)

licence = f'all IP rights are owned by {args.company}' if args.kind_licence == "private" else 'is released under the "MIT License Agreement"'

header = f"""# -*- coding: utf-8 -*-
\"\"\"
{name_fig}
Copyright {args.year} by {args.name if args.kind_licence == "public" else args.company}.
All rights reserved.

This file is part of {args.project},
and {licence}.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

Please see the LICENSE file that should have been included as part of this package.
\"\"\"
__maintainer__ = "{args.name}"
__email__ = "{args.email}"
__version__ = "{args.version}"
"""

print(header)
