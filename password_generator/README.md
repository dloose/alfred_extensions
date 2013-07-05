Password Generator
==================

An Alfred workflow that generates several long but memorable passwords based on the excellent [XKCD strip](http://xkcd.com/936/).

Download from https://dl.dropboxusercontent.com/u/30180245/Alfred/Password%20Generator.alfredworkflow

Usage
-----

Type `pw` in the Alfred window to generate 5 long, fairly random passwords. You can copy your favorite to the clipboard by highlighting it and pressing Enter. If you press Cmd+Enter, the password will be copied to the clipboard *and* written to the active window.

The workflow will generate passwords in the system's default language if that language is English, French, or Spanish. It falls back on English as a last resort, but you can force it to use one of the 3 listed by typing the 2 letter abbreviation after `pw`. For example:

* `pw en` will force the workflow to use English
* `pw fr` will force the workflow to use French
* `pw es` will force the workflow to use Spanish

Note: The workflow takes a few seconds to generate some entropy in order to make it harder to guess which words it will select.

Credit
======

All credit goes to Randall Munroe, Jeff Preshing, and Jinn Lynn. Please blame them if something goes horribly wrong (kidding!)

The concept comes from Mr. Munroe's excellent web comic, XKCD. For an explanation of why you'd want to use these passwords instead of randomly-generated gobbledegook, see http://xkcd.com/936/

The code is a poorly-ported Python version of Mr. Preshing's original JavaScript on http://passphra.se. The original is available from http://passphra.se/passphrase.js.php?language=en licensed under a modified version of the BSD license. See the included pw_gen.py file for more details.

I borrowed Jinn Lynn's Python module for Alfred integration. Visit him at http://jeeker.net. I couldn't find a direct link to his Alfred module, but it's included in this bundle (obviously). The code is licensed under the MIT license. See http://opensource.org/licenses/MIT for more details.