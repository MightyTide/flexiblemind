document.addEventListener('DOMContentLoaded', () => {
    // --- Логика для окна ОБРАТНОЙ СВЯЗИ (уже есть) ---
    const feedbackBtn = document.getElementById('feedback-btn');
    const feedbackModal = document.getElementById('feedback-modal');
    const closeModalBtn = document.getElementById('close-modal-btn');
    
    if (feedbackBtn) { // Добавляем проверки на случай, если элементов нет на странице
        feedbackBtn.addEventListener('click', () => {
            feedbackModal.style.display = 'flex';
        });
    }
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', () => {
            feedbackModal.style.display = 'none';
        });
    }
    if (feedbackModal) {
        feedbackModal.addEventListener('click', (event) => {
            if (event.target === feedbackModal) {
                feedbackModal.style.display = 'none';
            }
        });
    }

    // --- НОВАЯ ЛОГИКА для окна ПОМОЩИ ---
    const helpBtn = document.getElementById('help-btn');
    const helpModal = document.getElementById('help-modal');
    const closeHelpModalBtn = document.getElementById('close-help-modal-btn');

    if (helpBtn) {
        helpBtn.addEventListener('click', () => {
            helpModal.style.display = 'flex';
        });
    }
    if (closeHelpModalBtn) {
        closeHelpModalBtn.addEventListener('click', () => {
            helpModal.style.display = 'none';
        });
    }
    if (helpModal) {
        helpModal.addEventListener('click', (event) => {
            if (event.target === helpModal) {
                helpModal.style.display = 'none';
            }
        });
    }
});