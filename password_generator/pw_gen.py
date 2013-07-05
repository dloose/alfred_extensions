#!/usr/bin/python
#-------------------------------------------------------------------
# Copyright (c) 2011 Jeff Preshing
# http://passphra.se/
# All rights reserved.
#
# Some parts based on http://www.mytsoftware.com/dailyproject/PassGen/entropy.js, copyright 2003 David Finch.
#
# Released under the Modified BSD License:
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the <organization> nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------

import argparse
import sys

import subprocess
import multiprocessing as mult
from multiprocessing.pool import ThreadPool

# used for entropy generation, which isn't as good as Preshing's, but oh well.
import hashlib, platform, os, time, random

import alfred


def xkcd_pw_gen_read_words(locale):

    local_words_file = "words/%s.txt" % ( locale )
    default_words_file = "words/en.txt"
    words_file = local_words_file if os.path.isfile( local_words_file ) else default_words_file

    with open( words_file ) as f:
        return [ word.rstrip( '\n' ).decode( 'utf-8' ) for word in f.readlines() ]


# Get some entropy from the system clock:
def xkcd_pw_gen_time_ent():
    d = int( time.time() )
    i = 0
    while d == int( time.time() ):
        i += 1 # Measure iterations until next tick
    return str( d ) + str( i )


# Return a pseudorandom array of four 32-bit integers:
def xkcd_pw_gen_create_hash(hashFn, ent1, ent2):
    # A SHA-1 hash generated on the server which is unique for each visit:
    xkcd_pw_gen_server_hash = hashFn( " ".join( platform.uname() ) + str( time.time() ) ).hexdigest()

    # Entropy string built in a manner inspired by David Finch:
    entropy = xkcd_pw_gen_server_hash + ent1
    entropy += ','.join( os.environ.keys() + os.environ.values() ) + str( random.random() ) + str( random.random() )
    entropy += ent2

    # Hash and convert to 32-bit integers:
    hexString = hashFn( entropy ).hexdigest()
    result = [ int( hexString[i:i+8], 16 ) for i in range( 0, 32 ) ]
    return result

def xkcd_pw_gen_create_index(words, num):
    jsRandom = int( random.random() * 0x100000000 )
    index = ((jsRandom ^ num) + 0x100000000) % len( words )
    return index

# Generate a new passphrase and update the document:
def xkcd_pw_gen_generate(words, hashFn, ent1, ent2):
    hash = xkcd_pw_gen_create_hash( hashFn, ent1, ent2 )
    choices = [ words[xkcd_pw_gen_create_index(words, hash[w])] for w in range( 0, 4 ) ]
    return " ".join( choices )

def xkcd_pw_gen_main_mt(words, hashFn, numThreads, numPasswords, ent1, ent2):
    pool = ThreadPool( processes=numThreads )
    return pool.map( lambda x: xkcd_pw_gen_generate( words, hashFn, ent1, ent2 ), range( 0, numPasswords ) )

def xkcd_pw_gen_main_st(words, hashFn, numPasswords, ent1, ent2):
    return [ xkcd_pw_gen_generate( words, hashFn, ent1, ent2 ) for i in range( 0, numPasswords) ]

def xkcd_pw_gen_write_feedback(locale, pws):
    feedback = alfred.Feedback()
    for pw in pws:
        feedback.addItem( title = pw, arg = pw )
    feedback.output()

if __name__ == '__main__':
    default_locale = subprocess.check_output( 'defaults read .GlobalPreferences AppleLanguages | tr -d [:space:] | cut -c 2-3', shell=True ).rstrip( '\n' )

    parser = argparse.ArgumentParser( description='Generates strong passwords based on the concept from http://xkcd.com/936/ and code from http://passphra.se' )
    parser.add_argument( '--hash', '-H',
         type    = str,
         default = "SHA1",
         choices = [ "SHA1", "SHA224", "SHA384", "SHA512", "MD5" ],
         metavar = "hash_function",
         help    = 'The name of the hash function to use for entropy generation. The following functions are supported: "SHA1", "SHA224", "SHA384", "SHA512", and "MD5"'
         )
    parser.add_argument( '--num-passwords', '-p',
         type    = int,
         default = 10,
         metavar = "num_passwords",
         help    = 'The number of passwords to generate.'
         )
    parser.add_argument( '--num-threads', '-t',
         type    = int,
         default = 1,
         metavar = "num_threads",
         help    = 'The number of threads to use.'
         )
    parser.add_argument( '--output-for-alfred', '-a',
         action  = 'store_const',
         const   = True,
         default = False,
         help    = 'Write the passwords as XML for Alfred. If this isn\'t present, the passwords are written 1 per line.'
         )
    parser.add_argument( '--locale', '-l',
         type    = str,
         nargs   = '?',
         default = default_locale,
         help    = 'Override the system locale. The system locale is used by default'
         )

    args = parser.parse_args()

    hashFns = {
        'SHA1'  : hashlib.sha1,
        'SHA224': hashlib.sha224,
        'SHA384': hashlib.sha384,
        'SHA512': hashlib.sha512,
        'MD5'   : hashlib.md5
    }

    ent1 = xkcd_pw_gen_time_ent()
    ent2 = xkcd_pw_gen_time_ent()

    words = xkcd_pw_gen_read_words( args.locale )

    if args.num_threads == 1:
        mainFn = lambda x: xkcd_pw_gen_main_st( words, hashFns[args.hash], x, ent1, ent2 )
    else:
        mainFn = lambda x: xkcd_pw_gen_main_mt( words, hashFns[args.hash], args.num_threads, x, ent1, ent2 )

    pws = mainFn( args.num_passwords )

    if args.output_for_alfred:
        xkcd_pw_gen_write_feedback( args.locale, pws )
    else:
        print "\n".join( pws )