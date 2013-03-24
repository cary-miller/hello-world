# setwd('git-repos/hello-world/r_graphics')

library(plyr)
library(maps)
library(mapproj)
library(mapdata)
data(county.fips)  # maps: fips code to county.name
data(state.fips)  
colors = floor(runif(63)*657)
world.sub = c('USA', 'USA:Alaska', 'Mexico', 'Canada')





map.ds = function() {
}
if (T){
    # map function returns a data structure.
    country.names = map("world")$names
    state.names = map("state")$names
    county.names = map("county")$names
    state = map("state")

    # If we search for a country name we get a huge number of hits because
    # each non-contiguous part of the country gets its own row.
    usa = grep('^USA', country.names)  # n>130
    usa = grep('^USA$', country.names)  # 1
    ak = grep('^USA:Alaska$', country.names)  # 1
    mex = grep('^Mexico', country.names)  # n == 27
    mex = grep('^Mexico$', country.names)  # n == 1
    can = grep('^Canada$', country.names)  # n
}

# http://en.support.wordpress.com/code/posting-source-code/

############# Choropleth unemployment map for a few counties #####
data(unemp)
some.counties = c('colorado,weld', 'colorado,denver',
    'colorado,adams', 'colorado,arapahoe', 'colorado,larimer', 
    'colorado,jefferson', 
    'colorado,douglas', 
    'colorado,boulder') 


choro_unemp = function(some.counties){
    # fips data for some.counties
    fips.co = county.fips[county.fips$polyname %in% some.counties,]

    # unemployment rates for some.counties
    un.co = unemp[unemp$fips %in% fips.co$fips,]

    # Assign colors to counties.  Most of this code is undoing the
    # 'helpful' autoconversion of character data to factor.
    n = length(some.counties) - 1
    cols = gray( seq(n/2, 0, -0.5)/n +.5)

    new.df = cbind(un.co, fips.co$polyname, rep('a', dim(un.co)[1]))
    # convert factors to character.
    i <- sapply(new.df, is.factor)
    new.df[i] <- lapply(new.df[i], as.character)

    names(new.df) = c('fips', 'pop', 'unemp', 'name', 'col')
    # The map function 'helpfully' converts data frame character vectors
    # to factors whether you want it or not.  There are two ways to deal
    # with it.
    #  1.  Reorder the df to factor order. (as below).
    #  2.  Plot vectors instead of data frame columns.
    new.df = new.df[order(new.df$unemp),]
    new.df$col=cols
    new.df = new.df[order(new.df$name),]
    map("county", new.df$name, col=new.df$col, fill=T)
    map.text("county", new.df$name, add=T)
}


county.by.name = function(){
    # Color code counties by name
    # Lincoln == blue
    # Washington == red
    # other == black
    color.code = rep('black', length(county.names))
    color.code = rep('white', length(county.names))
    wash = grep('washington$', county.names) # n==32
    color.code[wash] = 'red'
    linc = grep('lincoln$', county.names) # n==24
    color.code[linc] = 'blue'
    map("county", col=color.code, fill=T)
#    map("county", col=color.code, fill=T, projection="polyconic")
}


color.mich = function(){
    # Color code Michigan
    color.code = rep('black', length(state.names))
    mich = grep('^michigan', state.names)
    color.code[mich] = 'green'
    map("state", col=color.code, fill=T, projection="polyconic")
}

hi.res = function(){
    # Plot world map and then subsets.
    map("world")
    country.names = map("world")$names

    map("world", col = colors, fill = T)
    names = map("world", world.sub, col = colors, fill = T)$names
    # High Resolution
    map("worldHires", world.sub, exact=T, col=colors, fill=T)
    map.cities(pch='.')
    map.text("world", world.sub, add=T, exact=T)
}

save.one = function(){
    quartz.options(bg='white')
    quartz.save('r_mapping_choro_n.png')
    quartz.save('r_mapping_world_n.png')
}


