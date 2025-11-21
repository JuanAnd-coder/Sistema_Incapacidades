/**
 * Firebase Authentication Handler
 * Maneja la autenticación con Google usando Firebase
 * Utiliza la configuración de firebaseconfig.js
 */

// Esperar a que firebaseconfig.js esté cargado
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar Firebase cuando el DOM esté listo
    if (typeof initializeFirebase === 'function') {
        const initialized = initializeFirebase();
        if (initialized) {
            checkAuthState();
        } else {
            disableGoogleButton();
        }
    } else {
        console.error('firebaseconfig.js no está cargado');
        disableGoogleButton();
    }
});

/**
 * Deshabilita el botón de Google si Firebase no está configurado
 */
function disableGoogleButton() {
    const btn = document.getElementById('btnGoogleLogin');
    if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24"><path fill="#999" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#999" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#999" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#999" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg> Google Login (No configurado)';
    }
}

/**
 * Inicia sesión con Google usando Firebase Auth
 */
async function signInWithGoogle() {
    // Verificar que Firebase esté inicializado
    if (typeof firebase === 'undefined' || !window.firebaseAuth || !window.googleProvider) {
        alert('Firebase no está configurado. Por favor, configura Firebase primero.');
        return;
    }
    
    const btn = document.getElementById('btnGoogleLogin');
    if (!btn) return;
    
    // Deshabilitar botón y mostrar loading
    btn.disabled = true;
    const originalHTML = btn.innerHTML;
    btn.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" style="animation: spin 1s linear infinite;"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/></svg> Cargando...';
    
    try {
        // Iniciar autenticación con popup
        const result = await window.firebaseAuth.signInWithPopup(window.googleProvider);
        
        // Obtener el token de ID
        const idToken = await result.user.getIdToken();
        
        // Enviar token al servidor para verificación
        const response = await fetch('/auth/google/callback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ idToken: idToken })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Mostrar mensaje de éxito
            showMessage('¡Autenticación exitosa! Redirigiendo...', 'success');
            
            // Redirigir al dashboard después de un breve delay
            setTimeout(() => {
                window.location.href = data.redirect;
            }, 500);
        } else {
            throw new Error(data.error || 'Error al autenticar');
        }
        
    } catch (error) {
        console.error('Error en autenticación:', error);
        
        // Mostrar mensaje de error
        let errorMessage = 'Error al autenticar con Google. ';
        
        if (error.code === 'auth/popup-closed-by-user') {
            errorMessage += 'La ventana de autenticación fue cerrada.';
        } else if (error.code === 'auth/popup-blocked') {
            errorMessage += 'El popup fue bloqueado. Por favor, permite popups para este sitio.';
        } else if (error.code === 'auth/network-request-failed') {
            errorMessage += 'Error de conexión. Verifica tu conexión a internet.';
        } else if (error.code === 'auth/unauthorized-domain') {
            errorMessage += 'Este dominio no está autorizado. ';
            errorMessage += 'Debes agregar "' + window.location.hostname + '" a los dominios autorizados en Firebase Console. ';
            errorMessage += 'Ve a Firebase Console > Authentication > Settings > Authorized domains y agrega el dominio.';
        } else {
            errorMessage += error.message || 'Intenta nuevamente.';
        }
        
        showMessage(errorMessage, 'error');
        
        // Restaurar botón
        btn.disabled = false;
        btn.innerHTML = originalHTML;
    }
}

/**
 * Muestra un mensaje al usuario
 */
function showMessage(message, type = 'info') {
    // Crear elemento de mensaje
    const messageDiv = document.createElement('div');
    messageDiv.className = `alert alert-${type}`;
    messageDiv.textContent = message;
    messageDiv.style.marginTop = '10px';
    
    // Insertar después del formulario
    const form = document.querySelector('form');
    if (form) {
        form.parentNode.insertBefore(messageDiv, form.nextSibling);
        
        // Remover después de 5 segundos
        setTimeout(() => {
            messageDiv.remove();
        }, 5000);
    }
}

/**
 * Verifica si el usuario ya está autenticado
 */
function checkAuthState() {
    if (!window.firebaseAuth) return;
    
    window.firebaseAuth.onAuthStateChanged((user) => {
        if (user) {
            console.log('Usuario autenticado:', user.email);
        } else {
            console.log('Usuario no autenticado');
        }
    });
}

/**
 * Cierra sesión de Firebase
 */
function signOutFirebase() {
    if (window.firebaseAuth) {
        window.firebaseAuth.signOut().then(() => {
            console.log('Sesión de Firebase cerrada');
        }).catch((error) => {
            console.error('Error al cerrar sesión:', error);
        });
    }
}

// Exportar funciones para uso global
if (typeof window !== 'undefined') {
    window.signInWithGoogle = signInWithGoogle;
    window.signOutFirebase = signOutFirebase;
}
