// static/js/menu.js
console.log("Script menu.js loaded!"); // Важная проверка загрузки

function initMenu() {
    console.log("Initializing menu...");
    
    document.querySelectorAll('[data-submenu-trigger]').forEach(trigger => {
        trigger.addEventListener('click', function(e) {
            console.log("Menu trigger clicked:", this);
            e.preventDefault();
            
            const parentItem = this.closest('li');
            const submenu = parentItem.querySelector('.submenu-container');
            
            // Закрыть другие меню того же уровня
            const sameLevel = parentItem.parentElement.querySelectorAll('.submenu-container');
            sameLevel.forEach(menu => {
                if (menu !== submenu) menu.style.display = 'none';
            });

            // Переключить текущее меню
            if (submenu) {
                submenu.style.display = submenu.style.display === 'block' ? 'none' : 'block';
                console.log("Submenu toggled:", submenu);
            }
        });
    });

    // Закрытие при клике вне меню
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.menu-item') && !e.target.closest('.submenu-item')) {
            document.querySelectorAll('.submenu-container').forEach(menu => {
                menu.style.display = 'none';
            });
        }
    });
}

// Инициализация при полной загрузке DOM
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMenu);
} else {
    initMenu();
}