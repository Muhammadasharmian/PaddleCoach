// IndexedDB helper function for retrieving video files
function getVideoFromIndexedDB(name) {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open('VideoDatabase', 1);
        
        request.onerror = () => reject(request.error);
        
        request.onsuccess = () => {
            const db = request.result;
            const transaction = db.transaction(['videos'], 'readonly');
            const store = transaction.objectStore('videos');
            const getRequest = store.get(name);
            
            getRequest.onsuccess = () => {
                if (getRequest.result) {
                    console.log(`✓ ${name} retrieved from IndexedDB`);
                    resolve(getRequest.result.file);
                } else {
                    reject(new Error(`${name} not found in IndexedDB`));
                }
            };
            getRequest.onerror = () => reject(getRequest.error);
        };
    });
}

// Get video data from IndexedDB
console.log('=== Video Comparison Page Loaded ===');
console.log('Checking for video files...');

let professionalVideoURL = null;
let yourVideoURL = null;
let professionalVideoFile = null;
let yourVideoFile = null;

// DOM Elements
const processingOverlay = document.getElementById('processingOverlay');
const comparisonView = document.getElementById('comparisonView');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');

const professionalVideo = document.getElementById('professionalVideo');
const yourVideo = document.getElementById('yourVideo');

const syncVideosBtn = document.getElementById('syncVideos');
const playbackSpeedBtn = document.getElementById('playbackSpeed');

// Processing steps
const steps = [
    { id: 'step1', duration: 1000, progress: 20 },
    { id: 'step2', duration: 1500, progress: 40 },
    { id: 'step3', duration: 2000, progress: 60 },
    { id: 'step4', duration: 1500, progress: 80 },
    { id: 'step5', duration: 1000, progress: 100 }
];

let currentPlaybackSpeed = 1;
const playbackSpeeds = [0.5, 1, 1.5, 2];

// Load videos from IndexedDB on page load
async function initializeVideos() {
    try {
        console.log('Loading videos from IndexedDB...');
        
        // Get video files from IndexedDB
        professionalVideoFile = await getVideoFromIndexedDB('professional');
        yourVideoFile = await getVideoFromIndexedDB('your');
        
        // Create blob URLs from the files
        professionalVideoURL = URL.createObjectURL(professionalVideoFile);
        yourVideoURL = URL.createObjectURL(yourVideoFile);
        
        console.log('✓ Professional video URL created');
        console.log('✓ Your video URL created');
        console.log('Videos ready for playback');
        
        return true;
    } catch (error) {
        console.error('Error loading videos:', error);
        alert('Error loading videos. Please upload them again.');
        window.location.href = 'index.html';
        return false;
    }
}

// Start processing simulation
function startProcessing() {
    let currentProgress = 0;
    let currentStepIndex = 0;

    function processStep() {
        if (currentStepIndex >= steps.length) {
            // Processing complete
            setTimeout(() => {
                processingOverlay.classList.remove('active');
                comparisonView.classList.add('active');
                loadVideos();
            }, 500);
            return;
        }

        const step = steps[currentStepIndex];
        const stepElement = document.getElementById(step.id);
        
        // Mark current step as active
        stepElement.classList.add('active');
        
        // Animate progress
        const startProgress = currentProgress;
        const endProgress = step.progress;
        const duration = step.duration;
        const startTime = Date.now();

        function animateProgress() {
            const elapsed = Date.now() - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            currentProgress = startProgress + (endProgress - startProgress) * progress;
            progressFill.style.width = currentProgress + '%';
            progressText.textContent = Math.round(currentProgress) + '%';

            if (progress < 1) {
                requestAnimationFrame(animateProgress);
            } else {
                // Mark step as completed
                stepElement.classList.remove('active');
                stepElement.classList.add('completed');
                
                // Move to next step
                currentStepIndex++;
                processStep();
            }
        }

        animateProgress();
    }

    processStep();
}

