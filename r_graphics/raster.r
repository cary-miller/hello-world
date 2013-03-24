
library(raster)
library(rasterVis)
library(colorspace)

#setwd('git-repos/hello-world/r_graphics')

ext <- extent(65, 135, 5, 55)

if (0){
    # 
    fname =  '~/data/875430rgb-167772161.0.FLOAT.TIFF'
    fname =  '~/data/world_map.tiff'
    pop <- raster(fname)
    pop <- crop(pop, ext)
    pop[pop==99999] <- NA
    pTotal <- levelplot(pop, zscaleLog=10, par.settings=BTCTheme)
    pTotal
}


