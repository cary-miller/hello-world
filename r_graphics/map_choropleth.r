
library(raster)
library(rasterVis)
library(colorspace)


ext <- extent(65, 135, 5, 55)

if (0){
    # 
    # 875430rgb-167772161.0.FLOAT.TIFF
    pop <- raster('data/875430rgb-167772161.0.FLOAT.TIFF')
    pop <- crop(pop, ext)
    pop[pop==99999] <- NA
    pTotal <- levelplot(pop, zscaleLog=10, par.settings=BTCTheme)
    pTotal
}



library(maps)
library(mapproj)
colors = floor(runif(63)*657)
if (1){
    map("state", col = colors, fill = T, resolution = 0)
    map("state", col = colors, fill = T, projection = "polyconic", resolution = 0)
    state.names = map("state")$names

    county.names = map("county")$names
    map("county", col = colors, fill = T, projection = "polyconic", resolution = 0)

    map("county", 'colorado,weld', col = colors, fill = T, projection = "polyconic", resolution = 0)

}
library(plyr)
library(rgdal)
library(maptools)
library(ggplot2)
library(rgeos)
library(gpclib)
gpclibPermit() # => fortify
# package rgdal
# On the Mac, the package resides on the “CRAN Extras” repository where
# difficult-to-compile packages can sometimes be found.  On the Mac, rgdal
# is installed as follows
# setRepositories(ind=1:2)
# install.packages("rgdal")
# 
# http://geography.uoregon.edu/geogr/topics/maps.htm

shp.dir = '/Users/marymiller/data/shp/county/WELD/'
fname = 'HIGHWAYS'
ext = '.shp'

fn = paste(shp.dir, fname, ext, sep='')
fname = 'LAKES'
fn2 = paste(shp.dir, fname, ext, sep='')


if (1){
#    readShapeSpatial
#    readShapePoly
#    readShapePoints
#    readShapeLines
    hwy = readShapeLines(fn)  # slow
    lake = readShapePoly(fn2)  # slow
    county =readShapeSpatial( paste(shp.dir, 'COUNTIES', ext, sep='') )
    county =readShapePoly( paste(shp.dir, 'COUNTIES', ext, sep='') )
    city =readShapePoly( paste(shp.dir, 'CITIES', ext, sep='') )
    major_roads = readShapeLines( paste(shp.dir, 'MAJOR_ROADS', ext, sep='') )


    ba = lake@class
    ba = lake@data
    ba = lake@polygons

    lake@data$id = rownames(lake@data)
    lake.points = fortify(lake, region='id')
    lake.df = join(lake.points, lake@data, by="id")
    lake.df$type = 'lake'

    county@data$id = rownames(county@data)
    county.points = fortify(county, region='id')
    county.df = join(county.points, county@data, by="id")
    county.df$type = 'county'

    hwy@data$id = rownames(hwy@data)
    hwy.points = fortify(hwy, region='id')
    hwy.df = join(hwy.points, hwy@data, by="id")
    hwy.df$type = 'hwy'

    major_roads@data$id = rownames(major_roads@data)
    major_roads.points = fortify(major_roads, region='id')
    major_roads.df = join(major_roads.points, major_roads@data, by="id")
    major_roads.df$type = 'major_roads'


    city@data$id = rownames(city@data)
    city.points = fortify(city, region='id')
    city.df = join(city.points, city@data, by="id")
    city.df$type = 'city'



    x.grid = seq(400,700,25) * 1000
    y.grid = seq(440,455,5) * 10000

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
        scale_x_continuous(breaks=NA, name='') +
        scale_y_continuous(breaks=NA, name='') +

        aes(long,lat,group=group) + 
        geom_polygon(data=city.df, color='gray70', alpha=.1) + 
        geom_path(color='black') +
        coord_equal() +
        scale_fill_brewer("") +
        geom_polygon(data=lake.df, color='blue') +
        geom_line(data=major_roads.df, color='tan') + 
        geom_line(data=hwy.df, color='brown') +
        geom_point(data=well.df, color='red', alpha=0.3)

}

if (0){
quartz.options(bg='white')
quartz.save('gis.ggplotx.png')
}


if (0){
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



