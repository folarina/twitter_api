while true
do 
    echo starting
    python process_tweets.py # only run if i have finished running 
    echo 'pre processed done'
    python plot_tweets.py #gives back the control
    echo 'Plotly Quit'
    sleep 10 #sleep for 10 seconds
done 

#run the statmenets while true for the loop.sh