// Configuración de la API - Usar URL relativa ya que el frontend se sirve desde el mismo servidor
const API_BASE_URL = '/api';

// Estado global de la aplicación
let estadoApp = {
    estudiante: null,
    user: null,
    token: null,
    materias: [],
    notas: [],
    asistencias: [],
    alertas: []
};

// Función para obtener el token del localStorage
function getToken() {
    return localStorage.getItem('auth_token');
}

// Función para guardar el token
function saveToken(token) {
    localStorage.setItem('auth_token', token);
    estadoApp.token = token;
}

// Función para eliminar el token
function removeToken() {
    localStorage.removeItem('auth_token');
    estadoApp.token = null;
    estadoApp.user = null;
    estadoApp.estudiante = null;
}

// Función para hacer peticiones autenticadas
async function apiRequest(url, options = {}) {
    const token = getToken();
    const headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        ...options.headers
    };
    
    if (token) {
        headers['Authorization'] = `Token ${token}`;
    }
    
    const fullUrl = `${API_BASE_URL}${url}`;
    console.log('Haciendo petición a:', fullUrl, 'con opciones:', options);
    
    let response;
    try {
        response = await fetch(fullUrl, {
            ...options,
            headers,
            credentials: 'same-origin'  // Mismo origen, no necesita mode: 'cors'
        });
    } catch (networkError) {
        console.error('Error de red:', networkError);
        throw new Error('No se pudo conectar con el servidor. Verifica que el backend esté corriendo.');
    }
    
    if (!response.ok) {
        let errorData;
        try {
            errorData = await response.json();
        } catch (jsonError) {
            const errorText = await response.text();
            console.error('Error del servidor (no JSON):', response.status, errorText);
            throw new Error(`Error del servidor (${response.status}): ${errorText || 'Error desconocido'}`);
        }
        
        console.error('Error del servidor:', response.status, errorData);
        
        // Formatear errores de validación para mostrar mensajes más claros
        if (errorData.errors) {
            const errorMessages = Object.entries(errorData.errors)
                .map(([field, message]) => {
                    const fieldNames = {
                        'codigo': 'Código de estudiante',
                        'username': 'Usuario',
                        'email': 'Email',
                        'password': 'Contraseña',
                        'carrera_id': 'Carrera',
                        'semestre_actual': 'Semestre'
                    };
                    const fieldName = fieldNames[field] || field;
                    return `${fieldName}: ${message}`;
                })
                .join('\n');
            throw new Error(errorMessages || 'Error de validación. Por favor, revisa los datos ingresados.');
        }
        
        throw new Error(errorData.error || errorData.detail || errorData.message || `Error en la petición (${response.status})`);
    }
    
    try {
        return await response.json();
    } catch (jsonError) {
        console.error('Error al parsear respuesta JSON:', jsonError);
        throw new Error('La respuesta del servidor no es válida');
    }
}

// Inicialización de la aplicación
document.addEventListener('DOMContentLoaded', () => {
    inicializarTema();
    verificarAutenticacion();
    configurarEventListenersAuth();
    inicializarApp();
});

// Verificar autenticación al cargar
async function verificarAutenticacion() {
    const token = getToken();
    if (token) {
        try {
            const data = await apiRequest('/auth/perfil/');
            estadoApp.user = data.user;
            estadoApp.estudiante = data.estudiante;
            mostrarAplicacion();
            await cargarDatos();
            actualizarPerfil();
        } catch (error) {
            console.error('Error al verificar autenticación:', error);
            removeToken();
            mostrarLogin();
        }
    } else {
        mostrarLogin();
        // Cargar carreras si la página de registro está visible
        setTimeout(() => {
            const registerPage = document.getElementById('register-page');
            if (registerPage && registerPage.style.display !== 'none') {
                cargarCarrerasParaRegistro();
            }
        }, 100);
    }
}

