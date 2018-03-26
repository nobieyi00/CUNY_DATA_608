library(shiny)
library(ggplot2)
library(reshape2)
mortality_data<-read.csv("https://raw.githubusercontent.com/charleyferrari/CUNY_DATA_608/master/module3/data/cleaned-cdc-mortality-1999-2010-2.csv")
m1 <- mortality_data %>% group_by(Year,ICD.Chapter)
m2<- m1 %>% summarise(total_deaths = sum(Deaths), total_Population = sum(Population))
m3 <- m2 %>% mutate(National_mortality_rate =total_deaths/total_Population)


# Define UI for application that draws a histogram
ui <- fluidPage(
   
   # Application title
   titlePanel("Rate of change of Mortality rates State vs National"),
   
   selectInput("State", "State:", 
               choices=as.vector(unique(mortality_data$State))),
  
   selectInput("Mortality", "Mortality Cause:", 
               choices=""),
   #as.vector(unique(mortality1$ICD.Chapter))
   
   # Create a spot for the barplot
   mainPanel(
     plotOutput("MortalityPlot")  
   )
   
)

# Define server logic required to draw a histogram
server <- function(input, output, session) {
  
  # outVar = reactive({
  #   mydata = get(input$State)
  #   #names(mydata)
  #   #subset(mortality_data, State==mydata)
  #   as.vector(unique((subset(mortality_data, State==mydata))$ICD.Chapter))
  # })
  # observe({
  #   updateSelectInput(session, "Mortality",
  #                     choices = outVar()
  #   )})
   
  
  observe({
    x <- input$State
    
    # Can use character(0) to remove all choices
    if (is.null(x))
      x <- character(0)
    
    # Can also set the label and select items
    updateSelectInput(session, "Mortality",
                      #label = paste("Select input label", length(x)),
                      choices = as.vector(unique((subset(mortality_data, State==x))$ICD.Chapter))
                      #,selected = tail(x, 1)
    )
  })
  output$MortalityPlot <- renderPlot({
    
    mortality_2 <-subset(mortality_data, ICD.Chapter==input$Mortality)
    mortality_sub_state <-subset(mortality_2, State==input$State)
    mortality_sub_state1 <- mortality_sub_state %>% mutate(State_mortality_rate =Deaths/Population)
    m4 <-mortality_sub_state1 %>% inner_join(m3, by=c('Year','ICD.Chapter'))
    m5 <- m4[c('Year','State_mortality_rate','National_mortality_rate')]
    
    for (i in 1:(nrow(m5))){
      
      m5$State_mort_Velocity[i] <- (m5$State_mortality_rate[i+1] - m5$State_mortality_rate[i])/(m5$Year[i+1] -m5$Year[i])
      m5$National_mort_Velocity[i] <- (m5$National_mortality_rate[i+1] -m5$National_mortality_rate[i])/(m5$Year[i+1]-m5$Year[i])
    }

    
    m6 <- m5[c('Year','State_mort_Velocity','National_mort_Velocity' )]

    mdf <- melt(m6,id.vars="Year" ,varnames=c("Mortality_rate_type"), value.name = "Mortality_rate_value")
    
    # Render a barplot
    ggplot(data=mdf, aes(x=Year, y=Mortality_rate_value, group = variable, colour = variable)) +
      geom_point() +
      geom_smooth()
    
    
    
  }, height = 500, width = 800)
}

# Run the application 
shinyApp(ui = ui, server = server)

