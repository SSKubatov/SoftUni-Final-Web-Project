let player;
let video_list;

window.onload = () => {
    player = document.getElementById('player');
    video_list = document.getElementById('video_list')

    maintainAspectRatio();
};

function maintainAspectRatio() {
    const containerWidth = player.parentElement.clientWidth;
    const aspectRatio = 16 / 9;
    const height = Math.floor(containerWidth / aspectRatio);
    player.style.height = `${height}px`;
    video_list.style.maxHeight = `${height}px`;
}

window.onresize = maintainAspectRatio;