// Mostrar página de login
function mostrarLogin() {
    document.getElementById('auth-pages').style.display = 'block';
    document.getElementById('login-page').style.display = 'block';
    document.getElementById('register-page').style.display = 'none';
    document.getElementById('main-content').style.display = 'none';
    document.getElementById('nav-menu').style.display = 'none';
}

// Mostrar aplicación
function mostrarAplicacion() {
    document.getElementById('auth-pages').style.display = 'none';
    document.getElementById('main-content').style.display = 'block';
    document.getElementById('nav-menu').style.display = 'flex';
}

// Función principal de inicialización
async function inicializarApp() {
    if (!getToken()) {
        return; // No inicializar si no está autenticado
    }
    
    try {
        await cargarDatos();
        inicializarGraficos();
        configurarEventListeners();
    } catch (error) {
        console.error('Error al inicializar la aplicación:', error);
        mostrarError('Error al cargar los datos. Por favor, recarga la página.');
    }
}

// Cargar datos desde la API
async function cargarDatos() {
    // Aquí se harían las llamadas a la API
    // Por ahora, usamos datos de ejemplo
    estadoApp.materias = [
        { id: 1, nombre: 'Matemáticas I', creditos: 4 },
        { id: 2, nombre: 'Programación I', creditos: 5 }
    ];
    
    estadoApp.notas = [];
    estadoApp.asistencias = [];
    estadoApp.alertas = [];

    actualizarUI();
}

// Actualizar la interfaz de usuario
function actualizarUI() {
    actualizarDashboard();
    actualizarSelectores();
    actualizarListas();
    actualizarAlertas();
}

// Actualizar el dashboard
function actualizarDashboard() {
    const promedio = calcularPromedioGeneral();
    const materiasCursando = estadoApp.materias.length;
    const asistenciaPromedio = calcularAsistenciaPromedio();
    const alertasActivas = estadoApp.alertas.length;

    document.getElementById('promedio-general').textContent = promedio.toFixed(2);
    document.getElementById('materias-cursando').textContent = materiasCursando;
    document.getElementById('asistencia-promedio').textContent = `${asistenciaPromedio}%`;
    document.getElementById('alertas-activas').textContent = alertasActivas;
}

// Calcular promedio general
function calcularPromedioGeneral() {
    if (estadoApp.notas.length === 0) return 0;
    
    let sumaPonderada = 0;
    let totalPorcentaje = 0;

    estadoApp.notas.forEach(nota => {
        sumaPonderada += nota.valor * (nota.porcentaje / 100);
        totalPorcentaje += nota.porcentaje;
    });

    return totalPorcentaje > 0 ? sumaPonderada / (totalPorcentaje / 100) : 0;
}

// Calcular asistencia promedio
function calcularAsistenciaPromedio() {
    if (estadoApp.asistencias.length === 0) return 0;
    
    const total = estadoApp.asistencias.length;
    const presentes = estadoApp.asistencias.filter(a => a.asistio).length;
    
    return Math.round((presentes / total) * 100);
}

// Actualizar selectores de formularios
function actualizarSelectores() {
    const materiaSelect = document.getElementById('materia-select');
    const asistenciaMateriaSelect = document.getElementById('asistencia-materia-select');

    [materiaSelect, asistenciaMateriaSelect].forEach(select => {
        // Limpiar opciones existentes (excepto la primera)
        while (select.options.length > 1) {
            select.remove(1);
        }

        // Agregar materias
        estadoApp.materias.forEach(materia => {
            const option = document.createElement('option');
            option.value = materia.id;
            option.textContent = materia.nombre;
            select.appendChild(option);
        });
    });
}

// Actualizar listas
function actualizarListas() {
    actualizarListaNotas();
    actualizarTarjetasAsistencias();
    actualizarListaAsistencias();
}