// Load videos (using the uploaded files from object URLs)
function loadVideos() {
    console.log('Loading videos...');
    console.log('Professional Video URL:', professionalVideoURL);
    console.log('Your Video URL:', yourVideoURL);
    
    // Set video sources
    if (professionalVideoURL) {
        professionalVideo.src = professionalVideoURL;
        console.log('Professional video source set');
    } else {
        console.error('No professional video URL found');
    }
    
    if (yourVideoURL) {
        yourVideo.src = yourVideoURL;
        console.log('Your video source set');
    } else {
        console.error('No your video URL found');
    }

    // Update video stats when metadata is loaded
    professionalVideo.addEventListener('loadedmetadata', () => {
        console.log('Professional video metadata loaded');
        updateVideoStats('pro', professionalVideo);
    });

    yourVideo.addEventListener('loadedmetadata', () => {
        console.log('Your video metadata loaded');
        updateVideoStats('your', yourVideo);
        
        // Clear IndexedDB and sessionStorage after successful load
        clearVideoData();
    });
    
    // Handle video load errors
    professionalVideo.addEventListener('error', (e) => {
        console.error('Error loading professional video:', e);
        console.error('Video source:', professionalVideo.src);
        alert('Error loading professional video. The video format may not be supported. Please try uploading again.');
        clearVideoData();
    });
    
    yourVideo.addEventListener('error', (e) => {
        console.error('Error loading your video:', e);
        console.error('Video source:', yourVideo.src);
        alert('Error loading your video. The video format may not be supported. Please try uploading again.');
        clearVideoData();
    });
}

// Clear video data from storage after successful load
function clearVideoData() {
    console.log('Cleaning up video data...');
    
    // Clear sessionStorage flag
    sessionStorage.removeItem('videosReady');
    
    // Clear IndexedDB
    const request = indexedDB.open('VideoDatabase', 1);
    request.onsuccess = () => {
        const db = request.result;
        const transaction = db.transaction(['videos'], 'readwrite');
        const store = transaction.objectStore('videos');
        store.clear();
        console.log('✓ Video data cleared from IndexedDB');
    };
    request.onerror = (e) => {
        console.error('Error clearing IndexedDB:', e);
    };
}

// Update video statistics
function updateVideoStats(type, videoElement) {
    const duration = formatTime(videoElement.duration);
    const prefix = type === 'pro' ? 'pro' : 'your';
    
    document.getElementById(`${prefix}Duration`).textContent = duration;
    
    // Simulated stats (in real implementation, these would come from AI analysis)
    if (type === 'pro') {
        document.getElementById('proSpeed').textContent = '85 km/h';
        document.getElementById('proAccuracy').textContent = '94%';
    } else {
        document.getElementById('yourSpeed').textContent = '72 km/h';
        document.getElementById('yourAccuracy').textContent = '81%';
    }
}

