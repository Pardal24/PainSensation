# PainSensation

To Do:
- [ ] Trim Dataset in order to every trial has the same number of frames and touch values
- [ ] Verify the validation code for the DMBN_2inputs.ipynb
- [ ] Divide the dataset into training, validation and test
- [ ] Verify the Memory problems
- [ ] Only use around 50k steps
- [ ] Develop the pipeline

Pipeline:
After training, at each 1k step I should test and save it in a folder called Snap_epoch_x (being x the current number of the step)
For the test, I should use the x data for the test and make x prediction for each of the 8 sensors, making an 10x8 matrix of possible plots.
The test should give the first 10 frames and touch values and try to predict the rest, so maybe is best to use coef of 0.5 for now.
I should save the model, the prediction and validation error and loss on the folder
Validation Loss should maybe have a coef of 0.5 as well

