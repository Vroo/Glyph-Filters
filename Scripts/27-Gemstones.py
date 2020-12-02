#MenuTitle: 27. Gemstones
# -*- coding: utf-8 -*-
__doc__="""
27. Gemstones
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *

# COMMON
font = Glyphs.font
selectedGlyphs = beginFilterNaN(font)


# ====== OFFSET LAYER CONTROLS ================== 

def doOffset( Layer, hoffset, voffset ):
	try:
		offsetCurveFilter = NSClassFromString("GlyphsFilterOffsetCurve")
		offsetCurveFilter.offsetLayer_offsetX_offsetY_makeStroke_autoStroke_position_error_shadow_( Layer, hoffset, voffset, False, False, 0.5, None,None)
	except Exception as e:
		print("offset failed")

def saveOffsetPaths( Layer , hoffset, voffset, removeOverlap):
	templayer = Layer.copy()
	templayer.name = "tempoutline"
	currentglyph = Layer.parent
	currentglyph.layers.append(templayer)
	tmplayer_id = templayer.layerId
	doOffset(templayer, hoffset, voffset)
	if removeOverlap==True: templayer.removeOverlap()
	offsetpaths = templayer.paths
	del currentglyph.layers[tmplayer_id]
	return offsetpaths

# ================================================


def MoonRocks(thislayer, outlinedata, iterations, maxgap):

	list_dots, rocks = [], []
	b = AllPathBounds(thislayer)

	if b is not None:

		ox, oy, w, h = b[0], b[1], b[2], b[3]

		for f in range(0, iterations):

			x = random.randrange(ox, ox+w)
			y = random.randrange(oy, oy+h)

			if withinGlyphBlack(x, y, outlinedata):

				rad = random.randrange(10,250)
				inside = True
				bufferdistcircle = maxgap

				for n in range(0, len(list_dots)):

					nx = list_dots[n][0]
					ny = list_dots[n][1]
					nr = list_dots[n][2]
					dist = math.hypot(nx - x, ny - y) #alt method

					if dist<(nr+rad+bufferdistcircle):
						inside=False
						break

				if inside==True:
					circles = []
					circle = drawCircle(x, y, rad*2, rad*2)
					circles.append(circle)
					circlea = doAngularizzle(circles, 10)
					circlea = setGlyphCoords(circlea)
					circlecoords = circlea[0][1]

					if ShapeWithinOutlines(circlecoords, outlinedata):
						list_dots.append([x, y, rad])

		for c in range(0, len(list_dots)):
			x, y = list_dots[c][0], list_dots[c][1]
			size = list_dots[c][2]
			circle = drawBlob(x, y, size*2, 5, False)
			rocks.append(circle)

		return rocks


# RETURN SPIKEY PATHS

def Spikes(thislayer, outlinedata, minpush, maxpush):

	spikepaths = []

	for path in outlinedata:

		direction = path[0]
		structure = path[1]
		nodelen = len(structure)
		spike = GSPath()
		n = 0

		while n < nodelen:

			x1 = structure[n][0]
			y1 = structure[n][1]
			minstep = 10
			maxstep = 22

			if direction=="False": maxstep=int(maxstep*0.5)
			step = random.randrange(minstep, maxstep)

			if n+step>=nodelen-1:
				n = nodelen
				break

			# --- set node pos for main or end
			if n<nodelen-1:
				x2 = structure[n+step][0]
				y2 = structure[n+step][1]
				n+=step
			else:
				x2 = structure[0][0]
				y2 = structure[0][1]

			a = atan2(y1-y2, x1-x2)
			a += radians(90)

			midx = x1 + ((x2-x1)/2)
			midy = y1 + ((y2-y1)/2)

			pushdist = random.randrange(minpush, maxpush)

			linex = pushdist * cos(a)
			liney = pushdist * sin(a)

			searchblack = DistanceToNextBlack(thislayer, [x1, y1], [x2, y2], outlinedata, 200)

			if direction=="False":
				linex*=0.7
				liney*=0.7
				pushdist*=0.7

			if searchblack is not None:
				if searchblack < 200:
					linex*=0.7
					liney*=0.7
					pushdist*=0.7

			midx += linex
			midy += liney

			# draw spikes
			spike.nodes.append(GSNode([midx, midy], type = GSLINE))
			spike.nodes.append(GSNode([x2, y2], type = GSLINE))

		spike.closed = True
		spikepaths.append(spike)

	return spikepaths


def Outputspike():

	for glyph in selectedGlyphs:

		glyph.beginUndo()
		beginGlyphNaN(glyph)

		# --- °°°°°°°

		thislayer = font.glyphs[glyph.name].layers[0]
		thislayer.beginChanges()

		# ---
		
		glyphsize = glyphSize(glyph)

		if glyphsize=="S": 
			offset = -5
			minpush, maxpush = 10, 20
			iterations = 50
		if glyphsize=="M": 
			offset = -10
			minpush, maxpush = 20, 40
			iterations = 400
		if glyphsize=="L": 
			offset = -20
			minpush, maxpush = 20, 40
			iterations = 420

		offsetpaths = saveOffsetPaths(thislayer, offset, offset, removeOverlap=False)
		pathlist = doAngularizzle(offsetpaths, 4)
		outlinedata = setGlyphCoords(pathlist)

		ClearPaths(thislayer)

		spikepaths = Spikes(thislayer, outlinedata, minpush, maxpush)
		AddAllPathsToLayer(spikepaths, thislayer)

		rockpaths = MoonRocks(thislayer, outlinedata, iterations, 8)
		rockpaths = ConvertPathlistDirection(rockpaths, 1)
		AddAllPathsToLayer(rockpaths, thislayer)

		# ---

		thislayer.endChanges()

		# --- °°°°°°°

		endGlyphNaN(glyph)
		glyph.endUndo()


# =======

Outputspike()

# =======

#OutputFur()
#OutputSpikes()

endFilterNaN(font)






