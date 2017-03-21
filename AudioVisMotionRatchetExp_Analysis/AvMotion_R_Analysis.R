# load required libraries
library(dplyr)
library(psych)
library(readxl)

# set directory and load Satoru stats package
#setwd("/Users/mkaillersmith/Documents/Suzuki Lab/Satoru R Stats/") #change it to the directory you want
setwd("C:\\Users\\lab-user\\Desktop\\Suzuki Lab\\Satoru R Stats\\")
load("ss_psych450_rws")
ss.starter() #loads the packages

# reset directory and load files 
#setwd("/Users/mkaillersmith/Documents/AudioVisMotionRatchetExp/AudioVisMotionRatchetExp_Analysis/")
setwd("C:\\Users\\lab-user\\Desktop\\AudioVisMotionRatchetExp\\AudioVisMotionRatchetExp_Analysis\\")
av_data200 <- read_excel("AvMotionData_200.xlsx", sheet = 1)
av_data250 <- read_excel("AvMotionData_250.xlsx", sheet = 1)

  
# rename Sound conditions
av_data200$Sound[av_data200$Sound == 1] = "InPhase"
av_data200$Sound[av_data200$Sound == 2] = "OutPhase"
av_data200$Sound[av_data200$Sound == 3] = "NoSound"
av_data200$Condition = 200

av_data250$Sound[av_data250$Sound == 1] = "InPhase"
av_data250$Sound[av_data250$Sound == 2] = "OutPhase"
av_data250$Sound[av_data250$Sound == 3] = "NoSound"
av_data250$Condition = 250

# View imported data 
View(av_data200)
describe(av_data200)

View(av_data250)
describe(av_data250)

av_data <- rbind(av_data200, av_data250)
View(av_data)

#################################################################################################################################
##---4Hz Data Analysis---##

# create summary variable of data -- remeber to include "p" in condcols
summary_av_data250 <- ss.summarize(longtable = av_data250, condcols = c("p", "Sound", "Rotation"), rtcol = "RT", trim_type = "mad")
summary_av_data250_collapse <- ss.summarize(longtable = av_data250, condcols = c("p", "Rotation"), rtcol = "RT", trim_type = "mad") # used mad to trim outliers by subject, exculded "Sound" to collapse overall RT mean

# plot data
##plot by within and between factors
ss.lineplot(longtable = summary_av_data250, dv = "RT_mean", factors = c("Sound", "Rotation"))
## plot subject data
ss.lineplot(longtable = summary_av_data250, dv = "RT_mean", factors = c("Sound", "p"), select = 3)
## barplot
ss.barplot(subset(summary_av_data250), dv = "RT_mean", factors = c("Sound", "Rotation"),framesize= c(5,5), b_width = 1,grid=0, axistitle_font = c("Georgia", 12,"plain","black"), ptitle = "4Hz", ytitle="Duration of MAE", xtitle="Sound Condition", legendtitle = "", legend_pos = "none", f1order=c("InPhase", "OutPhase", "NoSound"), ywin=c(3.5,4.5), ylimits=c(0,8), yticks=c(.5,.25), ydigits=1, select=1, fill_colors = c("red", "green", "blue"))

# median split analysis
## sorts 4Hz data by RT_mean -- used to observe differences between short and long MAE duration and Phase effect
arrange(ss.lineplot(summary_av_data250, dv = "RT_mean",factors = "p", tables = 1), RT_mean)
## short MAE
ss.barplot(subset(summary_av_data250, p != 27 & p != 23 & p != 31 & p != 32 & p != 24 & p != 20 & p != 34 & p != 30 & p != 35 & p != 33), dv = "RT_mean", factors = c("Sound", "Rotation"),framesize= c(5,5), b_width = 1,grid=0, axistitle_font = c("Georgia", 12,"plain","black"), ptitle = "4Hz - short", ytitle="Duration of MAE", xtitle="Sound Condition", legendtitle = "", legend_pos = "none", f1order=c("InPhase", "OutPhase", "NoSound"), ywin=c(2.5,3.5), ylimits=c(0,8), yticks=c(.5,.25), ydigits=1, select=1, fill_colors = c(rgb(.7,.7,.7), rgb(.5,.5,.5),rgb(.3,.3,.3)))
## long MAE
ss.barplot(subset(summary_av_data250, p != 18 & p != 36 & p != 17 & p != 22 & p != 26 & p != 21 & p != 29 & p != 19 & p != 25 & p != 28), dv = "RT_mean", factors = c("Sound", "Rotation"),framesize= c(5,5), b_width = 1,grid=0, axistitle_font = c("Georgia", 12,"plain","black"), ptitle = "4Hz - long", ytitle="Duration of MAE", xtitle="Sound Condition", legendtitle = "", legend_pos = "none", f1order=c("InPhase", "OutPhase", "NoSound"), ywin=c(5.5,6.5), ylimits=c(0,8), yticks=c(.5,.25), ydigits=1, select=1, fill_colors = c(rgb(.7,.7,.7), rgb(.5,.5,.5),rgb(.3,.3,.3)))

