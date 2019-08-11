#!/usr/bin/python3
import numpy as np
import discord
import os
from discord.ext import commands

bot = commands.Bot(command_prefix="?")

def make_pairs(corpus):
    for i in range(len(corpus)-1):
        yield (corpus[i], corpus[i+1])

def markovgen(corpus):
    pairs = make_pairs(corpus)

    word_dict = {}
    for word_1, word_2 in pairs:
        if word_1 in word_dict.keys():
            word_dict[word_1].append(word_2)
        else:
            word_dict[word_1] = [word_2]

    firstwords = []
    for w in corpus:
        if not w == 'END':
            firstwords.append(w)

    first_word = np.random.choice(firstwords)
    chain = [first_word]

    while True:
        choice = np.random.choice(word_dict[chain[-1]])
        if choice == 'END':
            break
        if len(chain) > 1995:
            break
        chain.append(choice)

    return ' '.join(chain)

@bot.event
async def on_ready():
    print("Bot running")

    activity = discord.Activity(name="bruh", type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)

@bot.command()
async def markov(ctx, arg):
    print(ctx.message.author.name + ' requests markov of ' + arg)
    user = ''
    corpus = []
    async for message in ctx.message.channel.history(limit=99999):
        if arg.lower() in message.author.name.lower() and not '?markov' in message.content:
            for e in message.embeds:
                corpus.append(e.url)
            user = message.author.name
            corpus.extend(message.content.split())
            corpus.append('END')
    print('selected ' + user)
    if len(corpus) > 1:
        res = markovgen(corpus)
        print(res)
        await ctx.send(res)
    else:
        print('user doesnt exist or hasnt send messages')
        await ctx.send('user doesnt exist or hasnt send messages')
    

if __name__ == "__main__":
    bot.run(os.environ['TOKEN'])
    