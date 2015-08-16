#!/usr/bin/python
###########################################################################################
#   promash - promash file object
#
#   Date        Author      Reason
#   ----        ------      ------
#   08/10/15    Lou King    Create
#
#   Copyright 2015 Lou King
#
#   **  MANY THANKS TO Brian Keyes <bkeyes@gmail.com> 
#   **  http://outofkey.com/promash-file-converter/ who figured out most of the formats 
#   **  used herein
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
###########################################################################################
'''
promash - promash file object
===================================================
'''

# standard
import pdb
import argparse

# pypi
import six
from construct import Struct, Array, String, CString, ULInt32, ULInt16, SLInt32, LFloat32, ULInt8, Enum, Byte, Flag
from construct import Embedded, Peek, Padding

# github

# home grown
# import version

#------------------------------------------------------------------------------------------
def FixedCString(name, length, terminators=six.b("\x00"), encoding=None):
#------------------------------------------------------------------------------------------
    """
    A string ending in a terminator.
    ``FixedCString`` is similar to the strings of C, C++, and other related
    programming languages, except it has a fixed length.
    By default, the terminator is the NULL byte (b``0x00``).
    :param name: name
    :param length: length of string
    :param terminators: sequence of valid terminators, in order of preference
    :param encoding: encoding (e.g. "utf8") or None for no encoding
    """

    fixedcstring = Embedded( Struct (None, 
            Peek (CString (name, terminators=terminators, encoding=encoding)),
            Padding (length), 
        )
    )

    return fixedcstring

## promash file structure

# Hop is array
hopstruct = Struct('Hop',
        FixedCString  ('Name',55), 
        LFloat32('Alpha'),  # from database
        LFloat32('Beta'),
        Flag('Noble'),
        LFloat32('Cohumulone'),
        LFloat32('Myrcene'),
        LFloat32('Humulene'),
        LFloat32('Caryophyllene'),
        Enum    (Byte('Type'),
                    Bittering   = 1, 
                    Aroma       = 2, 
                    Both        = 3, 
                    _default_ = 'unknown',
            ),
        Byte('Form'),   # 0,1,2,3=Whole, 17,18,19=Plug, 33,24,35=Pellet (this makes no sense, why multiple values for form?)
        LFloat32('StorageFactor'),
        FixedCString  ('Notes',155), 
        FixedCString  ('Origin',55), 
        FixedCString  ('BestFor',155), 
        FixedCString  ('Substitutes',155), 
        FixedCString  ('Unknown2',14), 
        LFloat32('ActualAA'),   # from recipe
        Byte    ('Unknown3'),
        LFloat32('Ounces'),
        ULInt16 ('BoilTime'),
        LFloat32('IBUs'),
    )

# Fermentable is array
fermentablestruct = Struct('Fermentable',
        FixedCString  ('Name',55), 
        FixedCString  ('Supplier',55), 
        FixedCString  ('Origin',55), 
        Enum    (Byte('Type'),
                    Grain   = 1,
                    Extract = 2,
                    Sugar   = 3,
                    Other   = 4,
            ),
        Byte    ('MustMash'),       # TODO: - what is this for?
        LFloat32('Potential'),
        LFloat32('Color'),
        LFloat32('Moisture'),
        LFloat32('Max'),
        LFloat32('DiastaticPower'),
        LFloat32('Protein'),
        LFloat32('TSN'),
        FixedCString  ('UseFor',155), 
        FixedCString  ('Comments',155), 
        LFloat32('Unknown1'),
        LFloat32('Unknown2'),
        LFloat32('FGDry'),
        LFloat32('CGDry'),
        LFloat32('Pounds'),     # was Amount
        LFloat32('Unknown3'),


)

