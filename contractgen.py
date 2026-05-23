##!/usr/bin/env python3
# contractgen.py - mercenary contract generator for: # 
# BattleTech Hot Spots: Hinterlands #
# Written in Python3 #

# imports block begins #
import random					# need to roll random numbers a lot.
import getopt					# future-proofing for generating opposing contracts from existing one, generating missions, etc. May need to do some JSON handling to pass contracts to file and back.
import sys						# need to handle exits, may want to write to files at some point.
# imports block ends #

# main function begins #
def main(argv):
#	do stuff
	print("Generating new mercenary contract.")
	systemRoll = rollD6()
	contractLocation = getSystem(systemRoll)
	print("Location (Primary Terrain): " + contractLocation)	# TODO add primary terrain generation.
	employer = getEmployer()
	print("Employer: " + employer)
	contractMissionType = getContractType()
	print("Type of Action: " + contractMissionType[0] + "("+ contractMissionType[1] + ")")
	contractLength = getContractLength(contractMissionType)
	print("Length of Contract: " + str(contractLength) + " months")
	contractBasePay = getBasePay(employer, contractMissionType)
	print("Base Pay: " + contractBasePay)
	contractSupport = getSupportRate(employer, contractMissionType)
	print("Support: " + contractSupport)
	contractTransportation = getTransportRate(employer, contractMissionType)
	print("Transportation: " + contractTransportation)
	contractSalvage = getSalvageRights(employer, contractMissionType)
	print("contractSalvage: " + contractSalvage)
	contractCommand = getCommandRights(employer, contractMissionType)
	print("Command Rights: " + contractCommand)
	sys.exit(0)
#main function ends#

# simple function to roll a D6 #
def rollD6():
	return random.randint(1,6)
# rollD6 ends#

# function to determine system #
def getSystem(jumpsRoll):
	oneJumps = ["Zoetermeer", "Baker", "Leskovik", "Dompaire", "Devin", "Antares"]
	twoJumps = ["Babaeski", "Morges", "A Place", "Vulcan", "Parakoila", "Matteo"]
	threeJumps = ["Bountiful Harvest", "Colmar", "Koniz", "Twycross", "Waldorff", "Romulus"]
	fourJumps = ["New Exford", "Ballynure", "Zanderij", "Trell I", "Deia", "Great X"]
	fiveJumps = ["Santana", "Blumenort", "Kooken's Pleasure Pit", "Hot Springs", "Derf", "Timovichi"]
	sixJumps = ["Bluque", "Roadside", "Clermont", "Black Earth", "Golandrinas", "Sargasso"]
	systemRoll = rollD6() - 1
	match jumpsRoll:
		case 1:
			return oneJumps[systemRoll]
		case 2:
			return twoJumps[systemRoll]
		case 3:
			return threeJumps[systemRoll]
		case 4:
			return fourJumps[systemRoll]
		case 5:
			return fiveJumps[systemRoll]
		case 6:
			return sixJumps[systemRoll]
# getSystem ends #

# function to determine primary terrain #
#def getPrimaryTerrain(systemIn):
#	contractTerrain["Light Industrial","Urban","Use Primary","Roll on Primary"]
#	terrainTypes["Desert","Wetlands","Light Industrial","Hills","Wooded","Grasslands","Savannahs","Urban","Mountains","Alien"]
#	match systemIn:
	
# function to determine employer #
def getEmployer():
	employer = ""
	employerList = ["Civilian","Planetary Government","Mercenary Subcontract","Corporation","House","Noble (local)"]
	roll = rollD6() + rollD6()
	match roll:
		case 2:
			employer = employerList[0]	# Civilian
		case 3 | 10:
			employer = employerList[1]	# Planetery Government
		case 4 | 12:
			employer = employerList[2]	# Mercenaries
		case 5 | 9:
			employer = employerList[3]	# Corporation
		case 6 | 7 | 11:
			employer = employerList[4]	# House
		case 8:
			employer = employerList[5]	# Noble
	return employer
# getEmployer ends #

# function to generate the contract type #
def getContractType():
	contractType = ""
	contractSubType = ""
	contractMainType = ["Expedition", "Garrison", "Raid", "Invasion"]
	expeditionSubType = ["Standard Expedition", "Pirate Hunt", "Guerilla Operation"]
	garrisonSubType = ["Cadre Duty", "Standard Garrison"]
	roll = rollD6() + rollD6()
	match roll:
		case 2 | 3 | 4:
			contractType = contractMainType[0]
			secondRoll=rollD6()+rollD6()
			print("Roll is: ", roll)
			match secondRoll:
				case "9" | "10" | "11":
					contractSubType = expeditionSubType[1]
				case "12":
					contractSubType = expeditionSubType[2]
				case _:
					contractSubType = expeditionSubType[0]
		case 5 | 6:
			contractType = contractMainType[1]
			secondRoll=rollD6()+rollD6()
			match secondRoll:
				case "2" | "3" | "4" | "5":
					contractSubType = garrisonSubType[0]
				case _:
					contractSubType = garrisonSubType[1]
		case 7 | 8 | 9:
			contractType = contractMainType[2]
			contractSubType = "None"
		case 10 | 11 | 12:
			contractType = contractMainType[3]
			print("Contract type is: " + contractType)
			contractSubType = "None"
	return [contractType, contractSubType]
