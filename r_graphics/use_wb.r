# Lattice plots for World Bank energy data.
library(lattice)
library(latticeExtra)
#library(rjson)


# ####################### data prep ########################## #

extension = '.csv'
names = c('EG.IMP.CONS.ZS', 'EG.USE.COMM.KT.OE', 'EG.EGY.PROD.KT.OE',
        'NY.GDP.MKTP.KD')   
fnames = sapply( names, function(name) paste(name, extension, sep=''))

get.data = function(fname){
    d = read.csv(fname, head=FALSE, sep='\t')
    names(d) = c('year', 'country', 'pct')
    return (d)
}

# Read the files.
importp = get.data(fnames[1]) # imports (% of use)
consume = get.data(fnames[2]) # use (KT)
produce = get.data(fnames[3]) # production (KT)
gdp = get.data(fnames[4]) # 'GDP (constant 2000 US$)'
names(consume) = c('year', 'country', 'vol')
names(produce) = c('year', 'country', 'vol')
names(gdp) = c('year', 'country', 'gdp')

# See if import == (consume-produce)/consume
target = (consume$vol-produce$vol) / consume$vol * 100
my.diff = target - importp$pct < 0.00000001
# yes.

# Get imports as volume instead of pct consumed.
import = importp
names(import) = c('year', 'country', 'vol')
import$vol = consume$vol-produce$vol

energy = data.frame(cbind(import, produce$vol, consume$vol, importp$pct))
names(energy) = c('year', 'country', 'import', 'produce', 'consume', 'importp')


country.names = levels(energy$country)

# ####################### Lattice ########################## #
# Define a shingle for GDP
av.gdp = by(gdp$gdp, gdp$country, mean)
energy$gdp = unlist(lapply(av.gdp, function(x) rep(x,30)))
energy$gdp = shingle(energy$gdp, co.intervals(energy$gdp, 3, overlap=-.5))
# NOTE negative overlap
# negative overlap because zero overlap includes overlap.


# type=c('p', 'l') == type='o'

lat.colors = heat.colors(10)
lat.colors = cm.colors(10)
lat.colors = terrain.colors(10)
lat.colors = topo.colors(10)
lat.colors = 1:10
lat.lty = 1:10
lat.lwd = 2

# Legend
key.list = list(
    text=list(levels(energy$country)),
    lines=list(col=lat.colors, lty=lat.lty, lwd=lat.lwd),
    space='right'
    )

# Panel function for grid lines
year.ticks = seq(from=1980, to=2010, by=5)
xy.pan = function(...){
    panel.abline(h=0, v=year.ticks, col='darkgray', lty=3)
    panel.xyplot(..., lty=lat.lty, lwd=lat.lwd)
    }

xyplot(import~year | gdp , group=country, data=energy,  
    type=c('l'), col=lat.colors,
    auto.key=TRUE, key=key.list,
    ylab=expression("Energy Imports (MT Oil Equivalent)"),
    xlab=expression("Year"),
    scales=list(
        x=list(rot=45),
        y=list(at=c(-5*10^5, 0, 5*10^5), lab=c(-500, 0, 500))
    ),
    panel=xy.pan,
    )

xyplot(import~year | gdp , group=country, data=energy,  
    type=c('l'), col=lat.colors,
    auto.key=TRUE, key=key.list
    ) 

#    ylab=expression("Energy imports (KT Oil Equivalent)"^2),
# xy.strip = function(...){
#     strip.names = c('a', 'b', 'c')   # no effect
#     strip.default(...)
#     }
#    strip=xy.strip,


# ##### file output ######## #

if (0){
quartz.options(bg='white')
quartz.save('wb.latticex.png')
}


# ####################### GGplot2 ########################## #
library(ggplot2)

energy$gdp.f = 'med'
energy[energy$country=="DE",]$gdp.f = 'high'
energy[energy$country=="JP",]$gdp.f = 'high'
energy[energy$country=="US",]$gdp.f = 'high'
energy[energy$country=="IN",]$gdp.f = 'low'
energy[energy$country=="MX",]$gdp.f = 'low'
energy[energy$country=="RU",]$gdp.f = 'low'


p = ggplot(energy, aes(year, import)) + 
    geom_line(aes(color=country, linetype=country)) +
    facet_wrap(~gdp.f)

y.grid = seq(-7*10^5,7*10^5, 10^5)
x.grid = seq(1980,2010,5)
y.tick.labs = seq(-600,600,200)
y.ticks = y.tick.labs * 1000

p = ggplot(energy, aes(year, import)) + 

    # Remove grid lines by overplotting.
    geom_hline(yintercept=y.grid, alpha=1, size=4, color='white') +
    geom_vline(xintercept=x.grid, alpha=1, size=4, color='white') +

    # New grid lines.
    geom_hline(yintercept=0, alpha=0.5, size=.4, linetype=3) +
    geom_vline(xintercept=x.grid, alpha=0.4, size=.4, linetype=3) +

    # The plots
    geom_line(aes(color=country, linetype=country)) +
    facet_wrap(~gdp.f) +
    
    # Decoration
    theme_bw() +
    scale_y_continuous(breaks=y.ticks, labels=y.tick.labs,
        name = "Energy Imports (MT Oil Equivalent)"
    ) +
    scale_x_continuous(name='Year') +
    opts(
        axis.text.x=theme_text(angle=45),
        legend.title = theme_blank()
    )

 
# http://stackoverflow.com/questions/6022898/how-can-i-remove-the-legend-title-in-ggplot2
# Answer near the bottom from Yuriy Petrovskiy is the only useful answer.




# problem with
#    geom_line(aes(color=country, linetype=1:10)) + 
# http://groups.google.com/group/ggplot2/browse_thread/thread/b3d65dc14933e74b
#
# h whickam says:
#
# You should never give vectors of values inside an aes call, since the
# way that they are combined with the existing data is unpredictable (I'd
# make it an error if I could figure out how).  If you can add those
# values to the data frame and then map that variable to linetype you
# should be fine.

# http://osdir.com/ml/ggplot2/2011-08/msg00023.html
# combine all geoms into one legend ???


if (0){
quartz.options(bg='white')
quartz.save('wb.ggplotx.png')
}

# ############ advantage Lattice #########
# shingle
# linetype  ???
# gridlines 
# rotated tick labels
# maturity
# continuity with model specification


# ############ advantage Ggplot2 #########
# legend          ??????
# http://had.co.nz/ggplot2/scale_manual.html
# theme_get()
# learning curve
# documentation
# community
# coding speed
 


