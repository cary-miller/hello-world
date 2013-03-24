# setwd('git-repos/hello-world/r_graphics')

library(ggmap)
library(plyr)
library(rjson)

# ############################## The Map ######################################
#
# Showing a basic map is two lines.  The *get_map* function fetches the map.
# Parameters:
#     source: google, stamen, osm, cloudmade
#     maptype: each source has different choices
#     location: center + zoom   or   4 coordinates

map_source = 'osm'     # maptype ignored
map_source = 'stamen'  # maptype: terrain watercolor toner
map_source = 'google'  # maptype: terrain satellite roadmap hybrid

# stamen maptypes
map_type = 'toner'     # black & white & super simple
map_type = 'watercolor'  # 500 error
map_type = 'terrain'

# google maptypes
map_type = 'roadmap'
map_type = 'satellite'
map_type = 'terrain'
map_type = 'hybrid'




x= -105.2
y= 38.6
dx = 0.5
dy = 0.5
location = c(x, y, x+dx, y+dy)

co = get_map(location=location, source=map_source, maptype=map_type)
coMap = ggmap(co) # Draw the map


# ####################### Adding data to the map ###############################
#
# Draw on the map using ggplot2.

boundary.date = function(date){
    # Read fire perimeter coordinates from date into a data frame,
    # adding a column for the date.
    base = '~/data/fire/ActiveFirePerimeters_'
    suffix = '.json'
    json_file = paste(base, date, suffix, sep='')
    nested_list = fromJSON(paste(readLines(json_file), collapse=""))

    boundary.f = function(lst){
        # Convert nested lists to data frame.
        boundary.df = as.data.frame(t(matrix(unlist(lst), nrow=2)))
        names(boundary.df) = c( "longitude", "latitude")
        return (boundary.df)
    }

    boundary.df = llply(nested_list, boundary.f)[1][[1]]
    boundary.df$date = date # faceting variable
    return (boundary.df)
}


# Stack by date
boundary.df = rbind(boundary.date('2012_06_27'), 
                    boundary.date('2012_07_03')
               )
alpha = 0.7

# Polygon layer
coMap = coMap + 
    geom_polygon(data=boundary.df, aes(x=longitude, y=latitude),
        fill='red', alpha=alpha)  + 
    facet_wrap(~date, ncol=2)



# inset another ggplot. 
n=7
df1 = data.frame(x=seq(n), y=runif(n), date='2012_06_27')
df2 = data.frame(x=seq(n), y=runif(n), date='2012_07_03')
df = rbind(df1, df2)

new.plot = ggplot(df) + 
    geom_line(data=df, aes(x=x,y=y, ymin=0, ymax=1), color='black', size=0.5) + 
    theme_bw()
#    + facet_wrap(~date,ncol=2)

y = 38.75
y = 38.65
y = 38.6
dx = 0.1
dx = 0.2

dy = 0.05
dy = 0.5
dy = 0.1
dy = 0.2

xmin =  x
xmax =  x+dx
ymin =  y
ymax =  y+dy

#coMap = coMap + inset(ggplotGrob(new.plot), xmin, xmax, ymin, ymax)


# helpful urls
# http://stackoverflow.com/questions/11056738/plotting-points-from-a-data-frame-using-openstreetmap?rq=1

# inset
# https://github.com/dkahle/ggmap/issues/6
# http://stackoverflow.com/questions/3305613/using-grid-and-ggplot2-to-create-join-plots-using-r

# TODO
#   distinct inset per facet.
#   deal with boundary within boundary.



# aside
kv = list()
kv$map_type = 'terrain'
kv$map_source = 'stamen'