# getContractType ends#

# function to generate the opposing contract type #
def getOpposingContractType(contractTypeIn):
	roll = rollD6()
	match contractTypeIn:
		case "Expedition":
			match roll:
				case 9 | 10 | 11 | 12:
					return "Raid"
				case _:
					return "Garrison"
		case "Garrison":
			match roll:
				case 2 | 3 | 4:
					return "Expedition"
				case 9 | 10 | 11 | 12:
					return "Invasion"
				case _:
					return "Raid"
		case "Raid":
			match roll:
				case 8 | 9 | 10:
					return "Garrison"
				case 11:
					return "Raid"
				case 12:
					return "Invasion"
				case _:
					return "Expedition"
		case "Invasion":
			match roll:
				case 2 | 3 | 4:
					return "Expedition"
				case 9:
					return "Raid"
				case 10 | 11 | 12:
					return "Invasion"
				case _:
					return "Garrison"
# getOpposingContractType ends #

# function to determine contract length #
def getContractLength(typeIn):
	if typeIn == "Raid":
		duration = 3
		return duration
	else:
		duration = 6
		return duration
# getContractLength ends #

# function to determine base pay #
def getBasePay(employerType, missionIn):
	payStepList = ["50% (1)", 
				"55% (2)", 
				"60% (3)",
				"70% (4)",
				"80% (5)",
				"90% (6)",
				"100% (7)",
				"110% (8)",
				"120 (9)",
				"130% (10)",
				"150% (11)",
				"175% (12)",
				"200% (13)"]
	stepRolled = 0
	roll = rollD6() + rollD6()
	# generate the base random result #
	match roll:
		case 2 | 3:
			stepRolled = 2
		case 4 | 5:
			stepRolled = 3
		case 6 | 7:
			stepRolled = 4
		case 8 | 9:
			stepRolled = 5
		case 10 | 11:
			stepRolled = 6
		case 12:
			stepRolled = 7
	# add or remove steps for the employer type #
	match employerType:
		case "Civilian":
			stepRolled = stepRolled - 2
		case "Mercenary":
			stepRolled = stepRolled - 1
		case "House":
			stepRolled = stepRolled + 1
		case "Corporation":
			stepRolled = stepRolled + 2
	# do the same for the mission type #
	match missionIn:
		case "Expedition":
			stepRolled = stepRolled + 1
		case "Invasion":
			stepRolled = stepRolled + 2
	if stepRolled > 12:
		stepRolled = 12
	if stepRolled < 0:
		stepRolled = 0
	return payStepList[stepRolled]
	
# getBasePay ends #


# function to determine support #
def getSupportRate(employerType, missionIn):
	supportStepList = ["None (1)",
						"Straight/20% (2)", 
						"Straight/40% (3)",
						"Straight/60% (4)",
						"Straight/80% (5)",
						"Straight/100% (6)",
						"Battle/10% (7)",
						"Battle/20% (8)",
						"Battle/30 (9)",
						"Battle/40% (10)",
						"Battle/50% (11)",
						"Battle/75% (12)",
						"Battle/100% (13)"]
	roll = rollD6() + rollD6()
	match roll:
		case 2 | 3 | 4 | 5:
			stepRolled = 3
		case 6 | 7:
			stepRolled = 4
		case 8 | 9:
			stepRolled = 5
		case 10 | 11:
			stepRolled = 6
		case 12:
			stepRolled = 7
	match employerType:
		case "Civilian" | "Corporation":
			stepRolled = stepRolled - 2
		case "Planetary Government":
			stepRolled = stepRolled + 1
		case "House":
			stepRolled = stepRolled + 2
	match missionIn:
		case "Expedition":
			stepRolled = stepRolled + 1
		case "Invasion":
			stepRolled = stepRolled + 2
	if stepRolled > 12:
		stepRolled = 12
	if stepRolled < 0:
		stepRolled = 0
	return supportStepList[stepRolled]

