/**
 * Firebase Configuration
 * Configuración de Firebase para el Sistema de Incapacidades
 * 
 * Nota: Este archivo usa Firebase Compat Mode para compatibilidad con navegadores antiguos
 */

// Configuración de Firebase
const firebaseConfig = {
  apiKey: "AIzaSyB1MxpdmNDNphu4KaLL7ky5BpY2M5cMssM",
  authDomain: "incapacidades-system.firebaseapp.com",
  projectId: "incapacidades-system",
  storageBucket: "incapacidades-system.firebasestorage.app",
  messagingSenderId: "907978562840",
  appId: "1:907978562840:web:b68ede62dd315b4276d26d"
};

/**
 * Inicializa Firebase con la configuración
 * Requiere que firebase-app-compat.js y firebase-auth-compat.js estén cargados
 */
function initializeFirebase() {
    if (typeof firebase === 'undefined') {
        console.error('Firebase SDK no está cargado. Asegúrate de incluir los scripts de Firebase.');
        return false;
    }
    
    try {
        // Inicializar Firebase App
        window.firebaseApp = firebase.initializeApp(firebaseConfig);
        
        // Inicializar Firebase Auth
        window.firebaseAuth = firebase.auth();
        
        // Configurar proveedor de Google
        window.googleProvider = new firebase.auth.GoogleAuthProvider();
        window.googleProvider.addScope('email');
        window.googleProvider.addScope('profile');
        
        console.log('✅ Firebase inicializado correctamente');
        return true;
    } catch (error) {
        console.error('❌ Error al inicializar Firebase:', error);
        return false;
    }
}

// Exportar para uso global
if (typeof window !== 'undefined') {
    window.firebaseConfig = firebaseConfig;
    window.initializeFirebase = initializeFirebase;
}