library(plyr)
#library(rgdal) # Geospatial Data Abstraction Library.
library(maptools) # shapefiles, kml files, super-sophisticated, super-control, super-buggy
library(ggplot2)
#library(rgeos) # Interface to Geometry Engine - Open Source (GEOS)
#library(gpclib) # General Polygon Clipping Library
#gpclibPermit() # => fortify
#library(sp) # classes and methods for spatial data

# re package rgdal:  info from
# http://geography.uoregon.edu/geogr/topics/maps.htm
# 
# On the Mac, the package resides on the “CRAN Extras” repository where
# difficult-to-compile packages can sometimes be found.  On the Mac, rgdal
# is installed as follows
# setRepositories(ind=1:2)
# install.packages("rgdal")

shp.dir = '~/data/shp/county/WELD/'
ext = '.shp'
fn = function(name) paste(shp.dir, name, ext, sep='')


magic.df = function(ob, obname){
    ob@data$id = rownames(ob@data)
    ob.points = fortify(ob, region='id')
    ob.df = join(ob.points, ob@data, by="id")
    ob.df$type = obname
    return (ob.df)
}
# TODO
#   either name from object or
#   object from name


f1 = function() {
#    readShapeSpatial
#    readShapePoly
#    readShapePoints
#    readShapeLines
    hwy         = readShapeLines( fn('HIGHWAYS') )
    lake        = readShapePoly( fn('LAKES') )
    county      = readShapeSpatial( fn('COUNTIES') ) ######
    county      = readShapePoly( fn('COUNTIES') )
    city        = readShapePoly( fn('CITIES') )
    major_roads = readShapeLines( fn('MAJOR_ROADS') )

    lake.df        = magic.df(lake, 'lake')
    county.df      = magic.df(county, 'county')
    hwy.df         = magic.df(hwy, 'hwy')
    major_roads.df = magic.df(major_roads, 'major_roads')
    city.df        = magic.df(city, 'city')


    ba = slotNames(lake)
    ba = slotNames(lake@polygons[[1]])  # ok
    ba = slotNames(lake@polygons[1])  # fails

    ba = lake@class
    ba = lake@data
    ba = lake@polygons





#    x.grid = seq(400,700,25) * 1000
#    y.grid = seq(440,455,5) * 10000

    # Generate fake data to plot.
    n = 500
    f = 2
    well.x = (530 + f*7*rnorm(n)) * 1000
    well.y = (450 + f*1*rnorm(n)) * 10000
    well.x = well.x + (well.y-min(well.y)) * 0.9
    well.df = as.data.frame(cbind(well.x, well.y, as.factor(1)))
    names(well.df) = c('long', 'lat', 'group')

    ggplot(county.df) + 
        theme_bw() +   # white background
        # Remove grid lines and tick marks.
        scale_x_continuous(breaks=NULL, name='') +
        scale_y_continuous(breaks=NULL, name='') +

        aes(long,lat,group=group) + 
        geom_polygon(data=city.df, color='gray70', alpha=.1) + 
        geom_path(color='black') +
        coord_equal() +
        scale_fill_brewer("") +
        geom_polygon(data=lake.df, color='blue') +
        geom_line(data=major_roads.df, color='tan') + 
        geom_line(data=hwy.df, color='brown') +
        geom_point(data=well.df, color='red', alpha=0.3)
        # Amazing!
        # I'm plotting bunches of data frames without naming any of their
        # individual columns.  The *aes* call does it all.

}

if (0){
quartz.options(bg='white')
quartz.save('gis.ggplotx.png')
}


library('rgdal')
library('maptools')
library('ggplot2')
# http://rgm2.lab.nig.ac.jp/RGM2/func.php?rd_id=rgdal:readOGR
dsn = '/Users/marymiller/data/shp/county/WELD'  #yes

f3 = function(){
    # It works now.
    layer = 'AIRPORTS'
    layer = 'LAKES'
    bla = ogrInfo(dsn=dsn, layer=layer)
    lago = readOGR(dsn=dsn, layer=layer)
    lago@data$id = rownames(lago@data)
    lago.points = fortify(lago, region="id")
    lago.df = join(lago.points, lago@data, by="id")

# http://gis.stackexchange.com/
# http://gis.stackexchange.com/questions/21566/gis-r-and-shapefiles
# http://cran.r-project.org/web/views/Spatial.html
# sp package
# http://examples.oreilly.com/9780596008659/  web mapping illustrated
    ba = slotNames(lago@polygons[[1]]@Polygons[[1]])
    
    # Try again the KML file.
    dsn = '/Users/marymiller/data/fire'  #?
    layer = 'ActiveFirePerimeters_2012_07_03' #.kml
    layer = 'ActiveFirePerimeters_2012_07_03.kml' 
    bla = ogrInfo(dsn=dsn, layer=layer) # cannot open file
    # https://stat.ethz.ch/pipermail/r-sig-geo/2009-January/004760.html
    # gdal/rgdal/ogr built with expat parser ??????

}
# http://mikemainguy.blogspot.com/2011/10/gorillarinas-putting-agile-skirt-on.html



f2 = function (){
    #    da = SpatialPolygons(city)  # NO
    #    blah = overlay(hwy, lake)
    #    blah = rbind(hwy, lake)
    #    blah = spRbind(hwy, lake) # NO. combining lines/polygons
    #    blah = spRbind(county, lake) # NO. non-unique polygon ids.
         # to fix use spChFIDs from maptools.
    #    blah = spRbind(spChFIDs (county), spChFIDs (lake)) # NO. 
    #    blah = rbind.SpatialPolygons(county, lake) # NO. non-unique ids.
        blah = rbind.SpatialPolygons(county, lake, city, makeUniqueIDs=TRUE) # yes!
        # makeUniqueIDs works but preferred to use spChFIDs.
        plot(blah)
        lines(hwy, col='red')
    #    plot(lake, col='blue')
}



