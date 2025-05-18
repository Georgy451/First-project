document.addEventListener('DOMContentLoaded', function() {
    // Универсально ищем плеер
    const audioPlayer = document.getElementById('main-audio-player') || document.getElementById('audio');
    const playBtn = document.getElementById('play-btn');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const progressBar = document.getElementById('progress-bar');
    const progressContainer = document.getElementById('progress-bar-container');
    const currentTimeEl = document.getElementById('current-time');
    const durationEl = document.getElementById('duration');
    const currentTrackEl = document.getElementById('current-track');
    const trackItems = document.querySelectorAll('.track-item, .playlist-track');
    const volumeDownBtn = document.getElementById('volume-down-btn');
    const volumeUpBtn = document.getElementById('volume-up-btn');
    const volumeSlider = document.getElementById('volume-slider');

    let currentTrackIndex = 0;
    let isPlaying = false;
    let isDragging = false;

    // Загрузка трека
    function loadTrack(index) {
        if (!trackItems.length) return;

        const trackItem = trackItems[index];
        const audioUrl = trackItem.getAttribute('data-audio-url');
        const trackTitle = trackItem.querySelector('.track-title').textContent;

        audioPlayer.src = audioUrl;
        if (currentTrackEl) currentTrackEl.textContent = trackTitle;

        // Сбрасываем активные стили
        trackItems.forEach(item => item.style.backgroundColor = '');
        trackItem.style.backgroundColor = '#f0f0f0';

        // Обновляем время после загрузки
        audioPlayer.onloadedmetadata = function() {
            updateTimeInfo();
        };
    }

    // Воспроизведение/пауза
    function togglePlay() {
        if (audioPlayer.paused) {
            audioPlayer.play()
                .then(() => {
                    isPlaying = true;
                    if (playBtn) playBtn.innerHTML = '<i class="fas fa-pause"></i>';
                })
                .catch(error => console.error('Ошибка воспроизведения:', error));
        } else {
            audioPlayer.pause();
            isPlaying = false;
            if (playBtn) playBtn.innerHTML = '<i class="fas fa-play"></i>';
        }
    }

    // Обновление времени
    function updateTimeInfo() {
        if (isDragging) return;

        const duration = audioPlayer.duration || 0;
        const currentTime = audioPlayer.currentTime || 0;

        // Прогресс бар
        if (progressBar) {
            const progressPercent = (currentTime / duration) * 100 || 0;
            progressBar.style.width = `${progressPercent}%`;
        }

        // Время
        if (durationEl) durationEl.textContent = formatTime(duration);
        if (currentTimeEl) currentTimeEl.textContent = formatTime(currentTime);
    }

    // Форматирование времени
    function formatTime(seconds) {
        if (isNaN(seconds)) return "0:00";
        const minutes = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${minutes}:${secs < 10 ? '0' : ''}${secs}`;
    }

    // Следующий трек
    function nextTrack() {
        if (!trackItems.length) return;
        currentTrackIndex = (currentTrackIndex + 1) % trackItems.length;
        loadTrack(currentTrackIndex);
        if (isPlaying) audioPlayer.play();
    }

    // Предыдущий трек
    function prevTrack() {
        if (!trackItems.length) return;
        currentTrackIndex = (currentTrackIndex - 1 + trackItems.length) % trackItems.length;
        loadTrack(currentTrackIndex);
        if (isPlaying) audioPlayer.play();
    }

    // Управление громкостью
    function setVolume(volume) {
        audioPlayer.volume = volume;
        if (volumeSlider) volumeSlider.value = volume;
    }

    function increaseVolume() {
        setVolume(Math.min(audioPlayer.volume + 0.1, 1));
    }

    function decreaseVolume() {
        setVolume(Math.max(audioPlayer.volume - 0.1, 0));
    }

    // Перемотка трека
    function seekToPosition(e) {
        if (!audioPlayer.duration) return;

        const rect = progressContainer.getBoundingClientRect();
        const pos = (e.clientX - rect.left) / rect.width;
        audioPlayer.currentTime = pos * audioPlayer.duration;
    }

    // Обработчики событий
    if (playBtn) playBtn.addEventListener('click', togglePlay);
    if (prevBtn) prevBtn.addEventListener('click', prevTrack);
    if (nextBtn) nextBtn.addEventListener('click', nextTrack);

    if (volumeDownBtn) volumeDownBtn.addEventListener('click', decreaseVolume);
    if (volumeUpBtn) volumeUpBtn.addEventListener('click', increaseVolume);
    if (volumeSlider) volumeSlider.addEventListener('input', () => setVolume(volumeSlider.value));

    if (progressContainer) {
        progressContainer.addEventListener('click', seekToPosition);

        // Для плавной перемотки при drag
        progressContainer.addEventListener('mousedown', () => isDragging = true);
        document.addEventListener('mouseup', () => isDragging = false);
        document.addEventListener('mousemove', (e) => {
            if (isDragging) seekToPosition(e);
        });
    }

    if (audioPlayer) {
        audioPlayer.addEventListener('timeupdate', updateTimeInfo);
        audioPlayer.addEventListener('ended', nextTrack);
    }

    // Обработчик клика по треку (или кнопке play)
    trackItems.forEach((item, index) => {
        item.addEventListener('click', function(e) {
            // Игнорируем клики по встроенному аудиоплееру
            if (e.target.tagName === 'AUDIO' || e.target.closest('audio')) return;

            const audioUrl = item.getAttribute('data-audio-url');
            const titleElem = item.querySelector('.track-title');
            if (audioUrl) {
                audioPlayer.src = audioUrl;
                if (currentTrackEl && titleElem) {
                    currentTrackEl.textContent = titleElem.textContent;
                }
                currentTrackIndex = index;
                audioPlayer.play()
                    .then(() => {
                        isPlaying = true;
                        if (playBtn) playBtn.innerHTML = '<i class="fas fa-pause"></i>';
                    })
                    .catch(error => console.error('Ошибка воспроизведения:', error));
            }
        });
    });

    // Инициализация
    if (trackItems.length > 0) {
        loadTrack(0);
    }
    setVolume(1);
});