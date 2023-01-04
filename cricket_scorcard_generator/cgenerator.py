import math
from platform import python_version
from datetime import datetime
start_time = datetime.now()
#getting name of the player
def getPlayer(player):
	for person in allPlyrs:
		if player in person:
			return person

def makeScoreCard():
			#dictionary for the scoreboard 
			iningA = {'runs': 0, 'wickets': 0, 'balls': 0, 'batting': {player : {'runs': 0, 'balls': 0, '4s': 0, '6s': 0, 'status': ''} for player in pakPlyrs}, 'bowling': {player : {'runs': 0, 'balls': 0, 'maidens': 0, 'wickets': 0, 'nb': 0, 'wide': 0} for player in indPlyrs}, 'extras': {'byes': 0, 'nb': 0, 'lb': 0, 'wide': 0, 'pty': 0}, 'dnb': pakPlyrs.copy(), 'fow': [], 'powerplay': 0}
			iningB = {'runs': 0, 'wickets': 0, 'balls': 0, 'batting': {player : {'runs': 0, 'balls': 0, '4s': 0, '6s': 0, 'status': ''} for player in indPlyrs}, 'bowling': {player : {'runs': 0, 'balls': 0, 'maidens': 0, 'wickets': 0, 'nb': 0, 'wide': 0} for player in pakPlyrs}, 'extras': {'byes': 0, 'nb': 0, 'lb': 0, 'wide': 0, 'pty': 0}, 'dnb': indPlyrs.copy(), 'fow': [], 'powerplay': 0}
			#startining is a variable = run the bowler gave just before delivering the over(for finding the maiden over)
			startining=-1
			#Reading the innings text file and printing output text file for displaying the scoreboard
			with open('pak_inns1.txt', 'r') as pak_inns, open('india_inns2.txt', 'r') as ind_inns, open('output.txt','w') as output:
				#Reading all the lines in the textfiles
				totLines1 = pak_inns.readlines()
				totLines2 = ind_inns.readlines()
				#Count to find who is batsman
				count=0
				print("", file=output)
				#loops through both the country's inns
				for inns, lines in zip([iningA, iningB], [totLines1, totLines2]):
					#lines of the comment section for getting the information	
					for info in [line for line in lines if line.strip()]:
						
						batter = getPlayer(info.split(",")[0].split(" ", 1)[1].split("to")[1].strip())
						bowler = getPlayer(info.split(",")[0].split(" ", 1)[1].split("to")[0].strip())
						res = info.split(",")[1].strip()
						over=info.split(",")[0].split(" ", 1)[0].strip()
						# as a bowler starts his over, his runs stored in a variable, it is used for finding maiden over
						if inns['bowling'][bowler]['balls']%6==0:
							startining=inns['bowling'][bowler]['runs']
						# runs for the powerplay updated here
						if(inns['balls']==36):
							inns['powerplay'] = inns['runs']
						# older player is removed from the did not bat list
						if batter in inns['dnb']:
							inns['dnb'].remove(batter)
						# updated scoreboard for different kind of balls and runs
						if res == "no run":
							inns['balls']+=1
							inns['batting'][batter]['balls']+=1
							inns['batting'][batter]['status']="not out"
							inns['bowling'][bowler]['balls']+=1
						if res == "no ball":
							inns['runs']+=1
							inns['bowling'][bowler]['nb']+=1
							inns['bowling'][bowler]['runs']+=1
							inns['batting'][batter]['status']="not out"
							inns['extras']['nb'] += 1
						elif res == "wide":
							inns['runs']+=1
							inns['extras']['wide'] += 1
							inns['batting'][batter]['status']="not out"
							inns['bowling'][bowler]['runs'] += 1
							inns['bowling'][bowler]['wide'] += 1
						elif res == '2 wides':
							inns['runs'] += 2
							inns['extras']['wide'] += 2
							inns['bowling'][bowler]['runs'] += 2
							inns['batting'][batter]['status']="not out"
							inns['bowling'][bowler]['wide'] += 2
						elif res == '3 wides':
							inns['runs'] += 3
							inns['extras']['wide'] += 3
							inns['bowling'][bowler]['runs'] += 3
							inns['batting'][batter]['status']="not out"
							inns['bowling'][bowler]['wide'] += 3
						elif res == '4 wides':
							inns['runs'] += 4
							inns['extras']['wide'] += 4
							inns['bowling'][bowler]['runs'] += 4
							inns['batting'][batter]['status']="not out"
							inns['bowling'][bowler]['wide'] += 4
						elif res == '5 wides':
							inns['runs'] += 5
							inns['extras']['wide'] += 5
							inns['bowling'][bowler]['runs'] += 5
							inns['batting'][batter]['status']="not out"
							inns['bowling'][bowler]['wide'] += 5
						elif res == "1 run":
							inns['balls'] += 1
							inns['runs'] += 1
							inns['batting'][batter]['runs'] += 1
							inns['batting'][batter]['balls'] += 1
							inns['batting'][batter]['status']="not out"
							inns['bowling'][bowler]['runs'] += 1
							inns['bowling'][bowler]['balls'] += 1
						elif res == "2 runs":
							inns['balls'] += 1
							inns['runs'] += 2
							inns['batting'][batter]['runs'] += 2
							inns['batting'][batter]['balls'] += 1
							inns['batting'][batter]['status']="not out"
							inns['bowling'][bowler]['runs'] += 2
							inns['bowling'][bowler]['balls'] += 1
						elif res == "3 runs":
							inns['balls'] += 1
							inns['runs'] += 3
							inns['batting'][batter]['runs'] += 3
							inns['batting'][batter]['balls'] += 1
							inns['batting'][batter]['status']="not out"
							inns['bowling'][bowler]['runs'] += 3
							inns['bowling'][bowler]['balls'] += 1
						elif res == "FOUR":
							inns['balls'] += 1
							inns['runs'] += 4
							inns['batting'][batter]['runs'] += 4
							inns['batting'][batter]['balls'] += 1
							inns['batting'][batter]['status']="not out"
							inns['bowling'][bowler]['runs'] += 4
							inns['bowling'][bowler]['balls'] += 1
							inns['batting'][batter]['4s'] += 1
						elif res == "SIX":
							inns['balls'] += 1
							inns['runs'] += 6
							inns['batting'][batter]['runs'] += 6
							inns['batting'][batter]['balls'] += 1
							inns['batting'][batter]['status']="not out"
							inns['bowling'][bowler]['runs'] += 6
							inns['bowling'][bowler]['balls'] += 1
							inns['batting'][batter]['6s'] += 1
						elif res.split(" ")[0].strip() == "out":
							inns['balls'] += 1
							inns['wickets'] += 1	
							inns['batting'][batter]['balls'] += 1
							inns['bowling'][bowler]['wickets'] += 1
							inns['bowling'][bowler]['balls'] += 1
							inns['fow'].append(f"{inns['runs']}-{inns['wickets']} {batter}, {over}")
							if res.startswith('out Caught by'):
								inns['batting'][batter]['status'] = f"c {res.split('!!')[0].split('out Caught by', 1)[1].strip()} b {bowler}"
							elif res.startswith('out Bowled!!'):
								inns['batting'][batter]['status'] = f"b {bowler}"
							elif res.startswith('out Lbw!!'):
								inns['batting'][batter]['status'] = f"lbw b {bowler}"
						elif res == "byes" or res == "leg byes":
							inns['balls'] += 1
							inns['batting'][batter]['balls'] += 1
							inns['batting'][batter]['status']="not out"
							inns['bowling'][bowler]['balls'] += 1
							runs = info.split(",")[2].strip()
							if(runs == 'no run'):
								continue
							elif(runs == '1 run'):
								inns['runs'] += 1
								if res == "byes":
									inns['extras']['byes'] += 1
								else:
									inns['extras']['lb'] += 1
							elif(runs == '2 runs'):
								inns['runs'] += 2
								if res == "byes":
									inns['extras']['byes'] += 2
								else:
									inns['extras']['lb'] += 2
							elif(runs == '3 runs'):
								inns['runs'] += 3
								if res == "byes":
									inns['extras']['byes'] += 3
								else:
									inns['extras']['lb'] += 3
							elif(runs == 'FOUR'):
								inns['runs'] += 4
								if res == "byes":
									inns['extras']['byes'] += 4
								else:
									inns['extras']['lb'] += 4
						# if the bowler gets a maiden over
						if inns['bowling'][bowler]['balls']%6==0:
							if inns['bowling'][bowler]['runs']==startining:
								inns['bowling'][bowler]['maidens']+=1
					# code to display the scoreboard
					if count==0:
						print(f"{'Pakistan inns' : <50}{f'''{inns['runs']}-{inns['wickets']} ({over} Ov)''' : >90}", file=output)
						count+=1
					else:
						print(f"{'Indian inns' : <50}{f'''{inns['runs']}-{inns['wickets']} ({over} Ov)''' : >90}", file=output)
					print("", file=output)
					# details of all the batters
					for i in range(1):
						print(f"{'': <25}{'Batter' : <25}{'' : <50}{'R' : >8}{'B' : >8}{'4s' : >8}{'6s' : >8}{'SR' : >12}", file=output)
						for batsman, data in inns['batting'].items():
							if data['status'] != '':
								print(f"{'': <25}{batsman : <25}{data['status'] : <50}{data['runs'] : >8}{data['balls'] : >8}{data['4s'] : >8}{data['6s'] : >8}{round((data['runs']/data['balls'])*100, 2) : >12}", file=output)
						print("", file=output)
						print(f"{'': <25}{'Extras' : <50}{inns['extras']['wide'] : >44}", file=output)
						print(f"{'': <25}{'Total' : <50}{f'''{inns['runs']} ({inns['wickets']} wkts, {over} Ov)''' : >44}", file=output)
					# batters who did not bat
					if inns['dnb']:
						print(f"{'': <25}{'Did not Bat' : <50}{', '.join(inns['dnb']) : >44}", file=output)
					print("", file=output)
					# fall of wickets
					print(f"{'' :<25}""Fall of Wickets", file=output)
					wickets = ", ".join(inns['fow'])
					print(f"{'' :<25}{wickets : ^100}{'' :>25}", file=output)
					print("", file=output)
					#details of all the bowlers
					for i in range(1):
						print(f"{'': <25}{'Bowler' : <25}{'' : <50}{'O' : >7}{'M' : >10}{'R' : >8}{'W' : >8}{'NB' : >8}{'WD' : >8}{'ECO' : >12}", file=output)
						for bowler, data in inns['bowling'].items():
							if data['balls']:
								total_overs=data['balls']//6
								extra_balls=data['balls']%6
								overall_overs=str(total_overs)+'.'+str(extra_balls)
								print(f"{'': <25}{bowler : <25}{'' : <50}{overall_overs : >9}{data['maidens'] : >8}{data['runs'] : >8}{data['wickets'] : >8}{data['nb'] : >8}{data['wide'] : >8}{round(data['runs']/(total_overs+(extra_balls/6)),1) : >12}", file=output)
						print("", file=output)
					# Display the runs taken in powerplay
					print(f"{'': <25}{'Powerplays' : <15}{'Overs' : >15}{'Runs' : >15}", file=output)
					for i in range(1):	
						print(f"{'': <25}{'Mandatory' : <15}{'0.1-6' : >15}{inns['powerplay']: >15}", file=output)
						print("", file=output)



###Code

from platform import python_version
ver = python_version()

if ver == "3.8.10":
	print("Correct Version Installed")
else:
	print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

indPlyrs = ['Rohit Sharma (c)', 'KL Rahul', 'Virat Kohli', 'Suryakumar Yadav', 'Dinesh Karthik (w)', 'Hardik Pandya', 'Ravindra Jadeja', 'Bhuvneshwar Kumar', 'Avesh Khan', 'Yuzvendra Chahal', 'Arshdeep Singh']
pakPlyrs = ['Babar Azam (c)', 'Mohammad Rizwan (w)', 'Fakhar Zaman', 'Iftikhar Ahmed', 'Khushdil Shah', 'Asif Ali', 'Shadab Khan', 'Mohammad Nawaz', 'Naseem Shah', 'Haris Rauf', 'Shahnawaz Dahani']
allPlyrs = indPlyrs + pakPlyrs
makeScoreCard()
print("o/p file is ready :]")
#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
