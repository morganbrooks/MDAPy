# This line we use to get the arguments sent to Rscript by the subprocess
args = commandArgs(trailingOnly=TRUE)
# then we list all required code and install, load the packages.
pkgs <- c("IsoplotR")
installed <- (pkgs %in% rownames(installed.packages()))
if (!all(installed)) {install.packages(pkgs[!installed], repos = "http://cran.us.r-project.org")}
load_all_libraries <- lapply(pkgs, require, character.only = TRUE)
# note that the working directory is important here, otherwise you will need to provide a full path to the folder containing the data.
file <- paste0(getwd(), "/", args[1]) 
# we load the data 
mixtures <- read.csv2(file, dec = "." , sep = ",", colClasses = c('numeric','numeric'))
# set where the file will be saved (note that the second argumetn is used to name the image file)
png(filename = paste0("/assets/plots/IsoplotR/plot_", args[2], ".png"))
# then we generate the plot
radialplot(mixture, k = 'min', bg ='cornflowerblue', transformation='log', sigdig=2,alpha=0.05)
# save on disk
invisible(dev.off())
# and calculate the parameter, returning it to python
cat(peakfit(mixture, k = 'min', sigdig = 2, alpha=0.05)$peaks[1])




