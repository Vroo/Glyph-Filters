# MenuTitle: Burned
# -*- coding: utf-8 -*-
__doc__ = """
Burned
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNGFSpacePartition import *
from NaNGFNoise import *
from NaNFilter import NaNFilter
from NaNGlyphsEnvironment import glyphsEnvironment as G


def returnRoundedPaths(paths):
    roundedpathlist = []
    for p in paths:
        roundedpath = RoundPath(p, "nodes")
        try:
            roundedpathlist.append(convertToFitpath(roundedpath, True))
        except Exception as e:
            print(("returnRoundedPaths failed:", e))
    return roundedpathlist


class Burn(NaNFilter):
    params = {
        "S": {"offset": 0, "gridsize": 40},
        "M": {"offset": 4, "gridsize": 45},
        "L": {"offset": 4, "gridsize": 50},
    }

    def processLayer(self, thislayer, params):
        outlinedata = setGlyphCoords(ConvertPathsToSkeleton(thislayer.paths, 20))
        bounds = AllPathBounds(thislayer)

        offsetpaths = self.saveOffsetPaths(
            thislayer, params["offset"], params["offset"], removeOverlap=True
        )
        outlinedata2 = setGlyphCoords(ConvertPathsToSkeleton(offsetpaths, 4))

        ClearPaths(thislayer)

        newtris = self.SortCollageSpace(
            thislayer,
            outlinedata,
            outlinedata2,
            params["gridsize"],
            bounds,
            action="overlap",
            randomize=True,
        )
        maxchain = random.randrange(200, 400)
        groups = BreakUpSpace(
            thislayer, outlinedata, newtris, params["gridsize"], maxchain
        )
        for g in groups:
            if len(g) > 2:
                G.add_paths(thislayer, g)

        G.remove_overlap(thislayer)
        roundedpathlist = returnRoundedPaths(thislayer.paths)
        ClearPaths(thislayer)
        AddAllPathsToLayer(roundedpathlist, thislayer)
        self.CleanOutlines(thislayer, remSmallPaths=True, remSmallSegments=True, remStrayPoints=True, remOpenPaths=True, keepshape=False)

Burn()