// Format time in MM:SS
function formatTime(seconds) {
    if (isNaN(seconds)) return '--:--';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

// Sync videos playback
if (syncVideosBtn) {
    syncVideosBtn.addEventListener('click', () => {
        // Pause both videos
        professionalVideo.pause();
        yourVideo.pause();
        
        // Reset both to start
        professionalVideo.currentTime = 0;
        yourVideo.currentTime = 0;
        
        // Play both simultaneously
        Promise.all([
            professionalVideo.play(),
            yourVideo.play()
        ]).catch(err => {
            console.error('Error syncing videos:', err);
        });
        
        // Show feedback
        syncVideosBtn.innerHTML = '<i class="fas fa-check"></i> Synced!';
        setTimeout(() => {
            syncVideosBtn.innerHTML = '<i class="fas fa-sync"></i> Sync Videos';
        }, 2000);
    });
}

// Playback speed control
if (playbackSpeedBtn) {
    playbackSpeedBtn.addEventListener('click', () => {
        const currentIndex = playbackSpeeds.indexOf(currentPlaybackSpeed);
        const nextIndex = (currentIndex + 1) % playbackSpeeds.length;
        currentPlaybackSpeed = playbackSpeeds[nextIndex];
        
        // Apply to both videos
        professionalVideo.playbackRate = currentPlaybackSpeed;
        yourVideo.playbackRate = currentPlaybackSpeed;
        
        playbackSpeedBtn.innerHTML = `<i class="fas fa-tachometer-alt"></i> Speed: ${currentPlaybackSpeed}x`;
    });
}

// Tab switching
const analysisTabs = document.querySelectorAll('.analysis-tab');
const tabContents = document.querySelectorAll('.tab-content');

analysisTabs.forEach(tab => {
    tab.addEventListener('click', () => {
        const targetTab = tab.dataset.tab;
        
        // Remove active class from all tabs and contents
        analysisTabs.forEach(t => t.classList.remove('active'));
        tabContents.forEach(c => c.classList.remove('active'));
        
        // Add active class to clicked tab and corresponding content
        tab.classList.add('active');
        const targetContent = document.querySelector(`[data-content="${targetTab}"]`);
        if (targetContent) {
            targetContent.classList.add('active');
        }
    });
});

// Timeline controls
const timelineSlider = document.getElementById('timelineSlider');
const timelineTime = document.getElementById('timelineTime');
const playTimelineBtn = document.getElementById('playTimeline');

let timelineInterval;
let isTimelinePlaying = false;

if (playTimelineBtn) {
    playTimelineBtn.addEventListener('click', () => {
        if (isTimelinePlaying) {
            // Pause
            clearInterval(timelineInterval);
            playTimelineBtn.innerHTML = '<i class="fas fa-play"></i>';
            isTimelinePlaying = false;
        } else {
            // Play
            playTimelineBtn.innerHTML = '<i class="fas fa-pause"></i>';
            isTimelinePlaying = true;
            
            timelineInterval = setInterval(() => {
                let currentValue = parseInt(timelineSlider.value);
                if (currentValue >= 100) {
                    clearInterval(timelineInterval);
                    playTimelineBtn.innerHTML = '<i class="fas fa-play"></i>';
                    isTimelinePlaying = false;
                    timelineSlider.value = 0;
                } else {
                    timelineSlider.value = currentValue + 1;
                    updateTimelineDisplay();
                }
            }, 100);
        }
    });
}

if (timelineSlider) {
    // Update display as user moves slider
    timelineSlider.addEventListener('input', () => {
        updateTimelineDisplay();
    });
    
    // Seek videos when user releases the slider
    timelineSlider.addEventListener('change', () => {
        const value = parseInt(timelineSlider.value);
        const totalDuration = Math.max(professionalVideo.duration || 0, yourVideo.duration || 0);
        const seekTime = (value / 100) * totalDuration;
        
        professionalVideo.currentTime = seekTime;
        yourVideo.currentTime = seekTime;
    });
}

function updateTimelineDisplay() {
    const value = parseInt(timelineSlider.value);
    const totalDuration = Math.max(professionalVideo.duration || 0, yourVideo.duration || 0);
    const currentTime = (value / 100) * totalDuration;
    
    timelineTime.textContent = `${formatTime(currentTime)} / ${formatTime(totalDuration)}`;
    
    // Only update video time if user is manually scrubbing the timeline
    // Don't interfere with normal playback
}

// Export report functionality
const exportBtn = document.querySelector('.btn-export');
if (exportBtn) {
    exportBtn.addEventListener('click', () => {
        alert('Report export functionality will be implemented. This will generate a PDF with all analysis, insights, and recommendations.');
        // TODO: Implement PDF generation with all analysis data
    });
}

// Practice drills buttons
const practiceButtons = document.querySelectorAll('.btn-action');
practiceButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        const buttonText = btn.textContent.trim();
        if (buttonText.includes('Tutorial')) {
            alert('Video tutorial will be shown here with detailed technique breakdown.');
            // TODO: Open tutorial modal/page
        } else if (buttonText.includes('Drills')) {
            alert('Practice drills and exercises will be shown here to improve this specific skill.');
            // TODO: Open drills modal/page
        }
    });
});

// Store video files in sessionStorage (for demo purposes)
// Store video names for display
if (sessionStorage.getItem('professionalVideoName')) {
    const proName = sessionStorage.getItem('professionalVideoName');
    document.getElementById('professionalPlayerName').textContent = proName || 'Professional Player';
}

if (sessionStorage.getItem('yourVideoName')) {
    const yourName = sessionStorage.getItem('yourVideoName');
    document.getElementById('yourPlayerName').textContent = yourName || 'Your Performance';
}

// Start the processing animation when page loads
window.addEventListener('load', async () => {
    console.log('Page loaded, initializing videos...');
    
    // Check if videos were uploaded
    const videosReady = sessionStorage.getItem('videosReady');
    if (!videosReady) {
        console.error('No videos found. Redirecting to home page...');
        alert('No videos found. Please upload videos first.');
        window.location.href = 'index.html';
        return;
    }
    
    // Initialize videos from IndexedDB
    const success = await initializeVideos();
    
    if (success) {
        // Start processing animation
        startProcessing();
    }
});

// Video sync is now manual only - user must click "Sync Videos" button
// Removed automatic sync on play to prevent interference with normal playback

// Update timeline as videos play
professionalVideo.addEventListener('timeupdate', () => {
    if (!timelineSlider) return;
    const progress = (professionalVideo.currentTime / professionalVideo.duration) * 100;
    if (!isTimelinePlaying) {
        timelineSlider.value = progress;
        updateTimelineDisplay();
    }
});