// Actualizar lista de notas
function actualizarListaNotas() {
    const notasList = document.getElementById('notas-list');
    notasList.innerHTML = '';

    if (estadoApp.notas.length === 0) {
        notasList.innerHTML = '<p style="text-align: center; padding: 2rem; color: var(--dark-light); background: var(--white); border-radius: var(--border-radius); box-shadow: var(--shadow-md);">No hay notas registradas. Usa el formulario de arriba para registrar tus notas.</p>';
        return;
    }

    // Agrupar notas por materia
    const notasPorMateria = {};
    estadoApp.notas.forEach(nota => {
        const materiaNombre = obtenerNombreMateria(nota.materia_id);
        if (!notasPorMateria[materiaNombre]) {
            notasPorMateria[materiaNombre] = [];
        }
        notasPorMateria[materiaNombre].push(nota);
    });

    // Mostrar notas agrupadas por materia
    Object.keys(notasPorMateria).forEach(materiaNombre => {
        const notasMateria = notasPorMateria[materiaNombre];
        const promedioMateria = notasMateria.reduce((sum, n) => sum + (n.valor * n.porcentaje / 100), 0) / 
                                notasMateria.reduce((sum, n) => sum + n.porcentaje, 0) * 100;

        notasMateria.forEach(nota => {
            const notaItem = document.createElement('div');
            notaItem.className = 'nota-item';
            
            // Determinar color según la nota
            let colorNota = 'var(--danger-color)';
            if (nota.valor >= 16) colorNota = 'var(--secondary-color)';
            else if (nota.valor >= 12) colorNota = 'var(--warning-color)';
            
            notaItem.innerHTML = `
                <div style="flex: 1;">
                    <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem;">
                        <strong style="font-size: 1.1rem; color: var(--dark-color);">${materiaNombre}</strong>
                        <span style="padding: 0.25rem 0.75rem; border-radius: 50px; background: rgba(37, 99, 235, 0.1); color: var(--primary-color); font-size: 0.875rem; font-weight: 600;">
                            ${nota.porcentaje}%
                        </span>
                    </div>
                    <p style="color: var(--dark-light); margin: 0; display: flex; align-items: center; gap: 0.5rem;">
                        <span>📅</span> ${formatearFecha(nota.fecha)}
                        ${nota.descripcion ? `<span style="margin-left: 1rem;">📝 ${nota.descripcion}</span>` : ''}
                    </p>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 2.5rem; font-weight: 700; color: ${colorNota}; line-height: 1;">
                        ${nota.valor.toFixed(2)}
                    </div>
                    <div style="font-size: 0.875rem; color: var(--dark-light); margin-top: 0.25rem;">
                        de 20.00
                    </div>
                </div>
            `;
            notasList.appendChild(notaItem);
        });
    });
}

