setwd("C:\\Users\\lab-user\\Desktop\\Suzuki Lab\\Satoru R Stats") #change it to the directory you want
load("satoru_rws")
ss.starter() #loads the packages
library(readxl)

## Getting in AV motion data from copy/paste
av_motion <- read.clipboard()
View(av_motion)
describe(av_motion)


#Loading data from Excel Files
av_motion_200 <- read_excel("C:\\Users\\lab-user\\Desktop\\AudioVisMotionRatchetExp\\AudioVisMotionRatchetExp_Analysis\\AvMotionData_200.xlsx")
av_motion_250 <- read_excel("C:\\Users\\lab-user\\Desktop\\AudioVisMotionRatchetExp\\AudioVisMotionRatchetExp_Analysis\\AvMotionData_250.xlsx")
av_motion_250_ex <- read_excel("C:\\Users\\lab-user\\Desktop\\AudioVisMotionRatchetExp\\AudioVisMotionRatchetExp_Analysis\\AvMotionData_250_ex.xlsx")

## Make edits in the variable names

av_motion$Sound[av_motion$Sound==1]="InPhase"
av_motion$Sound[av_motion$Sound==2]="OutPhase"
av_motion$Sound[av_motion$Sound==3]="NoSound"

av_motion_200$Sound[av_motion_200$Sound==1]="InPhase"
av_motion_200$Sound[av_motion_200$Sound==2]="OutPhase"
av_motion_200$Sound[av_motion_200$Sound==3]="NoSound"

av_motion_250$Sound[av_motion_250$Sound==1]="InPhase"
av_motion_250$Sound[av_motion_250$Sound==2]="OutPhase"
av_motion_250$Sound[av_motion_250$Sound==3]="NoSound"

av_motion_250_ex$Sound[av_motion_250_ex$Sound==1]="InPhase"
av_motion_250_ex$Sound[av_motion_250_ex$Sound==2]="OutPhase"
av_motion_250_ex$Sound[av_motion_250_ex$Sound==3]="NoSound"

#View and Describe data
View(av_motion_200)
describe(av_motion_200)

View(av_motion_250)
describe(av_motion_250)

View(av_motion_250_ex)
describe(av_motion_250_ex)



## Satoru's functions
summary_av_motion = ss.summarize(av_motion,condcols = c("p", "Sound", "Rotation"), rtcol = "RT")

summary_av_motion_200 = ss.summarize(av_motion_200,condcols = c("p", "Rotation", "Sound"), rtcol = "RT")
summary_av_motion_250 = ss.summarize(av_motion_250,condcols = c("p", "Rotation", "Sound"), rtcol = "RT")
summary_av_motion_250_ex = ss.summarize(av_motion_250_ex,condcols = c("p", "Rotation", "Sound"), rtcol = "RT")


# Bar Plot Tutorial Functions
ss.barplot(summary_av_motion_200, dv = "RT_mean", factors = c("Sound", "Rotation"),framesize= c(5,5), b_width = 1,grid=0, axistitle_font = c("Georgia", 12,"plain","black"), ptitle = "5Hz", ytitle="Duration of MAE", xtitle="Sound Condition", legendtitle = "", legend_pos = "none", f1order=c("InPhase", "OutPhase", "NoSound"), ywin=c(3.5,4.5), ylimits=c(0,8), yticks=c(.5,.25), ydigits=1, select=1, fill_colors = c(rgb(.7,.7,.7), rgb(.5,.5,.5),rgb(.3,.3,.3)))
ss.barplot(summary_av_motion_250, dv = "RT_mean", factors = c("Sound", "Rotation"),framesize= c(5,5), b_width = 1,grid=0, axistitle_font = c("Georgia", 12,"plain","black"), ptitle = "4Hz", ytitle="Duration of MAE", xtitle="Sound Condition", legendtitle = "", legend_pos = "none", f1order=c("InPhase", "OutPhase", "NoSound"), ywin=c(3.5,4.5), ylimits=c(0,8), yticks=c(.5,.25), ydigits=1, select=1, fill_colors = c(rgb(.7,.7,.7), rgb(.5,.5,.5),rgb(.3,.3,.3)))
ss.barplot(summary_av_motion_250_ex, dv = "RT_mean", factors = c("Sound", "Rotation"),framesize= c(5,5), b_width = 1,grid=0, axistitle_font = c("Georgia", 12,"plain","black"), ptitle = "4Hz", ytitle="Duration of MAE", xtitle="Sound Condition", legendtitle = "", legend_pos = "none", f1order=c("InPhase", "OutPhase", "NoSound"), ywin=c(3.5,4.5), ylimits=c(0,8), yticks=c(.5,.25), ydigits=1, select=1, fill_colors = c(rgb(.7,.7,.7), rgb(.5,.5,.5),rgb(.3,.3,.3)))

ss.lineplot(summary_av_motion_200, dv = "RT_mean", factors = c("Sound", "Rotation"))

##ANOVA (Need to feed in only the correct rt data!)
{options(contrasts=c("contr.sum","contr.poly"))
  anova_result = ezANOVA(
    summary_av_motion_200
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

