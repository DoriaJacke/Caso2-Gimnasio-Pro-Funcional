// ==========================================
// GIMNASIO PRO FUNCIONAL - VERSION INTEGRADA CON BACKEND
// ==========================================

const API_URL = 'http://localhost:5000/api';
let currentUserId = null;
let reservas = [];
let bloques = [];
let historialReservas = [];

// === TOGGLE PASSWORD FIELD ===
function togglePasswordField() {
    const role = document.getElementById('role').value;
    const passwordField = document.getElementById('password');
    
    if (role === 'admin') {
        passwordField.style.display = 'block';
    } else {
        passwordField.style.display = 'none';
    }
}

// === LOGIN ===
async function login() {
    const role = document.getElementById('role').value;
    const username = document.getElementById('username').value.trim();
    
    if (!username) {
        showToast('⚠️ Ingresa un usuario');
        return;
    }

    try {
        let response, data;
        
        // Login diferente para administradores
        if (role === 'admin') {
            const password = document.getElementById('password').value;
            
            if (!password) {
                showToast('⚠️ Ingresa la contraseña de administrador');
                return;
            }
            
            response = await fetch(`${API_URL}/admin/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password })
            });
            
            data = await response.json();
            
            if (data.success) {
                currentUserId = data.admin_id;
            }
        } else {
            // Login normal para clientes y entrenadores (auto-registro)
            response = await fetch(`${API_URL}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, role })
            });

            data = await response.json();
            
            if (data.success) {
                currentUserId = data.user_id;
            }
        }

        if (data.success) {
            document.getElementById('login-section').style.display = 'none';

            if (role === 'cliente') {
                document.getElementById('cliente-section').style.display = 'block';
                await cargarReservasDelServidor();
                await cargarHistorialDelServidor();
            } else if (role === 'admin') {
                document.getElementById('admin-section').style.display = 'block';
                await cargarBloquesDelServidor();
                await cargarEntrenadoresParaAdmin();
            } else if (role === 'entrenador') {
                document.getElementById('entrenador-section').style.display = 'block';
                await mostrarAlumnosDelServidor(username);
            }
            
            showToast(`✅ Bienvenido ${username}!`);
        } else {
            showToast(`❌ ${data.error || 'Error al iniciar sesión'}`);
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('❌ Error de conexión con el servidor');
    }
}

// BOTON RETROCEDER
function volverLogin(section) {
    document.getElementById(section + '-section').style.display = 'none';
    document.getElementById('login-section').style.display = 'block';
    currentUserId = null;
}

// === FECHAS Y HORAS ===
const hoy = new Date();
const hoyStr = hoy.toISOString().split('T')[0];
document.getElementById('fecha').min = hoyStr;
document.getElementById('fecha-admin').min = hoyStr;

function llenarHoras(selectId, fechaInputId) {
    const select = document.getElementById(selectId);
    select.innerHTML = '';
    const fechaSeleccionada = new Date(document.getElementById(fechaInputId).value);
    const ahora = new Date();
    const horaActual = ahora.getHours();
    const minutoActual = ahora.getMinutes();

    for (let h = 10; h <= 21; h++) {
        if (fechaSeleccionada.toDateString() === ahora.toDateString()) {
            if (h < horaActual || (h === horaActual && minutoActual > 0)) continue;
        }
        const option = document.createElement('option');
        option.value = `${h}:00`;
        option.textContent = `${h}:00`;
        select.appendChild(option);
    }
}

document.getElementById('fecha').addEventListener('change', () => llenarHoras('hora', 'fecha'));
document.getElementById('fecha-admin').addEventListener('change', () => llenarHoras('hora-admin', 'fecha-admin'));

window.addEventListener('load', () => {
    document.getElementById('fecha').value = hoyStr;
    document.getElementById('fecha-admin').value = hoyStr;
    llenarHoras('hora', 'fecha');
    llenarHoras('hora-admin', 'fecha-admin');
});

// === CLIENTE ===
function mostrarCrearReserva() {
    document.getElementById('crear-reserva').style.display = 'block';
    document.getElementById('lista-reservas-section').style.display = 'none';
    document.getElementById('progreso-section').style.display = 'none';
    document.getElementById('historial-section').style.display = 'none';
}

async function cargarReservasDelServidor() {
    try {
        const response = await fetch(`${API_URL}/reservas/${currentUserId}`);
        const data = await response.json();
        reservas = data.map(r => ({
            id: r.id,
            actividad: r.actividad,
            fecha: r.fecha,
            hora: r.hora.substring(0, 5), // Convertir HH:MM:SS a HH:MM
            entrenador: r.nombre_entrenador
        }));
    } catch (error) {
        console.error('Error al cargar reservas:', error);
        showToast('Error al cargar reservas');
    }
}

