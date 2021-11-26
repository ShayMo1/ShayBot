import os
import random
import sys
import getopt
import re

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
verbose = False

argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv,"hv",["help","verbose"])
except getopt.GetoptError:
    print('Error')
    sys.exit(2)
for opt, arg in opts:
    if opt in ('-h', '--help'):
        print('nothing yet')
        sys.exit(1)
    elif opt in ("-v", "--verbose"):
        verbose = True

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('Shaybot reporting for duty!')

@bot.command(name='sb')
async def sb(ctx, *, arg):
    args = arg.split()
    if verbose:
        print(f'Received command {args[0]}')

    if args[0].lower() == 'roll':
        if verbose:
            print('  We rollin''')
        results = ''
        error = ''
        for die in args:
            if die.lower() == 'roll':
                continue

            if re.search(r'^\d+d\d+$', die) is None:
                error = error + die + ' '
                continue

            die_vals = die.lower().split('d')
            quantity = int(die_vals[0])
            faces = int(die_vals[1])
            if verbose:
                print(f'  {quantity}:{faces}')
            die_results = f'{die}='
            total = 0
            for die_num in range(0, quantity):
                roll_val = random.randrange(1, faces, 1)
                total = total + roll_val
                die_results = die_results + str(roll_val) + ','
                if verbose:
                    print(f'  die #{die_num}={die_results}')
            results = results + die_results[:-1] + f'={total}\n'
        if verbose:
            print(f'  final result: {results}\nerrors: {error}')
        if len(error) > 0:
            results = results + f'\nI didn\'t recognize these as valid dice.\n{error}'
        await ctx.send(results)

    if args[0].lower() == 'help':
        help_text =  'I recognize these commands:\n'
        help_text += '**help**: Show this message.\n'
        help_text += '**roll**: Roll dice. Enter in the standard format (1d4 2d6 etc).'
        await ctx.send(help_text)

bot.run(TOKEN)
