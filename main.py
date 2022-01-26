from keep_alive import keep_alive
import discord
import os
import random
import time
import threading
import asyncio
import requests
import re

TOKEN = os.getenv("TOKEN")
SU = [827078677794783244, 424188671332319233]
prefix = "!"
client = discord.Client()
whitelist = []

def wait():
  time.sleep(0.09)

async def status():
  while True:
    await client.change_presence(activity=discord.Game(name=prefix+f"help dans {len(client.guilds)} serveurs"))
    time.sleep(30)
    await client.change_presence(activity=discord.Game(name="bit.ly/feurbot"))
    time.sleep(15)
    await client.change_presence(activity=discord.Game(name="made by elio27#6369"))
    time.sleep(10)

status_loop = threading.Thread(target=asyncio.run, args=(status(),))

@client.event
async def on_ready():
  print("Quoi-Feur bot ready !")
  whitelist = open("wl.txt",'r').read().splitlines()
  status_loop.start()


@client.event
async def on_message(message):

  if message.content.startswith("!bugreport "):
    data={"content" : message.content.replace("!bugreport ",""),"username" : str(message.author),"avatar_url": str(message.author.avatar_url)}
    requests.post("https://discord.com/api/webhooks/885962295803535360/ijvM_BzqBONCwh5VF5FVhxHXsvfKIidUEroD6yzxNSBfTA96axG5iDytGUz-hP7L6byk",json=data)
    await message.reply("Merci de votre retour !", mention_author=False)
    wait()


  if message.content.startswith(prefix + "help"):
    embed = discord.Embed(title="FeurBot - Page d'aide", colour=discord.Colour(0x87ff14), description="Bienvenue sur la page d'aide du FeurBot, n'hésite pas à la consulter au moindre doute !")
    embed.set_footer(text="Dev by @elio27#6369", icon_url="https://cdn.discordapp.com/avatars/424188671332319233/860d76f27b550e0a016c2a4cb5a8007b.png")
    embed.add_field(name=f"{prefix}help", value="Retourne la page d'aide que vous êtes en train de lire.")
    embed.add_field(name=f"{prefix}suggest", value="Suivie d'une suggestion au format ```quoi:feur```Cette commande envoie aux devs votre suggestions, qui choisiront de l'ajouter ou non.")
    embed.add_field(name=f"{prefix}bugreport", value="Suivie d'un constat de problème, cette commande envoie aux devs votre problème, et feront de leur mieux pour résoudre ce problème.")
    embed.add_field(name=f"{prefix}disable", value="Réservée aux personnes possédant le rôle d'administrateur sur le serveur, cette commande permet de désactiver le FeurBot dans le salon dans lequel elle est utilisée.")
    embed.add_field(name=f"{prefix}enable", value="Réservée aux personnes possédant le rôle d'administrateur sur le serveur, cette commande permet de réactiver le FeurBot dans le salon dans lequel elle est utilisée.")
    embed.add_field(name="Comment inviter le FeurBot ?", value="C'est simple ! Il suffit de cliquer sur le lien ci-dessous :\nhttps://bit.ly/feurbot")

    await message.reply(embed=embed, mention_author=False)
    wait()


  if message.content.startswith(prefix+"suggest "):
    content = message.content.replace(prefix+"suggest ","")
    with open("sugg.txt",'r+') as f:
      if not ":" in content:
        await message.reply("Déso frérot, format invalide")
      else:

        if not "\n"+content in f.read():

          f.write(f.read()+"\n"+content)
          await message.reply("Merci bg !")
        else:
            await message.reply("Déso poto, c'est déjà dans la liste.")
    wait()

  if message.author!=client.user and str(message.channel.id) not in whitelist:
    with open("list.txt",'r') as f:

      d={}
      for i in f.read().split("\n"):
        c=i.split(":")
        d[c[0]]=c[1]
        

    content=message.content.lower()
    content=''.join(filter(lambda w : str.isalnum(w) or w==' ',content))
    for k in d.keys():

      if content.endswith(" "+k) or content==k or content==k+" " or content.endswith(" "+k+" "):
        rep=random.choice(d[k].split("|"))
        await message.reply(rep, mention_author=False)
        break


  if message.content==prefix+"sview":
    pasmal="" 
    v=0
    with open("sugg.txt",'r') as f:
      jesouffre=f.read().split("\n")
      for i in jesouffre:
        if not i in open("list.txt",'r').read():
          v+=1
          pasmal += str(v)+ " " + i + '\n'

      embed = discord.Embed(colour=discord.Colour(0x87ff14))
      if pasmal:
        embed.add_field(name="Suggestions", value=f"```{pasmal}```")
      else:
        embed.add_field(name="Suggestions", value=f"Aucune suggestion !")

      await message.reply(embed=embed, mention_author=False)
    wait()

  if message.content.startswith(prefix+"sclear") and message.author.id in SU:
    with open("sugg.txt",'w') as f:
      f.write(open("list.txt",'r').read())
      await message.reply("C'est bon wati-bg !",mention_author=False)
    wait()

  if message.content.startswith(prefix+"saccept") and message.author.id in SU:
    req=int(message.content.replace(prefix+"saccept ",""))
    v=0
    with open("sugg.txt",'r+') as f:
      jesouffre=f.read().split("\n")
      for i in jesouffre:
        with open("list.txt",'r+') as j:
          if not i in j.read():
            v+=1
            if v==req:
              do=False
              for denis in jesouffre:
                if denis.startswith(i.split(':')[0]): do=True
              if do:
                for line in jesouffre:
                  if line.startswith(i.split(':')[0]):
                    j.write("\n".join(jesouffre).replace(line, line+"|"+i.split(':')[1]))
                    f.write(f.read().replace(i,""))
              else:
                j.write(j.read()+"\n"+i)
              await message.reply("C'est bon !", mention_author=False)
    wait()

  if message.content==prefix+"boblennon" and message.author.id in SU:
    m=message
    for line in open("pyrobarbare.txt",'r').read().split('\n'):
      m = await m.reply(line, mention_author=False)
      time.sleep(1.5)
    wait()

  if message.content.lower().endswith("uwu") or message.content.endswith("^^") or message.content.endswith(":3"):
    await message.add_reaction("🖕")


  if message.content.startswith("!disable") and (message.author.guild_permissions.administrator or message.author in SU):
    ex="(?<=<#).*(?=>)"
    with open("wl.txt",'w') as f:
      try:
        chan = re.findall(ex, message.content)[0]
        client.get_channel(chan)
        whitelist.append(str(chan))
        f.write("\n".join(whitelist))
        await message.reply("C'est bon bg !")
      except:
        whitelist.append(str(message.channel.id))
        f.write("\n".join(whitelist))
        await message.reply("C'est bon bg !")

  if message.content.startswith("!enable") and (message.author.guild_permissions.administrator or message.author in SU):
    ex="(?<=<#).*(?=>)"
    with open("wl.txt",'w') as f:
      try:
        chan = re.findall(ex, message.content)[0]
        client.get_channel(chan)
        whitelist.remove(str(chan))
        f.write("\n".join(whitelist))
        await message.reply("C'est bon bg !")
      except:
        whitelist.remove(str(message.channel.id))
        f.write("\n".join(whitelist))
        await message.reply("C'est bon bg !")


keep_alive()
client.run(TOKEN)