// Actualizar tarjetas rápidas de asistencias
function actualizarTarjetasAsistencias() {
    const quickActions = document.getElementById('asistencias-quick-actions');
    quickActions.innerHTML = '';

    if (estadoApp.materias.length === 0) {
        quickActions.innerHTML = '<p style="grid-column: 1 / -1; text-align: center; padding: 2rem; color: var(--dark-light);">No hay materias disponibles. Agrega materias para registrar asistencias.</p>';
        return;
    }

    estadoApp.materias.forEach(materia => {
        const card = document.createElement('div');
        card.className = 'asistencia-card';
        card.dataset.materiaId = materia.id;
        
        // Obtener fecha actual
        const fechaActual = new Date().toISOString().split('T')[0];
        
        // Verificar si ya hay asistencia registrada hoy
        const asistenciaHoy = estadoApp.asistencias.find(a => 
            a.materia_id === materia.id && 
            a.fecha === fechaActual
        );

        const estadoAsistencia = asistenciaHoy ? (asistenciaHoy.asistio ? 'presente' : 'ausente') : 'pendiente';
        const iconoEstado = asistenciaHoy ? (asistenciaHoy.asistio ? '✓' : '✗') : '📚';
        const colorEstado = asistenciaHoy ? (asistenciaHoy.asistio ? 'var(--secondary-color)' : 'var(--danger-color)') : 'var(--dark-light)';

        card.innerHTML = `
            <div class="asistencia-card-header">
                <h3 class="asistencia-card-title">${materia.nombre}</h3>
                <div class="asistencia-card-icon" style="background: ${estadoAsistencia === 'presente' ? 'var(--gradient-success)' : estadoAsistencia === 'ausente' ? 'var(--gradient-danger)' : 'var(--gradient-primary)'}">
                    ${iconoEstado}
                </div>
            </div>
            <div class="asistencia-card-body">
                <div class="asistencia-card-info">
                    <div><strong>📅 Fecha:</strong> ${formatearFecha(fechaActual)}</div>
                    <div><strong>📊 Estado:</strong> 
                        <span class="asistencia-status-badge ${estadoAsistencia}" style="margin-left: 0.5rem;">
                            ${estadoAsistencia === 'presente' ? '✓ Presente' : estadoAsistencia === 'ausente' ? '✗ Ausente' : '⏳ Pendiente'}
                        </span>
                    </div>
                </div>
            </div>
            <div class="asistencia-card-actions">
                <button class="btn-asistencia btn-asistencia-presente" data-materia-id="${materia.id}" data-asistio="true">
                    <span class="btn-asistencia-icon">✓</span>
                    <span>Presente</span>
                </button>
                <button class="btn-asistencia btn-asistencia-ausente" data-materia-id="${materia.id}" data-asistio="false">
                    <span class="btn-asistencia-icon">✗</span>
                    <span>Ausente</span>
                </button>
            </div>
        `;

        // Agregar evento de click a la tarjeta
        card.addEventListener('click', (e) => {
            if (!e.target.closest('.asistencia-card-actions')) {
                card.classList.toggle('selected');
            }
        });

        quickActions.appendChild(card);
    });

    // Agregar event listeners a los botones
    document.querySelectorAll('.btn-asistencia').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const materiaId = parseInt(btn.dataset.materiaId);
            const asistio = btn.dataset.asistio === 'true';
            registrarAsistenciaRapida(materiaId, asistio);
        });
    });
}

// Registrar asistencia rápida desde las tarjetas
function registrarAsistenciaRapida(materiaId, asistio) {
    const fechaActual = new Date().toISOString().split('T')[0];
    
    // Verificar si ya existe una asistencia para hoy
    const asistenciaExistente = estadoApp.asistencias.findIndex(a => 
        a.materia_id === materiaId && 
        a.fecha === fechaActual
    );

    const nuevaAsistencia = {
        id: asistenciaExistente >= 0 ? estadoApp.asistencias[asistenciaExistente].id : estadoApp.asistencias.length + 1,
        materia_id: materiaId,
        fecha: fechaActual,
        asistio: asistio
    };

    if (asistenciaExistente >= 0) {
        estadoApp.asistencias[asistenciaExistente] = nuevaAsistencia;
    } else {
        estadoApp.asistencias.push(nuevaAsistencia);
    }

    actualizarUI();
    mostrarMensaje(
        `Asistencia registrada: ${asistio ? 'Presente' : 'Ausente'} en ${obtenerNombreMateria(materiaId)}`,
        'success'
    );

    // Aquí se haría la llamada a la API
    // await fetch(`${API_BASE_URL}/asistencias/${nuevaAsistencia.id}/`, { 
    //     method: asistenciaExistente >= 0 ? 'PUT' : 'POST', 
    //     body: JSON.stringify(nuevaAsistencia) 
    // });
}

