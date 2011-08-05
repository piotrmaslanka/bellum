Copyright (c) 2009-2011 Piotr Maślanka <piotr.maslanka at henrietta dot com.pl> and Michał Żak <turimaren at gmail>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero Public License for more details.

You should have received a copy of the GNU Affero Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

All files in this package are licensed under GNU Affero Public License,
unless stated otherwise in given file's header.

Special thanks to:
	- Konrad Bachórz
	- Piotr Maszlanka
	- Michał Tokarczyk
	
Requires:
	Django:
		1.2+
	Mako:
		0.2+
	Django-mako:
		0.1+
        simplejson-esque JSON support

                !!!!
                When Python doesn't have the default json module, and does only with simplejson, a module should be created in PYTHONPATH:
                it has to have content:

                        from simplejson import *
                !!!

Suite additionally requires PIL and aggdraw for planet preview generation.
Please ensure that PIL supports PNG/GIF/JPEG!

Suite doesn't use aggdraw to draw fonts, as some fuckhead compiled the binaries w/o freetype and I didn't have a compiler at hand. Now
shit is drawn using ImageFont and ImageDraw from PIL.

Sizes of main display window, as far as content is considered: 894px width

=== Where can I expect configurations?

bellum.settings
bellum.stats.__init__
bellum.common.utils.mail	


=== How do I install this?

First, install Django schemas by python manage.py syncdb. Then run a Django shell. Import suite and run it's commands:

generate_universe()
expand_planetview_icons()
expand_sectors()

and voila!