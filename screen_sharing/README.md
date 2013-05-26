Password Generator
==================

Starts a screen sharing session with a remote host. I try to load the hosts you've connected to in the past from `~/Library/Application Support/Screen Sharing`. If the argument doesn't match one of those, I just slap a `vnc://` in front of it. In either case, I start the session by running `/usr/bin/open {query}` because it worked in both cases. That could potentially lead to some unexpected effects (like, opening random files maybe?). I tried to use this maliciously and I didn't have any luck. So, good job Andrew & Vera!

Download from [https://dl.dropboxusercontent.com/u/30180245/Alfred/Start%20Screen%20Sharing.alfredworkflow]()

Credit
======

I borrowed Jinn Lynn's Python module for Alfred integration. Visit him at [http://jeeker.net](). I couldn't find a direct link to his Alfred module, but it's included in this bundle (obviously). The code is licensed under the MIT license. See [http://opensource.org/licenses/MIT]() for more details.