document.addEventListener('DOMContentLoaded', function() {
    // Показываем/скрываем поле комментария в зависимости от выбора "Да/Нет"
    document.querySelectorAll('[id^="id_question_"]').forEach(radio => {
        radio.addEventListener('change', function() {
            const questionId = this.name.split('_')[1];
            const commentField = document.getElementById(`id_comment_${questionId}`);
            
            if (this.value === 'yes' && this.checked) {
                commentField.style.display = 'block';
            } else {
                commentField.style.display = 'none';
                commentField.value = '';
            }
        });
    });

    // Инициализация состояния при загрузке страницы
    document.querySelectorAll('[id^="id_question_"]:checked').forEach(radio => {
        const questionId = radio.name.split('_')[1];
        const commentField = document.getElementById(`id_comment_${questionId}`);
        
        if (radio.value === 'yes') {
            commentField.style.display = 'block';
        } else {
            commentField.style.display = 'none';
        }
    });
});