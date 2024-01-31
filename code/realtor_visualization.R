# Clear the Environment
# Read csv file as a DataFrame

install.packages('ggcorrplot')
install.packages('visreg')
rm(list=ls())
df <- read.table('realtor.csv', header = TRUE, sep = ',')
df <- df[!duplicated(df), ]
df<-df[!(df$Beds==0 | df$Sizes ==0 ),]
df<-df[!(df$Beds==0 | df$Sizes >13000 ),]

price <- df$Price
beds <-df$Beds
baths <- df$Baths
sizes <-df$Sizes
zipcode <- df$Zipcode
nrow(df)
df

plot(sizes,price, main="Scatterplot of Size vs. Price")
options(scipen=999)
plot(baths,price, main="Scatterplot of Baths vs. Price")
plot(beds,price, main="Scatterplot of Beds vs Price")
plot(zipcode,price, main="Scatterplot of Zipcode vs Price")

#
#
logBaths <- log(baths+1)
logBeds <- log(beds+1)
logZip <- log(zipcode)
#
plot(logBaths,price, main="Scatterplot of price vs logBaths")
plot(logBeds,price, main="Scatterplot of price vs logBeds")
plot(logZip,price, main="Scatterplot of Zipcode vs Price")
#
# Checking correlations before and after transformations
#
M1 <- cbind(price, sizes, baths, beds, zipcode)
m1 <- cor(M1)
m1
M2 <- cbind(price, sizes, logBaths, logBeds, zipcode)
m2 <- cor(M2)
library(ppcor)

pcorr <- pcor(M2)
print(pcorr)

library(ggcorrplot)
ggcorrplot(m1, 
           type = "full",
           lab = TRUE)

ggcorrplot(m2, 
           type = "full",
           lab = TRUE)

#
mod1 <- lm(price ~ zipcode) 
summary(mod1)
library(ggplot2)
library(visreg)
visreg(mod1, "sizes", gg = TRUE) 



mod1 <- lm(price ~ sizes)
summary(mod1)


df$pred_price_one_predictor <- predict(mod1)
print(df)



m_reg1 <- lm(price ~ sizes+beds+baths)
summary(m_reg1)


df$pred_price_multiple_predictor <- predict(m_reg1)
#df$Resid_price <- residuals(m_reg1)
print(df)
#prediction mod 1

price_df <- data.frame(sizes=1295)
pred_1295_price <- predict(mod1, price_df) 
print(pred_1295_price)
#prediction mod 2
df_p <- data.frame(sizes=1295, baths=3, beds=2)
print(predict(m_reg1, df_p))

#

library(dplyr)
df %>% count(zipcode)
