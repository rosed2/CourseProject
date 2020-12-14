# CS 410 CourseProject

<ins>Project Proposal:</ins>     
We will be recreating the paper "Latent Aspect Rating Analysis Without Aspect Keyword Supervision."     

<ins>Code Overview:</ins>   
This code tries to implement Latent Aspect Rating Analysis (LARA) as a reproduction of research paper “Latent Aspect Rating Analysis without Aspect Keyword Supervision” by Hongning Wang, Yue Lu, and ChengXiang Zhai. It takes a set of reviews and a list of aspects/topics covered within them. It also takes a list of feature words for each topic. Then, it finds the reviewer’s ratings on these aspects and the weights the reviewer placed on these aspects to form the overall rating. This code can be used to analyze TripAdvisor reviews to find ratings on the following topics: Value, Rooms, Location, Cleanliness, Check in/front desk, Service, and Business service; and what weights the reviewer placed on each topic to construct the overall rating.      
      
<ins>Implementation:</ins>      
The code first preprocesses the reviews by removing stop words and stemming. Then the code assigns what topic each sentence in each review is about by comparing it to a list of user-defined topic feature words. The sentence is assigned the topic whose feature words it has the most of. Then, it uses sentiment analysis to determine topic ratings for each topic in each review. Next, it uses random variable initialization to determine the weights placed on each topic by the reviewer. We calculated which set of random weights returned the highest probability of getting the reviewer’s overall rating from a Normal distribution whose mean was the weighted mean of the aspect ratings we found.      
    
<ins>Software Usage Tutorial Presentation:</ins>     
https://illinois.zoom.us/rec/share/aHaip21p63f29jFbE96x2s2LgFm9d6Pa4qIdLK3IwpMeqnh-pJqWV9ZXdbejbLHJ.ThV8W0Z9PVQhu4fv?startTime=1607902233000      
      
<ins>Usage Notes:</ins>    
The code requires nltk, scipy, and numpy. Install using pip or other preferred python installation method.     
To use this code, download the repository, cd into the folder, and run the python file “code.py”.     
      
<ins>Main Results:</ins>     
We found the aspect ratings and aspect weights for every review we parsed in the file “test_result.txt”. To evaluate, we found the mean squared error of the aspect ratings was 2.383. In the paper, the desired result of the MSE was 2.130. Our result differed from the desired result by a very small amount. This difference could be due to the fact that we might’ve used a different sentiment analysis library and we weren’t sure how to handle large amounts of neutral words. We also weren’t sure how to determine the aspect weights, so we instead used a brute force approach where we tested random weights while the paper used gradient optimization but we couldn’t get that to work.      
    
<ins>Team Contributions:</ins>    
Rose Dinh: Worked on preprocessing, assigning topics to each sentence, and determining ratings of topics in each review     
Archisha Majee: Worked on determining topic weights and finding MSE to evaluate the results     


