// Script principal - inicialização da aplicação
document.addEventListener('DOMContentLoaded', function() {
    App.init();
});

const App = {

    init: () => {
        App.setupEventListeners();
        App.checkAuthenticationStatus();
    },

    setupEventListeners: () => {
        window.addEventListener('invalidAuthentication', (event) => {
            App.handleInvalidAuthentication(event.detail);
        });

        const loginForm = document.getElementById('login-form');
        loginForm.addEventListener('submit', App.handleLogin);
        
        const logoutButton = document.getElementById('logout-btn');
        logoutButton.addEventListener('click', App.handleLogout);
        
        const usernameInput = document.getElementById('username');
        const passwordInput = document.getElementById('password');
        usernameInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                passwordInput.focus();
            }
        });
    },

    checkAuthenticationStatus: async () => {
        const authStatus = window.Auth.recoverLocalStorageAuth();
        if (authStatus.authenticated) {
            const result = await window.Auth.validateAuth(); //handleInvalidAuth cobre todos os casos para valid = false
            if (result.valid) {
                App.showDashboard();
            } 
            else if(result.reason === 'Network error') {
                App.clearLoginForm();
                App.showLogin();  
                App.showLoginFormError('Sem conexão com o servidor.');
            } // Não precisa tratar os outros casos, pois o evento 'invalidAuthentication' já é disparado
        }
        else {
            App.clearLoginForm();
            App.showLogin();           
        }
    },
    
    handleLogin: async (e) => {
        e.preventDefault();
        App.hideLoginFormError();
        
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value.trim();
        if (!username || !password) {
            App.showLoginFormError('Preencha todos os campos.');
            return;
        }
        
        const submitButton = e.target.querySelector('button[type="submit"]');
        submitButton.disabled = true;
        
        const result = await window.Auth.login(username, password);
        if (result.success) {
            App.showDashboard();
            App.clearLoginForm();
        } else {
            App.showLoginFormError(result.message);
        }
        submitButton.disabled = false;
    },
    
    handleLogout: () => {
        const result = Auth.logout();
        if (result.success) {
            App.showLogin();
            App.clearLoginForm();
        }
    },
    
    showLogin: () => {
        document.getElementById('login-container').style.display = 'block';
        document.getElementById('dashboard').style.display = 'none';
        App.hideLoginFormError();
    },
    
    showDashboard: () => {
        document.getElementById('login-container').style.display = 'none';
        document.getElementById('dashboard').style.display = 'block';
        window.DashboardContents.init();
    },
    
    clearLoginForm: () => {
        document.getElementById('login-form').reset();
        App.hideLoginFormError();
    },
    
    showLoginFormError: (message) => {
        const errorDiv = document.getElementById('login-error');
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
    },
    
    hideLoginFormError: () => {
        const errorDiv = document.getElementById('login-error');
        errorDiv.style.display = 'none';
    },
    
    handleInvalidAuthentication: (detail) => {
        App.handleLogout();
        App.showLogin();
        App.showLoginFormError(detail.message || 'Sessão expirou. Faça login novamente.');
    }
};
