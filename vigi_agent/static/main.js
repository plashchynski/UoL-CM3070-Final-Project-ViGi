const recordingVideoModal = document.getElementById('recording_video_modal');
if (recordingVideoModal) {
    recordingVideoModal.addEventListener('show.bs.modal', event => {
        // Button that triggered the modal
        const button = event.relatedTarget;

        // find parent element with class 'recording_date_section'
        const recordingDateSection = button.closest('.recording_date_section');

        // get data from the parent element
        const date = recordingDateSection.dataset.date;

        // find child element with class 'recording_video'
        const recordingVideo = button.querySelector('.recording_card');

        // get data and camera_id from the child element
        const time = recordingVideo.dataset.time;
        const camera_id = recordingVideo.dataset.cameraId;

        // Update the modal's title
        const modalTitle = recordingVideoModal.querySelector('.modal-title')
        modalTitle.textContent = `Recording for ${date} at ${time} from camera #${camera_id}`;

        // find #video_source element among children of recording_video_modal
        const videoSource = recordingVideoModal.querySelector('#video_source');

        // update src attribute of the video source
        videoSource.src = `/recordings/${camera_id}/${date}/${time}/video`;

        // find video element among children of recording_video_modal
        const video = recordingVideoModal.querySelector('video');

        // read tags and update the tags element
        const tagsElement = recordingVideoModal.querySelector('#tags');

        // remove all children from #tags element
        while (tagsElement.firstChild) {
            tagsElement.removeChild(tagsElement.firstChild);
        }

        // split tags by comma
        const tags = recordingVideo.dataset.tags.split(',');
        
        // for each tag in tags create a span with badge bg-secondary classes and
        // append it to the tagsElement element
        tags.forEach(tag => {
            const span = document.createElement('span');
            span.className = "badge text-bg-info ms-1";
            span.textContent = tag;
            tagsElement.appendChild(span);
        });

        // load and play the video
        video.load();
        video.play();
    });
}
