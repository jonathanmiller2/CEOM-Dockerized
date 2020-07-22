Global Geo-Referenced Field Photo Library Download
ESRI Shapefile and DBF download archive.

Description:
    This archive contains ESRI shapefile data in the form of Shape points and data
    attributes stored in shapefile and dBase database file respectively as
    well as all the JPEG images associated with the shape points and other data.

Contents:
    shapefile.shp
    shapefile.shx
    shapefile.prj
    shapefile.dbf
    readme.txt
    *.jpg
    
Use:
    For ArcMap
    
    A:
    1. Load shapefile into ArcMap
    
    B:
    1. Right-click the shapefile layer. Open 'Layer Attribute Table'
    2. Click 'PICTURE' column to select the column.
    3. Right click 'PICTURE' tab again and select 'Field Calculator', press Yes if
        you get a warning.
    4. In the Field Calculator, type in quotes the directory to which you've 
        extracted the images, than character '&' and than [PICTURE]. For example:
        "C:\Documents and Settings\pavel\Desktop\data\"&[PICTURE]
    5. Press OK. This should append the location of the images to the filenames of
        the images contained in the 'PICTURE' column. 
    
    C:
    1. Right-click shapefile layer. Select properties.
    2. Go to 'Display' tab.
    3. In the Hyperlinks check of "Support Hyperlinks using field" and
    4. Select 'PICTURE' field. Leave 'Document' selected.
    
    5. Go to View->Toolbars and make sure 'Tools' is selected.
    6. Select 'Lightnign bolt' tool from the Tools toolbar.
    7. To view a thumb simply click a point with the tool.