// Actualizar lista de asistencias
function actualizarListaAsistencias() {
    const asistenciasList = document.getElementById('asistencias-list');
    asistenciasList.innerHTML = '';

    if (estadoApp.asistencias.length === 0) {
        asistenciasList.innerHTML = '<p style="text-align: center; padding: 2rem; color: var(--dark-light); background: var(--white); border-radius: var(--border-radius); box-shadow: var(--shadow-md);">No hay asistencias registradas. Usa las tarjetas de arriba para registrar tu asistencia rápidamente.</p>';
        return;
    }

    // Ordenar asistencias por fecha (más recientes primero)
    const asistenciasOrdenadas = [...estadoApp.asistencias].sort((a, b) => 
        new Date(b.fecha) - new Date(a.fecha)
    );

    asistenciasOrdenadas.forEach(asistencia => {
        const asistenciaItem = document.createElement('div');
        asistenciaItem.className = 'asistencia-item';
        
        const estadoBadge = asistencia.asistio 
            ? '<span class="asistencia-status-badge presente">✓ Presente</span>'
            : '<span class="asistencia-status-badge ausente">✗ Ausente</span>';
        
        asistenciaItem.innerHTML = `
            <div style="flex: 1;">
                <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem;">
                    <strong style="font-size: 1.1rem; color: var(--dark-color);">${obtenerNombreMateria(asistencia.materia_id)}</strong>
                    ${estadoBadge}
                </div>
                <p style="color: var(--dark-light); margin: 0; display: flex; align-items: center; gap: 0.5rem;">
                    <span>📅</span> ${formatearFecha(asistencia.fecha)}
                </p>
            </div>
            <div style="font-size: 2rem;">
                ${asistencia.asistio ? '✅' : '❌'}
            </div>
        `;
        asistenciasList.appendChild(asistenciaItem);
    });
}

// Actualizar alertas
function actualizarAlertas() {
    const alertasContainer = document.getElementById('alertas-container');
    alertasContainer.innerHTML = '';

    if (estadoApp.alertas.length === 0) {
        alertasContainer.innerHTML = '<p>No hay alertas activas.</p>';
        return;
    }

    estadoApp.alertas.forEach(alerta => {
        const alertaDiv = document.createElement('div');
        alertaDiv.className = `alerta ${alerta.tipo}`;
        alertaDiv.innerHTML = `
            <h4>${alerta.titulo}</h4>
            <p>${alerta.mensaje}</p>
        `;
        alertasContainer.appendChild(alertaDiv);
    });
}

// Inicializar gráficos con Chart.js
function inicializarGraficos() {
    const ctx = document.getElementById('progreso-chart');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Semestre 1', 'Semestre 2', 'Semestre 3', 'Semestre 4'],
            datasets: [{
                label: 'Promedio por Semestre',
                data: [0, 0, 0, 0],
                borderColor: 'rgb(74, 144, 226)',
                backgroundColor: 'rgba(74, 144, 226, 0.1)',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 20
                }
            }
        }
    });
}

// Configurar event listeners de autenticación
function configurarEventListenersAuth() {
    // Formulario de login
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', manejarLogin);
    }

    // Formulario de registro
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', manejarRegistro);
    }

    // Toggle entre login y registro
    const showRegister = document.getElementById('show-register');
    const showLogin = document.getElementById('show-login');
    
    if (showRegister) {
        showRegister.addEventListener('click', (e) => {
            e.preventDefault();
            document.getElementById('login-page').style.display = 'none';
            document.getElementById('register-page').style.display = 'block';
            // Cargar carreras cuando se muestra la página de registro
            cargarCarrerasParaRegistro();
        });
    }
    
    if (showLogin) {
        showLogin.addEventListener('click', (e) => {
            e.preventDefault();
            document.getElementById('register-page').style.display = 'none';
            document.getElementById('login-page').style.display = 'block';
        });
    }

    // Botón de logout
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            manejarLogout();
        });
    }

    // Toggle de tema
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTema);
    }
}

// Configurar event listeners
function configurarEventListeners() {
    // Formulario de notas
    const notaForm = document.getElementById('nota-form');
    if (notaForm) {
        notaForm.addEventListener('submit', manejarRegistroNota);
    }

    // Formulario de asistencias
    const asistenciaForm = document.getElementById('asistencia-form');
    if (asistenciaForm) {
        asistenciaForm.addEventListener('submit', manejarRegistroAsistencia);
    }

    // Establecer fecha actual por defecto en el formulario de asistencias
    const fechaInput = document.getElementById('fecha-input');
    if (fechaInput) {
        fechaInput.value = new Date().toISOString().split('T')[0];
    }
}

