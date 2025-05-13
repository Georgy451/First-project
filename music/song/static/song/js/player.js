// Инициализация плеера
document.addEventListener('DOMContentLoaded', function() {
    const audioPlayer = document.getElementById('main-audio-player');
    const playBtn = document.getElementById('play-btn');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const progressBar = document.getElementById('progress-bar');
    const currentTimeEl = document.getElementById('current-time');
    const durationEl = document.getElementById('duration');
    const currentTrackEl = document.getElementById('current-track');
    const trackItems = document.querySelectorAll('.track-item');
    const playButtons = document.querySelectorAll('.play-btn');
    const searchInput = document.getElementById('track-search');
    
    let currentTrackIndex = 0;
    let isPlaying = false;
    
    // Загрузка трека
    function loadTrack(index) {
        const trackItem = trackItems[index];
        const audioUrl = trackItem.getAttribute('data-audio-url');
        const trackTitle = trackItem.querySelector('.track-title').textContent;
        
        audioPlayer.src = audioUrl;
        currentTrackEl.textContent = trackTitle;
        
        // Сбрасываем активные классы
        trackItems.forEach(item => item.classList.remove('active'));
        trackItem.classList.add('active');
        
        // Обновляем время после загрузки метаданных
        audioPlayer.addEventListener('loadedmetadata', function() {
            updateTimeInfo();
        });
    }
    
    // Воспроизведение/пауза
    function togglePlay() {
        if (audioPlayer.paused) {
            audioPlayer.play();
            isPlaying = true;
            playBtn.innerHTML = '<i class="fas fa-pause"></i>';
        } else {
            audioPlayer.pause();
            isPlaying = false;
            playBtn.innerHTML = '<i class="fas fa-play"></i>';
        }
    }
    
    // Обновление времени
    function updateTimeInfo() {
        const duration = audioPlayer.duration;
        const currentTime = audioPlayer.currentTime;
        
        // Прогресс бар
        const progressPercent = (currentTime / duration) * 100;
        progressBar.style.setProperty('--progress', `${progressPercent}%`);
        
        // Время
        durationEl.textContent = formatTime(duration);
        currentTimeEl.textContent = formatTime(currentTime);
    }
    
    // Форматирование времени
    function formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${minutes}:${secs < 10 ? '0' : ''}${secs}`;
    }
    
    // Следующий трек
    function nextTrack() {
        currentTrackIndex = (currentTrackIndex + 1) % trackItems.length;
        loadTrack(currentTrackIndex);
        if (isPlaying) audioPlayer.play();
    }
    
    // Предыдущий трек
    function prevTrack() {
        currentTrackIndex = (currentTrackIndex - 1 + trackItems.length) % trackItems.length;
        loadTrack(currentTrackIndex);
        if (isPlaying) audioPlayer.play();
    }
    
    // Поиск треков
    function searchTracks() {
        const searchTerm = searchInput.value.toLowerCase();
        trackItems.forEach(item => {
            const title = item.querySelector('.track-title').textContent.toLowerCase();
            if (title.includes(searchTerm)) {
                item.style.display = 'flex';
            } else {
                item.style.display = 'none';
            }
        });
    }
    
    // Обработчики событий
    playBtn.addEventListener('click', togglePlay);
    prevBtn.addEventListener('click', prevTrack);
    nextBtn.addEventListener('click', nextTrack);
    
    audioPlayer.addEventListener('timeupdate', updateTimeInfo);
    audioPlayer.addEventListener('ended', nextTrack);
    
    playButtons.forEach((btn, index) => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            currentTrackIndex = index;
            loadTrack(currentTrackIndex);
            audioPlayer.play();
            isPlaying = true;
            playBtn.innerHTML = '<i class="fas fa-pause"></i>';
        });
    });
    
    trackItems.forEach((item, index) => {
        item.addEventListener('click', function() {
            currentTrackIndex = index;
            loadTrack(currentTrackIndex);
            audioPlayer.play();
            isPlaying = true;
            playBtn.innerHTML = '<i class="fas fa-pause"></i>';
        });
    });
    
    searchInput.addEventListener('input', searchTracks);
    
    // Инициализация первого трека
    if (trackItems.length > 0) {
        loadTrack(0);
    }
});