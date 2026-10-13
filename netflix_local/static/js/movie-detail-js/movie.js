const video = document.getElementById("video-player");

// build parameters
function fetch_data(){

    const movieIdValue = document.getElementById("movie-id").value;
    const csrfToken = document.getElementById("csrf-token").value;
    const userProfile = document.getElementById("user-profile").value;

    return {video:video, movieIdValue:movieIdValue, csrfToken:csrfToken, userProfile:userProfile};
}

// prepare data send to endpoint to track history
function watch_history_post(data, csrfToken){

//  only post watch history data. Don't do anything after success
    fetch("/record-watch-history/", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken
    },
    body: JSON.stringify(data)
});
}



// default set the progress interval to null
let progressInterval = null;

// function invoked when video starts playing
// also track the realtime progress invoking js method to track history
video.addEventListener("play", function () {

    const values = fetch_data();

    const post_data = {
        movie_id: values.movieIdValue,
        progress_seconds: video.currentTime,
        duration_seconds: video.duration,
        user_profile: values.userProfile,
    };

    watch_history_post(post_data, values.csrfToken);
    console.log("====video.currentTime===", video.currentTime);

    if (video.currentTime > 0.00){
        if (!progressInterval) {

            progressInterval = setInterval(function () {
                saveWatchProgress();
            }, 30000);

        }
    }
});


// function invoked when video is paused.
video.addEventListener("pause", function () {

    const values = fetch_data()
    console.log("pause called");

    const post_data = {
        movie_id: values.movieIdValue,
        progress_seconds: video.currentTime,
        duration_seconds: video.duration,
        user_profile: values.userProfile,
    };

    watch_history_post(post_data, values.csrfToken);

    saveWatchProgress();

    clearInterval(progressInterval);
    progressInterval = null;

});

// load video metadata while video is load to track the real time progress
video.addEventListener("loadedmetadata", function () {

    const resumePosition = parseFloat(document.getElementById("resume-position").value);

    console.log("resumePosition", resumePosition);
    console.log("video.duration", video.duration);
    console.log("video.currentTime", video.currentTime);

    if (resumePosition > 0 && resumePosition < video.duration) {
        video.currentTime = resumePosition;
    }
    console.log("video.currentTime", video.currentTime);

});

//function invoked when video is paused.
video.addEventListener("ended", function () {
    const values = fetch_data()
    console.log("ended called");

    const post_data = {
        movie_id: values.movieIdValue,
        progress_seconds: video.currentTime,
        duration_seconds: video.duration,
        user_profile: values.userProfile,
    };

    watch_history_post(post_data, values.csrfToken);

    saveWatchProgress();

    clearInterval(progressInterval);
    progressInterval = null;
});


function saveWatchProgress() {
    console.log("track when called!")

    const values = fetch_data()

    const post_data = {
        movie_id: values.movieIdValue,
        progress_seconds: video.currentTime,
        duration_seconds: video.duration,
        user_profile: values.userProfile,
    };

    watch_history_post(post_data, values.csrfToken);
}