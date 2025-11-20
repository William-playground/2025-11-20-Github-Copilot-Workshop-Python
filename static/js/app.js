// ポモドーロタイマーアプリケーション

class PomodoroTimer {
    constructor() {
        this.workDuration = 25 * 60; // 25分（秒単位）
        this.breakDuration = 5 * 60; // 5分（秒単位）
        this.timeRemaining = this.workDuration;
        this.isRunning = false;
        this.isWorkSession = true;
        this.intervalId = null;
        this.completedSessions = 0;
        this.totalFocusTime = 0; // 秒単位
        
        // DOM要素
        this.timerDisplay = document.getElementById('timerDisplay');
        this.statusText = document.getElementById('statusText');
        this.startBtn = document.getElementById('startBtn');
        this.resetBtn = document.getElementById('resetBtn');
        this.progressCircle = document.getElementById('progressCircle');
        this.completedCount = document.getElementById('completedCount');
        this.totalTime = document.getElementById('totalTime');
        
        // 進捗の円の設定
        this.radius = 120;
        this.circumference = 2 * Math.PI * this.radius;
        this.progressCircle.style.strokeDasharray = `${this.circumference} ${this.circumference}`;
        this.progressCircle.style.strokeDashoffset = this.circumference;
        
        this.initializeEventListeners();
        this.updateDisplay();
        this.loadProgress();
    }
    
    initializeEventListeners() {
        this.startBtn.addEventListener('click', () => this.toggleTimer());
        this.resetBtn.addEventListener('click', () => this.resetTimer());
    }
    
    toggleTimer() {
        if (this.isRunning) {
            this.pauseTimer();
        } else {
            this.startTimer();
        }
    }
    
    startTimer() {
        this.isRunning = true;
        this.startBtn.textContent = '一時停止';
        this.startBtn.classList.add('btn-pause');
        
        this.intervalId = setInterval(() => {
            this.timeRemaining--;
            
            if (this.timeRemaining <= 0) {
                this.completeSession();
            }
            
            this.updateDisplay();
        }, 1000);
    }
    
    pauseTimer() {
        this.isRunning = false;
        this.startBtn.textContent = '開始';
        this.startBtn.classList.remove('btn-pause');
        
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
    }
    
    resetTimer() {
        this.pauseTimer();
        this.isWorkSession = true;
        this.timeRemaining = this.workDuration;
        this.statusText.textContent = '作業中';
        this.updateDisplay();
    }
    
    completeSession() {
        if (this.isWorkSession) {
            // 作業セッション完了
            this.completedSessions++;
            this.totalFocusTime += this.workDuration;
            this.saveProgress();
            this.updateProgressDisplay();
            
            // 休憩モードに切り替え
            this.isWorkSession = false;
            this.timeRemaining = this.breakDuration;
            this.statusText.textContent = '休憩中';
        } else {
            // 休憩終了、作業モードに戻る
            this.isWorkSession = true;
            this.timeRemaining = this.workDuration;
            this.statusText.textContent = '作業中';
        }
        
        // 通知音を鳴らす（オプション）
        this.playNotificationSound();
        this.updateDisplay();
    }
    
    updateDisplay() {
        // タイマー表示を更新
        const minutes = Math.floor(this.timeRemaining / 60);
        const seconds = this.timeRemaining % 60;
        this.timerDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        // 進捗円を更新
        const totalDuration = this.isWorkSession ? this.workDuration : this.breakDuration;
        const progress = (totalDuration - this.timeRemaining) / totalDuration;
        const offset = this.circumference - (progress * this.circumference);
        this.progressCircle.style.strokeDashoffset = offset;
        
        // 休憩中は円の色を変更
        if (this.isWorkSession) {
            this.progressCircle.style.stroke = '#667eea';
        } else {
            this.progressCircle.style.stroke = '#10b981';
        }
    }
    
    updateProgressDisplay() {
        // 完了セッション数を更新
        this.completedCount.textContent = this.completedSessions;
        
        // 合計時間を更新
        const hours = Math.floor(this.totalFocusTime / 3600);
        const minutes = Math.floor((this.totalFocusTime % 3600) / 60);
        this.totalTime.textContent = `${hours}時間${minutes}分`;
    }
    
    saveProgress() {
        // ローカルストレージに進捗を保存
        const today = new Date().toDateString();
        const progress = {
            date: today,
            completed: this.completedSessions,
            totalTime: this.totalFocusTime
        };
        localStorage.setItem('pomodoroProgress', JSON.stringify(progress));
    }
    
    loadProgress() {
        // ローカルストレージから進捗を読み込み
        const saved = localStorage.getItem('pomodoroProgress');
        if (saved) {
            const progress = JSON.parse(saved);
            const today = new Date().toDateString();
            
            if (progress.date === today) {
                this.completedSessions = progress.completed;
                this.totalFocusTime = progress.totalTime;
                this.updateProgressDisplay();
            } else {
                // 新しい日なのでリセット
                this.completedSessions = 0;
                this.totalFocusTime = 0;
                this.saveProgress();
            }
        }
    }
    
    playNotificationSound() {
        // Web Audio APIで簡単な通知音を作成
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
    }
}

// アプリケーション初期化
document.addEventListener('DOMContentLoaded', () => {
    new PomodoroTimer();
});
