from espn_api.football import League
from tabulate import tabulate
from dotenv import load_dotenv
import os, discord

currWeek = 8
def calculateLuck():
	league = League(league_id=1667721, year=2021)

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
GUILD = os.getenv('DISCORD_GUILD')

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
	channel = client.get_channel(904773474957033486)
	await channel.send(f"Here's the Luckiness Differential through Week {currWeek-1}:\n\n`" + calculateLuck() + "`\n*** Positive is luckier, negative is unluckier!")
	exit(0)

client.run(TOKEN)
 