// Manejar registro de nota
function manejarRegistroNota(e) {
    e.preventDefault();
    
    const materiaId = parseInt(document.getElementById('materia-select').value);
    const valor = parseFloat(document.getElementById('nota-input').value);
    const porcentaje = parseFloat(document.getElementById('porcentaje-input').value);

    const nuevaNota = {
        id: estadoApp.notas.length + 1,
        materia_id: materiaId,
        valor: valor,
        porcentaje: porcentaje,
        fecha: new Date().toISOString()
    };

    estadoApp.notas.push(nuevaNota);
    actualizarUI();
    
    // Aquí se haría la llamada a la API
    // await fetch(`${API_BASE_URL}/notas/`, { method: 'POST', body: JSON.stringify(nuevaNota) });

    e.target.reset();
    mostrarMensaje('Nota registrada exitosamente', 'success');
}

// Manejar registro de asistencia
function manejarRegistroAsistencia(e) {
    e.preventDefault();
    
    const materiaId = parseInt(document.getElementById('asistencia-materia-select').value);
    const fecha = document.getElementById('fecha-input').value;
    const asistio = document.getElementById('asistio-input').checked;

    if (!materiaId) {
        mostrarError('Por favor, selecciona una materia');
        return;
    }

    // Verificar si ya existe una asistencia para esta materia y fecha
    const asistenciaExistente = estadoApp.asistencias.findIndex(a => 
        a.materia_id === materiaId && 
        a.fecha === fecha
    );

    const nuevaAsistencia = {
        id: asistenciaExistente >= 0 ? estadoApp.asistencias[asistenciaExistente].id : estadoApp.asistencias.length + 1,
        materia_id: materiaId,
        fecha: fecha,
        asistio: asistio
    };

    if (asistenciaExistente >= 0) {
        estadoApp.asistencias[asistenciaExistente] = nuevaAsistencia;
        mostrarMensaje('Asistencia actualizada exitosamente', 'success');
    } else {
        estadoApp.asistencias.push(nuevaAsistencia);
        mostrarMensaje('Asistencia registrada exitosamente', 'success');
    }
    
    actualizarUI();
    
    // Aquí se haría la llamada a la API
    // await fetch(`${API_BASE_URL}/asistencias/${nuevaAsistencia.id}/`, { 
    //     method: asistenciaExistente >= 0 ? 'PUT' : 'POST', 
    //     body: JSON.stringify(nuevaAsistencia) 
    // });

    e.target.reset();
    // Establecer fecha actual por defecto
    document.getElementById('fecha-input').value = new Date().toISOString().split('T')[0];
}

// Funciones auxiliares
function obtenerNombreMateria(materiaId) {
    const materia = estadoApp.materias.find(m => m.id === materiaId);
    return materia ? materia.nombre : 'Materia desconocida';
}

function formatearFecha(fecha) {
    return new Date(fecha).toLocaleDateString('es-ES');
}

