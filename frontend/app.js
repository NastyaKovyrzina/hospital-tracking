// Функция для загрузки данных с бэкенда
async function loadDevices() {
    try {
        // 1. Отправляем запрос к вашему API (бэкенду)
        const response = await fetch('http://localhost:5000/api/devices');

        // 2. Если ошибка (например, бэкенд не запущен)
        if (!response.ok) {
            throw new Error('Ошибка при загрузке данных');
        }

        // 3. Получаем данные в формате JSON
        const devices = await response.json();

        // 4. Находим таблицу в HTML
        const tableBody = document.getElementById('devices-table');

        // 5. Очищаем старые данные
        tableBody.innerHTML = '';

        // 6. Для каждого устройства создаём строку в таблице
        devices.forEach(device => {
            const row = document.createElement('tr');

            row.innerHTML = `
                <td>${device.device_id}</td>
                <td>${device.room}</td>
                <td>Ш: ${device.lat.toFixed(4)}, Д: ${device.lon.toFixed(4)}</td>
            `;

            tableBody.appendChild(row);
        });

    } catch (error) {
        console.error('Произошла ошибка:', error);
        alert('Не удалось загрузить данные. Проверьте, запущен ли бэкенд!');
    }
}

// Загружаем данные сразу при открытии страницы
loadDevices();

// Обновляем данные каждые 10 секунд
setInterval(loadDevices, 10000);