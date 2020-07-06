#!/usr/bin Rscript
# setup a powerpoint
# packages ----------------------------------------------------------------
library(magrittr)
library(officer)
library(data.table)
library(ggplot2)
library(knitr)

# create_powerpoint -------------------------------------------------------
# open the file and create the pres object
# file_name <- officer::read_pptx('template.pptx')
file_name <- officer::read_pptx('blank.pptx')
message(sprintf('Using %s as template', file_name))
pres <- officer::read_pptx(file_name)

# retrieve the layouts, so we know what we can layout
available_layouts <- data.table::data.table(layout_summary(pres))
message(sprintf('Layout Summary:\n%s', layout_summary(pres)))

# the blank pptx can have slides added to it, the template.pptx is the one
# created specifically for this project
layouts <- available_layouts[['layout']]  # ensure use of a valid layout
# generate the slides -----------------------------------------------------



# Export thte file --------------------------------------------------------
# this will be the final write out name
file_out_name <- paste0('/tmp/', 'NowCast_',
                        format(Sys.time(), format = '%Y-%M-%D_%H%M%S'), '.pptx')
# print out the file, do a direct call to check for errors
officer::print.rpptx(pres, file_out_name)
