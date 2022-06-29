df<-read.csv("/media/esmx/dane/git/lfa/python/qp.csv")
head(df)
df<-df[-c(1,2,3,4),]
head(df)
print("1 spread")
summary(df$ask-df$bid)
sd(df$ask-df$bid)

print("2 spread")
summary(df$ask2-df$bid2)
sd(df$ask2-df$bid2)

print("diff ask")
summary(df$ask2-df$ask)
sd(df$ask2-df$ask)

plot((df$ask2-df$ask), ylim=c(min(df$ask2-df$ask)-30,max(df$ask2-df$ask)+30 ),type="l",col=2)
plot((df$ask2-df$ask), ylim=c(min(df$ask2-df$ask)-3,max(df$ask2-df$ask)+3 ),type="l",col=2)
abline(h=seq(-180,-140,10))
print("diff bid")
summary(df$bid2-df$bid)
sd(df$bid2-df$bid)

points(x=df$X,(df$bid2-df$bid), type="l",col=3)
min(df$timestamp)
head(df)

print("diff price")
max(df$ask2-df$ask)-min(df$ask2-df$ask)


############################
df<-read.csv("/media/esmx/dane/git/lfa/python/qp.dax_arb.csv")
head(df)
df<-df[-c(1,2,3,4),]
head(df)

df$eu<-(df$bid3+df$bid4+df$ask3+df$ask4)
df$dax<-(df$ask+df$ask2+df$bid+df$bid2)/2.0
df$diff<-df$dax-df$eu

# DAX *5
# EU  *10
summary(df$eu)
summary(df$dax)
summary(df$diff)
sd(df$eu)
sd(df$dax)
sd(df$diff)

par(mfrow=c(1,1))

par(mfrow=c(1,3))
plot(df$eu, type="l",col=2)
plot((df$dax), type="l",col=2)
plot((df$diff), type="l",col=2)



abline(h=seq(-180,-140,10))
print("diff bid")
summary(df$bid2-df$bid)
sd(df$bid2-df$bid)

points(x=df$X,(df$bid2-df$bid), type="l",col=3)
min(df$timestamp)
head(df)

print("diff price")
max(df$ask2-df$ask)-min(df$ask2-df$ask)