## barplot -- excludes particpants with mean RT > 5.0 sec
ss.barplot(subset(summary_av_data250, p != 33 & p != 35 & p != 30 & p != 34 & p != 20 & p != 24), dv = "RT_mean", factors = c("Sound", "Rotation"),framesize= c(5,5), b_width = 1,grid=0, axistitle_font = c("Georgia", 12,"plain","black"), ptitle = "4Hz - long", ytitle="Duration of MAE", xtitle="Sound Condition", legendtitle = "", legend_pos = "none", f1order=c("InPhase", "OutPhase", "NoSound"), ywin=c(2.5,4.5), ylimits=c(0,8), yticks=c(.5,.25), ydigits=1, select=1, fill_colors = c(rgb(.7,.7,.7), rgb(.5,.5,.5),rgb(.3,.3,.3)))


# correlational analysis - desired outcome X RT_mean
## Creat new data frames with only In or Out Phase data to to perform desired pattern comparison
summary_av_data250_Out <- subset(summary_av_data250, Sound == "OutPhase")
summary_av_data250_In <- subset(summary_av_data250, Sound == "InPhase")

## OutMinusIn = subject RT_mean of OutPhase - In Phase (calculation to set up correlation between desired phase outcome and overall mean RT)
summary_av_data250_In$OutMinusIn <- summary_av_data250_Out$RT_mean - summary_av_data250_In$RT_mean
summary_av_data250_In$RT_overall <- summary_av_data250_collapse$RT_mean

## correlation scatter plots - used to identify correlation between desired outcome(OutPhase-InPhase) and overall mean RT
ss.scatter_wt(summary_av_data250_In, xitem = "RT_overall", yitems = "OutMinusIn")
ss.scatter_wt(summary_av_data250_In, xitem = "RT_overall", yitems = "OutMinusIn", fits = "poly1") # adds correlation line with poly1
ss.scatter_wt(summary_av_data250_In, xitem = "RT_overall", yitems = "OutMinusIn", fits = "poly1", stats = 1) # adds stats with intercept ans slope b1 = slope
ss.scatter_wt(summary_av_data250_In, xitem = "RT_overall", yitems = "OutMinusIn", fits = "poly1", conf_ellipse = .99) # adds confidence ellipse with 99% confidence interval 
ss.scatter_wt(summary_av_data250_In, xitem = "RT_overall", yitems = "OutMinusIn", fits = "poly1", conf_ellipse = 0) # adds confidence ellipse with 99% confidence interval 

## Exclude Outliers based on correlation scatterplot eyeball - 99% confidence ellipse
ss.barplot(subset(summary_av_data250, p != 33 & p != 35 & p != 34), tables = 1, dv = "RT_mean", factors = c("Sound", "Rotation"),framesize= c(5,5), b_width = 1,grid=0, axistitle_font = c("Georgia", 12,"plain","black"), ptitle = "4Hz", ytitle="Duration of MAE", xtitle="Sound Condition", legendtitle = "", legend_pos = "none", f1order=c("InPhase", "OutPhase", "NoSound"), ywin=c(3.5,4.5), ylimits=c(0,8), yticks=c(.5,.25), ydigits=1, select=1, fill_colors = c("red", "green", "blue"))

# ANOVA av_data250 -- (Need to feed in only the correct rt data!)
{options(contrasts=c("contr.sum","contr.poly"))
  anova_result = ezANOVA(
    subset(summary_av_data250,p != 33 & p != 35 & p != 34) 
    , dv = .(RT_mean)
    , wid = .(p)
    , within = .(Sound)
    , between = .(Rotation)
    , observed = NULL
    , diff = NULL
    , reverse_diff = FALSE
    , type = 3
    , white.adjust = FALSE
    , detailed = FALSE
    , return_aov = TRUE ## FALSE for not showing details
  )
  print(anova_result)}