function mostrarMensaje(mensaje, tipo) {
    // Crear elemento de notificación
    const notification = document.createElement('div');
    notification.className = `notification ${tipo}`;
    notification.innerHTML = `
        <span style="font-size: 1.5rem;">${tipo === 'success' ? '✓' : tipo === 'error' ? '✗' : 'ℹ'}</span>
        <span>${mensaje}</span>
    `;
    
    document.body.appendChild(notification);
    
    // Remover después de 3 segundos
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

function mostrarError(mensaje) {
    mostrarMensaje(mensaje, 'error');
}

// Agregar animación de salida
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Manejar login
async function manejarLogin(e) {
    e.preventDefault();
    
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    
    try {
        const data = await apiRequest('/auth/login/', {
            method: 'POST',
            body: JSON.stringify({ username, password })
        });
        
        saveToken(data.token);
        estadoApp.user = data.user;
        estadoApp.estudiante = data.estudiante;
        
        mostrarAplicacion();
        await cargarDatos();
        actualizarPerfil();
        mostrarMensaje('¡Bienvenido de nuevo!', 'success');
    } catch (error) {
        mostrarError(error.message || 'Error al iniciar sesión');
    }
}

// Manejar registro
async function manejarRegistro(e) {
    e.preventDefault();
    
    // Validar que todos los campos estén llenos
    const carreraId = document.getElementById('register-carrera').value;
    if (!carreraId || carreraId === '') {
        mostrarError('Por favor, selecciona una carrera');
        return;
    }
    
    const formData = {
        username: document.getElementById('register-username').value,
        email: document.getElementById('register-email').value,
        password: document.getElementById('register-password').value,
        first_name: document.getElementById('register-first-name').value,
        last_name: document.getElementById('register-last-name').value,
        codigo: document.getElementById('register-codigo').value,
        carrera_id: parseInt(carreraId),
        semestre_actual: parseInt(document.getElementById('register-semestre').value)
    };
    
    console.log('Datos del formulario:', formData);
    console.log('URL completa:', `${API_BASE_URL}/auth/registro/`);
    
    // Mostrar indicador de carga
    const submitButton = e.target.querySelector('button[type="submit"]');
    const originalButtonText = submitButton ? submitButton.textContent : '';
    if (submitButton) {
        submitButton.disabled = true;
        submitButton.textContent = 'Registrando...';
    }
    
    try {
        const data = await apiRequest('/auth/registro/', {
            method: 'POST',
            body: JSON.stringify(formData)
        });
        
        console.log('Respuesta del servidor:', data);
        
        saveToken(data.token);
        estadoApp.user = data.user;
        estadoApp.estudiante = data.estudiante;
        
        mostrarAplicacion();
        await cargarDatos();
        actualizarPerfil();
        mostrarMensaje('¡Registro exitoso! Bienvenido a Ruta Académica', 'success');
        
        // Limpiar formulario
        e.target.reset();
    } catch (error) {
        console.error('Error completo en registro:', error);
        
        // Mostrar error detallado
        let errorMessage = error.message || 'Error al registrarse';
        
        // Si el error contiene múltiples líneas (errores de validación), mostrarlas todas
        if (errorMessage.includes('\n')) {
            const errors = errorMessage.split('\n');
            errorMessage = errors.join('. ');
        }
        
        mostrarError(errorMessage);
    } finally {
        // Restaurar botón
        if (submitButton) {
            submitButton.disabled = false;
            submitButton.textContent = originalButtonText;
        }
    }
}

// Manejar logout
async function manejarLogout() {
    try {
        await apiRequest('/auth/logout/', {
            method: 'POST'
        });
    } catch (error) {
        console.error('Error al cerrar sesión:', error);
    } finally {
        removeToken();
        mostrarLogin();
        mostrarMensaje('Sesión cerrada exitosamente', 'info');
    }
}

// Actualizar perfil
function actualizarPerfil() {
    if (!estadoApp.estudiante || !estadoApp.user) return;
    
    const nombreCompleto = estadoApp.user.first_name && estadoApp.user.last_name
        ? `${estadoApp.user.first_name} ${estadoApp.user.last_name}`
        : estadoApp.user.username;
    
    const hora = new Date().getHours();
    const saludo = hora < 12 ? 'Buenos días' : hora < 18 ? 'Buenas tardes' : 'Buenas noches';
    
    document.getElementById('profile-welcome').textContent = `¡${saludo}!`;
    document.getElementById('profile-name').textContent = nombreCompleto;
    document.getElementById('profile-details').textContent = `Código: ${estadoApp.estudiante.codigo}`;
    document.getElementById('profile-carrera').textContent = estadoApp.estudiante.carrera?.nombre || '-';
    document.getElementById('profile-semestre').textContent = estadoApp.estudiante.semestre_actual || '-';
    document.getElementById('profile-email').textContent = estadoApp.user.email || '-';
    
    // Iniciales del avatar
    const initials = nombreCompleto.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
    document.getElementById('profile-initials').textContent = initials || '👤';
}

// Inicializar tema
function inicializarTema() {
    const temaGuardado = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', temaGuardado);
    actualizarIconoTema(temaGuardado);
}

// Toggle tema
function toggleTema() {
    const temaActual = document.documentElement.getAttribute('data-theme');
    const nuevoTema = temaActual === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', nuevoTema);
    localStorage.setItem('theme', nuevoTema);
    actualizarIconoTema(nuevoTema);
}

// Actualizar icono del tema
function actualizarIconoTema(tema) {
    const icono = document.querySelector('.theme-icon');
    if (icono) {
        icono.textContent = tema === 'dark' ? '☀️' : '🌙';
    }
}

// Cargar carreras para el formulario de registro
async function cargarCarrerasParaRegistro() {
    const select = document.getElementById('register-carrera');
    if (!select) {
        console.warn('Select de carreras no encontrado');
        return;
    }

    try {
        // Limpiar opciones existentes (excepto la primera)
        while (select.options.length > 1) {
            select.remove(1);
        }

        // Mostrar estado de carga
        select.disabled = true;
        const optionLoading = document.createElement('option');
        optionLoading.value = '';
        optionLoading.textContent = 'Cargando carreras...';
        optionLoading.disabled = true;
        select.appendChild(optionLoading);

        // Hacer petición a la API (sin token, ya que las carreras deben ser públicas)
        // Usar URL relativa para evitar problemas de CORS
        const url = `${API_BASE_URL}/carreras/`;
        console.log('Intentando cargar carreras desde:', url);
        
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            credentials: 'same-origin'  // Mismo origen ya que se sirve desde Django
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error('Error del servidor:', response.status, errorText);
            let errorMessage = 'Error al cargar las carreras';
            
            if (response.status === 404) {
                errorMessage = 'El endpoint de carreras no fue encontrado';
            } else if (response.status === 500) {
                errorMessage = 'Error interno del servidor';
            } else if (response.status === 0 || response.status === '') {
                errorMessage = 'No se pudo conectar con el servidor. Verifica que el backend esté corriendo';
            }
            
            throw new Error(errorMessage);
        }

        let data;
        try {
            data = await response.json();
        } catch (jsonError) {
            console.error('Error al parsear JSON:', jsonError);
            throw new Error('La respuesta del servidor no es válida');
        }

        // Remover opción de carga
        select.remove(select.options.length - 1);
        select.disabled = false;

        // La API puede devolver datos paginados o un array directo
        const carreras = data.results || data || [];

        // Agregar carreras al select
        if (carreras && carreras.length > 0) {
            carreras.forEach(carrera => {
                const option = document.createElement('option');
                option.value = carrera.id;
                option.textContent = carrera.nombre;
                select.appendChild(option);
            });
        } else {
            const optionEmpty = document.createElement('option');
            optionEmpty.value = '';
            optionEmpty.textContent = 'No hay carreras disponibles';
            optionEmpty.disabled = true;
            select.appendChild(optionEmpty);
            select.disabled = true;
        }
    } catch (error) {
        console.error('Error completo al cargar carreras:', error);
        console.error('URL intentada:', `${API_BASE_URL}/carreras/`);
        
        const select = document.getElementById('register-carrera');
        if (select) {
            // Limpiar y mostrar error
            while (select.options.length > 1) {
                select.remove(1);
            }
            const optionError = document.createElement('option');
            optionError.value = '';
            optionError.textContent = error.message || 'Error al cargar carreras';
            optionError.disabled = true;
            select.appendChild(optionError);
            select.disabled = true;
        }
        mostrarError(error.message || 'No se pudieron cargar las carreras. Por favor, verifica que el servidor esté corriendo y recarga la página.');
    }
}

