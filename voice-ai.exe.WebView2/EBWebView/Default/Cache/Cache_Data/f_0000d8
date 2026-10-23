// Voice AI Studio 2.0 — Speech to Text (Whisper) & Text to Speech (Kokoro)

document.addEventListener('DOMContentLoaded', () => {
  if (window.lucide) {
    lucide.createIcons();
  }

  // ----------------------------------------------------
  // Global State
  // ----------------------------------------------------
  let mainMode = 'stt'; // 'stt' | 'tts' | 'compressor'

  // Whisper STT State
  let currentFile = null;
  let recordedBlob = null;
  let activeInputTab = 'upload';
  let currentTask = 'transcribe';
  let transcriptionResult = null;
  let currentAudioUrl = null;

  let mediaRecorder = null;
  let audioChunks = [];
  let recordStartTime = 0;
  let recordTimerInterval = null;
  let recordElapsedBeforePause = 0;
  let audioContext = null;
  let analyserNode = null;
  let animFrameId = null;

  // Kokoro TTS State
  let allVoices = [];
  let selectedVoice = 'af_heart';
  let activeVoiceFilter = 'all';
  let voiceSearchQuery = '';

  // Audio Compressor State
  let compCurrentFile = null;
  let compResult = null;
  let compOriginalAudioUrl = null;
  let lastTtsAudioBlob = null;
  let lastTtsFilename = null;

  // ----------------------------------------------------
  // DOM Elements - Navigation & Shared
  // ----------------------------------------------------
  const navSttBtn = document.getElementById('navSttBtn');
  const navTtsBtn = document.getElementById('navTtsBtn');
  const navCompressorBtn = document.getElementById('navCompressorBtn');
  const navSttBtnMobile = document.getElementById('navSttBtnMobile');
  const navTtsBtnMobile = document.getElementById('navTtsBtnMobile');
  const navCompressorBtnMobile = document.getElementById('navCompressorBtnMobile');
  const sectionStt = document.getElementById('sectionStt');
  const sectionTts = document.getElementById('sectionTts');
  const sectionCompressor = document.getElementById('sectionCompressor');

  const deviceText = document.getElementById('deviceText');
  const themeToggleBtn = document.getElementById('themeToggleBtn');
  const themeSun = document.getElementById('themeSun');
  const themeMoon = document.getElementById('themeMoon');
  const toast = document.getElementById('toast');
  const toastMsg = document.getElementById('toastMsg');
  let toastTimeout = null;

  // ----------------------------------------------------
  // DOM Elements - Whisper STT
  // ----------------------------------------------------
  const tabUploadBtn = document.getElementById('tabUploadBtn');
  const tabRecordBtn = document.getElementById('tabRecordBtn');
  const tabUploadContent = document.getElementById('tabUploadContent');
  const tabRecordContent = document.getElementById('tabRecordContent');

  const dropZone = document.getElementById('dropZone');
  const audioFileInput = document.getElementById('audioFileInput');
  const fileInfoCard = document.getElementById('fileInfoCard');
  const fileName = document.getElementById('fileName');
  const fileSize = document.getElementById('fileSize');
  const removeFileBtn = document.getElementById('removeFileBtn');

  const waveformCanvas = document.getElementById('waveformCanvas');
  const recordTimer = document.getElementById('recordTimer');
  const startRecordBtn = document.getElementById('startRecordBtn');
  const pauseRecordBtn = document.getElementById('pauseRecordBtn');
  const stopRecordBtn = document.getElementById('stopRecordBtn');
  const cancelRecordBtn = document.getElementById('cancelRecordBtn');
  const recordStatus = document.getElementById('recordStatus');
  const recordPreviewCard = document.getElementById('recordPreviewCard');
  const recordedAudioPlayer = document.getElementById('recordedAudioPlayer');
  const recordDurationInfo = document.getElementById('recordDurationInfo');

  const modelRadios = document.querySelectorAll('input[name="model"]');
  const taskTranscribeBtn = document.getElementById('taskTranscribeBtn');
  const taskTranslateBtn = document.getElementById('taskTranslateBtn');
  const languageSelect = document.getElementById('languageSelect');
  const wordTimestampsCheckbox = document.getElementById('wordTimestampsCheckbox');
  const temperatureSlider = document.getElementById('temperatureSlider');
  const tempValue = document.getElementById('tempValue');
  const initialPromptInput = document.getElementById('initialPromptInput');
  const transcribeBtn = document.getElementById('transcribeBtn');
  const loadingIndicator = document.getElementById('loadingIndicator');
  const loadingTimer = document.getElementById('loadingTimer');
  const loadingStatusText = document.getElementById('loadingStatusText');

  const emptyResultPlaceholder = document.getElementById('emptyResultPlaceholder');
  const resultContainer = document.getElementById('resultContainer');
  const statDuration = document.getElementById('statDuration');
  const statTime = document.getElementById('statTime');
  const statSpeed = document.getElementById('statSpeed');
  const statLanguage = document.getElementById('statLanguage');
  const mainAudioPlayer = document.getElementById('mainAudioPlayer');
  const sendToTtsBtn = document.getElementById('sendToTtsBtn');

  const viewSegmentsBtn = document.getElementById('viewSegmentsBtn');
  const viewWordsBtn = document.getElementById('viewWordsBtn');
  const viewTextBtn = document.getElementById('viewTextBtn');
  const viewSubtitlesBtn = document.getElementById('viewSubtitlesBtn');
  const segmentsViewContainer = document.getElementById('segmentsViewContainer');
  const wordsViewContainer = document.getElementById('wordsViewContainer');
  const wordsStatsInfo = document.getElementById('wordsStatsInfo');
  const wordsGrid = document.getElementById('wordsGrid');
  const textViewContainer = document.getElementById('textViewContainer');
  const subtitlesViewContainer = document.getElementById('subtitlesViewContainer');
  const plainTextContent = document.getElementById('plainTextContent');
  const textStatsInfo = document.getElementById('textStatsInfo');
  const srtContent = document.getElementById('srtContent');

  const speedBtns = document.querySelectorAll('.speed-btn');
  const copyBtn = document.getElementById('copyBtn');
  const downloadDropdownBtn = document.getElementById('downloadDropdownBtn');
  const downloadMenu = document.getElementById('downloadMenu');
  const downloadOptBtns = document.querySelectorAll('.download-opt-btn');
  const searchInput = document.getElementById('searchInput');
  const clearSearchBtn = document.getElementById('clearSearchBtn');

  // ----------------------------------------------------
  // DOM Elements - Kokoro TTS
  // ----------------------------------------------------
  const ttsTextInput = document.getElementById('ttsTextInput');
  const ttsCharCount = document.getElementById('ttsCharCount');
  const clearTtsTextBtn = document.getElementById('clearTtsTextBtn');
  const ttsSampleBtns = document.querySelectorAll('.tts-sample-btn');
  const ttsSpeedSlider = document.getElementById('ttsSpeedSlider');
  const ttsSpeedVal = document.getElementById('ttsSpeedVal');
  const generateSpeechBtn = document.getElementById('generateSpeechBtn');
  const ttsLoadingIndicator = document.getElementById('ttsLoadingIndicator');
  const ttsLoadingTimer = document.getElementById('ttsLoadingTimer');

  const ttsPlayerCard = document.getElementById('ttsPlayerCard');
  const ttsAudioPlayer = document.getElementById('ttsAudioPlayer');
  const playerVoiceAvatar = document.getElementById('playerVoiceAvatar');
  const playerVoiceName = document.getElementById('playerVoiceName');
  const playerVoiceTrait = document.getElementById('playerVoiceTrait');
  const downloadTtsAudioBtn = document.getElementById('downloadTtsAudioBtn');
  const ttsStatDuration = document.getElementById('ttsStatDuration');
  const ttsStatGenTime = document.getElementById('ttsStatGenTime');
  const ttsStatSpeed = document.getElementById('ttsStatSpeed');

  const voicesGrid = document.getElementById('voicesGrid');
  const voiceFilterBtns = document.querySelectorAll('.voice-filter-btn');
  const voiceSearchInput = document.getElementById('voiceSearchInput');

  // ----------------------------------------------------
  // DOM Elements - History
  // ----------------------------------------------------
  const toggleHistoryBtn = document.getElementById('toggleHistoryBtn');
  const historyDrawer = document.getElementById('historyDrawer');
  const closeHistoryBtn = document.getElementById('closeHistoryBtn');
  const clearAllHistoryBtn = document.getElementById('clearAllHistoryBtn');
  const historyListContainer = document.getElementById('historyListContainer');
  const historyCountBadge = document.getElementById('historyCountBadge');

  // ----------------------------------------------------
  // Initial App Setup
  // ----------------------------------------------------
  fetchSystemInfo();
  fetchLanguages();
  fetchVoices();
  updateHistoryBadge();
  setupTheme();

  // ----------------------------------------------------
  // Top-Level Mode Switching (STT vs TTS vs Compressor)
  // ----------------------------------------------------
  navSttBtn.addEventListener('click', () => switchMainMode('stt'));
  navTtsBtn.addEventListener('click', () => switchMainMode('tts'));
  if (navCompressorBtn) navCompressorBtn.addEventListener('click', () => switchMainMode('compressor'));
  navSttBtnMobile.addEventListener('click', () => switchMainMode('stt'));
  navTtsBtnMobile.addEventListener('click', () => switchMainMode('tts'));
  if (navCompressorBtnMobile) navCompressorBtnMobile.addEventListener('click', () => switchMainMode('compressor'));

  function switchMainMode(mode) {
    mainMode = mode;
    const activeDesktop = 'flex items-center gap-2 px-4 py-1.5 rounded-lg text-xs font-semibold transition-all duration-200 bg-white/[0.1] text-white shadow-sm border border-white/[0.08]';
    const inactiveDesktop = 'flex items-center gap-2 px-4 py-1.5 rounded-lg text-xs font-semibold transition-all duration-200 text-slate-400 hover:text-slate-200';
    const activeMob = 'flex-1 flex items-center justify-center gap-1.5 py-1.5 px-2 rounded-lg text-xs font-semibold bg-white/[0.1] text-white border border-white/[0.08] whitespace-nowrap';
    const inactiveMob = 'flex-1 flex items-center justify-center gap-1.5 py-1.5 px-2 rounded-lg text-xs font-semibold text-slate-400 whitespace-nowrap';

    navSttBtn.className = mode === 'stt' ? activeDesktop : inactiveDesktop;
    navTtsBtn.className = mode === 'tts' ? activeDesktop : inactiveDesktop;
    if (navCompressorBtn) navCompressorBtn.className = mode === 'compressor' ? activeDesktop : inactiveDesktop;

    navSttBtnMobile.className = mode === 'stt' ? activeMob : inactiveMob;
    navTtsBtnMobile.className = mode === 'tts' ? activeMob : inactiveMob;
    if (navCompressorBtnMobile) navCompressorBtnMobile.className = mode === 'compressor' ? activeMob : inactiveMob;

    sectionStt.classList.toggle('hidden', mode !== 'stt');
    sectionTts.classList.toggle('hidden', mode !== 'tts');
    if (sectionCompressor) sectionCompressor.classList.toggle('hidden', mode !== 'compressor');

    // Update quick load buttons in Compressor if audio is present
    updateCompressorSourceOptions();

    if (window.lucide) lucide.createIcons();
  }

  if (sendToTtsBtn) {
    sendToTtsBtn.addEventListener('click', () => {
      if (!transcriptionResult || !transcriptionResult.text) return;
      ttsTextInput.value = transcriptionResult.text;
      updateTtsCharCount();
      switchMainMode('tts');
      ttsTextInput.scrollIntoView({ behavior: 'smooth' });
      showToast('Transcript loaded into Kokoro TTS');
    });
  }

  // ----------------------------------------------------
  // System Info & Languages
  // ----------------------------------------------------
  async function fetchSystemInfo() {
    try {
      const res = await fetch('/api/info');
      if (!res.ok) return;
      const data = await res.json();
      deviceText.textContent = `${data.device.toUpperCase()} · ${data.device_name}`;
    } catch (e) {
      deviceText.textContent = 'CPU Ready';
    }
  }

  async function fetchLanguages() {
    try {
      const res = await fetch('/api/languages');
      if (!res.ok) return;
      const langs = await res.json();
      langs.forEach(lang => {
        const opt = document.createElement('option');
        opt.value = lang.code;
        opt.textContent = `${lang.name} (${lang.code})`;
        languageSelect.appendChild(opt);
      });
    } catch (e) {
      console.warn('Could not load languages list:', e);
    }
  }

  // ----------------------------------------------------
  // Theme Toggle
  // ----------------------------------------------------
  function setupTheme() {
    const isDark = localStorage.getItem('theme') !== 'light';
    applyTheme(isDark);

    themeToggleBtn.addEventListener('click', () => {
      const currentlyDark = document.documentElement.classList.contains('dark');
      applyTheme(!currentlyDark);
    });
  }

  function applyTheme(dark) {
    if (dark) {
      document.documentElement.classList.add('dark');
      themeSun.classList.add('hidden');
      themeMoon.classList.remove('hidden');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      themeSun.classList.remove('hidden');
      themeMoon.classList.add('hidden');
      localStorage.setItem('theme', 'light');
    }
    if (window.lucide) lucide.createIcons();
  }

  // ----------------------------------------------------
  // Whisper STT: Tabs & Upload
  // ----------------------------------------------------
  tabUploadBtn.addEventListener('click', () => switchInputTab('upload'));
  tabRecordBtn.addEventListener('click', () => switchInputTab('record'));

  function switchInputTab(tab) {
    activeInputTab = tab;
    if (tab === 'upload') {
      tabUploadBtn.className = 'flex items-center gap-1.5 py-1 px-3 rounded-md text-xs font-medium transition-all bg-indigo-600 text-white shadow-sm';
      tabRecordBtn.className = 'flex items-center gap-1.5 py-1 px-3 rounded-md text-xs font-medium transition-all text-slate-400 hover:text-slate-200';
      tabUploadContent.classList.remove('hidden');
      tabRecordContent.classList.add('hidden');
    } else {
      tabRecordBtn.className = 'flex items-center gap-1.5 py-1 px-3 rounded-md text-xs font-medium transition-all bg-indigo-600 text-white shadow-sm';
      tabUploadBtn.className = 'flex items-center gap-1.5 py-1 px-3 rounded-md text-xs font-medium transition-all text-slate-400 hover:text-slate-200';
      tabRecordContent.classList.remove('hidden');
      tabUploadContent.classList.add('hidden');
    }
    if (window.lucide) lucide.createIcons();
  }

  dropZone.addEventListener('click', () => audioFileInput.click());

  dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('border-indigo-500/80', 'bg-indigo-500/[0.06]');
  });

  dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('border-indigo-500/80', 'bg-indigo-500/[0.06]');
  });

  dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('border-indigo-500/80', 'bg-indigo-500/[0.06]');
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFileSelected(e.dataTransfer.files[0]);
    }
  });

  audioFileInput.addEventListener('change', (e) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFileSelected(e.target.files[0]);
    }
  });

  function handleFileSelected(file) {
    currentFile = file;
    fileName.textContent = file.name;
    fileSize.textContent = formatBytes(file.size);
    fileInfoCard.classList.remove('hidden');
    dropZone.classList.add('hidden');
    if (window.lucide) lucide.createIcons();
  }

  removeFileBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    currentFile = null;
    audioFileInput.value = '';
    fileInfoCard.classList.add('hidden');
    dropZone.classList.remove('hidden');
  });

  // ----------------------------------------------------
  // Whisper STT: Microphone Recording
  // ----------------------------------------------------
  startRecordBtn.addEventListener('click', startRecording);
  pauseRecordBtn.addEventListener('click', togglePauseRecording);
  stopRecordBtn.addEventListener('click', stopRecording);
  cancelRecordBtn.addEventListener('click', cancelRecording);

  async function startRecording() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      audioChunks = [];
      recordElapsedBeforePause = 0;
      recordStartTime = Date.now();

      audioContext = new (window.AudioContext || window.webkitAudioContext)();
      const source = audioContext.createMediaStreamSource(stream);
      analyserNode = audioContext.createAnalyser();
      analyserNode.fftSize = 256;
      source.connect(analyserNode);

      mediaRecorder = new MediaRecorder(stream);
      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) audioChunks.push(e.data);
      };

      mediaRecorder.onstop = () => {
        const tracks = stream.getTracks();
        tracks.forEach(track => track.stop());
        if (audioContext && audioContext.state !== 'closed') {
          audioContext.close();
        }
        cancelAnimationFrame(animFrameId);
        clearCanvas();

        if (audioChunks.length > 0) {
          recordedBlob = new Blob(audioChunks, { type: mediaRecorder.mimeType || 'audio/webm' });
          const audioUrl = URL.createObjectURL(recordedBlob);
          recordedAudioPlayer.src = audioUrl;
          recordPreviewCard.classList.remove('hidden');
          recordDurationInfo.textContent = `${recordTimer.textContent} · Ready`;
        }
      };

      mediaRecorder.start(250);

      startRecordBtn.classList.add('hidden');
      pauseRecordBtn.classList.remove('hidden');
      stopRecordBtn.classList.remove('hidden');
      cancelRecordBtn.classList.remove('hidden');
      recordPreviewCard.classList.add('hidden');
      recordStatus.textContent = 'Recording live audio...';
      recordStatus.className = 'text-[11px] text-rose-400 font-medium mt-2.5 animate-pulse';

      startRecordTimer();
      drawVisualizer();
      if (window.lucide) lucide.createIcons();

    } catch (err) {
      console.error('Microphone error:', err);
      showToast('Microphone access denied: ' + err.message, true);
    }
  }

  function togglePauseRecording() {
    if (!mediaRecorder) return;
    if (mediaRecorder.state === 'recording') {
      mediaRecorder.pause();
      clearInterval(recordTimerInterval);
      recordElapsedBeforePause += Date.now() - recordStartTime;
      pauseRecordBtn.innerHTML = '<i data-lucide="play" class="w-4 h-4"></i>';
      recordStatus.textContent = 'Recording paused';
      recordStatus.className = 'text-[11px] text-amber-400 font-medium mt-2.5';
    } else if (mediaRecorder.state === 'paused') {
      mediaRecorder.resume();
      recordStartTime = Date.now();
      startRecordTimer();
      pauseRecordBtn.innerHTML = '<i data-lucide="pause" class="w-4 h-4"></i>';
      recordStatus.textContent = 'Recording live audio...';
      recordStatus.className = 'text-[11px] text-rose-400 font-medium mt-2.5 animate-pulse';
    }
    if (window.lucide) lucide.createIcons();
  }

  function stopRecording() {
    if (!mediaRecorder) return;
    mediaRecorder.stop();
    clearInterval(recordTimerInterval);
    resetRecordButtons();
    recordStatus.textContent = 'Audio captured';
    recordStatus.className = 'text-[11px] text-emerald-400 font-medium mt-2.5';
  }

  function cancelRecording() {
    if (!mediaRecorder) return;
    mediaRecorder.stop();
    clearInterval(recordTimerInterval);
    audioChunks = [];
    recordedBlob = null;
    resetRecordButtons();
    recordTimer.textContent = '00:00.0';
    recordPreviewCard.classList.add('hidden');
    recordStatus.textContent = 'Recording discarded';
    recordStatus.className = 'text-[11px] text-slate-500 mt-2.5';
  }

  function resetRecordButtons() {
    startRecordBtn.classList.remove('hidden');
    pauseRecordBtn.classList.add('hidden');
    stopRecordBtn.classList.add('hidden');
    cancelRecordBtn.classList.add('hidden');
    if (window.lucide) lucide.createIcons();
  }

  function startRecordTimer() {
    recordTimerInterval = setInterval(() => {
      const elapsed = recordElapsedBeforePause + (Date.now() - recordStartTime);
      const totalSec = elapsed / 1000;
      const mins = Math.floor(totalSec / 60);
      const secs = Math.floor(totalSec % 60);
      const tenths = Math.floor((totalSec % 1) * 10);
      recordTimer.textContent = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}.${tenths}`;
    }, 100);
  }

  function drawVisualizer() {
    if (!analyserNode) return;
    const canvas = waveformCanvas;
    const ctx = canvas.getContext('2d');
    const bufferLength = analyserNode.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    const render = () => {
      animFrameId = requestAnimationFrame(render);
      analyserNode.getByteFrequencyData(dataArray);

      ctx.fillStyle = '#07080c';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      const barWidth = (canvas.width / bufferLength) * 2.5;
      let x = 0;

      for (let i = 0; i < bufferLength; i++) {
        const barHeight = (dataArray[i] / 255) * (canvas.height * 0.9);
        const gradient = ctx.createLinearGradient(0, canvas.height, 0, 0);
        gradient.addColorStop(0, '#6366f1');
        gradient.addColorStop(1, '#38bdf8');

        ctx.fillStyle = gradient;
        ctx.fillRect(x, canvas.height - barHeight, barWidth - 1.5, barHeight);
        x += barWidth + 1;
      }
    };
    render();
  }

  function clearCanvas() {
    const ctx = waveformCanvas.getContext('2d');
    ctx.fillStyle = '#07080c';
    ctx.fillRect(0, 0, waveformCanvas.width, waveformCanvas.height);
  }

  // ----------------------------------------------------
  // Whisper STT: Configuration Controls
  // ----------------------------------------------------
  modelRadios.forEach(radio => {
    radio.addEventListener('change', () => {
      document.querySelectorAll('.model-card').forEach(card => {
        card.className = 'model-card border border-white/[0.07] bg-obsidian-950/60 rounded-xl p-3 cursor-pointer transition-all flex flex-col justify-between';
      });
      const parent = radio.closest('.model-card');
      parent.className = 'model-card selected-model border border-indigo-500/60 bg-indigo-500/[0.08] rounded-xl p-3 cursor-pointer transition-all flex flex-col justify-between';
    });
  });

  taskTranscribeBtn.addEventListener('click', () => setTaskMode('transcribe'));
  taskTranslateBtn.addEventListener('click', () => setTaskMode('translate'));

  function setTaskMode(mode) {
    currentTask = mode;
    if (mode === 'transcribe') {
      taskTranscribeBtn.className = 'py-1.5 px-2 rounded-lg text-xs font-medium bg-indigo-600 text-white transition';
      taskTranslateBtn.className = 'py-1.5 px-2 rounded-lg text-xs font-medium text-slate-400 hover:text-slate-200 transition';
    } else {
      taskTranslateBtn.className = 'py-1.5 px-2 rounded-lg text-xs font-medium bg-indigo-600 text-white transition';
      taskTranscribeBtn.className = 'py-1.5 px-2 rounded-lg text-xs font-medium text-slate-400 hover:text-slate-200 transition';
    }
  }

  temperatureSlider.addEventListener('input', (e) => {
    tempValue.textContent = Number(e.target.value).toFixed(1);
  });

  // ----------------------------------------------------
  // Whisper STT: Transcribe Execution
  // ----------------------------------------------------
  transcribeBtn.addEventListener('click', handleTranscribe);

  async function handleTranscribe() {
    let fileToUpload = null;

    if (activeInputTab === 'upload') {
      if (!currentFile) {
        showToast('Please select or drop an audio file first.', true);
        return;
      }
      fileToUpload = currentFile;
    } else {
      if (!recordedBlob) {
        showToast('Please record audio first before transcribing.', true);
        return;
      }
      fileToUpload = new File([recordedBlob], 'recording.webm', { type: recordedBlob.type || 'audio/webm' });
    }

    const selectedModelRadio = document.querySelector('input[name="model"]:checked');
    const modelName = selectedModelRadio ? selectedModelRadio.value : 'base';
    const language = languageSelect.value;
    const wordTimestamps = wordTimestampsCheckbox.checked;
    const temperature = parseFloat(temperatureSlider.value);
    const initialPrompt = initialPromptInput.value.trim();

    const formData = new FormData();
    formData.append('file', fileToUpload);
    formData.append('model_name', modelName);
    formData.append('task', currentTask);
    formData.append('word_timestamps', wordTimestamps);
    formData.append('temperature', temperature);
    if (language !== 'auto') {
      formData.append('language', language);
    }
    if (initialPrompt) {
      formData.append('initial_prompt', initialPrompt);
    }

    transcribeBtn.disabled = true;
    loadingIndicator.classList.remove('hidden');
    let elapsedSec = 0;
    loadingTimer.textContent = '00:00';
    const timerInterval = setInterval(() => {
      elapsedSec++;
      const m = Math.floor(elapsedSec / 60);
      const s = elapsedSec % 60;
      loadingTimer.textContent = `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
    }, 1000);

    try {
      loadingStatusText.innerHTML = '<i data-lucide="loader-2" class="w-3.5 h-3.5 animate-spin"></i> Running Whisper inference...';
      if (window.lucide) lucide.createIcons();

      const response = await fetch('/api/transcribe', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Transcription failed');
      }

      const data = await response.json();
      transcriptionResult = data;

      if (currentAudioUrl) {
        URL.revokeObjectURL(currentAudioUrl);
      }
      currentAudioUrl = URL.createObjectURL(fileToUpload);
      mainAudioPlayer.src = currentAudioUrl;

      renderResults(data);

      saveToHistory({
        id: Date.now(),
        type: 'stt',
        date: new Date().toLocaleString(),
        filename: fileToUpload.name,
        duration: data.duration,
        processing_time: data.processing_time,
        speed_factor: data.speed_factor,
        language_name: data.language_name,
        model_used: data.model_used,
        text: data.text,
        segments: data.segments,
        words: data.words || [],
        has_word_timestamps: data.has_word_timestamps,
        srt: data.srt,
        vtt: data.vtt
      });

      showToast('Transcription completed');
    } catch (err) {
      console.error(err);
      showToast('Error: ' + err.message, true);
    } finally {
      clearInterval(timerInterval);
      loadingIndicator.classList.add('hidden');
      transcribeBtn.disabled = false;
      if (window.lucide) lucide.createIcons();
    }
  }

  // ----------------------------------------------------
  // Whisper STT: Render Results & Views
  // ----------------------------------------------------
  function renderResults(data) {
    emptyResultPlaceholder.classList.add('hidden');
    resultContainer.classList.remove('hidden');

    statDuration.textContent = formatDuration(data.duration);
    statTime.textContent = `${data.processing_time}s`;
    statSpeed.textContent = `${data.speed_factor}x`;
    statLanguage.textContent = data.language_name || data.language;

    renderSegments(data.segments);

    const words = data.words || [];
    renderWordsGrid(words);
    if (words.length > 0) {
      viewWordsBtn.innerHTML = `<i data-lucide="clock" class="w-3.5 h-3.5 text-indigo-400"></i> Words (${words.length})`;
    } else {
      viewWordsBtn.innerHTML = `<i data-lucide="clock" class="w-3.5 h-3.5 text-slate-500"></i> Words`;
    }

    plainTextContent.textContent = data.text;
    const wordCount = data.text.trim() ? data.text.trim().split(/\s+/).length : 0;
    textStatsInfo.textContent = `${wordCount} words · ${data.text.length} characters`;

    srtContent.textContent = data.srt;
    switchResultView('segments');
    setupAudioTracking(data.segments);

    if (window.lucide) lucide.createIcons();
  }

  function renderSegments(segments, searchQuery = '') {
    segmentsViewContainer.innerHTML = '';
    const query = searchQuery.trim().toLowerCase();

    if (!segments || segments.length === 0) {
      segmentsViewContainer.innerHTML = '<p class="text-xs text-slate-500 py-8 text-center">No speech segments detected in audio.</p>';
      return;
    }

    segments.forEach((seg, idx) => {
      const segText = seg.text;
      if (query && !segText.toLowerCase().includes(query)) {
        return;
      }

      const card = document.createElement('div');
      card.className = 'segment-card p-3.5 rounded-xl bg-obsidian-950/60 border border-white/[0.06] cursor-pointer flex flex-col gap-2';
      card.dataset.start = seg.start;
      card.dataset.end = seg.end;
      card.dataset.index = idx;

      const header = document.createElement('div');
      header.className = 'flex items-center justify-between text-[11px]';

      const timeBadge = document.createElement('span');
      timeBadge.className = 'font-mono text-indigo-300 bg-indigo-500/10 px-2 py-0.5 rounded-md border border-indigo-500/20 flex items-center gap-1.5';
      timeBadge.innerHTML = `<i data-lucide="play" class="w-2.5 h-2.5 fill-current"></i> ${formatTimestamp(seg.start)} → ${formatTimestamp(seg.end)}`;

      const segNum = document.createElement('span');
      segNum.className = 'font-mono text-[10px] text-slate-500';
      segNum.textContent = `#${String(idx + 1).padStart(2, '0')}`;

      header.appendChild(timeBadge);
      header.appendChild(segNum);
      card.appendChild(header);

      const textElem = document.createElement('p');
      textElem.className = 'text-xs text-slate-200 leading-relaxed';

      if (seg.words && seg.words.length > 0) {
        seg.words.forEach(w => {
          const wSpan = document.createElement('span');
          wSpan.className = 'word-span';
          wSpan.textContent = w.word + ' ';
          wSpan.dataset.start = w.start;
          wSpan.dataset.end = w.end;
          wSpan.title = `${formatTimestamp(w.start)} – ${formatTimestamp(w.end)} (${Math.round((w.probability || 1) * 100)}%)`;
          
          wSpan.addEventListener('click', (e) => {
            e.stopPropagation();
            mainAudioPlayer.currentTime = w.start;
            mainAudioPlayer.play();
          });

          textElem.appendChild(wSpan);
        });
      } else {
        if (query) {
          textElem.innerHTML = highlightMatch(segText, query);
        } else {
          textElem.textContent = segText;
        }
      }

      card.appendChild(textElem);

      card.addEventListener('click', () => {
        mainAudioPlayer.currentTime = seg.start;
        mainAudioPlayer.play();
      });

      segmentsViewContainer.appendChild(card);
    });

    if (window.lucide) lucide.createIcons();
  }

  function renderWordsGrid(words, searchQuery = '') {
    wordsGrid.innerHTML = '';
    const query = searchQuery.trim().toLowerCase();

    if (!words || words.length === 0) {
      wordsGrid.innerHTML = '<p class="col-span-full text-xs text-slate-500 py-8 text-center">No word-level timestamps available. Enable "Word-by-Word Timestamps" before transcribing.</p>';
      wordsStatsInfo.textContent = '0 words';
      return;
    }

    const filtered = query ? words.filter(w => w.word.toLowerCase().includes(query)) : words;
    wordsStatsInfo.textContent = `${filtered.length} of ${words.length} word tokens`;

    filtered.forEach((w, idx) => {
      const card = document.createElement('div');
      card.className = 'word-card p-2.5 rounded-xl bg-obsidian-950/60 border border-white/[0.06] hover:border-indigo-500/40 cursor-pointer flex flex-col justify-between gap-1.5';
      card.dataset.start = w.start;
      card.dataset.end = w.end;
      card.dataset.index = idx;

      const durMs = Math.round((w.end - w.start) * 1000);
      const probPct = Math.round((w.probability !== undefined ? w.probability : 1.0) * 100);

      card.innerHTML = `
        <div class="flex items-center justify-between gap-1">
          <span class="text-xs font-semibold text-white truncate">${escapeHtml(w.word)}</span>
          <span class="text-[10px] px-1.5 py-0.2 rounded bg-white/[0.04] text-slate-400 font-mono">${durMs}ms</span>
        </div>
        <div class="flex items-center justify-between text-[10px] pt-1 border-t border-white/[0.05]">
          <span class="font-mono text-indigo-400">${formatTimestamp(w.start)}</span>
          <span class="font-mono text-emerald-400/90">${probPct}%</span>
        </div>
      `;

      card.addEventListener('click', () => {
        mainAudioPlayer.currentTime = w.start;
        mainAudioPlayer.play();
      });

      wordsGrid.appendChild(card);
    });
  }

  function setupAudioTracking() {
    mainAudioPlayer.ontimeupdate = () => {
      const curTime = mainAudioPlayer.currentTime;

      const allCards = segmentsViewContainer.querySelectorAll('.segment-card');
      allCards.forEach(card => {
        const start = parseFloat(card.dataset.start);
        const end = parseFloat(card.dataset.end);

        if (curTime >= start && curTime <= end) {
          if (!card.classList.contains('active-playback')) {
            card.classList.add('active-playback');
            card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
          }
        } else {
          card.classList.remove('active-playback');
        }
      });

      const allWordSpans = segmentsViewContainer.querySelectorAll('.word-span');
      allWordSpans.forEach(wSpan => {
        const wStart = parseFloat(wSpan.dataset.start);
        const wEnd = parseFloat(wSpan.dataset.end);
        if (curTime >= wStart && curTime <= wEnd) {
          wSpan.classList.add('active-word');
        } else {
          wSpan.classList.remove('active-word');
        }
      });

      const allWordCards = wordsGrid.querySelectorAll('.word-card');
      allWordCards.forEach(wCard => {
        const wStart = parseFloat(wCard.dataset.start);
        const wEnd = parseFloat(wCard.dataset.end);
        if (curTime >= wStart && curTime <= wEnd) {
          if (!wCard.classList.contains('active-word-card')) {
            wCard.classList.add('active-word-card');
            wCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
          }
        } else {
          wCard.classList.remove('active-word-card');
        }
      });
    };
  }

  speedBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      speedBtns.forEach(b => {
        b.className = 'speed-btn px-2 py-0.5 text-[11px] font-mono rounded-md text-slate-400 hover:text-white transition';
      });
      btn.className = 'speed-btn px-2 py-0.5 text-[11px] font-mono rounded-md bg-indigo-600 text-white font-semibold transition';
      mainAudioPlayer.playbackRate = parseFloat(btn.dataset.speed);
    });
  });

  viewSegmentsBtn.addEventListener('click', () => switchResultView('segments'));
  viewWordsBtn.addEventListener('click', () => switchResultView('words'));
  viewTextBtn.addEventListener('click', () => switchResultView('text'));
  viewSubtitlesBtn.addEventListener('click', () => switchResultView('subtitles'));

  function switchResultView(view) {
    const activeClass = 'px-3 py-1.5 rounded-lg text-xs font-semibold bg-indigo-600 text-white transition flex items-center gap-1.5 whitespace-nowrap';
    const inactiveClass = 'px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-white transition flex items-center gap-1.5 whitespace-nowrap';

    viewSegmentsBtn.className = view === 'segments' ? activeClass : inactiveClass;
    viewWordsBtn.className = view === 'words' ? activeClass : inactiveClass;
    viewTextBtn.className = view === 'text' ? activeClass : inactiveClass;
    viewSubtitlesBtn.className = view === 'subtitles' ? activeClass : inactiveClass;

    segmentsViewContainer.classList.toggle('hidden', view !== 'segments');
    wordsViewContainer.classList.toggle('hidden', view !== 'words');
    textViewContainer.classList.toggle('hidden', view !== 'text');
    subtitlesViewContainer.classList.toggle('hidden', view !== 'subtitles');

    if (window.lucide) lucide.createIcons();
  }

  searchInput.addEventListener('input', (e) => {
    const val = e.target.value.trim();
    clearSearchBtn.classList.toggle('hidden', val.length === 0);

    if (transcriptionResult) {
      if (transcriptionResult.segments) {
        renderSegments(transcriptionResult.segments, val);
      }
      if (transcriptionResult.words) {
        renderWordsGrid(transcriptionResult.words, val);
      }
    }
  });

  clearSearchBtn.addEventListener('click', () => {
    searchInput.value = '';
    clearSearchBtn.classList.add('hidden');
    if (transcriptionResult) {
      if (transcriptionResult.segments) {
        renderSegments(transcriptionResult.segments);
      }
      if (transcriptionResult.words) {
        renderWordsGrid(transcriptionResult.words);
      }
    }
  });

  copyBtn.addEventListener('click', async () => {
    if (!transcriptionResult) return;
    try {
      await navigator.clipboard.writeText(transcriptionResult.text);
      showToast('Copied transcript to clipboard');
    } catch (e) {
      showToast('Failed to copy text', true);
    }
  });

  downloadDropdownBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    downloadMenu.classList.toggle('hidden');
  });

  document.addEventListener('click', () => {
    downloadMenu.classList.add('hidden');
  });

  downloadOptBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      downloadMenu.classList.add('hidden');
      const format = btn.dataset.format;
      downloadResultAs(format);
    });
  });

  function downloadResultAs(format) {
    if (!transcriptionResult) return;
    const baseName = (transcriptionResult.filename || 'transcription').replace(/\.[^/.]+$/, '');
    let content = '';
    let mimeType = 'text/plain';
    let ext = format;

    if (format === 'txt') {
      content = transcriptionResult.text;
    } else if (format === 'srt') {
      content = transcriptionResult.srt;
    } else if (format === 'vtt') {
      content = transcriptionResult.vtt;
    } else if (format === 'csv') {
      const words = transcriptionResult.words || [];
      const rows = ['word,start_seconds,end_seconds,duration_seconds,probability'];
      words.forEach(w => {
        const escaped = `"${(w.word || '').replace(/"/g, '""')}"`;
        const dur = (w.end - w.start).toFixed(2);
        rows.push(`${escaped},${w.start},${w.end},${dur},${w.probability !== undefined ? w.probability : 1.0}`);
      });
      content = rows.join('\n');
      mimeType = 'text/csv';
    } else if (format === 'json') {
      content = JSON.stringify(transcriptionResult, null, 2);
      mimeType = 'application/json';
    }

    const blob = new Blob([content], { type: mimeType + ';charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${baseName}_transcript.${ext}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showToast(`Exported .${ext.toUpperCase()} file`);
  }

  // ----------------------------------------------------
  // Kokoro TTS: Voices, Community Blends & Mixer Lab
  // ----------------------------------------------------
  const voiceLibrarySubtitle = document.getElementById('voiceLibrarySubtitle');
  const filterAllVoicesBtn = document.getElementById('filterAllVoicesBtn');
  const filterCommunityVoicesBtn = document.getElementById('filterCommunityVoicesBtn');
  const toggleVoiceMixerBtn = document.getElementById('toggleVoiceMixerBtn');
  const closeVoiceMixerBtn = document.getElementById('closeVoiceMixerBtn');
  const voiceMixerPanel = document.getElementById('voiceMixerPanel');
  const mixVoiceASelect = document.getElementById('mixVoiceASelect');
  const mixVoiceBSelect = document.getElementById('mixVoiceBSelect');
  const mixWeightSlider = document.getElementById('mixWeightSlider');
  const mixWeightLabel = document.getElementById('mixWeightLabel');
  const mixVoiceNameInput = document.getElementById('mixVoiceNameInput');
  const mixVoiceTraitInput = document.getElementById('mixVoiceTraitInput');
  const mixVoiceAvatarInput = document.getElementById('mixVoiceAvatarInput');
  const saveCustomVoiceBtn = document.getElementById('saveCustomVoiceBtn');

  async function fetchVoices() {
    try {
      const res = await fetch('/api/tts/voices');
      if (!res.ok) return;
      allVoices = await res.json();
      updateVoiceCountsAndMixerOptions();
      applyVoiceFilters();
    } catch (e) {
      console.warn('Could not load Kokoro voices:', e);
    }
  }

  function updateVoiceCountsAndMixerOptions() {
    const totalCount = allVoices.length;
    const communityCount = allVoices.filter(v => v.category === 'community' || v.community).length;

    if (voiceLibrarySubtitle) {
      voiceLibrarySubtitle.textContent = `${totalCount} neural voices · Official, ${communityCount} Community Blends & Global`;
    }
    if (filterAllVoicesBtn) {
      filterAllVoicesBtn.textContent = `All (${totalCount})`;
    }
    if (filterCommunityVoicesBtn) {
      filterCommunityVoicesBtn.textContent = `✨ Community (${communityCount})`;
    }

    // Populate base voices for the Community Voice Lab Mixer
    if (mixVoiceASelect && mixVoiceBSelect) {
      const baseVoices = allVoices.filter(v => v.category === 'official' || v.category === 'international');
      const prevA = mixVoiceASelect.value || 'af_heart';
      const prevB = mixVoiceBSelect.value || 'af_nicole';

      mixVoiceASelect.innerHTML = '';
      mixVoiceBSelect.innerHTML = '';

      baseVoices.forEach(v => {
        const label = `${v.flag || ''} ${v.name} — ${v.accent} ${v.gender} (${v.trait})`;
        const optA = document.createElement('option');
        optA.value = v.id;
        optA.textContent = label;
        mixVoiceASelect.appendChild(optA);

        const optB = document.createElement('option');
        optB.value = v.id;
        optB.textContent = label;
        mixVoiceBSelect.appendChild(optB);
      });

      mixVoiceASelect.value = prevA;
      mixVoiceBSelect.value = prevB === prevA && baseVoices.length > 1 ? baseVoices[1].id : prevB;
      updateMixWeightReadout();
    }
  }

  function updateMixWeightReadout() {
    if (!mixWeightSlider || !mixWeightLabel) return;
    const wA = parseInt(mixWeightSlider.value, 10) || 50;
    const wB = 100 - wA;
    const vA = allVoices.find(v => v.id === (mixVoiceASelect && mixVoiceASelect.value));
    const vB = allVoices.find(v => v.id === (mixVoiceBSelect && mixVoiceBSelect.value));
    const nameA = vA ? vA.name : 'Voice A';
    const nameB = vB ? vB.name : 'Voice B';
    mixWeightLabel.textContent = `${wA}% ${nameA} + ${wB}% ${nameB}`;
  }

  if (toggleVoiceMixerBtn && voiceMixerPanel) {
    toggleVoiceMixerBtn.addEventListener('click', () => {
      voiceMixerPanel.classList.toggle('hidden');
      if (window.lucide) lucide.createIcons();
    });
  }

  if (closeVoiceMixerBtn && voiceMixerPanel) {
    closeVoiceMixerBtn.addEventListener('click', () => {
      voiceMixerPanel.classList.add('hidden');
    });
  }

  if (mixWeightSlider) {
    mixWeightSlider.addEventListener('input', updateMixWeightReadout);
  }
  if (mixVoiceASelect) {
    mixVoiceASelect.addEventListener('change', updateMixWeightReadout);
  }
  if (mixVoiceBSelect) {
    mixVoiceBSelect.addEventListener('change', updateMixWeightReadout);
  }

  if (saveCustomVoiceBtn) {
    saveCustomVoiceBtn.addEventListener('click', async () => {
      const name = (mixVoiceNameInput ? mixVoiceNameInput.value : '').trim();
      if (!name) {
        showToast('Please enter a Persona Name for your community voice.', true);
        if (mixVoiceNameInput) mixVoiceNameInput.focus();
        return;
      }

      const voiceA = mixVoiceASelect ? mixVoiceASelect.value : 'af_heart';
      const voiceB = mixVoiceBSelect ? mixVoiceBSelect.value : 'af_nicole';
      if (voiceA === voiceB) {
        showToast('Please choose two different base voices to blend.', true);
        return;
      }

      const weightA = parseInt(mixWeightSlider ? mixWeightSlider.value : '50', 10);
      const trait = (mixVoiceTraitInput ? mixVoiceTraitInput.value : '').trim();
      const avatar = (mixVoiceAvatarInput ? mixVoiceAvatarInput.value : '🧪').trim() || '🧪';

      saveCustomVoiceBtn.disabled = true;
      try {
        const res = await fetch('/api/tts/voices/custom', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            name,
            voice_a: voiceA,
            voice_b: voiceB,
            weight_a: weightA,
            trait,
            avatar
          })
        });

        const data = await res.json();
        if (!res.ok) {
          throw new Error(data.detail || 'Could not create custom community voice');
        }

        allVoices = data.voices || allVoices;
        selectedVoice = data.voice.id;
        updateVoiceCountsAndMixerOptions();
        applyVoiceFilters();
        updateSelectedVoiceInfo(data.voice);

        if (mixVoiceNameInput) mixVoiceNameInput.value = '';
        if (mixVoiceTraitInput) mixVoiceTraitInput.value = '';
        if (voiceMixerPanel) voiceMixerPanel.classList.add('hidden');

        showToast(`Created community voice "${data.voice.name}" (${data.voice.blend_label})`);
      } catch (err) {
        showToast(err.message, true);
      } finally {
        saveCustomVoiceBtn.disabled = false;
      }
    });
  }

  async function deleteCustomVoice(voiceId, voiceName) {
    try {
      const res = await fetch(`/api/tts/voices/custom/${encodeURIComponent(voiceId)}`, {
        method: 'DELETE'
      });
      if (!res.ok) return;
      const data = await res.json();
      allVoices = data.voices || allVoices;
      if (selectedVoice === voiceId) {
        selectedVoice = 'af_heart';
      }
      updateVoiceCountsAndMixerOptions();
      applyVoiceFilters();
      showToast(`Removed custom voice "${voiceName}"`);
    } catch (e) {
      showToast('Failed to remove custom voice', true);
    }
  }

  function applyVoiceFilters() {
    let filtered = allVoices;

    if (activeVoiceFilter === 'community') {
      filtered = filtered.filter(v => v.category === 'community' || v.community);
    } else if (activeVoiceFilter === 'official') {
      filtered = filtered.filter(v => v.category === 'official');
    } else if (activeVoiceFilter === 'international') {
      filtered = filtered.filter(v => v.category === 'international');
    } else if (activeVoiceFilter === 'us') {
      filtered = filtered.filter(v => v.accent.toLowerCase().includes('american'));
    } else if (activeVoiceFilter === 'uk') {
      filtered = filtered.filter(v => v.accent.toLowerCase().includes('british'));
    } else if (activeVoiceFilter === 'female') {
      filtered = filtered.filter(v => v.gender.toLowerCase() === 'female');
    } else if (activeVoiceFilter === 'male') {
      filtered = filtered.filter(v => v.gender.toLowerCase() === 'male');
    }

    if (voiceSearchQuery) {
      const q = voiceSearchQuery.toLowerCase();
      filtered = filtered.filter(v =>
        v.name.toLowerCase().includes(q) ||
        v.trait.toLowerCase().includes(q) ||
        v.accent.toLowerCase().includes(q) ||
        (v.blend_label && v.blend_label.toLowerCase().includes(q))
      );
    }

    renderVoiceCards(filtered);
  }

  function renderVoiceCards(voices) {
    voicesGrid.innerHTML = '';

    if (voices.length === 0) {
      voicesGrid.innerHTML = '<p class="col-span-full text-xs text-slate-500 py-8 text-center">No matching voices found.</p>';
      return;
    }

    voices.forEach(v => {
      const isSelected = v.id === selectedVoice;
      const isCommunity = v.category === 'community' || v.community;
      const isGlobal = v.category === 'international';

      const card = document.createElement('div');
      card.className = `voice-card p-3 rounded-xl border cursor-pointer flex items-center justify-between gap-2 ${
        isSelected
          ? 'selected-voice border-purple-500/70 bg-purple-500/10'
          : 'border-white/[0.06] bg-obsidian-950/60'
      }`;

      let badgeHtml = '';
      if (v.custom) {
        badgeHtml = '<span class="text-[9px] font-mono bg-amber-500/20 text-amber-300 border border-amber-500/30 px-1.5 py-0.2 rounded">CUSTOM</span>';
      } else if (isCommunity) {
        badgeHtml = '<span class="text-[9px] font-mono bg-fuchsia-500/20 text-fuchsia-300 border border-fuchsia-500/30 px-1.5 py-0.2 rounded">COMMUNITY</span>';
      } else if (isGlobal) {
        badgeHtml = `<span class="text-[9px] font-mono bg-emerald-500/15 text-emerald-300 border border-emerald-500/25 px-1.5 py-0.2 rounded">${escapeHtml(v.accent.toUpperCase())}</span>`;
      } else if (v.recommended) {
        badgeHtml = '<span class="text-[9px] font-mono bg-purple-500/20 text-purple-300 border border-purple-500/30 px-1.5 py-0.2 rounded">FLAGSHIP</span>';
      }

      const blendRecipeHtml = v.blend_label
        ? `<p class="text-[10px] font-mono text-purple-300/85 truncate mt-0.5 flex items-center gap-1">
             <span class="inline-block w-1.5 h-1.5 rounded-full bg-purple-400"></span>
             ${escapeHtml(v.blend_label)}
           </p>`
        : '';

      const genderClass = v.gender === 'Female'
        ? 'bg-pink-500/10 text-pink-300 border border-pink-500/20'
        : v.gender === 'Male'
          ? 'bg-sky-500/10 text-sky-300 border border-sky-500/20'
          : 'bg-purple-500/10 text-purple-300 border border-purple-500/20';

      card.innerHTML = `
        <div class="flex items-center gap-3 overflow-hidden">
          <div class="w-9 h-9 rounded-xl bg-white/[0.04] border border-white/[0.07] flex items-center justify-center text-base shrink-0">
            ${v.avatar || '🎙️'}
          </div>
          <div class="truncate">
            <div class="flex items-center gap-1.5 flex-wrap">
              <span class="text-xs font-semibold text-white">${escapeHtml(v.name)}</span>
              <span class="text-[11px]">${v.flag || ''}</span>
              ${badgeHtml}
            </div>
            <p class="text-[11px] text-slate-400 truncate mt-0.5">${escapeHtml(v.trait)}</p>
            ${blendRecipeHtml}
          </div>
        </div>

        <div class="flex items-center gap-1.5 shrink-0 pl-1">
          ${v.custom ? `
            <button type="button" class="del-custom-voice-btn p-1 rounded-lg text-slate-500 hover:text-rose-400 hover:bg-white/[0.06] transition" title="Delete custom voice">
              <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
            </button>
          ` : ''}
          <span class="text-[10px] font-mono px-1.5 py-0.5 rounded ${genderClass}">
            ${escapeHtml(v.gender)}
          </span>
          <div class="w-3.5 h-3.5 rounded-full border flex items-center justify-center ${isSelected ? 'border-purple-400 bg-purple-500' : 'border-white/20'}">
            ${isSelected ? '<span class="w-1.5 h-1.5 rounded-full bg-white"></span>' : ''}
          </div>
        </div>
      `;

      const delBtn = card.querySelector('.del-custom-voice-btn');
      if (delBtn) {
        delBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          deleteCustomVoice(v.id, v.name);
        });
      }

      card.addEventListener('click', () => {
        selectedVoice = v.id;
        applyVoiceFilters();
        updateSelectedVoiceInfo(v);
        const desc = v.blend_label ? `${v.name} (${v.blend_label})` : `${v.name} (${v.accent})`;
        showToast(`Selected ${desc}`);
      });

      voicesGrid.appendChild(card);
    });

    if (window.lucide) lucide.createIcons();
  }

  function updateSelectedVoiceInfo(v) {
    if (!v) return;
    playerVoiceAvatar.textContent = v.avatar || '❤️';
    playerVoiceName.textContent = `${v.name} (${v.accent})`;
    playerVoiceTrait.textContent = v.blend_label ? `${v.trait} · ${v.blend_label}` : v.trait;
  }

  voiceFilterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      voiceFilterBtns.forEach(b => {
        b.className = 'voice-filter-btn px-2.5 py-1 rounded-lg font-semibold text-slate-400 hover:text-white transition whitespace-nowrap';
      });
      btn.className = 'voice-filter-btn px-2.5 py-1 rounded-lg font-semibold bg-purple-600 text-white transition whitespace-nowrap';

      activeVoiceFilter = btn.dataset.filter;
      applyVoiceFilters();
    });
  });

  if (voiceSearchInput) {
    voiceSearchInput.addEventListener('input', (e) => {
      voiceSearchQuery = e.target.value.trim();
      applyVoiceFilters();
    });
  }

  // TTS Input Helpers & Samples
  ttsTextInput.addEventListener('input', updateTtsCharCount);

  function updateTtsCharCount() {
    const text = ttsTextInput.value;
    const chars = text.length;
    const words = text.trim() ? text.trim().split(/\s+/).length : 0;
    ttsCharCount.textContent = `${chars} characters · ${words} words`;
  }

  clearTtsTextBtn.addEventListener('click', () => {
    ttsTextInput.value = '';
    updateTtsCharCount();
  });

  const sampleTexts = {
    greeting: "Hello there! Welcome to Voice AI Studio. Powered by Kokoro-82M, I can turn any written script into natural, expressive speech in real time.",
    story: "Deep within the quiet observatory, where starlight filtered through the glass dome, an old radio receiver began to hum with a signal from across the sea.",
    assistant: "Good morning. All neural speech pipelines are online. Your Whisper transcription engine and Kokoro voice models are cached and ready."
  };

  ttsSampleBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const type = btn.dataset.sample;
      if (sampleTexts[type]) {
        ttsTextInput.value = sampleTexts[type];
        updateTtsCharCount();
        showToast('Loaded preset script');
      }
    });
  });

  ttsSpeedSlider.addEventListener('input', (e) => {
    ttsSpeedVal.textContent = `${parseFloat(e.target.value).toFixed(2)}x`;
  });

  generateSpeechBtn.addEventListener('click', handleGenerateSpeech);

  async function handleGenerateSpeech() {
    const text = ttsTextInput.value.trim();
    if (!text) {
      showToast('Please enter text to synthesize.', true);
      ttsTextInput.focus();
      return;
    }

    const speed = parseFloat(ttsSpeedSlider.value);

    generateSpeechBtn.disabled = true;
    ttsLoadingIndicator.classList.remove('hidden');

    let elapsedSec = 0;
    ttsLoadingTimer.textContent = '00:00';
    const timerInterval = setInterval(() => {
      elapsedSec++;
      const m = Math.floor(elapsedSec / 60);
      const s = elapsedSec % 60;
      ttsLoadingTimer.textContent = `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
    }, 1000);

    try {
      const res = await fetch('/api/tts/synthesize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: text,
          voice: selectedVoice,
          speed: speed
        })
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Synthesis failed');
      }

      const data = await res.json();

      ttsPlayerCard.classList.remove('hidden');
      ttsAudioPlayer.src = data.audio_url;
      ttsAudioPlayer.play();

      downloadTtsAudioBtn.href = data.audio_url;
      downloadTtsAudioBtn.download = `voice_ai_${data.voice}_${Date.now()}.wav`;

      lastTtsFilename = data.filename;
      lastTtsAudioBlob = data.audio_url;
      updateCompressorSourceOptions();

      ttsStatDuration.textContent = `${data.duration}s`;
      ttsStatGenTime.textContent = `${data.processing_time}s`;
      ttsStatSpeed.textContent = `${data.speed_ratio}x`;

      if (data.voice_info) {
        updateSelectedVoiceInfo(data.voice_info);
      }

      saveToHistory({
        id: Date.now(),
        type: 'tts',
        date: new Date().toLocaleString(),
        voice: data.voice,
        voice_name: data.voice_info ? data.voice_info.name : data.voice,
        duration: data.duration,
        processing_time: data.processing_time,
        speed_factor: data.speed_ratio,
        text: data.text,
        audio_url: data.audio_url
      });

      showToast('Audio synthesized with Kokoro');
    } catch (err) {
      console.error(err);
      showToast('TTS Error: ' + err.message, true);
    } finally {
      clearInterval(timerInterval);
      ttsLoadingIndicator.classList.add('hidden');
      generateSpeechBtn.disabled = false;
      if (window.lucide) lucide.createIcons();
    }
  }

  // ----------------------------------------------------
  // Audio Compressor & DSP Leveler Studio
  // ----------------------------------------------------
  const compLoadSttBtn = document.getElementById('compLoadSttBtn');
  const compLoadTtsBtn = document.getElementById('compLoadTtsBtn');
  const compDropZone = document.getElementById('compDropZone');
  const compFileInput = document.getElementById('compFileInput');
  const compFileInfoCard = document.getElementById('compFileInfoCard');
  const compFileName = document.getElementById('compFileName');
  const compFileSize = document.getElementById('compFileSize');
  const compFileFormat = document.getElementById('compFileFormat');
  const compRemoveFileBtn = document.getElementById('compRemoveFileBtn');

  const compProfileBtns = document.querySelectorAll('.comp-profile-btn');
  const compFormatSelect = document.getElementById('compFormatSelect');
  const compBitrateSelect = document.getElementById('compBitrateSelect');
  const compChannelsSelect = document.getElementById('compChannelsSelect');
  const compSampleRateSelect = document.getElementById('compSampleRateSelect');

  const compEnableDspCheckbox = document.getElementById('compEnableDspCheckbox');
  const compDspControls = document.getElementById('compDspControls');
  const compThresholdSlider = document.getElementById('compThresholdSlider');
  const compThresholdVal = document.getElementById('compThresholdVal');
  const compRatioSlider = document.getElementById('compRatioSlider');
  const compRatioVal = document.getElementById('compRatioVal');
  const compMakeupSlider = document.getElementById('compMakeupSlider');
  const compMakeupVal = document.getElementById('compMakeupVal');
  const compNormalizeCheckbox = document.getElementById('compNormalizeCheckbox');

  const compressBtn = document.getElementById('compressBtn');
  const compLoadingIndicator = document.getElementById('compLoadingIndicator');
  const compLoadingTimer = document.getElementById('compLoadingTimer');

  const compEmptyPlaceholder = document.getElementById('compEmptyPlaceholder');
  const compResultContainer = document.getElementById('compResultContainer');
  const compSavingsBadge = document.getElementById('compSavingsBadge');
  const compStatOrigSize = document.getElementById('compStatOrigSize');
  const compStatNewSize = document.getElementById('compStatNewSize');
  const compStatSavedBytes = document.getElementById('compStatSavedBytes');
  const compAudioFormatBadge = document.getElementById('compAudioFormatBadge');
  const compAudioPlayer = document.getElementById('compAudioPlayer');
  const compToggleOriginalBtn = document.getElementById('compToggleOriginalBtn');
  const compOriginalPlayerWrapper = document.getElementById('compOriginalPlayerWrapper');
  const compOriginalAudioPlayer = document.getElementById('compOriginalAudioPlayer');
  const compDurationInfo = document.getElementById('compDurationInfo');
  const compDownloadBtn = document.getElementById('compDownloadBtn');
  const compSendToSttBtn = document.getElementById('compSendToSttBtn');
  const compStatCodec = document.getElementById('compStatCodec');
  const compStatChannels = document.getElementById('compStatChannels');
  const compStatSampleRate = document.getElementById('compStatSampleRate');
  const compStatProcessTime = document.getElementById('compStatProcessTime');

  const compProfiles = {
    whisper: {
      format: 'mp3',
      bitrate: '32k',
      channels: '1',
      sampleRate: '16000',
      enableDsp: true,
      threshold: -20,
      ratio: 4.0,
      makeup: 2.0,
      normalize: true
    },
    podcast: {
      format: 'mp3',
      bitrate: '64k',
      channels: '1',
      sampleRate: '44100',
      enableDsp: true,
      threshold: -18,
      ratio: 3.5,
      makeup: 2.0,
      normalize: true
    },
    balanced: {
      format: 'mp3',
      bitrate: '128k',
      channels: '2',
      sampleRate: '44100',
      enableDsp: false,
      threshold: -20,
      ratio: 3.0,
      makeup: 0.0,
      normalize: false
    },
    hifi: {
      format: 'm4a',
      bitrate: '192k',
      channels: '2',
      sampleRate: '48000',
      enableDsp: false,
      threshold: -16,
      ratio: 2.0,
      makeup: 0.0,
      normalize: false
    }
  };

  // Profile presets switching
  compProfileBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      compProfileBtns.forEach(b => {
        b.className = 'comp-profile-btn border border-white/[0.07] bg-obsidian-950/60 rounded-xl p-2.5 text-left transition-all flex flex-col justify-between';
      });
      btn.className = 'comp-profile-btn border border-emerald-500/60 bg-emerald-500/[0.08] rounded-xl p-2.5 text-left transition-all flex flex-col justify-between';

      const profKey = btn.dataset.profile;
      const conf = compProfiles[profKey];
      if (conf) {
        if (compFormatSelect) compFormatSelect.value = conf.format;
        if (compBitrateSelect) compBitrateSelect.value = conf.bitrate;
        if (compChannelsSelect) compChannelsSelect.value = conf.channels;
        if (compSampleRateSelect) compSampleRateSelect.value = conf.sampleRate;
        if (compEnableDspCheckbox) {
          compEnableDspCheckbox.checked = conf.enableDsp;
          compDspControls.classList.toggle('opacity-50', !conf.enableDsp);
        }
        if (compThresholdSlider) {
          compThresholdSlider.value = conf.threshold;
          compThresholdVal.textContent = `${conf.threshold} dB`;
        }
        if (compRatioSlider) {
          compRatioSlider.value = conf.ratio;
          compRatioVal.textContent = `${conf.ratio.toFixed(1)}:1`;
        }
        if (compMakeupSlider) {
          compMakeupSlider.value = conf.makeup;
          compMakeupVal.textContent = `+${conf.makeup.toFixed(1)} dB`;
        }
        if (compNormalizeCheckbox) compNormalizeCheckbox.checked = conf.normalize;
      }
    });
  });

  // DSP Controls
  if (compEnableDspCheckbox) {
    compEnableDspCheckbox.addEventListener('change', () => {
      const on = compEnableDspCheckbox.checked;
      compDspControls.classList.toggle('opacity-50', !on);
    });
  }

  if (compThresholdSlider) {
    compThresholdSlider.addEventListener('input', (e) => {
      compThresholdVal.textContent = `${e.target.value} dB`;
    });
  }
  if (compRatioSlider) {
    compRatioSlider.addEventListener('input', (e) => {
      compRatioVal.textContent = `${parseFloat(e.target.value).toFixed(1)}:1`;
    });
  }
  if (compMakeupSlider) {
    compMakeupSlider.addEventListener('input', (e) => {
      compMakeupVal.textContent = `+${parseFloat(e.target.value).toFixed(1)} dB`;
    });
  }

  // File Dropzone & Selection
  if (compDropZone) {
    compDropZone.addEventListener('click', () => compFileInput.click());
    compDropZone.addEventListener('dragover', (e) => {
      e.preventDefault();
      compDropZone.classList.add('border-emerald-500/80', 'bg-emerald-500/[0.06]');
    });
    compDropZone.addEventListener('dragleave', () => {
      compDropZone.classList.remove('border-emerald-500/80', 'bg-emerald-500/[0.06]');
    });
    compDropZone.addEventListener('drop', (e) => {
      e.preventDefault();
      compDropZone.classList.remove('border-emerald-500/80', 'bg-emerald-500/[0.06]');
      if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
        handleCompFileSelected(e.dataTransfer.files[0]);
      }
    });
  }

  if (compFileInput) {
    compFileInput.addEventListener('change', (e) => {
      if (e.target.files && e.target.files.length > 0) {
        handleCompFileSelected(e.target.files[0]);
      }
    });
  }

  function handleCompFileSelected(file) {
    compCurrentFile = file;
    compFileName.textContent = file.name;
    compFileSize.textContent = formatBytes(file.size);
    const ext = (file.name.split('.').pop() || 'AUDIO').toUpperCase();
    compFileFormat.textContent = ext;
    compFileInfoCard.classList.remove('hidden');
    compDropZone.classList.add('hidden');
    if (compOriginalAudioUrl) URL.revokeObjectURL(compOriginalAudioUrl);
    compOriginalAudioUrl = URL.createObjectURL(file);
    compOriginalAudioPlayer.src = compOriginalAudioUrl;
    if (window.lucide) lucide.createIcons();
  }

  if (compRemoveFileBtn) {
    compRemoveFileBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      compCurrentFile = null;
      compFileInput.value = '';
      compFileInfoCard.classList.add('hidden');
      compDropZone.classList.remove('hidden');
      if (compOriginalAudioUrl) {
        URL.revokeObjectURL(compOriginalAudioUrl);
        compOriginalAudioUrl = null;
      }
    });
  }

  function updateCompressorSourceOptions() {
    if (compLoadSttBtn) {
      const hasSttAudio = !!currentFile || !!recordedBlob;
      compLoadSttBtn.classList.toggle('hidden', !hasSttAudio);
    }
    if (compLoadTtsBtn) {
      compLoadTtsBtn.classList.toggle('hidden', !lastTtsAudioBlob);
    }
  }

  if (compLoadSttBtn) {
    compLoadSttBtn.addEventListener('click', () => {
      if (currentFile) {
        handleCompFileSelected(currentFile);
        showToast('Loaded active STT audio into Compressor');
      } else if (recordedBlob) {
        const file = new File([recordedBlob], 'microphone_recording.webm', { type: recordedBlob.type || 'audio/webm' });
        handleCompFileSelected(file);
        showToast('Loaded recorded microphone audio into Compressor');
      }
    });
  }

  if (compLoadTtsBtn) {
    compLoadTtsBtn.addEventListener('click', async () => {
      if (!lastTtsAudioBlob) return;
      try {
        const res = await fetch(lastTtsAudioBlob);
        const blob = await res.blob();
        const file = new File([blob], lastTtsFilename || 'kokoro_synthesized.wav', { type: 'audio/wav' });
        handleCompFileSelected(file);
        showToast('Loaded Kokoro TTS audio into Compressor');
      } catch (e) {
        showToast('Could not load TTS audio: ' + e.message, true);
      }
    });
  }

  // A/B Comparison Toggle
  if (compToggleOriginalBtn) {
    compToggleOriginalBtn.addEventListener('click', () => {
      const isHidden = compOriginalPlayerWrapper.classList.contains('hidden');
      compOriginalPlayerWrapper.classList.toggle('hidden', !isHidden);
      if (isHidden) {
        compToggleOriginalBtn.innerHTML = '<i data-lucide="eye-off" class="w-3.5 h-3.5"></i><span>Hide Original Player</span>';
      } else {
        compToggleOriginalBtn.innerHTML = '<i data-lucide="repeat" class="w-3.5 h-3.5"></i><span>Listen to Original (A/B Test)</span>';
      }
      if (window.lucide) lucide.createIcons();
    });
  }

  // Compress Action Button
  if (compressBtn) {
    compressBtn.addEventListener('click', handleCompressAudio);
  }

  async function handleCompressAudio() {
    if (!compCurrentFile) {
      showToast('Please select or drop an audio file first.', true);
      return;
    }

    const format = compFormatSelect.value;
    const bitrate = compBitrateSelect.value;
    const channels = compChannelsSelect.value;
    const sampleRate = compSampleRateSelect.value;
    const enableDsp = compEnableDspCheckbox.checked;
    const threshold = parseFloat(compThresholdSlider.value);
    const ratio = parseFloat(compRatioSlider.value);
    const makeupGain = parseFloat(compMakeupSlider.value);
    const normalize = compNormalizeCheckbox.checked;

    const formData = new FormData();
    formData.append('file', compCurrentFile);
    formData.append('target_format', format);
    formData.append('bitrate', bitrate);
    formData.append('channels', channels);
    formData.append('sample_rate', sampleRate);
    formData.append('enable_dsp', enableDsp);
    formData.append('threshold', threshold);
    formData.append('ratio', ratio);
    formData.append('attack', 20.0);
    formData.append('release', 250.0);
    formData.append('makeup_gain', makeupGain);
    formData.append('normalize', normalize);
    formData.append('target_lufs', -16.0);

    compressBtn.disabled = true;
    compLoadingIndicator.classList.remove('hidden');
    let elapsedSec = 0;
    compLoadingTimer.textContent = '00:00';
    const timerInterval = setInterval(() => {
      elapsedSec++;
      const m = Math.floor(elapsedSec / 60);
      const s = elapsedSec % 60;
      compLoadingTimer.textContent = `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
    }, 1000);

    try {
      const response = await fetch('/api/compress', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Compression failed');
      }

      const data = await response.json();
      compResult = data;
      renderCompressResults(data);

      saveToHistory({
        id: Date.now(),
        type: 'compressor',
        date: new Date().toLocaleString(),
        filename: data.filename,
        original_filename: data.original_filename,
        original_size: data.original_size,
        compressed_size: data.compressed_size,
        saved_bytes: data.saved_bytes,
        saved_percent: data.saved_percent,
        format: data.format,
        bitrate: data.bitrate,
        duration: data.duration,
        audio_url: data.audio_url,
        processing_time: data.processing_time
      });

      showToast(`Compressed audio: -${data.saved_percent}% space saved!`);
    } catch (err) {
      console.error(err);
      showToast('Compression Error: ' + err.message, true);
    } finally {
      clearInterval(timerInterval);
      compLoadingIndicator.classList.add('hidden');
      compressBtn.disabled = false;
      if (window.lucide) lucide.createIcons();
    }
  }

  function renderCompressResults(data) {
    compEmptyPlaceholder.classList.add('hidden');
    compResultContainer.classList.remove('hidden');

    compSavingsBadge.textContent = `-${data.saved_percent}% SAVED`;
    compStatOrigSize.textContent = formatBytes(data.original_size);
    compStatNewSize.textContent = formatBytes(data.compressed_size);
    compStatSavedBytes.textContent = formatBytes(data.saved_bytes);

    compAudioPlayer.src = data.audio_url;
    compAudioPlayer.play().catch(() => {});

    compDownloadBtn.href = data.audio_url;
    compDownloadBtn.download = data.filename;

    const channelLabel = data.channels === 1 ? 'Mono' : 'Stereo';
    compAudioFormatBadge.textContent = `${data.format.toUpperCase()} · ${data.bitrate} ${channelLabel}`;

    compDurationInfo.textContent = formatDuration(data.duration);
    compStatCodec.textContent = (data.compressed_meta && data.compressed_meta.codec_name) || data.format;
    compStatChannels.textContent = `${data.channels} (${channelLabel})`;
    compStatSampleRate.textContent = `${Number(data.sample_rate).toLocaleString()} Hz`;
    compStatProcessTime.textContent = `${data.processing_time}s`;

    if (window.lucide) lucide.createIcons();
  }

  // Bridge: Send compressed audio to Whisper STT
  if (compSendToSttBtn) {
    compSendToSttBtn.addEventListener('click', async () => {
      if (!compResult || !compResult.audio_url) return;
      try {
        showToast('Transferring compressed audio to Whisper STT...');
        const res = await fetch(compResult.audio_url);
        const blob = await res.blob();
        const file = new File([blob], compResult.filename, { type: blob.type || 'audio/mpeg' });
        handleFileSelected(file);
        switchMainMode('stt');
        showToast('Compressed audio loaded into Whisper STT!');
      } catch (e) {
        showToast('Failed to load into STT: ' + e.message, true);
      }
    });
  }

  // ----------------------------------------------------
  // Unified History (localStorage)
  // ----------------------------------------------------
  toggleHistoryBtn.addEventListener('click', openHistoryDrawer);
  closeHistoryBtn.addEventListener('click', closeHistoryDrawer);
  clearAllHistoryBtn.addEventListener('click', clearAllHistory);

  function openHistoryDrawer() {
    renderHistoryList();
    historyDrawer.classList.remove('hidden');
    if (window.lucide) lucide.createIcons();
  }

  function closeHistoryDrawer() {
    historyDrawer.classList.add('hidden');
  }

  function getHistory() {
    try {
      return JSON.parse(localStorage.getItem('voice_ai_history') || localStorage.getItem('whisper_history') || '[]');
    } catch {
      return [];
    }
  }

  function saveToHistory(item) {
    const history = getHistory();
    history.unshift(item);
    if (history.length > 30) history.pop();
    localStorage.setItem('voice_ai_history', JSON.stringify(history));
    updateHistoryBadge();
  }

  function updateHistoryBadge() {
    const history = getHistory();
    historyCountBadge.textContent = history.length;
  }

  function renderHistoryList() {
    const history = getHistory();
    historyListContainer.innerHTML = '';

    if (history.length === 0) {
      historyListContainer.innerHTML = '<p class="text-xs text-slate-500 py-12 text-center">No session history recorded yet.</p>';
      return;
    }

    history.forEach(item => {
      const card = document.createElement('div');
      card.className = 'p-3.5 rounded-xl bg-obsidian-950/70 border border-white/[0.06] space-y-2 hover:border-white/15 transition';

      const isTts = item.type === 'tts';
      const isComp = item.type === 'compressor';
      const badgeIcon = isTts ? 'sparkles' : (isComp ? 'gauge' : 'mic');
      const badgeColor = isTts 
        ? 'bg-purple-500/15 text-purple-300 border border-purple-500/25' 
        : (isComp 
          ? 'bg-emerald-500/15 text-emerald-300 border border-emerald-500/25' 
          : 'bg-indigo-500/15 text-indigo-300 border border-indigo-500/25');
      const title = isTts 
        ? `Kokoro · ${item.voice_name || item.voice}` 
        : (isComp ? `Compressed · ${item.filename}` : (item.filename || 'Audio Transcript'));

      const desc = isComp
        ? `${formatBytes(item.original_size)} → ${formatBytes(item.compressed_size)} (-${item.saved_percent}% saved) · ${String(item.format).toUpperCase()} ${item.bitrate}`
        : escapeHtml(item.text);

      const typeLabel = isTts ? '24kHz TTS' : (isComp ? 'FFmpeg' : (item.language_name || 'STT'));

      card.innerHTML = `
        <div class="flex items-center justify-between gap-2">
          <div class="flex items-center gap-2 overflow-hidden">
            <span class="p-1 rounded-md ${badgeColor}">
              <i data-lucide="${badgeIcon}" class="w-3 h-3"></i>
            </span>
            <p class="text-xs font-semibold text-slate-100 truncate">${escapeHtml(title)}</p>
          </div>
          <span class="text-[10px] text-slate-500 font-mono shrink-0">${item.date}</span>
        </div>
        <p class="text-xs text-slate-400 line-clamp-2 leading-relaxed">${desc}</p>
        <div class="flex items-center justify-between pt-1">
          <div class="flex items-center gap-1.5 text-[10px] font-mono text-slate-500">
            <span>${typeLabel}</span>
            <span>·</span>
            <span>${item.duration}s</span>
          </div>
          <div class="flex items-center gap-1.5">
            <button class="load-hist-btn px-2.5 py-1 rounded-lg bg-white/[0.05] hover:bg-emerald-600 text-slate-200 hover:text-white text-[11px] font-medium transition" data-id="${item.id}">
              ${isTts ? 'Load & Play' : (isComp ? 'View Audio' : 'Inspect')}
            </button>
            <button class="del-hist-btn p-1 text-slate-500 hover:text-rose-400 transition" data-id="${item.id}" title="Delete">
              <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
            </button>
          </div>
        </div>
      `;

      card.querySelector('.load-hist-btn').addEventListener('click', () => {
        if (isTts) {
          switchMainMode('tts');
          ttsTextInput.value = item.text;
          updateTtsCharCount();
          if (item.audio_url) {
            ttsPlayerCard.classList.remove('hidden');
            ttsAudioPlayer.src = item.audio_url;
            ttsAudioPlayer.play();
            downloadTtsAudioBtn.href = item.audio_url;
          }
        } else if (isComp) {
          switchMainMode('compressor');
          renderCompressResults(item);
        } else {
          switchMainMode('stt');
          transcriptionResult = item;
          renderResults(item);
        }
        closeHistoryDrawer();
        showToast('Restored from history');
      });

      card.querySelector('.del-hist-btn').addEventListener('click', (e) => {
        e.stopPropagation();
        deleteHistoryItem(item.id);
      });

      historyListContainer.appendChild(card);
    });

    if (window.lucide) lucide.createIcons();
  }

  function deleteHistoryItem(id) {
    let history = getHistory();
    history = history.filter(item => item.id !== id);
    localStorage.setItem('voice_ai_history', JSON.stringify(history));
    updateHistoryBadge();
    renderHistoryList();
  }

  function clearAllHistory() {
    if (!confirm('Clear all saved history?')) return;
    localStorage.removeItem('voice_ai_history');
    localStorage.removeItem('whisper_history');
    updateHistoryBadge();
    renderHistoryList();
    showToast('History cleared');
  }

  // ----------------------------------------------------
  // Helpers
  // ----------------------------------------------------
  function escapeHtml(str) {
    if (!str) return '';
    return String(str).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
  }

  function highlightMatch(text, query) {
    if (!query) return text;
    const regex = new RegExp(`(${escapeRegex(query)})`, 'gi');
    return text.replace(regex, '<mark class="search-highlight">$1</mark>');
  }

  function escapeRegex(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  function formatBytes(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  }

  function formatDuration(seconds) {
    const s = Math.round(seconds || 0);
    const m = Math.floor(s / 60);
    const rem = s % 60;
    return `${String(m).padStart(2, '0')}:${String(rem).padStart(2, '0')}`;
  }

  function formatTimestamp(seconds) {
    const sec = Math.floor(seconds);
    const millis = Math.floor((seconds - sec) * 10);
    const m = Math.floor(sec / 60);
    const s = sec % 60;
    return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}.${millis}`;
  }

  function showToast(message, isError = false) {
    toastMsg.textContent = message;
    const icon = document.getElementById('toastIcon');

    if (isError) {
      toast.className = 'fixed bottom-5 right-5 z-50 transform translate-y-0 opacity-100 transition-all duration-300 flex items-center gap-2.5 px-4 py-3 rounded-xl bg-rose-950/90 border border-rose-500/30 text-rose-200 shadow-2xl text-xs font-medium backdrop-blur-xl';
      icon.setAttribute('data-lucide', 'alert-circle');
      icon.className = 'w-4 h-4 text-rose-400';
    } else {
      toast.className = 'fixed bottom-5 right-5 z-50 transform translate-y-0 opacity-100 transition-all duration-300 flex items-center gap-2.5 px-4 py-3 rounded-xl bg-obsidian-900/95 border border-white/10 text-slate-100 shadow-2xl text-xs font-medium backdrop-blur-xl';
      icon.setAttribute('data-lucide', 'check-circle');
      icon.className = 'w-4 h-4 text-emerald-400';
    }

    if (window.lucide) lucide.createIcons();

    clearTimeout(toastTimeout);
    toastTimeout = setTimeout(() => {
      toast.classList.remove('translate-y-0', 'opacity-100');
      toast.classList.add('translate-y-16', 'opacity-0');
    }, 3500);
  }
});