#################################################################################################################################
##---5Hz Data Analysis---##

# create summary variable of data -- remeber to include "p" in condcols
summary_av_data200 <- ss.summarize(longtable = av_data200, condcols = c("p","Sound", "Rotation"), rtcol = "RT", trim_type = "mad")
summary_av_data200_collapse <- ss.summarize(longtable = av_data200, condcols = c("p", "Rotation"), rtcol = "RT", trim_type = "mad") # used mad to trim outliers by subject, exculded "Sound" to collapse overall RT mean

# trial split comparison
summary_av_data200_first <- ss.summarize(subset(av_data200, Trial <= 60), condcols = c("p","Sound", "Rotation"), rtcol = "RT")
summary_av_data200_last <- ss.summarize(subset(av_data200, Trial >=61), condcols = c("p","Sound", "Rotation"), rtcol = "RT")

# plot data
##plot by within and between factors
ss.lineplot(longtable = summary_av_data200, dv = "RT_mean", factors = c("Sound", "Rotation"))

## plot subject data
ss.lineplot(longtable = summary_av_data200, dv = "RT_mean", factors = c("Sound", "p"), select = 3)

## barplot 
ss.barplot(summary_av_data200, dv = "RT_mean", factors = c("Sound", "Rotation"),framesize= c(5,5), tables = 1, b_width = 1,grid=0, axistitle_font = c("Georgia", 12,"plain","black"), ptitle = "5Hz", ytitle="Duration of MAE", xtitle="Sound Condition", legendtitle = "", legend_pos = "none", f1order=c("InPhase", "OutPhase", "NoSound"), ywin=c(3.5,4.5), ylimits=c(0,8), yticks=c(.5,.25), ydigits=1, select=1, fill_colors = c("red", "green", "blue"))

## barplot first/last half trials
ss.barplot(summary_av_data200_first, dv = "RT_mean", factors = c("Sound", "Rotation"),framesize= c(5,5), b_width = 1,grid=0, axistitle_font = c("Georgia", 12,"plain","black"), ptitle = "5Hz - First", ytitle="Duration of MAE", xtitle="Sound Condition", legendtitle = "", legend_pos = "none", f1order=c("InPhase", "OutPhase", "NoSound"), ywin=c(3.5,4.5), ylimits=c(0,8), yticks=c(.5,.25), ydigits=1, select=1, fill_colors = c(rgb(.7,.7,.7), rgb(.5,.5,.5),rgb(.3,.3,.3)))
ss.barplot(summary_av_data200_last, dv = "RT_mean", factors = c("Sound", "Rotation"),framesize= c(5,5), b_width = 1,grid=0, axistitle_font = c("Georgia", 12,"plain","black"), ptitle = "5Hz - Last", ytitle="Duration of MAE", xtitle="Sound Condition", legendtitle = "", legend_pos = "none", f1order=c("InPhase", "OutPhase", "NoSound"), ywin=c(3.5,4.5), ylimits=c(0,8), yticks=c(.5,.25), ydigits=1, select=1, fill_colors = c(rgb(.7,.7,.7), rgb(.5,.5,.5),rgb(.3,.3,.3)))

# median split analysis
## sorts 4Hz data by RT_mean -- used to observe differences between short and long MAE duration and Phase effect
arrange(ss.lineplot(summary_av_data200, dv = "RT_mean",factors = "p", tables = 1), RT_mean)
## short MAE
ss.barplot(subset(summary_av_data200, p != 8 & p != 11 & p != 42 & p != 15 & p != 14 & p != 38 & p != 7 & p != 9 & p != 10), dv = "RT_mean", factors = c("Sound", "Rotation"),framesize= c(5,5), b_width = 1,grid=0, axistitle_font = c("Georgia", 12,"plain","black"), ptitle = "5Hz - short", ytitle="Duration of MAE", xtitle="Sound Condition", legendtitle = "", legend_pos = "none", f1order=c("InPhase", "OutPhase", "NoSound"), ywin=c(2.5,3.5), ylimits=c(0,8), yticks=c(.5,.25), ydigits=1, select=1, fill_colors = c(rgb(.7,.7,.7), rgb(.5,.5,.5),rgb(.3,.3,.3)))
## long MAE
ss.barplot(subset(summary_av_data200, p != 37 & p != 41 & p != 39 & p != 13 & p != 16 & p != 40 & p != 43 & p != 12 & p != 44), dv = "RT_mean", factors = c("Sound", "Rotation"),framesize= c(5,5), b_width = 1,grid=0, axistitle_font = c("Georgia", 12,"plain","black"), ptitle = "5Hz - long", ytitle="Duration of MAE", xtitle="Sound Condition", legendtitle = "", legend_pos = "none", f1order=c("InPhase", "OutPhase", "NoSound"), ywin=c(4.5,5.5), ylimits=c(0,8), yticks=c(.5,.25), ydigits=1, select=1, fill_colors = c(rgb(.7,.7,.7), rgb(.5,.5,.5),rgb(.3,.3,.3)))