# Misc [ingredient] is array
miscstruct = Struct('Misc',
        FixedCString  ('Name',55), 
        Enum    (Byte('Type'),
                    Spice   = 0,
                    Fruit   = 1,
                    Coffee  = 2,
                    Other   = 3,
                    Fining  = 4,
                    Herb    = 5,
            ),
        ULInt32 ('Time'),
        Enum    (Byte('Location'),
                    Boil        = 0,
                    Fermenter   = 1,
                    Mash        = 2,
            ),
        Enum    (Byte('TimeUnits'),
                    Days    = 0,
                    Minutes = 1,
            ),
        Enum    (Byte('MeasurementUnits'),
                    Ounces  = 0,
                    Grams   = 1,
                    Pounds  = 2,
                    Tsp     = 3,
                    Tbsp    = 4,
                    Cups    = 5,
                    Units   = 6,
            ),
        ULInt32 ('Unknown1'),
        FixedCString  ('Use',255), 
        FixedCString  ('Comment',255), 
        LFloat32('Amount'),
        FixedCString  ('Unknown2',8), 
)

# [mash] Step is array
stepstruct = Struct('Step',
        FixedCString  ('Name',255), 
        Enum    (Byte('Type'),
                    Infusion    = 0,
                    Direct      = 1,
                    Decoction   = 2,
                    _default_   = 'unknown',
            ),
        SLInt32 ('StartTemp'),
        SLInt32 ('StopTemp'),
        SLInt32 ('InfuseTemp'),
        SLInt32 ('RestTime'),
        SLInt32 ('StepTime'),
        LFloat32('InfuseRatio'),
        LFloat32('InfuseAmount'),
        ULInt32 ('StepColor'),      # RGBA
        ULInt32 ('RestColor'),      # RGBA
)

