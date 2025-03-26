
const socket = new WebSocket('ws://' + window.location.host + '/ws/notificaciones/');

function showNotification(nombre, codigo) {
    const notificationsContainer = document.getElementById('notifications');
    const notification = document.createElement('div');
    notification.className = 'alert alert-info alert-dismissible fade show';
    notification.role = 'alert';
    notification.innerHTML = `Nombre: ${nombre}, Código: ${codigo}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            `;
    notificationsContainer.appendChild(notification);

    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 60000); // Elimina el nodo después de la animación
    }, 60000);
}

socket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log('data:', data);

    let notifications = JSON.parse(localStorage.getItem('notifications')) || [];
    notifications.push({ nombre: data.pedido.nombre, codigo: data.pedido.codigo });

    localStorage.setItem('notifications', JSON.stringify(notifications));


    showNotification(data.pedido.nombre, data.pedido.codigo);
};


window.onload = function () {

    const notifications = JSON.parse(localStorage.getItem('notifications')) || [];



    notifications.forEach(notification => {

        if (notification && notification.nombre && notification.codigo) {
            showNotification(notification.nombre, notification.codigo);
        } else {
            console.error('Notificación inválida:', notification);
        }
    });


    setTimeout(() => {
        localStorage.removeItem('notifications');
    }, 120000);
};

socket.onclose = function (e) {
    console.log(e);
    console.error('Conexión cerrada');
};

socket.onopen = function (e) {
    console.log('Conectado');
};