## bar plot excluding particpants with RT_mean > 5.0 secs
ss.barplot(subset(summary_av_data200, p != 9 & p != 10), dv = "RT_mean", factors = c("Sound", "Rotation"),framesize= c(5,5), b_width = 1,grid=0, axistitle_font = c("Georgia", 12,"plain","black"), ptitle = "5Hz - exclude 7, 9 & 10", ytitle="Duration of MAE", xtitle="Sound Condition", legendtitle = "", legend_pos = "none", f1order=c("InPhase", "OutPhase", "NoSound"), ywin=c(3.0,4.0), ylimits=c(0,8), yticks=c(.5,.25), ydigits=1, select=1, fill_colors = c(rgb(.7,.7,.7), rgb(.5,.5,.5),rgb(.3,.3,.3)))

# correlational analysis - desired outcome X RT_mean
## Creat new data frames with only In or Out Phase data to to perform desired pattern comparison
summary_av_data200_Out <- subset(summary_av_data200, Sound == "OutPhase")
summary_av_data200_In <- subset(summary_av_data200, Sound == "InPhase")

## OutMinusIn = subject RT_mean of OutPhase - In Phase (calculation to set up correlation between desired phase outcome and overall mean RT)
summary_av_data200_In$OutMinusIn <- summary_av_data200_Out$RT_mean - summary_av_data200_In$RT_mean
summary_av_data200_In$RT_overall <- summary_av_data200_collapse$RT_mean

## correlation scatter plots - used to identify correlation between desired outcome(OutPhase-InPhase) and overall mean RT
ss.scatter_wt(summary_av_data200_In, xitem = "RT_overall", yitems = "OutMinusIn")
ss.scatter_wt(summary_av_data200_In, xitem = "RT_overall", yitems = "OutMinusIn", fits = "poly1") # adds correlation line with poly1
ss.scatter_wt(summary_av_data200_In, xitem = "RT_overall", yitems = "OutMinusIn", fits = "poly1", stats = 1) # adds stats with intercept ans slope b1 = slope
ss.scatter_wt(summary_av_data200_In, xitem = "RT_overall", yitems = "OutMinusIn", fits = "poly1", conf_ellipse = .99) # adds confidence ellipse with 99% confidence interval 
ss.scatter_wt(summary_av_data200_In, xitem = "RT_overall", yitems = "OutMinusIn", fits = "poly1", conf_ellipse = 0) # adds confidence ellipse with 99% confidence interval 


# ANOVA av_data200 -- (Need to feed in only the correct rt data!)
{options(contrasts=c("contr.sum","contr.poly"))
  anova_result = ezANOVA(
    subset(summary_av_data200, Sound != "OutPhase"), 
    , dv = .(RT_mean)
    , wid = .(p)
    , within = .(Sound)
    , between = .(Rotation)
    , observed = NULL
    , diff = NULL
    , reverse_diff = FALSE
    , type = 3
    , white.adjust = FALSE
    , detailed = FALSE
    , return_aov = TRUE ## FALSE for not showing details
  )
  print(anova_result)}


######################################################################################################################
##---4Hz vs 5Hz---##

summary_av_data <- ss.summarize(longtable = av_data, condcols = c("p","Sound", "Condition", "Rotation"), rtcol = "RT", trim_type = "mad")

# ANOVA av_data -- (Need to feed in only the correct rt data!)
{options(contrasts=c("contr.sum","contr.poly"))
  anova_result = ezANOVA(
    summary_av_data 
    , dv = .(RT_mean)
    , wid = .(p)
    , within = .(Sound)
    , between = .(Condition)
    , observed = NULL
    , diff = NULL
    , reverse_diff = FALSE
    , type = 2
    , white.adjust = FALSE
    , detailed = FALSE
    , return_aov = TRUE ## FALSE for not showing details
  )
  print(anova_result)}
