function reloadJs(src) {
    src = $('script[src$="' + src + '"]').attr("src");
    $('script[src$="' + src + '"]').remove();
    $('<script/>').attr('src', src).appendTo('head');
}

function formatTime(seconds) {
    let h = Math.floor(seconds / 3600);
    let m = Math.floor((seconds % 3600) / 60);
    let s = Math.floor(seconds % 60);
    return (h < 10 ? "0" : "") + h + ":" + (m < 10 ? "0" : "") + m + ":" + (s < 10 ? "0" : "") + s;
}

function removeOptions(selectElement) {
    var i, L = selectElement.options.length - 1;
    for(i = L; i >= 0; i--) {
       selectElement.remove(i);
    }
 }

 function getVideos(response, elemName){
    let videos = response.videos;
    let selectElement = document.getElementById(elemName);
    let videoOptions = selectElement.options;
    let currentlySelectedVideo = $("#"+elemName).val()
    removeOptions(selectElement);

    for (let i = 0; i < videos.length; i++) {
         let optionElement = $('<option></option>');
         let video = videos[i];
         optionElement.attr('value', video).text(video);
         if (video == currentlySelectedVideo) {
             optionElement.attr('selected', 'selected');
         }
         $('#'+elemName).append(optionElement);
    };
 }

$(document).ready(() => {
    var videoPlayer = document.getElementById('video-player');
    let cutStart = null;
    let awaitingCloseMark = false;
    $('#loadingSpinner').hide();

    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

    $('#video-form').submit(function (e) {
        e.preventDefault();
        $.post($(this).attr('action'), $(this).serialize(), function (response) {
            location.reload();
        });
    });

    $('#title').click(() => {
        reloadJs("{{url_for('static', filename='script.js')}}")
    });
    $('#start-video').click(() =>{
        videoPlayer.play();
    });

    $('#pause-video').click(() => {
        videoPlayer.pause();
    });

    $('#next-video').click(() => {
        $.get('/control/next', function (response) {
            location.reload();
        });
    });

    $('#previous-video').click(() => {
        $.get('/control/previous', function (response) {
            location.reload();
        });
    });

    $('#skip-back-1s').click(() => {
        videoPlayer.currentTime = Math.max(videoPlayer.currentTime - 1, 0);
    });

    $('#skip-forward-1s').click(() => {
        videoPlayer.currentTime = Math.min(videoPlayer.currentTime + 1, videoPlayer.duration);
    });

    $('#skip-back-10s').click(() => {
        videoPlayer.currentTime = Math.max(videoPlayer.currentTime - 10, 0);
    });

    $('#skip-forward-10s').click(() => {
        videoPlayer.currentTime = Math.min(videoPlayer.currentTime + 10, videoPlayer.duration);
    });

    $('#open-cut-mark').click(() => {
        if (!awaitingCloseMark || $('textarea.form-control').val() === '') {
            cutStart = formatTime(videoPlayer.currentTime);
            let textArea = $('textarea.form-control');
            textArea.val(textArea.val() + cutStart);
            awaitingCloseMark = true;
        }
    });

    $('#close-cut-mark').click(() => {
        if (cutStart !== null) {
            let cutEnd = formatTime(videoPlayer.currentTime);
            let textArea = $('textarea.form-control');
            textArea.val(textArea.val() + " - " + cutEnd + "\n");
            cutStart = null;
            awaitingCloseMark = false;
        }
    });

    $('#ffmpeg-create-splits').click(() => {
        let textArea = $('textarea.form-control');
        let currentText = textArea.val();
        let videoPath = "static/" + $("#videoSelect").val();

        if (currentText.slice(-1) !== "\n" && currentText !== "") {
            currentText += "\n";
        }

        currentText += videoPath;

        let videoName = $("#videoSelect").val();
        $('#ffmpeg-create-splits').prop('disabled', true);
        $('#loadingSpinner').show();

        $.post('/save_crop', {
            video_name: videoName[0].split("/").pop().split(".")[0],
            content: currentText
        }, function (response) {
            console.log(response);
            $('#loadingSpinner').hide();
            $('#ffmpeg-create-splits').prop('disabled', false);
        });
    });

    $('#selectVideoModal').on('show.bs.modal', (e) => {
        $.get('/get_video_list', (response) => {
            getVideos(response, 'videoSelect')
        });
    });

    $('#manageVideoModal').on('show.bs.modal', (e) => {
        $.get('/get_video_list', (response) => {
            getVideos(response, 'videoManage')
        });
    });

    $('#delete-video-btn').click(() => {
        let currentlySelectedVideo = $("#videoManage").val()
        if (currentlySelectedVideo) {
            $.post('delete-video', { 'video_name': currentlySelectedVideo }, function (response) {
                location.reload();
            });
        }
    });
});
