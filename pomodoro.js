// Timer States
const TimerState = {
    STOPPED: 'stopped',
    WORKING: 'working',
    BREAK: 'break',
    PAUSED: 'paused'
};

class PomodoroTimer {
    constructor() {
        // DOM Elements
        this.timeDisplay = document.getElementById('timeDisplay');
        this.statusDisplay = document.getElementById('statusDisplay');
        this.startBtn = document.getElementById('startBtn');
        this.pauseBtn = document.getElementById('pauseBtn');
        this.resetBtn = document.getElementById('resetBtn');
        this.workDurationInput = document.getElementById('workDuration');
        this.breakDurationInput = document.getElementById('breakDuration');
        this.timerContainer = document.querySelector('.timer-container');
        this.progressCircle = document.querySelector('.progress-ring-circle');
        
        // Timer state
        this.state = TimerState.STOPPED;
        this.timeRemaining = 0;
        this.totalTime = 0;
        this.timerInterval = null;
        
        // Settings
        this.workDuration = 25 * 60; // 25 minutes in seconds
        this.breakDuration = 5 * 60; // 5 minutes in seconds
        
        // Initialize
        this.init();
    }
    
    init() {
        // Set up progress circle
        this.setupProgressCircle();
        
        // Event listeners
        this.startBtn.addEventListener('click', () => this.start());
        this.pauseBtn.addEventListener('click', () => this.pause());
        this.resetBtn.addEventListener('click', () => this.reset());
        
        this.workDurationInput.addEventListener('change', (e) => {
            this.workDuration = parseInt(e.target.value) * 60;
            if (this.state === TimerState.STOPPED) {
                this.reset();
            }
        });
        
        this.breakDurationInput.addEventListener('change', (e) => {
            this.breakDuration = parseInt(e.target.value) * 60;
        });
        
        // Initialize display
        this.reset();
    }
    
    setupProgressCircle() {
        const radius = this.progressCircle.r.baseVal.value;
        const circumference = radius * 2 * Math.PI;
        
        this.progressCircle.style.strokeDasharray = `${circumference} ${circumference}`;
        this.progressCircle.style.strokeDashoffset = circumference;
        
        this.circumference = circumference;
    }
    
    updateProgressCircle() {
        const progress = this.timeRemaining / this.totalTime;
        const offset = this.circumference - (progress * this.circumference);
        this.progressCircle.style.strokeDashoffset = offset;
    }
    
    start() {
        if (this.state === TimerState.STOPPED) {
            // Start work session
            this.state = TimerState.WORKING;
            this.timeRemaining = this.workDuration;
            this.totalTime = this.workDuration;
            this.updateDisplay();
            this.updateStatus('作業中');
            this.timerContainer.className = 'timer-container working';
        } else if (this.state === TimerState.PAUSED) {
            // Resume from pause
            if (this.timerContainer.classList.contains('break')) {
                this.state = TimerState.BREAK;
            } else {
                this.state = TimerState.WORKING;
            }
        }
        
        // Start the countdown
        this.timerInterval = setInterval(() => this.tick(), 1000);
        
        // Update buttons
        this.startBtn.disabled = true;
        this.pauseBtn.disabled = false;
    }
    
    pause() {
        clearInterval(this.timerInterval);
        this.state = TimerState.PAUSED;
        this.updateStatus('一時停止中');
        
        // Update buttons
        this.startBtn.disabled = false;
        this.pauseBtn.disabled = true;
    }
    
    reset() {
        clearInterval(this.timerInterval);
        this.state = TimerState.STOPPED;
        this.timeRemaining = this.workDuration;
        this.totalTime = this.workDuration;
        this.updateDisplay();
        this.updateStatus('準備完了');
        this.timerContainer.className = 'timer-container stopped';
        this.updateProgressCircle();
        
        // Update buttons
        this.startBtn.disabled = false;
        this.pauseBtn.disabled = true;
    }
    
    tick() {
        this.timeRemaining--;
        
        if (this.timeRemaining < 0) {
            // Time's up, switch states
            clearInterval(this.timerInterval);
            
            if (this.state === TimerState.WORKING) {
                // Switch to break
                this.startBreak();
            } else if (this.state === TimerState.BREAK) {
                // Break is over, back to stopped
                this.reset();
                this.playNotification();
                alert('休憩が終わりました！新しい作業セッションを開始してください。');
            }
        } else {
            this.updateDisplay();
            this.updateProgressCircle();
        }
    }
    
    startBreak() {
        this.state = TimerState.BREAK;
        this.timeRemaining = this.breakDuration;
        this.totalTime = this.breakDuration;
        this.updateDisplay();
        this.updateStatus('休憩中');
        this.timerContainer.className = 'timer-container break';
        this.updateProgressCircle();
        
        this.playNotification();
        alert('作業時間が終了しました！休憩を取りましょう。');
        
        // Automatically start break timer
        this.timerInterval = setInterval(() => this.tick(), 1000);
    }
    
    updateDisplay() {
        const minutes = Math.floor(this.timeRemaining / 60);
        const seconds = this.timeRemaining % 60;
        this.timeDisplay.textContent = 
            `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }
    
    updateStatus(status) {
        this.statusDisplay.textContent = status;
    }
    
    playNotification() {
        // Simple beep using Web Audio API
        try {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            oscillator.frequency.value = 800;
            oscillator.type = 'sine';
            
            gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
            
            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.5);
        } catch (e) {
            console.log('Audio notification not supported');
        }
    }
}

// Initialize timer when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new PomodoroTimer();
});
