// --- DOM элементы ---
const input = document.getElementById('qr-input');
const generateBtn = document.getElementById('generate-btn');
const downloadBtn = document.getElementById('download-btn');
const qrcodeContainer = document.getElementById('qrcode-container');
const colorDot = document.getElementById('color-dot');
const colorBg = document.getElementById('color-bg');
const sizeSlider = document.getElementById('size');
const sizeValue = document.getElementById('size-value');
const correctionLevel = document.getElementById('correction-level');
const inputError = document.getElementById('input-error');
const privacyWarning = document.getElementById('privacy-warning');
const historyBlock = document.querySelector('.history-items');
const logoInput = document.getElementById('logo-input');
const logoPreview = document.getElementById('logo-preview');
const removeLogoBtn = document.getElementById('remove-logo-btn');
let logoImg = null;

// --- Константы ---
const HISTORY_KEY = 'qr_history_v1';
const HISTORY_LIMIT = 5;

// --- Вспомогательные функции ---
function isLikelyUrl(str) {
  return /^(https?:\/\/)?[\w\-]+(\.[\w\-]+)+[\w\-._~:/?#[\]@!$&'()*+,;=.]+$/.test(str);
}
function ensureHttps(str) {
  if (/^https?:\/\//.test(str)) return str;
  if (isLikelyUrl(str)) return 'https://' + str;
  return str;
}
function showError(msg) {
  inputError.textContent = msg;
  input.classList.add('error');
}
function clearError() {
  inputError.textContent = '';
  input.classList.remove('error');
}
function showPrivacyWarning(show) {
  privacyWarning.style.display = show ? '' : 'none';
}
function animateQR() {
  const qr = qrcodeContainer.querySelector('img, canvas');
  if (qr) {
    qr.classList.add('qr-appear');
    setTimeout(() => qr.classList.remove('qr-appear'), 800);
  }
}
function setPlaceholder() {
  qrcodeContainer.innerHTML = `<svg class="placeholder" width="120" height="120" viewBox="0 0 24 24"><rect x="2" y="2" width="8" height="8" rx="2" fill="#e0e0e0"/><rect x="14" y="2" width="8" height="8" rx="2" fill="#e0e0e0"/><rect x="2" y="14" width="8" height="8" rx="2" fill="#e0e0e0"/><rect x="9" y="9" width="6" height="6" rx="1" fill="#e0e0e0"/></svg>`;
  downloadBtn.disabled = true;
}

// --- История ---
function saveToHistory(dataUrl, text, opts) {
  let history = JSON.parse(localStorage.getItem(HISTORY_KEY) || '[]');
  history.unshift({ dataUrl, text, opts });
  history = history.slice(0, HISTORY_LIMIT);
  localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
}
function renderHistory() {
  let history = JSON.parse(localStorage.getItem(HISTORY_KEY) || '[]');
  historyBlock.innerHTML = '';
  history.forEach((item, idx) => {
    const img = document.createElement('img');
    img.src = item.dataUrl;
    img.className = 'history-thumb';
    img.title = item.text;
    img.onclick = () => {
      input.value = item.text;
      colorDot.value = item.opts.colorDot;
      colorBg.value = item.opts.colorBg;
      sizeSlider.value = item.opts.size;
      sizeValue.textContent = item.opts.size;
      correctionLevel.value = item.opts.correctionLevel;
      generateQR();
    };
    historyBlock.appendChild(img);
  });
}

// --- Генерация QR ---
function generateQR() {
  clearError();
  let val = input.value.trim();
  if (val.length < 4) {
    showError('Минимум 4 символа!');
    setPlaceholder();
    showPrivacyWarning(false);
    return;
  }
  if (isLikelyUrl(val)) {
    val = ensureHttps(val);
    input.value = val;
  }
  // Предупреждение о приватности
  showPrivacyWarning(/(парол|логин|passport|card|secret|key|token|pin|личн|private|bank|iban|inn|snils|email|@|mail)/i.test(val));

  // Очистить контейнер
  qrcodeContainer.innerHTML = '';
  // Генерация
  const opts = {
    text: val,
    width: +sizeSlider.value,
    height: +sizeSlider.value,
    colorDark: colorDot.value,
    colorLight: colorBg.value,
    correctLevel: QRCode.CorrectLevel[correctionLevel.value]
  };
  const qr = new QRCode(qrcodeContainer, opts);
  setTimeout(() => {
    // --- Исправление: если сгенерирован <img>, заменяем на <canvas> ---
    let img = qrcodeContainer.querySelector('img');
    let canvas = qrcodeContainer.querySelector('canvas');
    if (img && !canvas) {
      // Создаём canvas и копируем туда QR
      canvas = document.createElement('canvas');
      canvas.width = img.width;
      canvas.height = img.height;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 0, img.width, img.height);
      qrcodeContainer.innerHTML = '';
      qrcodeContainer.appendChild(canvas);
    }
    // Вставка логотипа
    if (canvas && logoImg) {
      const ctx = canvas.getContext('2d');
      const qrSize = canvas.width;
      const logoMax = Math.floor(qrSize * 0.2);
      let w = logoImg.width, h = logoImg.height;
      if (w > h) {
        h = Math.round(h * logoMax / w);
        w = logoMax;
      } else {
        w = Math.round(w * logoMax / h);
        h = logoMax;
      }
      const x = (qrSize - w) / 2;
      const y = (qrSize - h) / 2;
      ctx.save();
      ctx.beginPath();
      ctx.arc(qrSize/2, qrSize/2, Math.max(w,h)/2+6, 0, 2*Math.PI); // мягкая маска
      ctx.closePath();
      ctx.clip();
      ctx.drawImage(logoImg, x, y, w, h);
      ctx.restore();
    }
    animateQR();
    downloadBtn.disabled = false;
    // Сохраняем в историю
    if (canvas) {
      saveToHistory(canvas.toDataURL('image/png'), val, {
        colorDot: colorDot.value,
        colorBg: colorBg.value,
        size: sizeSlider.value,
        correctionLevel: correctionLevel.value
      });
      renderHistory();
    }
  }, 200);
}

// --- Скачивание PNG ---
downloadBtn.addEventListener('click', () => {
  const canvas = qrcodeContainer.querySelector('canvas');
  if (!canvas) return;
  // Если есть логотип, он уже на canvas
  canvas.toBlob(blob => saveAs(blob, 'qrcode.png'));
});

// --- Генерация по кнопке ---
generateBtn.addEventListener('click', generateQR);
input.addEventListener('keydown', e => { if (e.key === 'Enter') generateQR(); });

// --- Слайдер размера ---
sizeSlider.addEventListener('input', () => {
  sizeValue.textContent = sizeSlider.value;
});

// --- Инициализация ---
setPlaceholder();
renderHistory();

// --- Очистка ошибки при вводе ---
input.addEventListener('input', clearError);

logoInput.addEventListener('change', e => {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = ev => {
    logoImg = new window.Image();
    logoImg.onload = () => {
      logoPreview.src = logoImg.src;
      logoPreview.style.display = '';
      removeLogoBtn.style.display = '';
    };
    logoImg.src = ev.target.result;
  };
  reader.readAsDataURL(file);
});
removeLogoBtn.addEventListener('click', () => {
  logoImg = null;
  logoPreview.src = '';
  logoPreview.style.display = 'none';
  removeLogoBtn.style.display = 'none';
  logoInput.value = '';
  generateQR();
}); 