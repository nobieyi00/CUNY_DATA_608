library(shiny)
library(ggplot2)
library(plotly)
#install.packages('plotly')
mortality_data<-read.csv("https://raw.githubusercontent.com/charleyferrari/CUNY_DATA_608/master/module3/data/cleaned-cdc-mortality-1999-2010-2.csv")
mortality1<-subset(mortality_data, Year=='2010')

ui <- fluidPage(
 
  # Give the page a title
  titlePanel("2010 Mortality Rate by State for a disease Cause"),
  
  selectInput("Mortality", "Mortality Cause:", 
              choices=as.vector(unique(mortality1$ICD.Chapter))),
  
  # Create a spot for the barplot
  mainPanel(
    
    plotlyOutput("MortalityPlot",width = "500%")
  )
  
  
)

server <- function(input, output) {
  
  
  #mortality_sub <-subset(mortality1, ICD.Chapter==input$Mortality) 
  # Fill in the spot we created for a plot
  
  output$MortalityPlot <- renderPlotly({
    plot_ly(subset(mortality1, ICD.Chapter==input$Mortality), x =~Crude.Rate , y =~State , height = 600, width = 500)
  
  })
 

}

shinyApp(ui = ui, server = server)