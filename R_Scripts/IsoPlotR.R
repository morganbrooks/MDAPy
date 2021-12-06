# This line we use to get the arguments sent to Rscript by the subprocess
args = commandArgs(trailingOnly = TRUE)
# then we list all required code and install, load the packages.
invisible({
    suppressPackageStartupMessages({
  pkgs <- c("IsoplotR", "dplyr", "rjson", "openxlsx", "readxl")
  installed <- (pkgs %in% rownames(installed.packages()))
  if (!all(installed)) {install.packages(pkgs[!installed], quiet = TRUE, 
                                         verbose = FALSE,
                                         repos = "http://cran.us.r-project.org")}
  load_all_libraries <- lapply(pkgs, require, character.only = TRUE)
        })
  # note that the working directory is important here, otherwise you will need to
  # provide a full path to the folder containing the data.
  file <- paste0(getwd(), "/", args[1])
  # we load the data
  # data <- read.xlsx(file, sheet = "Data")
  data <- read_excel(file, sheet = "Data")
  #
  samples <- rjson::fromJSON(args[2])
  #
  peak_values <- sapply(samples, function(sample) {
    mixtures <- data %>% filter(Sample_ID == sample) %>% select(-Sample_ID)
    # then we generate the plot
    png(filename = paste0(getwd(), "/assets/plots/IsoplotR/plot_", sample, ".png"))
    radialplot(as.data.frame(mixtures), k = 'min', bg = 'cornflowerblue', transformation='log', sigdig=2,alpha=0.05)
    invisible(dev.off())
    svg(filename = paste0(getwd(), "/assets/plots/IsoplotR/plot_", sample, ".svg"))
    radialplot(as.data.frame(mixtures), k = 'min', bg = 'cornflowerblue', transformation='log', sigdig=2,alpha=0.05)
    invisible(dev.off())
    #title(main = sample, adj = 1, line = 2)
    # save on disk
    # and calculate the parameter, returning it to python
   peakfit(as.data.frame(mixtures), k = 'min', sigdig = 2, alpha = 0.05)$peaks
    }, simplify = FALSE, USE.NAMES = TRUE)
  })
#
cat(rjson::toJSON(peak_values))