# function to determine transport #
def getTransportRate(employerType, missionIn):
	transportStepList = ["0% (1)",
						"0% (2)", 
						"0% (3)",
						"0% (4)",
						"0% (5)",
						"25% (6)",
						"50% (7)",
						"75% (8)",
						"100% (9)",
						"100% (10)",
						"100% (11)",
						"100% (12)",
						"100% (13)"]
	roll = rollD6() + rollD6()
	match roll:
		case 2 | 3 | 4 | 5:
			stepRolled = 4
		case 6 | 7:
			stepRolled = 5
		case 8 | 9:
			stepRolled = 6
		case 10 | 11:
			stepRolled = 7
		case 12:
			stepRolled = 8
	match employerType:
		case "Civilian":
			stepRolled = stepRolled - 1
		case "Corporation" | "House":
			stepRolled = stepRolled + 1
	match missionIn:
		case "Garrison":
			stepRolled = stepRolled + 1
		case "Invasion":
			stepRolled = stepRolled - 1
	if stepRolled > 12:
		stepRolled = 12
	if stepRolled < 0:
		stepRolled = 0
	return transportStepList[stepRolled]
			
# function to determine salvage rights #
def getSalvageRights(employerType, missionIn):
	salvageStepList = ["None (1)",
						"Exchange (2)", 
						"Exchange (3)",
						"10% (4)",
						"20% (5)",
						"30% (6)",
						"40% (7)",
						"50% (8)",
						"60% (9)",
						"70% (10)",
						"80% (11)",
						"90% (12)",
						"100% (13)"]
	roll = rollD6() + rollD6()
	match roll:
		case 2 | 3 | 4 | 5:
			stepRolled = 2
		case 6 | 7:
			stepRolled = 3
		case 8 | 9:
			stepRolled = 4
		case 10 | 11:
			stepRolled = 5
		case 12:
			stepRolled = 6
	match employerType:
		case "Civilian":
			stepRolled = stepRolled + 4
		case "Corporation":
			stepRolled = stepRolled + 2
		case "Planetary Government":
			stepRolled = stepRolled + 1
		case "House":
			stepRolled = stepRolled - 1
	match missionIn:
		case "Raid":
			stepRolled = stepRolled - 1
		case "Garrison":
			stepRolled = stepRolled - 2
		case "Invasion":
			stepRolled = stepRolled + 1
	if stepRolled > 12:
		stepRolled = 12
	if stepRolled < 0:
		stepRolled = 0
	return salvageStepList[stepRolled]

# function to determine command rights #
def getCommandRights(employerType, missionIn):
	commandStepList = ["Integrated (1)",
						"Integrated (2)", 
						"Integrated (3)",
						"House (4)",
						"House (5)",
						"House (6)",
						"House (7)",
						"Liason (8)",
						"Liason (9)",
						"Liason (10)",
						"Independant (11)",
						"Independant (12)",
						"Independant (13)"]
	roll = rollD6() + rollD6()
	match roll:
		case 2 | 3 | 4 | 5:
			stepRolled = 4
		case 6 | 7:
			stepRolled = 5
		case 8 | 9:
			stepRolled = 6
		case 10 | 11:
			stepRolled = 7
		case 12:
			stepRolled = 8
	match employerType:
		case "Civilian":
			stepRolled = stepRolled + 4
		case "Mercenary":
			stepRolled = stepRolled + 3
		case "House" | "House":
			stepRolled = stepRolled - 3
	match missionIn:
		case "Invasion":
			stepRolled = stepRolled - 2
		case "Expedition":
			stepRolled = stepRolled + 2
	if stepRolled > 12:
		stepRolled = 12
	if stepRolled < 0:
		stepRolled = 0
	return commandStepList[stepRolled]

# function to generate the number of tracks #
def getTrackNumber(missionTypeIn):
	roll = rollD6 + rollD6
	match missionTypeIn:
		case "Raid" | "Expedition":
				match roll:
					case 9 | 10 | 11:
						return 2
					case 12:
						return 3
					case _:
						return 1
		case "Garrison" | "Retainer"
				match roll:
					case 2 | 3 | 4:
						return 0
					case 5 | 6:
						return 1
					case 7 | 8:
						return 2
					case 9: 
						return 3
					case 10:
						return 4
					case 11 | 12:
						return 4
# getTrackNumber ends #

# function to determine attacker/defender #
#def determineAttackerDefender(missionTypeIn):
#	roll = rollD6()
	#match missionTypeIn:
#	if missionTypeIn == "Raid":

	#elif missionTypeIn == "Garrison":
		
	#elif missionTypeIn == "Expedition":
		
	#elif missionTypeIn == "Invasion":
		
	#elif missionTypeIn == "Retainer":

# run main #
if __name__ == "__main__":
    main(sys.argv[1:])
