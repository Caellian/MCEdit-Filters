# Smart Flood Fill - A filter for MCEdit
# Replaces start adjacent non-downward chosen blocks with the selected block.
# This filter is based on 'Flood fill' filter by 'Marco Conti'.
#
# Author: Tin Svagelj (a.k.a. Caellian)
# Version: 1.0.0
#

displayName = "Smart Flood Fill"

inputs = (
	("Gravity:", ("Down (-Y)", "Up (Y)", "North (-Z)", "West (-X)", "South (Z)", "East (X)")),
	("Start X:", (0, -29999984, 29999984)),
	("Start Y:", (0, 0, 256)),
	("Start Z:", (0, -29999984, 29999984)),
	("Replacement block:","blocktype"),
	("Replaced block:","blocktype"),
)

def inside(box, x, y, z):
	return box.minx <= x and x < box.maxx and box.miny <= y and y < box.maxy and box.minz <= z and z < box.maxz

# Gets the block at the given position
def getBlock(position):
	return level.blockAt(position['x'], position['y'], position['z'])

# Creates a new point
def newPos(x,y,z):
	return {'x':x, 'y':y, 'z':z}

# Check for the block to be replaceable; if true, adds it to queue
def checkAndQueue(level, queue, replace, replacedBlock, x, y, z):
	if(y <= 0):
		return
	try:
		chunk = level.getChunk(x/16, z/16).dirty = True
	except:
		print "CHUNK LIMIT REACHED ON ", x, ",", z
		return # no valid chunk

	block = level.blockAt(x,y,z)
	data = level.blockDataAt(x,y,z)
	if block == replacedBlock.ID and data == replacedBlock.blockData:
		level.setBlockAt(x,y,z,replace.ID)
		level.setBlockDataAt(x, y, z, replace.blockData)
		queue.append(newPos(x,y,z))

# Main
def perform(level, box, options):
	replacementBlock = options["Replacement block:"]
	replacedBlock = options["Replaced block:"]
	startX = options["Start X:"]
	startY = options["Start Y:"]
	startZ = options["Start Z:"]

	gravity = options["Gravity:"]

	if(replacementBlock == replacedBlock):
		return

	if inside(box, startX, startY, startZ):
		x = startX
		y = startY
		z = startZ
	else:
		if (gravity == "West (-X)"):
			x = box.maxx - 1
		elif (gravity == "East (X)"):
			x = box.minx
		else:
			x = box.minx + (box.maxx - box.minx) / 2

		if (gravity == "Down (-Y)"):
			y = box.maxy - 1
		elif (gravity == "Up (Y)"):
			y = box.miny
		else:
			y = box.miny + (box.maxy - box.miny) / 2

		if (gravity == "North (-Z)"):
			z = box.maxz - 1
		elif (gravity == "South (Z)"):
			z = box.minz
		else:
			z = box.minz + (box.maxz - box.minz) / 2

	queue = []

	level.setBlockAt(x, y, z, replacementBlock.ID)
	level.setBlockDataAt(x, y, z, replacementBlock.blockData)
	queue.append(newPos(x, y, z))
	level.getChunk(0, 0)

	while len(queue) > 0:
		pos = queue.pop(0)
		x = pos['x']
		y = pos['y']
		z = pos['z']
		for X in [-1,0,1]:
			for Y in [-1,0,1]:
				for Z in [-1,0,1]:
					if (X == 0 and Y == 0 and Z == 0):
						continue
					if ((Y == 0 and (X == Z or X == -Z)) or (Y != 0 and (X != 0 or Z != 0 ))):
						continue
					if (not inside(box, x+X, y+Y, z+Z)):
						continue
					if (gravity == "Down (-Y)" and Y == 1) or (gravity == "Up (Y)" and Y == -1):
						continue
					if (gravity == "North (-Z)" and Z == 1) or (gravity == "South (Z)" and Z == -1):
						continue
					if (gravity == "West (-X)" and X == 1) or (gravity == "East (X)" and X == -1):
						continue

					checkAndQueue(level, queue, replacementBlock, replacedBlock, x+X, y+Y, z+Z)
