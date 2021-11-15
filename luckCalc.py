from espn_api.football import League
from tabulate import tabulate
from dotenv import load_dotenv
from datetime import date
import os, discord

today = date.today()
currDate = date(today.year,today.month,today.day)
startDate = date(2021,9,13)
currWeek = ((currDate-startDate).days)//7+2
currYear = 2021

def calculateLuck():
	league = League(league_id=1667721, year=currYear, espn_s2='AECIpIF9Pcz1tcX4djuq3%2F0wTXHA5mQY8jeJ%2BER6Ef28kErjnPgyeN4XLfzMzlvko5%2F%2FAjyH8BxnysrETw%2FWOwJELD6KKMM9MFXjvlSlL5CjZAkDyp6W9aED%2BNRwYGHXsDFT%2B%2BXjKL0RbMRcnpF8tc5EERHO%2Br1zMzLxwsf2XNw1lFdX1qrx4Bg2ok10ta4oDjNq67supQl51iAFYCSXtnn5I9TUMNuOwJFeCqQRwvFKKf%2F6OLWt20UQX2mxFnVsmTSFOtfGLNsqGLGHJN51SANeHS6waf58c%2Fn61hAHteP5oQ%3D%3D', swid='{9CDAE063-F1E8-4260-B2D9-F457E5214403}')

	actualWins = {}
	expectedWins = {}
	for team in league.teams:
		actualWins[team.team_name] = team.wins
		expectedWins[team.team_name] = 0
		
	scores = {}
	for x in range(1,currWeek):
		for matchup in league.scoreboard(x):
			scores[matchup.home_team.team_name] = matchup.home_score
			scores[matchup.away_team.team_name] = matchup.away_score
		sortedScores = dict(sorted(scores.items(), key = lambda x: x[1]))
		
		keysList = list(sortedScores)
		for y in range(len(sortedScores)):
			expectedWins[keysList[y]] = expectedWins[keysList[y]] + y
		
		scores = {}

	output = []
	for team in league.teams:
		output.append([team.team_name,actualWins[team.team_name]/((currWeek-1)),expectedWins[team.team_name]/((currWeek-1)*9),actualWins[team.team_name]/((currWeek-1)) - expectedWins[team.team_name]/((currWeek-1)*9)])

	sortedOutput = sorted(output, key=lambda x: x[3], reverse=True)
	return tabulate(sortedOutput, headers=['Team', 'Act.', 'Exp.', 'Luck'], tablefmt="rst", stralign="left", floatfmt=".3f")

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD1') # My server
#GUILD = os.getenv('DISCORD_GUILD2') # Wallerstein

client = discord.Client()

@client.event
async def on_ready():
	for guild in client.guilds:
		if guild.name == GUILD:
			break

	print(
		f'{client.user} is connected to the following guild:\n'
		f'{guild.name}(id: {guild.id})'
	)
	channel = client.get_channel(904773474957033486) # My server
	#channel = client.get_channel(904492778636066890) # Wallerstein
	await channel.send(f"Here's the Luckiness Differential through Week {currWeek-1}:\n\n`" + calculateLuck() + "`\n*** Positive is luckier, negative is unluckier!")
	exit(0)

client.run(TOKEN)
 