# full file structure
promashstruct = Struct('promashfile',
    Struct('Header',
        FixedCString  ('Name',85), 
        ULInt32 ('NumHopRecs'),
        ULInt32 ('NumFermRecs'),
        ULInt32 ('NumMiscRecs'),
        LFloat32('BatchSize'),      # TODO: where does this come from?
        LFloat32('WortSize'),
        LFloat32('EstGravity'),     # gravity = 1 + EstGravity/1000
        LFloat32('TotalIBU'),
        LFloat32('EstEfficiency'),  # TODO: where does this come from
        SLInt32 ('BoilTime'),
        SLInt32 ('Unknown1'),       # TODO: what is this? where is SRM?
        ULInt8  ('Type'),           # TODO: what does this mean?
    ),

    Struct('Style',
        FixedCString  ('CatName',55), 
        FixedCString  ('SubCatName',55), 
        Enum    (Byte('CatType'),
                    Ale             = 0, 
                    Lager           = 1, 
                    AleLagerMixed   = 2, 
                    Mead            = 3, 
                    Cider           = 4,
            ),
        LFloat32('MinSG'),
        LFloat32('MaxSG'),
        LFloat32('MinFG'),
        LFloat32('MaxFG'),
        LFloat32('AlcByWeight'),
        LFloat32('AlcByVolume'),
        LFloat32('MinIBU'),
        LFloat32('MaxIBU'),
        LFloat32('MinColor'),
        LFloat32('MaxColor'),
        FixedCString  ('ColorNote',155), 
        FixedCString  ('MaltNote',155), 
        FixedCString  ('HopNote',155), 
        FixedCString  ('YeastNote',155), 
        FixedCString  ('Examples',155), 
        FixedCString  ('Unknown1',100), 
        ULInt8  ('CatNumber'),
        ULInt8  ('Unknown3'),
        FixedCString  ('SubCatLetter',1), 
        ULInt8  ('Unknown2'),
        ULInt8  ('Guidelines'),

    ),

    Array(lambda ctx:ctx.Header.NumHopRecs, hopstruct),
    Array(lambda ctx:ctx.Header.NumFermRecs, fermentablestruct),
    Array(lambda ctx:ctx.Header.NumMiscRecs, miscstruct),

    Struct('Yeast',
        FixedCString  ('Name',55), 
        FixedCString  ('Lab',55), 
        FixedCString  ('CatNumber',25), 
        Enum    (Byte('Type'),
                    Ale         = 0, 
                    Lager       = 1, 
                    Wine        = 2, 
                    Champagne   = 3, 
            ),
        Enum    (Byte('Medium'),
                    Dry         = 0, 
                    Liquid      = 1, 
                    Slant       = 2, 
            ),
        FixedCString  ('Flavors',155), 
        FixedCString  ('Comments',155), 
        FixedCString  ('Unknown1',8), 
        ULInt32 ('AttenLow'),
        ULInt32 ('AttenHigh'),
        LFloat32('Temp'),
        Enum    (Byte('Flocculation'),
                    High        = 0, 
                    Medium      = 1, 
                    Low         = 2, 
            ),
        FixedCString  ('Unknown2',5), 
    ),

    Struct('Water',
        FixedCString  ('Name',27), 
        LFloat32('Calcium'),
        LFloat32('Magnesium'),
        LFloat32('Sodium'),
        FixedCString  ('Unknown1',4), 
        LFloat32('Sulfate'),
        LFloat32('Chloride'),
        LFloat32('Bicarbonate'),
        LFloat32('PH'),
        FixedCString  ('KnownFor',163), 
    ),

    Struct('Mash',
        Enum    (Byte('RecipeSimpleMashType'),
                    SingleStep  = 2, 
                    MultiStep   = 3, 
            ),
        FixedCString  ('RecipeChunk1',8), 
        ULInt32 ('acid_rest_temp'),
        ULInt32 ('acid_rest_time'),
        ULInt32 ('protein_rest_temp'),
        ULInt32 ('protein_rest_time'),
        ULInt32 ('intermediate_rest_temp'),
        ULInt32 ('intermediate_rest_time'),
        ULInt32 ('saccharification_rest_temp'),
        ULInt32 ('saccharification_rest_time'),
        ULInt32 ('mash_out_rest_temp'),
        ULInt32 ('mash_out_rest_time_min'),
        ULInt32 ('sparge_temp'),
        ULInt32 ('sparge_time'),
        LFloat32('mash_in_qt'),
        Byte    ('recipe_properties_03'),
        FixedCString  ('recipe_notes',4028), 
        FixedCString  ('recipe_awards',4028),
        FixedCString  ('recipe_chunk_02',255), 
        ULInt32 ('MashSteps'),
        ULInt32 ('Graintemp'),
        FixedCString  ('Unknown1',4), 
        Array   (50, stepstruct),
        FixedCString  ('Unknown2',292), 
        FixedCString  ('ScheduleName',255), 
    ),

)

#--------------------------------------------------------------------------------
def parsefile (filename):
#--------------------------------------------------------------------------------
    '''
    Parse a promash file, returning data structure.

    :param filename: name of file to parse
    :rtype: object containing parsed data from file. Use :func:`getattrs` to get the tree of attributes returned
    '''
    SS = open(filename,'rb')
    filedata = SS.read()
    SS.close()

    parseddata = promashstruct.parse(filedata)

    return parseddata

#--------------------------------------------------------------------------------
def _getattrs (con):
#--------------------------------------------------------------------------------
    '''
    get the attribute of a construct or subconstruct

    :param con: construct or subconstruct for which attributes should be returned
    :rtype: list of attributes, may be list of lists
    '''

    # call _getattrs() recursively until bottom of tree is found
    pass

#--------------------------------------------------------------------------------
def getattrs ():
#--------------------------------------------------------------------------------
    '''
    Return a tree of attributes stored in the return from :func:`parsefile`

     :rtype: list of attributes, may be list of lists
   '''
    pass

#--------------------------------------------------------------------------------
def main():
#--------------------------------------------------------------------------------

    pass

################################################################################
################################################################################
if __name__ == "__main__":
    main()
