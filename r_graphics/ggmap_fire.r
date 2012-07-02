# http://stackoverflow.com/questions/11056738/plotting-points-from-a-data-frame-using-openstreetmap?rq=1

library(ggmap)
library(plyr)
library(rjson)

x= -105.2
y= 38.6
dx = 0.5
dy = 0.5
location = c(x, y, x+dx, y+dy)


# source = 'osm|google|stamen|cloudmadeNO'
map_source = 'osm'     # maptype ignored
map_source = 'stamen'  # maptype: terrain watercolor toner
map_source = 'google'  # maptype: terrain satellite roadmap hybrid

map_type = 'roadmap'
map_type = 'satellite'
map_type = 'terrain'
map_type = 'hybrid'

map_type = 'toner'     # black & white & super simple
map_type = 'watercolor'  # 500 error
map_type = 'terrain'

kv = list()
kv$map_type = 'terrain'
kv$map_source = 'stamen'

co = get_map(location=location, source=map_source, maptype=map_type)
coMap = ggmap(co) # Draw the map

alpha = 1
alpha = 0.3
alpha = 0.7

json_file = '~/data/fire/ActiveFirePerimeters_2012_06_27.json'
json_data = fromJSON(paste(readLines(json_file), collapse=""))


fx = function(lst){
    boundary.df = as.data.frame(t(matrix(unlist(lst), nrow=2)))
    names(boundary.df) = c( "longitude", "latitude")
    return (boundary.df)
}

coord_list = llply(json_data, fx)
boundary.df = coord_list[1]

# Polygon layer
coMap = coMap + geom_polygon(data=boundary.df[[1]], 
    aes(x=longitude, y=latitude),
    size=0, color='yellow', fill='red', alpha=alpha)


# check out ggmap *inset* for inset graphic.


