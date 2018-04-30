library(shiny)
library(ggplot2)
library(reshape2)
dataset_euro<-read.csv("https://raw.githubusercontent.com/nobieyi00/CUNY_DATA_608/master/module6/hlth_cd_anr_1_Data.csv")
head(dataset_euro)
m1 <- subset(dataset_euro,SEX != 'Total') #filter out aggregated rows
m2 <- subset(m1,AGE == 'Total')

#convert Value column to numeric
m2$Value <- as.numeric(gsub('[,]', '', m2$Value))

#filter out rows with NA value
m3<- subset(m2, is.na(Value) == FALSE)

m4 <- subset(m3, ICD10 !='All causes of death (A00-Y89) excluding S00-T98')
#m5<- subset(m4,GEO=='Bulgaria')

#ggplot(data=m5, aes(x=ICD10, y=Value, fill = SEX)) +
 # geom_bar(stat="identity",position=position_dodge()) 

# Define UI for application that draws a histogram
ui <- fluidPage(
  
  # Application title
  titlePanel("Number of Deaths due to Diseases in Europe"),
  
  selectInput("Country", "Country:", 
              choices=as.vector(unique(m4$GEO))),
  
  
  # Create a spot for the barplot
  mainPanel(
    plotOutput("MortalityPlot")  
  )
  
)

# Define server logic required to draw a histogram ----
server <- function(input, output) {
  
 
  output$MortalityPlot<- renderPlot({
    
    m5<- subset(m4,GEO==input$Country)
    
    ggplot(data=m5, aes(x=ICD10, y=Value, fill = SEX)) +
      geom_bar(stat="identity",position=position_dodge()) 
    
  }, height = 600, width = 930)
  
}

# Run the application 
shinyApp(ui = ui, server = server)

