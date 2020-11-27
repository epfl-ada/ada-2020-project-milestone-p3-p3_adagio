Title: What is status (in Epinions dataset)?

Abstract: Moulik

Research questions: assuming that the results found in the paper hold (temporal directed triads are consistent with status theory), can we build a model that will predict the relative status of each node (positive or negative link) using the features at our disposition?
Which features explain best status?
?????

Proposed dataset: Epinions dataset from the paper as well as the extended dataset http://trustlet.org/extended_epinions.html
* articles by user dataset:
CONTENT_ID The object ID of the article.
AUTHOR_ID The ID of the user who wrote the article
SUBJECT_ID The ID of the subject that the article is supposed to be about
* ratings: 
OBJECT_ID The object ID is the object that is being rated. The only valid objects at the present time are the content_id of the member_content table. This means that at present this table only stores the ratings on reviews and essays
MEMBER_ID Stores the id of the member who is rating the object
RATING Stores the 1-5 (1- Not helpful , 2 - Somewhat Helpful, 3 - Helpful 4 - Very Helpful 5- Most Helpful) rating of the object by member [There are some 6s, treat them as 5]
STATUS The display status of the rating. 1 :- means the member has chosen not to show his rating of the object and 0 meaning the member does not mind showing his name beside the rating.
CREATION The date on which the member first rated this object
LAST_MODIFIED The latest date on which the member modified his rating of the object
TYPE If and when we allow more than just content rating to be stored in this table, then this column would store the type of the object being rated.
VERTICAL_ID Vertical_id of the review.

Methods: Marie

First step: we clean the dataset to only consider the edges that are contextualized (node A to B in Figure 2).
Second step: create the dataset with the new features and the sign of the edges: (node_A_features, node_B_features, sign_A_to_B). 
Third step: dataset statistics to have an idea of trends 
Fourth step: create a model to predict the sign of the edges. Determine using the findings of the paper, what is an acceptable accuracy for drawing conclusions on features and status.
Fifth step: assuming the model works, we check the statistical significance of each features and draw conclusion on their relation with status (as defined in the paper).


As we really don't know what to expect from our analysis, we plan on doing most of the steps together to figure out what to do at each step, if it doesn't go as planed.

Week 1: Steps 1, 2 (Haeeun), 3, 4 (Haeeun, Moulik, Marie)
Week 2: Step 5 and other solution if step 5 doesn't give expected results
Week 3: Writing the report & personal replications
Between the 18th and the 20th: video!

Questions for the TA:

Is it dramatic if we find out that the features don't actually explain status?
Moulik
We are following the assumptions and results exposed in the paper, is this a correct approach?