async function mostrarReservas() {
    await cargarReservasDelServidor();
    
    document.getElementById('crear-reserva').style.display = 'none';
    document.getElementById('lista-reservas-section').style.display = 'block';
    document.getElementById('progreso-section').style.display = 'none';
    document.getElementById('historial-section').style.display = 'none';
    
    const ul = document.getElementById('lista-reservas');
    ul.innerHTML = '';
    
    reservas.forEach(r => {
        const li = document.createElement('li');
        li.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 5px;">
                <span>${r.fecha} ${r.hora} - ${r.actividad} con ${r.entrenador}</span>
                <button onclick="cancelarReserva(${r.id})" style="width: auto; padding: 5px 10px; margin: 0; background: linear-gradient(90deg,#dc3545,#c82333);">
                    Cancelar
                </button>
            </div>
        `;
        ul.appendChild(li);
    });
}

async function verProgreso() {
    document.getElementById('crear-reserva').style.display = 'none';
    document.getElementById('lista-reservas-section').style.display = 'none';
    document.getElementById('progreso-section').style.display = 'block';
    document.getElementById('historial-section').style.display = 'none';
    
    try {
        const response = await fetch(`${API_URL}/progreso/${currentUserId}`);
        const data = await response.json();
        
        document.getElementById('progreso-text').textContent = 
            `Progreso del entrenamiento: ${data.porcentaje}% completado. (${data.completadas}/${data.total} clases)`;
    } catch (error) {
        console.error('Error al cargar progreso:', error);
        document.getElementById('progreso-text').textContent = 
            'Progreso del entrenamiento: 0% completado.';
    }
}

async function cargarHistorialDelServidor() {
    try {
        const response = await fetch(`${API_URL}/historial/${currentUserId}`);
        const data = await response.json();
        historialReservas = data.map(r => ({
            id: r.id,
            actividad: r.actividad,
            fecha: r.fecha,
            hora: r.hora.substring(0, 5),
            entrenador: r.nombre_entrenador,
            estado: r.estado,
            fechaCreacion: new Date(r.fecha_creacion).toLocaleString('es-ES'),
            fechaModificacion: new Date(r.fecha_modificacion).toLocaleString('es-ES')
        }));
    } catch (error) {
        console.error('Error al cargar historial:', error);
        showToast('Error al cargar historial');
    }
}

async function mostrarHistorial() {
    await cargarHistorialDelServidor();
    
    document.getElementById('crear-reserva').style.display = 'none';
    document.getElementById('lista-reservas-section').style.display = 'none';
    document.getElementById('progreso-section').style.display = 'none';
    document.getElementById('historial-section').style.display = 'block';
    
    const ul = document.getElementById('lista-historial');
    ul.innerHTML = '';
    
    if (historialReservas.length === 0) {
        ul.innerHTML = '<li style="text-align: center; color: #666;">No hay reservas en el historial</li>';
        return;
    }
    
    historialReservas.forEach(r => {
        const li = document.createElement('li');
        const estadoColor = r.estado === 'activa' ? '#28a745' : '#dc3545';
        const estadoIcon = r.estado === 'activa' ? '✅' : '❌';
        
        li.innerHTML = `
            <div style="padding: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                    <strong style="color: ${estadoColor};">${estadoIcon} ${r.estado.toUpperCase()}</strong>
                    <small style="color: #666;">Creada: ${r.fechaCreacion}</small>
                </div>
                <div style="margin-bottom: 5px;">
                    <strong>${r.fecha} ${r.hora}</strong> - ${r.actividad} con ${r.entrenador}
                </div>
                ${r.estado === 'cancelada' ? 
                    `<small style="color: #666;">Cancelada: ${r.fechaModificacion}</small>` : 
                    '<small style="color: #28a745;">Reserva activa</small>'
                }
            </div>
        `;
        ul.appendChild(li);
    });
}

async function reservarClase() {
    const actividad = document.getElementById('actividad').value;
    const fecha = document.getElementById('fecha').value;
    const hora = document.getElementById('hora').value;
    const entrenador = document.getElementById('entrenador').value;

    try {
        // Llamar al endpoint de Webpay para crear la transacción
        showToast('💳 Procesando pago...');
        
        const response = await fetch(`${API_URL}/webpay/crear`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: currentUserId,
                actividad,
                fecha,
                hora,
                entrenador
            })
        });

        const data = await response.json();

        if (data.success) {
            // Mostrar información del pago
            showToast(`💰 Redirigiendo a Webpay... Monto: $${data.amount.toLocaleString('es-CL')} CLP`);
            
            // Esperar 1.5 segundos y redirigir a Webpay
            setTimeout(() => {
                // Crear formulario para enviar a Webpay
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = data.url;
                
                const tokenInput = document.createElement('input');
                tokenInput.type = 'hidden';
                tokenInput.name = 'token_ws';
                tokenInput.value = data.token;
                
                form.appendChild(tokenInput);
                document.body.appendChild(form);
                form.submit();
            }, 1500);
        } else {
            showToast('❌ Error al crear pago: ' + (data.error || 'Intenta de nuevo'));
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('❌ Error de conexión con el servidor');
    }
}

// === API CANCELACION ===
function validarTiempoCancelacion(fechaReserva, horaReserva) {
    const [year, month, day] = fechaReserva.split('-');
    const [hour, minute] = horaReserva.split(':');
    const fechaHoraReserva = new Date(year, month - 1, day, hour, minute || 0);
    const ahora = new Date();
    const diferenciaHoras = (fechaHoraReserva - ahora) / (1000 * 60 * 60);
    return diferenciaHoras >= 2;
}

async function cancelarReserva(reservaId) {
    const reserva = reservas.find(r => r.id == reservaId);
    
    if (!reserva) {
        showToast('Error: Reserva no encontrada');
        return;
    }
    
    if (!validarTiempoCancelacion(reserva.fecha, reserva.hora)) {
        showToast('❌ Petición rechazada: No se puede cancelar con menos de 2 horas de anticipación');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/reservas/${reservaId}`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (data.success) {
            showToast('✅ Reserva cancelada exitosamente');
            await mostrarReservas();
            await cargarHistorialDelServidor();
        } else {
            showToast('Error al cancelar reserva');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('Error de conexión con el servidor');
    }
}

// === ADMIN ===
async function cargarBloquesDelServidor() {
    try {
        const response = await fetch(`${API_URL}/bloques`);
        const data = await response.json();
        bloques = data.map(b => ({
            id: b.id,
            actividad: b.actividad,
            fecha: b.fecha,
            hora: b.hora.substring(0, 5),
            entrenador: b.nombre_entrenador,
            cupos: b.cupos_disponibles
        }));
        mostrarBloques();
    } catch (error) {
        console.error('Error al cargar bloques:', error);
        showToast('Error al cargar bloques');
    }
}

async function crearBloque() {
    const actividad = document.getElementById('act-admin').value;
    const fecha = document.getElementById('fecha-admin').value;
    const hora = document.getElementById('hora-admin').value;
    const entrenador_nombre = document.getElementById('entrenador-admin').value;
    const capacidad_maxima = parseInt(document.getElementById('cupos-admin').value) || 10;

    if (!fecha || !hora || !entrenador_nombre) {
        showToast('⚠️ Completa todos los campos');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/admin/cupos`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                fecha,
                hora,
                entrenador_nombre,
                actividad,
                capacidad_maxima
            })
        });

        const data = await response.json();

        if (data.success) {
            showToast('✅ Cupo creado exitosamente!');
            await cargarBloquesDelServidor();
            // Limpiar formulario
            document.getElementById('fecha-admin').value = '';
            document.getElementById('cupos-admin').value = '10';
        } else {
            showToast(`❌ ${data.error || 'Error al crear cupo'}`);
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('❌ Error de conexión con el servidor');
    }
}

function mostrarBloques() {
    const ul = document.getElementById('lista-bloques');
    ul.innerHTML = '';
    bloques.forEach(b => {
        ul.innerHTML += `<li>${b.fecha} ${b.hora} - ${b.actividad} con ${b.entrenador} [Cupos: ${b.cupos}]</li>`;
    });
}

// === ENTRENADOR ===
async function mostrarAlumnosDelServidor(nombreEntrenador) {
    try {
        const response = await fetch(`${API_URL}/entrenador/${encodeURIComponent(nombreEntrenador)}/alumnos`);
        const alumnos = await response.json();
        
        const ul = document.getElementById('lista-alumnos');
        ul.innerHTML = '';
        
        if (alumnos.length === 0) {
            ul.innerHTML = '<li>No tienes alumnos asignados aún</li>';
        } else {
            alumnos.forEach(alumno => {
                ul.innerHTML += `<li>Alumno: ${alumno.username}</li>`;
            });
        }
    } catch (error) {
        console.error('Error al cargar alumnos:', error);
        const ul = document.getElementById('lista-alumnos');
        ul.innerHTML = '<li>Error al cargar alumnos</li>';
    }
}

// === PERFIL DEL CLIENTE ===
function mostrarPerfil() {
    ocultarTodasLasSeccionesCliente();
    document.getElementById('perfil-section').style.display = 'block';
    cargarPerfilDelServidor();
}

async function cargarPerfilDelServidor() {
    try {
        const response = await fetch(`${API_URL}/usuarios/${currentUserId}`);
        const data = await response.json();
        
        if (data.success) {
            const usuario = data.usuario;
            document.getElementById('perfil-email').value = usuario.email || '';
            document.getElementById('perfil-telefono').value = usuario.telefono || '';
            document.getElementById('perfil-direccion').value = usuario.direccion || '';
            document.getElementById('perfil-fechaNac').value = usuario.fecha_nacimiento || '';
            document.getElementById('perfil-peso').value = usuario.peso || '';
            document.getElementById('perfil-altura').value = usuario.altura || '';
            document.getElementById('perfil-objetivo').value = usuario.objetivo || '';
        }
    } catch (error) {
        console.error('Error al cargar perfil:', error);
        showToast('❌ Error al cargar perfil');
    }
}

async function guardarPerfil() {
    const perfil = {
        email: document.getElementById('perfil-email').value,
        telefono: document.getElementById('perfil-telefono').value,
        direccion: document.getElementById('perfil-direccion').value,
        fecha_nacimiento: document.getElementById('perfil-fechaNac').value,
        peso: parseFloat(document.getElementById('perfil-peso').value) || null,
        altura: parseFloat(document.getElementById('perfil-altura').value) || null,
        objetivo: document.getElementById('perfil-objetivo').value
    };
    
    try {
        const response = await fetch(`${API_URL}/usuarios/${currentUserId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(perfil)
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('✅ Perfil actualizado correctamente');
        } else {
            showToast('❌ Error al guardar perfil');
        }
    } catch (error) {
        console.error('Error al guardar perfil:', error);
        showToast('❌ Error de conexión con el servidor');
    }
}

function ocultarTodasLasSeccionesCliente() {
    document.getElementById('crear-reserva').style.display = 'none';
    document.getElementById('lista-reservas-section').style.display = 'none';
    document.getElementById('progreso-section').style.display = 'none';
    document.getElementById('historial-section').style.display = 'none';
    document.getElementById('perfil-section').style.display = 'none';
}

// === ADMINISTRADOR - ENTRENADORES ===
function mostrarCrearEntrenador() {
    document.getElementById('crear-entrenador-admin').style.display = 'block';
    document.getElementById('crear-bloque').style.display = 'none';
    document.getElementById('lista-bloques').style.display = 'none';
}

function mostrarCrearCupo() {
    document.getElementById('crear-entrenador-admin').style.display = 'none';
    document.getElementById('crear-bloque').style.display = 'block';
    document.getElementById('lista-bloques').style.display = 'none';
}

function mostrarListaBloques() {
    document.getElementById('crear-entrenador-admin').style.display = 'none';
    document.getElementById('crear-bloque').style.display = 'none';
    document.getElementById('lista-bloques').style.display = 'block';
}

async function crearEntrenador() {
    const nombre = document.getElementById('nombre-entrenador').value.trim();
    const especialidad = document.getElementById('especialidad-entrenador').value.trim();
    
    if (!nombre) {
        showToast('⚠️ Ingresa el nombre del entrenador');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/admin/entrenadores`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ nombre, especialidad })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('✅ Entrenador creado exitosamente');
            document.getElementById('nombre-entrenador').value = '';
            document.getElementById('especialidad-entrenador').value = '';
            await cargarEntrenadoresParaAdmin();
        } else {
            showToast(`❌ ${data.error || 'Error al crear entrenador'}`);
        }
    } catch (error) {
        console.error('Error al crear entrenador:', error);
        showToast('❌ Error de conexión con el servidor');
    }
}

async function cargarEntrenadoresParaAdmin() {
    try {
        const response = await fetch(`${API_URL}/entrenadores`);
        const entrenadores = await response.json();
        
        const select = document.getElementById('entrenador-admin');
        select.innerHTML = '';
        
        entrenadores.forEach(e => {
            const option = document.createElement('option');
            option.value = e.nombre;
            option.textContent = `${e.nombre}${e.especialidad ? ' - ' + e.especialidad : ''}`;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error al cargar entrenadores:', error);
    }
}

// === TOASTS ===
function showToast(msg) {
    const toasts = document.getElementById('toasts');
    const div = document.createElement('div');
    div.className = 'toast';
    div.textContent = msg;
    toasts.appendChild(div);
    setTimeout(() => div.remove(), 3000);
}

