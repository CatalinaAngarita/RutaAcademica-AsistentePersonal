// Configuración de la API
const API_BASE_URL = 'http://localhost:8000/api';

// Estado global de la aplicación
let estadoApp = {
    estudiante: null,
    materias: [],
    notas: [],
    asistencias: [],
    alertas: []
};

// Inicialización de la aplicación
document.addEventListener('DOMContentLoaded', () => {
    inicializarApp();
});

// Función principal de inicialización
async function inicializarApp() {
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
    actualizarListaAsistencias();
}

// Actualizar lista de notas
function actualizarListaNotas() {
    const notasList = document.getElementById('notas-list');
    notasList.innerHTML = '';

    if (estadoApp.notas.length === 0) {
        notasList.innerHTML = '<p>No hay notas registradas.</p>';
        return;
    }

    estadoApp.notas.forEach(nota => {
        const notaItem = document.createElement('div');
        notaItem.className = 'nota-item';
        notaItem.innerHTML = `
            <div>
                <strong>${obtenerNombreMateria(nota.materia_id)}</strong>
                <p>Nota: ${nota.valor} | Porcentaje: ${nota.porcentaje}%</p>
            </div>
            <span class="stat-value">${nota.valor}</span>
        `;
        notasList.appendChild(notaItem);
    });
}

// Actualizar lista de asistencias
function actualizarListaAsistencias() {
    const asistenciasList = document.getElementById('asistencias-list');
    asistenciasList.innerHTML = '';

    if (estadoApp.asistencias.length === 0) {
        asistenciasList.innerHTML = '<p>No hay asistencias registradas.</p>';
        return;
    }

    estadoApp.asistencias.forEach(asistencia => {
        const asistenciaItem = document.createElement('div');
        asistenciaItem.className = 'asistencia-item';
        asistenciaItem.innerHTML = `
            <div>
                <strong>${obtenerNombreMateria(asistencia.materia_id)}</strong>
                <p>Fecha: ${formatearFecha(asistencia.fecha)}</p>
            </div>
            <span class="${asistencia.asistio ? 'stat-value' : ''}" style="color: ${asistencia.asistio ? 'var(--secondary-color)' : 'var(--danger-color)'}">
                ${asistencia.asistio ? '✓ Presente' : '✗ Ausente'}
            </span>
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

    const nuevaAsistencia = {
        id: estadoApp.asistencias.length + 1,
        materia_id: materiaId,
        fecha: fecha,
        asistio: asistio
    };

    estadoApp.asistencias.push(nuevaAsistencia);
    actualizarUI();
    
    // Aquí se haría la llamada a la API
    // await fetch(`${API_BASE_URL}/asistencias/`, { method: 'POST', body: JSON.stringify(nuevaAsistencia) });

    e.target.reset();
    mostrarMensaje('Asistencia registrada exitosamente', 'success');
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
    // Implementar sistema de notificaciones
    console.log(`${tipo}: ${mensaje}`);
}

function mostrarError(mensaje) {
    console.error(mensaje);
    // Implementar sistema de notificaciones de error
}

