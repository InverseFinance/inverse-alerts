from  discord_webhook import DiscordWebhook, DiscordEmbed

webhook = DiscordWebhook(url='https://discord.com/api/webhooks/966024633113509889/pf-pISCGQe3c0aRgm8y2NPcvNHULUC-vHcWOnHP1VjmzNgmKSGYrve8AJGHH3a3JPiFI')

embed = DiscordEmbed(title='Your Title', description='Lorem ipsum dolor sit', color='03b2f8')

# set author
embed.set_author(name='Author Name', url='author url', icon_url='author icon url')
embed = DiscordEmbed.set_image("https://dune.com/embeds/601327/1123320/73b0c170-f50e-4964-a436-d358b4357b28")



# add fields to embed
embed.add_embed_field(name='Field 1', value='Lorem ipsum')
embed.add_embed_field(name='Field 2', value='dolor sit')

# add embed object to webhook
webhook.add_embed(embed)

response = webhook.execute()